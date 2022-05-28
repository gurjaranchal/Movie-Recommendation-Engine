import streamlit as st
from PIL import Image
import json
from Classifier import KNearestNeighbours
from bs4 import BeautifulSoup
import requests,io
import PIL.Image
from urllib.request import urlopen


logo=Image.open('logo.png')
st.set_page_config(page_title="Movie Recommendation Engine",

page_icon=logo,layout="centered",
     initial_sidebar_state="expanded",)

def set_bg_hack_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
            
             background: url("https://greatloveart.com/wp-content/uploads/2021/12/Batman-Wallpaper-2021.jpg");
             background-size: cover;
             font-size: 10px;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
set_bg_hack_url()

def movie_poster_fetcher(imdb_link):
    url_data = requests.get(imdb_link).text
    s_data = BeautifulSoup(url_data, 'html.parser')
    imdb_dp = s_data.find("meta", property="og:image")
    movie_poster_link = imdb_dp.attrs['content']
    u = urlopen(movie_poster_link)
    raw_data = u.read()
    img = PIL.Image.open(io.BytesIO(raw_data))
    st.image(img,width=300)

def get_movie_info(imdb_link):
    url_data = requests.get(imdb_link).text
    s_data = BeautifulSoup(url_data, 'html.parser')
    imdb_content = s_data.find("meta", property="og:description")
    movie_descr = imdb_content.attrs['content']
    movie_descr = str(movie_descr).split('.')
    movie_director = movie_descr[0]
    movie_cast = str(movie_descr[1]).replace('With', 'Cast: ').strip()
    movie_story = 'Story: ' + str(movie_descr[2]).strip()+'.'
    return movie_director,movie_cast,movie_story

def KNN(test_point, k):
    target = [0 for item in movie_titles]
    model = KNearestNeighbours(data, target, test_point, k=k)
    model.fit()
    table = []
    for i in model.indices:
           table.append([movie_titles[i][0], movie_titles[i][2],data[i][-1]])
    return table


def get_movie():
    st.title("Movie Recommendation Engine")
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
    movies = [title[0] for title in movie_titles]
    category = ['--Select--', 'Movie based', 'Genre based']
    cat_op = st.selectbox('Select Recommendation Type', category)
    if cat_op == category[0]:
        st.info('Please Select Recommendation Type')
    elif cat_op == category[1]:
        select_movie = st.selectbox(' How would you like ? ', ['--Select--'] + movies)
        select_radio = st.radio("Do you want to Fetch Movie Poster?", ('Yes', 'No'))
        if select_radio == 'No':
            if select_movie == '--Select--':
                st.info('Please select Movie.....')
            else:
                no_of_reco = st.slider('Number of movies you want to Recommend', min_value=5, max_value=20, step=1)
                genres = data[movies.index(select_movie)]
                test_points = genres
                table = KNN(test_points, no_of_reco+1)
                link1=table[0][1]
                movie1=table[0][0]
                rating1=table[0][2]
                table.pop(0)
                k = 0
                if st.button('Get Selected Movie Info'):
                         
                        director,cast,story = get_movie_info(link1)
                        st.markdown(f"[{movie1}]({link1})")
                        st.markdown(director)
                        st.markdown(cast)
                        st.markdown(story)
                        st.markdown('IMDB Rating: ' + str(rating1) + '⭐')
                
                    
                if  st.button('Recommended Movies'):
                    for movie, link, ratings in table:
                        k+=1
                        director,cast,story = get_movie_info(link)
                        st.markdown(f"{k}. [{movie}]({link})")
                        st.markdown(director)
                        st.markdown(cast)
                        st.markdown(story)
                    
                        st.markdown('IMDB Rating: ' + str(ratings) + '⭐')
        else:
             if select_movie == '--Select--':
                st.info('Please select Movie.....')
             else:
                no_of_reco = st.slider('Number of movies you want to Recommend', min_value=5, max_value=20, step=1)
                genres = data[movies.index(select_movie)]
                test_points = genres
                table = KNN(test_points, no_of_reco+1)
                link1=table[0][1]
                movie1=table[0][0]
                rating1=table[0][2]
                table.pop(0)
                k = 0
                if st.button('Get Selected Movie Info'):
                        
                        director,cast,story = get_movie_info(link1)
                        movie_poster_fetcher(link1)
                        st.markdown(f"[{movie1}]({link1})")
                        st.markdown(director)
                        st.markdown(cast)
                        st.markdown(story)
                        st.markdown('IMDB Rating: ' + str(rating1) + '⭐')
                
                if st.button('Recommended Movies'):
                    for movie, link, ratings in table:
                         k += 1
                         st.markdown(f"{k}. [{movie}]({link})")
                         movie_poster_fetcher(link)
                         director,cast,story = get_movie_info(link)
                         st.markdown(director)
                         st.markdown(cast)
                         st.markdown(story)
                         st.markdown('IMDB Rating: ' + str(ratings) + '⭐')
    elif cat_op == category[2]:
        sel_gen = st.multiselect('Select Genres ', genres)
        select_radio = st.radio("Do you want to Fetch Movie Poster?", ('Yes', 'No'))
        if select_radio == 'No':
                if sel_gen:
                    imdb_score = st.slider('Choose IMDb score:', 1, 10, 7)
                    no_of_reco = st.number_input('Number of movies you want to Recommend', min_value=5, max_value=20, step=1)
                    if st.button('Recommended Movies'):
                        test_point = [1 if genre in sel_gen else 0 for genre in genres]
                        test_point.append(imdb_score)
                        table = KNN(test_point, no_of_reco)
                        k = 0
                        for movie, link, ratings in table:
                            k += 1
                            st.markdown(f"{k}. [ {movie}]({link})")
                            director,cast,story = get_movie_info(link)
                            st.markdown(director)
                            st.markdown(cast)
                            st.markdown(story)
                            st.markdown('IMDB Rating: ' + str(ratings) + '⭐')
        else:
            if sel_gen:
                imdb_score = st.slider('Choose IMDb score:', 1, 10, 8)
                no_of_reco = st.number_input('Number of movies you want to Recommend', min_value=5, max_value=20, step=1)
                
                if st.button('Recommended Movies'):
                       test_point = [1 if genre in sel_gen else 0 for genre in genres]
                       test_point.append(imdb_score)
                       table = KNN(test_point, no_of_reco)
                       k = 0
                       for movie, link, ratings in table:
                           k += 1
                           st.markdown(f"{k}. [ {movie}]({link})")
                           movie_poster_fetcher(link)
                           director,cast,story = get_movie_info(link)
                           st.markdown(director)
                           st.markdown(cast)
                           st.markdown(story)
                           st.markdown('IMDB Rating: ' + str(ratings) + '⭐')


with open(r'data.json', 'r+', encoding='utf-8') as fd:
    data = json.load(fd)
with open(r'title.json', 'r+', encoding='utf-8') as fd:
    movie_titles = json.load(fd)

if __name__ == '__main__':
    get_movie()
