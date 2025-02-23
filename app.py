import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import pandas as pd

# Set OpenAI API Key (Replace with your own key)
openai.api_key = "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"

# Function to fetch latest NFL games from Pro Football Reference
def get_latest_nfl_games():
    base_url = "https://www.pro-football-reference.com/boxscores/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    game_links = []
    for link in soup.find_all('a', href=True):
        if '/boxscores/' in link['href'] and link['href'].endswith('.htm'):
            game_links.append("https://www.pro-football-reference.com" + link['href'])
    
    return game_links[:5]  # Return the latest 5 games

# Function to scrape NFL box scores
def scrape_nfl_box_score(game_url):
    response = requests.get(game_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extracting score
    teams = soup.find_all('div', class_='scorebox')
    scores = {team.find('strong').text: team.find('div', class_='score').text for team in teams}
    
    # Extracting key player stats (example: QB stats)
    stats = {}
    stat_table = soup.find('table', {'id': 'player_offense'})
    if stat_table:
        df = pd.read_html(str(stat_table))[0]
        stats = df.to_dict(orient='records')
    
    return scores, stats

# Function to generate AI-generated summary
def generate_game_summary(scores, stats):
    prompt = f"""
    Generate a post-game summary based on the following box score:
    
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
st.title("🏈 AI-Powered NFL Post-Game Summary Generator")

games = get_latest_nfl_games()
selected_game = st.selectbox("Select a Game:", games)

if st.button("Generate Summary"):
    scores, stats = scrape_nfl_box_score(selected_game)
    if scores:
        summary = generate_game_summary(scores, stats)
        st.subheader("Generated Game Summary:")
        st.write(summary)
    else:
        st.error("Could not retrieve game data. Make sure the URL is correct.")
