import faiss
import pickle
import pandas as pd

# Load vector index
index = faiss.read_index("movie_index.faiss")

# Load vectorizer
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Load data
train_df = pd.read_csv("movies_df.csv")

# Vectorize the tags
vectors = vectorizer.transform(train_df['tags']).toarray()

# Recommend function
def recommend(movie_title, top_n=5):
    matches = train_df[train_df['title'] == movie_title]
    
    if matches.empty:
        print(f"❌ Movie '{movie_title}' not found in the dataset.")
        return
    
    movie_idx = matches.index[0]

    D, I = index.search(vectors[movie_idx].reshape(1, -1), top_n + 1)

    recommendations = []
    for i in I[0][1:]:  # skip input movie
        movie_id = train_df.iloc[i]['id']
        movie_data = train_df[train_df['id'] == movie_id].iloc[0]
        
        recommendations.append({
            'title': movie_data['title'],
            'overview': movie_data['overview'],
            'release_date': movie_data['release_date'],
            'vote_average': movie_data['vote_average']
        })

    return recommendations


# Test
recommendations = recommend("Deadpool 2")
for rec in recommendations:
    print(rec)
    print("-" * 50)