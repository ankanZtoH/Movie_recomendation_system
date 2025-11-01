import streamlit as st
import pickle
import pandas as pd

# ===============================
# LOAD DATA
# ===============================
movies = pickle.load(open('movies.pkl', "rb"))
similarity = pickle.load(open('similarity.pkl', "rb"))
movie_name = movies['title'].values

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🎥",
    layout="wide",
)

# ===============================
# CUSTOM CSS (Enhanced Style)
# ===============================
st.markdown("""
    <style>
        body {
            background-color: #0E1117;
            color: white;
            font-family: 'Poppins', sans-serif;
        }

        h1 {
            color: #F5C518;
            text-align: center;
            font-size: 2.8rem;
            font-weight: 800;
            text-shadow: 0 0 15px rgba(245,197,24,0.4);
            margin-bottom: 0.5rem;
        }

        .subheader {
            text-align: center;
            color: #CCCCCC;
            font-size: 1.1rem;
            margin-bottom: 2.5rem;
        }

        .stSelectbox label {
            display: none !important;
        }

        /* Align search and button */
        .search-row {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            width: 70%;
            margin: 0 auto 2rem auto;
        }

        .stButton>button {
            background: linear-gradient(90deg, #F5C518, #D4AF37);
            color: black;
            font-weight: 700;
            border: none;
            border-radius: 10px;
            padding: 0.7rem 1.8rem;
            font-size: 1rem;
            height: 3rem;
            transition: 0.3s;
        }

        .stButton>button:hover {
            background: linear-gradient(90deg, #FFD700, #F5C518);
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(245,197,24,0.5);
        }

        /* Movie cards */
        .movie-card {
            background: linear-gradient(145deg, #1A1E24, #0C0E11);
            border-radius: 15px;
            padding: 1.5rem 1rem;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 0 12px rgba(245,197,24,0.15);
            border: 1px solid rgba(245,197,24,0.1);
        }

        .movie-card:hover {
            transform: scale(1.07);
            box-shadow: 0 0 20px rgba(245,197,24,0.4);
            background: linear-gradient(145deg, #20242B, #121418);
        }

        /* Movie title styling */
        .movie-title {
            color: #FFD95A;
            font-size: 1.15rem;
            font-weight: 700;
            text-decoration: none !important;
            display: block;
            margin-top: 0.5rem;
            letter-spacing: 0.5px;
            text-transform: capitalize;
            transition: color 0.3s ease, text-shadow 0.3s ease;
        }

        .movie-title:hover {
            color: #FFFFFF;
            text-shadow: 0 0 10px rgba(255, 217, 90, 0.6);
        }

        /* Center heading */
        .recommend-heading {
            text-align: center;
            font-size: 1.6rem;
            color: #F5C518;
            font-weight: 700;
            margin-top: 1.5rem;
        }

        .recommend-sub {
            text-align: center;
            color: #CCCCCC;
            margin-bottom: 2rem;
        }

        .footer {
            text-align: center;
            color: grey;
            margin-top: 3rem;
        }
    </style>
""", unsafe_allow_html=True)

# ===============================
# HEADER
# ===============================
st.markdown("<h1>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>💡 Discover movies similar to your favorites — explore and relive the magic!</div>", unsafe_allow_html=True)

# ===============================
# RECOMMEND FUNCTION
# ===============================
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]
    recommended = []
    for i in movies_list:
        recommended.append(movies.iloc[i[0]].title)
    return recommended

# ===============================
# SEARCH BAR + BUTTON
# ===============================
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    c1, c2 = st.columns([4, 1])
    with c1:
        selected_movie_name = st.selectbox(
            '',
            ['-- Select a movie --'] + list(movie_name),
            key="movie_select",
            index=0
        )
    with c2:
        recommend_button = st.button('Recommend 🎯', use_container_width=True)

# ===============================
# RECOMMENDATION DISPLAY
# ===============================
if recommend_button:
    if selected_movie_name == '-- Select a movie --':
        st.warning("⚠️ Please select a movie first!")
    else:
        recommendations = recommend(selected_movie_name)

        # Center heading
        st.markdown("<div class='recommend-heading'>🌟 Recommended for You</div>", unsafe_allow_html=True)
        st.markdown("<div class='recommend-sub'>Click any movie below to explore more on Google 🔍</div>", unsafe_allow_html=True)

        # Grid layout
        cols_per_row = 3
        for i in range(0, len(recommendations), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(recommendations):
                    movie = recommendations[i + j]
                    google_link = f"https://www.google.com/search?q={movie.replace(' ', '+')}+movie"
                    with col:
                        st.markdown(
                            f"""
                            <div class='movie-card'>
                                <a href='{google_link}' target='_blank' class='movie-title'>
                                    🎥 {movie}
                                </a>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

# ===============================
# FOOTER
# ===============================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='footer'>Made with ❤️ using Streamlit | © MovieVerse</div>", unsafe_allow_html=True)
