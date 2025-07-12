import streamlit as st
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(page_title="Movie Recommender", layout="centered")

st.markdown("""
<style>
/* Smooth gradient title */
.gradient-text {
    background: linear-gradient(to right, #ff6a00, #ee0979);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
    padding-top: 10px;
}

body {
    background-color: #0f1117;
    color: white;
}

.stApp {
    background-color: #0f1117;
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
}

.stButton > button {
    background-color: #00adb5;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    transition: all 0.3s ease;
    padding: 0.5em 2em;
}

.stButton > button:hover {
    background-color: #007c80;
    transform: scale(1.05);
}

.recommend-box {
    background-color: #1f222f;
    border-radius: 12px;
    padding: 20px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="gradient-text">Movie Recommender</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Find similar movies you'll love 🍿</p>", unsafe_allow_html=True)


@st.cache_data
def load_data():
    movies = pd.read_csv("tmdb_5000_movies.csv")
    credits = pd.read_csv("tmdb_5000_credits.csv")
    movies = movies.merge(credits, left_on='id', right_on='movie_id')[['title_x', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    movies.rename(columns={'title_x': 'title'}, inplace=True)

    def convert(obj):
        try:
            return [i['name'] for i in ast.literal_eval(obj)]
        except:
            return []

    def get_director(obj):
        try:
            for i in ast.literal_eval(obj):
                if i['job'] == 'Director':
                    return i['name']
        except:
            return ""

    movies.dropna(inplace=True)
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(lambda x: convert(x)[:3])
    movies['crew'] = movies['crew'].apply(get_director)
    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast']
    movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))

    df = movies[['title', 'tags']]
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(df['tags']).toarray()
    similarity = cosine_similarity(vectors)
    return df, similarity

df, similarity = load_data()

def recommend(movie, df, similarity):
    movie = movie.lower()
    if movie not in df['title'].str.lower().values:
        return []
    index = df[df['title'].str.lower() == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    return [df.iloc[i[0]].title for i in distances[1:6]]

st.subheader("📽️ Choose a Movie")
movie_list = sorted(df['title'].values)
selected_movie = st.selectbox("Pick from the list", movie_list)

if st.button("🎯 Recommend"):
    with st.spinner("Generating recommendations..."):
        recs = recommend(selected_movie, df, similarity)
    st.markdown("### 🎉 Top 5 Recommendations")
    for i, title in enumerate(recs, 1):
        st.markdown(f'<div class="recommend-box"><b>{i}. {title}</b></div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: gray;'>Built with ❤️ by Rajdeep</p>", unsafe_allow_html=True)


