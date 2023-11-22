import streamlit as st
import pickle
import pandas as pd
import requests

#Creating a function that will return the poster path
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Now create a function which will output top 5 similar movie names
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies_posters = []
    recommended_movies = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        #Fetching poster from the API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

#Opening the dataframe here
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

#Opening the similarity function here
similarity = pickle.load(open('similarity.pkl', 'rb'))

#Giving the title to the homepage
st.title('Movies Recommender System')

#Creating a Selectbox
movie_name = st.selectbox(
    'Select a Movie',
    movies['title'].values)

#Create a button for recommendation
if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.subheader(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.subheader(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.subheader(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.subheader(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.subheader(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])