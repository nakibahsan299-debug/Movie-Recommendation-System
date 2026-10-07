import streamlit as st
import pickle
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.DataFrame(pickle.load(open('movies_dict.pkl', 'rb')))
def build_similarity(tags):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(tags)          # keep sparse to save memory
    return cosine_similarity(vectors).astype('float32')
similarity = build_similarity(movies['tags'])

@st.cache_data
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": st.secrets["API_KEY"], "language": "en-US"}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        path = r.json().get("poster_path")
        if path:
            return "https://image.tmdb.org/t/p/w500" + path
    except requests.RequestException:
        pass
    return "https://via.placeholder.com/500x750?text=No+Poster"

def recommend_movies(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    names, posters = [], []
    for i in movie_list:
        row = movies.iloc[i[0]]
        names.append(row.title)
        posters.append(fetch_poster(row.movie_id))
    return names, posters

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

# Poster for the selected movie
selected_id = movies[movies['title'] == selected_movie_name].iloc[0].movie_id
left, _ = st.columns([1, 3])
with left:
    st.image(fetch_poster(selected_id), caption=selected_movie_name)

if st.button('Recommend Similar movies'):
    names, posters = recommend_movies(selected_movie_name)
    st.subheader('Recommended for you')
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.image(poster)
            st.caption(name)