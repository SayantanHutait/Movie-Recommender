# main.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from rec import recommend
import pickle
import pandas as pd

app = FastAPI()
templates = Jinja2Templates(directory="templates")
with open("movies_df.pkl", "rb") as f:
    train_df = pickle.load(f)


movie_titles = sorted(train_df['title'].tolist())

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "titles": movie_titles})

@app.get("/recommend")
def get_recommendations(title: str):
    recommendations = recommend(title)
    return {"recommendations": recommendations}
