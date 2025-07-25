## 🎬 Movie Recommendation System 

A sleek and responsive movie recommendation system built with Streamlit, utilizing content-based filtering to suggest movies similar in genre, cast, keywords, and more.


## 🚀 Features

🔍 Content-Based Filtering: Recommends movies similar to your selection based on metadata like genres, cast, crew, and keywords.

🖼 Modern UI: Built with Streamlit for a clean, professional user experience.

🎞 Fetches posters dynamically via TMDB API.


## Download Required Datasets

⚠️ NOTE: The TMDB datasets are not included in this repository.

Download these files manually from Kaggle:

TMDB 5000 Movie Dataset

You'll need:

tmdb_5000_movies.csv

tmdb_5000_credits.csv


## 🧠 Tech Stack

Python

Streamlit — modern web UI

pandas, numpy — data processing

scikit-learn — cosine similarity

Requests — TMDB API


## Run the app
```bash
streamlit run app.py
```
