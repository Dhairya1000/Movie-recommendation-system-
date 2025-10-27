import streamlit as st
import pickle
import pandas as pd
import requests

# ------------------- CONFIG -------------------
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"  # Your TMDB API key
st.set_page_config(page_title="🎬 Movie Recommender", page_icon="🍿", layout="wide")

# ------------------- LOAD DATA -------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ------------------- FUNCTIONS -------------------
def fetch_poster(movie_name):
    """Fetch movie poster using TMDB API safely"""
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data["results"]:
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path
    except requests.exceptions.RequestException:
        pass
    return "https://via.placeholder.com/200x300?text=No+Poster"

def recommend(movie):
    """Return recommended movies and their posters"""
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))

    return recommended_movies, recommended_posters

# ------------------- UI -------------------
st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color:#FF4B4B;">🍿 Movie Recommendation System 🎬</h1>
    </div>
    """,
    unsafe_allow_html=True
)

selected_movie_name = st.selectbox(
    "🎥 Choose a movie:",
    movies['title'].values
)

if st.button("✨ Show Recommendations"):
    names, posters = recommend(selected_movie_name)

    st.subheader("🔮 We think you’ll like:")
    cols = st.columns(5)

    for i, col in enumerate(cols):
        with col:
            st.image(posters[i], use_container_width=True)  # updated param
            st.markdown(
                f"<h4 style='text-align:center; color:#333;'>{names[i]}</h4>",
                unsafe_allow_html=True
            )

st.markdown(
    """
    <hr>
    <p style="text-align:center; font-size:14px; color:grey;">
    Made with ❤️ using Streamlit | Enjoy your movie night! 🍿
    </p>
    """,
    unsafe_allow_html=True
)

