import streamlit as st
import requests
import openai
from PIL import Image
from io import BytesIO
import random

# Set OpenAI API Key (Replace with your own key)
openai.api_key = "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"

# Function to get movie recommendations from TMDB API
def get_movie_recommendations(genre):
    api_key = "36bc59273ae877478e029fc346bb6026"
    base_url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": api_key,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "with_genres": genre,
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        movies = response.json()["results"]
        return random.choice(movies) if movies else None
    return None

# Function to generate a movie poster with DALL-E
def generate_movie_poster(movie_title):
    prompt = f"Create a visually appealing movie poster for the movie '{movie_title}'. Make it eye-catching and cinematic."
    response = openai.images.generate(
        model="dall-e-2",
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response.data[0].url
    return image_url

# Streamlit UI
st.title("🎬 AI-Powered Movie Recommender & Poster Generator")

genres = {"Action": "28", "Comedy": "35", "Drama": "18", "Horror": "27", "Sci-Fi": "878"}
selected_genre = st.selectbox("Select a Movie Genre:", list(genres.keys()))

if st.button("Get Movie Recommendation"):
    movie = get_movie_recommendations(genres[selected_genre])
    if movie:
        st.subheader(f"🎥 Recommended Movie: {movie['title']}")
        st.write(f"📅 Release Date: {movie['release_date']}")
        st.write(f"⭐ Rating: {movie['vote_average']}")
        st.write(f"📖 Overview: {movie['overview']}")
        
        poster_url = generate_movie_poster(movie['title'])
        response = requests.get(poster_url)
        image = Image.open(BytesIO(response.content))
        st.image(image, caption=f"AI-Generated Poster for {movie['title']}")
    else:
        st.error("No movies found for this genre. Try again!")
