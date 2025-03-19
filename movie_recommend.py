import pickle
import streamlit as st
import requests
import streamlit.components.v1 as components  # Import components for rendering raw HTML

# Function to fetch movie poster from TMDb API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=707a923f9f0d388565a8396fc3348b27&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    return None  # Handle missing posters

# Function to recommend movies based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_links = []

    for i in distances[1:6]:  # Get top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_links.append(f"https://www.themoviedb.org/movie/{movie_id}")

    return recommended_movie_names, recommended_movie_posters, recommended_movie_links

# Streamlit UI
st.header('🎬 Movie Recommender System')

# Load movies and similarity data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Type or select a movie from the dropdown", movie_list)

if st.button('🎞️ Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_links = recommend(selected_movie)

    # Construct HTML for displaying images and titles in a row
    html_code = '''
    <div style="display: flex; gap: 20px; justify-content: center; align-items: flex-start; flex-wrap: wrap;">
    '''

    for idx in range(5):
        html_code += f'''
        <div style="text-align: center; width: 120px;">
            <a href="{recommended_movie_links[idx]}" target="_blank">
                <img src="{recommended_movie_posters[idx]}" width="120px" style="border-radius: 10px;">
            </a>
<p style="font-size: 14px; font-weight: bold; margin-top: 5px; width: 120px; line-height: 1.2; 
word-wrap: break-word; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">{recommended_movie_names[idx]}</p>
        </div>
        '''

    html_code += '</div>'

    # Use components.html to force proper rendering of HTML
    components.html(html_code, height=300)
