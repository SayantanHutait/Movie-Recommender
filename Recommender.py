# app.py
import streamlit as st
import pickle
import pandas as pd
from rec import recommend
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")
# Load movie data
with open("movies_df.pkl", "rb") as f:
    train_df = pickle.load(f)

movie_titles = sorted(train_df['title'].tolist())

st.title("Movie Recommender")

selected_movie = st.selectbox("Select a movie:", movie_titles)

if st.button("Get Recommendations"):
    recommendations = recommend(selected_movie)

    st.subheader("📽️ Recommendations:")
    for movie in recommendations:
        col1, col2 = st.columns([1, 2])
        release_date = pd.to_datetime(movie['release_date']).strftime("%d-%m-%Y")

        with col1:
            st.image(f"https://image.tmdb.org/t/p/w200{movie['poster_path']}")

        with col2:
            st.markdown(f"**{movie['title']}** | *{movie['release_date'].year}*")
            st.markdown(movie['overview'])
            st.markdown(f"IMDb: {movie['imdb_rating']}")

        st.markdown("---")
