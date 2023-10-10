import requests_with_caching
import json

def get_movies_from_tastedive(name):
    baseurl = "https://tastedive.com/api/similar"
    params_diction = {}
    params_diction['q'] = name
    params_diction['type'] = 'movies'
    params_diction['limit'] = 5
    tastedive_resp = requests_with_caching.get(baseurl, params = params_diction)
     
    return tastedive_resp.json()

def extract_movie_titles(movies):
    movie_title = []
        
    for i in range(5) :
        movie_title.append(movies["Similar"]["Results"][i]['Name'])
    
    return movie_title

def get_related_titles(lst_movie_titles):
    comb_movie_titles = []
    for lst_movie_title in lst_movie_titles:
        extract_Mtitles= extract_movie_titles(get_movies_from_tastedive(lst_movie_title))
        
        for extract_Mtitle in extract_Mtitles:
            if extract_Mtitle not in comb_movie_titles:
                comb_movie_titles.append(extract_Mtitle)
    return comb_movie_titles

def get_movie_data(title):
    baseurl = "http://www.omdbapi.com/"
    params_diction = {}
    params_diction['t'] = title
    params_diction['r'] = 'json'
    OMDB_resp = requests_with_caching.get(baseurl, params = params_diction)
   
    return OMDB_resp.json()

def get_movie_rating(OMDB_Dict):
    try:
        if (OMDB_Dict['Ratings'][1]['Source'] == 'Rotten Tomatoes'):
            return int(OMDB_Dict['Ratings'][1]['Value'].replace('%' ,''))
        else:
            return 0
    except:
        return 0

def get_sorted_recommendations(x):    
    y = sorted(get_related_titles(x), key = lambda title: (get_movie_rating(get_movie_data(title)), title), reverse = True)
    return y

get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
