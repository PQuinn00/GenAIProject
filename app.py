import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import pandas as pd

# Set OpenAI API Key (Replace with your own key)
openai.api_key = "your-api-key-here"

# Function to fetch past NFL games from Pro Football Reference
def get_past_nfl_games():
    base_url = "https://www.pro-football-reference.com/years/2024/games.htm"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    game_links = {}
    table = soup.find("table", id="games")
    if table:
        rows = table.find("tbody").find_all("tr")
        for row in rows:
            date = row.find("th").text if row.find("th") else ""
            teams = row.find_all("td", class_="right gamelink")
            if len(teams) == 1:
                link = teams[0].find("a")
                if link:
                    team_names = row.find_all("td", class_="left")
                    if len(team_names) >= 2:
                        matchup = team_names[0].text + " vs " + team_names[1].text
                        game_links[matchup] = "https://www.pro-football-reference.com" + link["href"]
    
    return game_links

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
    prompt = f"""Generate a post-game summary based on the following box score:

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

games = get_past_nfl_games()
if games:
    selected_game = st.selectbox("Select a Past Game:", list(games.keys()))

    if st.button("Generate Summary"):
        game_url = games[selected_game]
        scores, stats = scrape_nfl_box_score(game_url)
        if scores:
            summary = generate_game_summary(scores, stats)
            st.subheader("Generated Game Summary:")
            st.write(summary)
        else:
            st.error("Could not retrieve game data. Make sure the URL is correct.")
else:
    st.error("No past games found. Please check the data source.")
