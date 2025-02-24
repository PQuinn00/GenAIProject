import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import pandas as pd

# Set OpenAI API Key (Replace with your own key)
openai.api_key = "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"

# Function to fetch past NBA games from ESPN
def get_past_nba_games():
    base_url = "https://www.espn.com/nba/scoreboard"
    response = requests.get(base_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    game_links = {}
    games = soup.find_all("section", class_="Scoreboard")
    for game in games:
        teams = game.find_all("span", class_="sb-team-short")
        if len(teams) == 2:
            matchup = f"{teams[0].text} vs {teams[1].text}"
            link = game.find("a", class_="AnchorLink")
            if link and "boxscore" in link["href"]:
                game_links[matchup] = "https://www.espn.com" + link["href"]
    
    return game_links

# Function to scrape NBA box scores from ESPN
def scrape_nba_box_score(game_url):
    response = requests.get(game_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extracting score
    scores = {}
    teams = soup.find_all("div", class_="ScoreCell__TeamName")
    score_values = soup.find_all("div", class_="ScoreCell__Score")
    
    if teams and score_values:
        scores[teams[0].text] = score_values[0].text
        scores[teams[1].text] = score_values[1].text
    
    # Extracting key player stats
    stats = {}
    stat_tables = soup.find_all("table", class_="mod-data")
    for table in stat_tables:
        df = pd.read_html(str(table))[0]
        stats[df.columns[0]] = df.to_dict(orient='records')
    
    return scores, stats

# Function to generate AI-generated summary
def generate_game_summary(scores, stats):
    prompt = f"""
    Generate a post-game summary based on the following NBA box score:
    
    Final Score:
    {list(scores.keys())[0]}: {list(scores.values())[0]}
    {list(scores.keys())[1]}: {list(scores.values())[1]}
    
    Key Player Stats:
    {stats}
    
    Generate three versions:
    1. Casual fan-friendly recap
    2. In-depth analysis
    3. Funny/meme-style summary
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a sports journalist."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.title("🏀 AI-Powered NBA Post-Game Summary Generator")

games = get_past_nba_games()
if games:
    selected_game = st.selectbox("Select a Past Game:", list(games.keys()))
    if st.button("Generate Summary"):
        game_url = games[selected_game]
        scores, stats = scrape_nba_box_score(game_url)
        if scores:
            summary = generate_game_summary(scores, stats)
            st.subheader("Generated Game Summary:")
            st.write(summary)
        else:
            st.error("Could not retrieve game data. Make sure the URL is correct.")
else:
    st.error("No past games found. Please check the data source.")
