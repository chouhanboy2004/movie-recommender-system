import streamlit as st
import pickle
import pandas as pd
import requests
from time import sleep

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

Selected_Movie_Name = st.selectbox(
    'Which Type Of Movies You Want To See :',
    movies['title'].values
)

# for also print poster
# def fetch_poster(movie_id):
#    response =  requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2260406e357eb41f6abd23c6fb08c24f&language=en-US'.format(movie_id))
#    data = response.json()
#    return "https://image.tmdb.org/t/p/original"+data['poster_path']
# 🛠 Safe poster fetcher with retry and fallback
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=2260406e357eb41f6abd23c6fb08c24f&language=en-US'
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return "https://image.tmdb.org/t/p/original" + data['poster_path']
        except Exception as e:
            print(f"Poster fetch failed (Attempt {attempt + 1}): {e}")
            sleep(1)
    # Fallback image
    return "https://via.placeholder.com/300x450?text=Poster+Unavailable"
# try–except concept ek error handling mechanism hai jo aapke code ko crash hone se bachata hai, jab koi runtime error aata hai.
def Recommand(selected_movie):
    movie_index = movies[movies['title'] == selected_movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    Recommanded_movies = []
    Recommanded_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id  # fetch poster from API
        Recommanded_movies.append(movies.iloc[i[0]].title)
        Recommanded_movies_posters.append(fetch_poster(movie_id))
    return Recommanded_movies,Recommanded_movies_posters

if st.button('recommand'):
    st.write('This type of movies are recommanding : ')
    names,posters = Recommand(Selected_Movie_Name)

    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

# for run write in terminal :- streamlit run app.py
# deploy karna abhi baki hai