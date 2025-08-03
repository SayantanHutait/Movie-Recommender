# recommender_engine.py

import pickle
import pandas as pd

# Load the pickled data once
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movie_list)

def recommend(movie):
    movie_i = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_i]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    rec_movies = []
    for i in movie_list:
        rec_movies.append(movies.title.iloc[i[0]])
    return rec_movies
