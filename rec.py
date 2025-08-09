import faiss
import pickle
import pandas as pd

# Load vector index
index = faiss.read_index("movie_index.faiss")

# Load vectorizer
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("movies_df.pkl", "rb") as f:
    train_df = pickle.load(f)
# Load data


# Vectorize the tags
vectors = vectorizer.transform(train_df['tags']).toarray().astype('float32')

# Recommend function
def recommend(movie_title, top_n=20):
    matches = train_df[train_df['title'] == movie_title]
    
    if matches.empty:
        print(f"❌ Movie '{movie_title}' not found in the dataset.")
        return
    
    movie_idx = matches.index[0]

    D, I = index.search(vectors[movie_idx].reshape(1, -1), top_n + 1)

    recommendations = []
    for i in I[0][1:]:
        movie_id = train_df.iloc[i]['id']
        movie_data = train_df[train_df['id'] == movie_id].iloc[0]
        
        recommendations.append({
            'title': movie_data['title'],
            'overview': movie_data['overview'],
            'release_date': movie_data['release_date'],
            'imdb_rating': movie_data['imdb_rating'],
            'poster_path': movie_data['poster_path']
        })

    return recommendations


# Test
if __name__ == "__main__":
    recommendations = recommend("Deadpool 2")
    for rec in recommendations:
        print(rec)
        print("-" * 50)