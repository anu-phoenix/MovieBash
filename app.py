import streamlit as st
import pandas as pd
import pickle
import requests
import math
# import sklearn

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# tfidf = TfidfVectorizer()

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


def poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=980a9870aa7f50bf36a1e70d77a5e74c&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


# data_tfidf = []
# for i in movies['tags']:
#     data_tfidf.append(i)
# result = tfidf.fit_transform(data_tfidf)
# resultMatrix = result.toarray()
#
# similarity = cosine_similarity(resultMatrix)


def recommend(movie, movieCount):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_poster = []
    for i in distances[1:movieCount+1]:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_poster.append(poster(movies.iloc[i[0]].movie_id))
    return recommended_movies, recommended_poster


st.title('Movie Bash')

movie_selected = st.selectbox(
    'Which type of movie you will like to watch?',
    movies['title'].values)
moviesCount = st.selectbox(
    'Number of Movies we should recommend?',
    [i for i in range(1, 31)])

if st.button('Recommend'):
    movie_names, poster = recommend(movie_selected, moviesCount)

    count = 0
    for _ in range(math.ceil(moviesCount/5)):
        cols = list(st.columns(5))
        temp = int(count / 5)
        for col in range(len(cols)):
            with cols[col]:
                st.text(movie_names[temp*5+col])
                st.image(poster[temp*5+col])
            count += 1
            if count >= moviesCount:
                break
        if count >= moviesCount:
            break
