import streamlit as st
import pickle
import pandas as pd

def recommend(movie):
    movie_i = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_i]
    movie_list = sorted(list(enumerate(distances)),reverse = True,key = lambda x: x[1])[1:6]

    rec_movies = []
    for i in movie_list:
        movie_id = []
        rec_movies.append(movies.title.iloc[i[0]])
    return rec_movies


similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movie_list)
st.title("Your Movie Recommender")
option = st.selectbox(
    "Write down the movie name you liked",
    movies['title'].values
)

if st.button("Recommend"):
    recommendations = recommend(option)
    for i in recommendations:
        st.write(i)