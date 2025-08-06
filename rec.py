import faiss
import pickle
import pandas as pd

# Load everything
index = faiss.read_index("movie_index.faiss")

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

train_df = pd.read_csv("movies_df.csv")
id_to_title = dict(enumerate(train_df['title']))

# Recreate recommend function
def recommend(movie_title, top_n=5):
    movie_idx = title_to_id.get(movie_title)
    if movie_idx is None:
        print("Movie not found!")
        return

    # Query FAISS
    D, I = index.search(vectors[movie_idx].reshape(1, -1), top_n + 1)

    # Skip the first match (it will be the same movie), and collect details
    results = []
    for i in I[0][1:]:  # Skipping the first index
        row = train_df.iloc[i]
        results.append({
            'title': row['title'],
            'overview': row['overview'],
            'release_date': row['release_date'],
            'vote_average': row['vote_average']
        })

    return results


recommendations = recommend("Deadpool 2")
for rec in recommendations:
    print(rec)
    print("-" * 50)

