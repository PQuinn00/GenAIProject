# import needed libraries 
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

# Set OpenAI API Key 
openai.api_key = "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"

# Function to fetch top news headlines
def get_latest_news():
    url = "https://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_links = {}
    articles = soup.find_all("article")
    for article in articles:
        headline_tag = article.find("h3")
        if headline_tag and headline_tag.a:
            headline = headline_tag.text.strip()
            link = "https://news.google.com" + headline_tag.a["href"].replace("./", "/")
            news_links[headline] = link
    
    return news_links

# Function to summarize an article
def summarize_article(article_url):
    response = requests.get(article_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    paragraphs = soup.find_all("p")
    article_text = " ".join([p.text for p in paragraphs[:10]])  # Get first 10 paragraphs
    
    prompt = f"""
    Summarize the following news article:
    {article_text}
    
    Generate three versions:
    1. Short professional summary
    2. Clickbait-style headline
    3. Meme-style summary
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a professional news editor."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.title("📰 AI-Powered News Headline & Summary Generator")

news = get_latest_news()
if news:
    selected_article = st.selectbox("Select a News Headline:", list(news.keys()))
    if st.button("Generate Summary"):
        article_url = news[selected_article]
        summary = summarize_article(article_url)
        st.subheader("Generated Summary:")
        st.write(summary)
else:
    st.error("No news found. Please check the data source.")
