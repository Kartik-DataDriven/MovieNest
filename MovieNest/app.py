# import pickle
# from flask import Flask, render_template, request
# import requests

# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

# def recommend(movie):
#     index = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommended_movie_names = []
#     recommended_movie_posters = []
#     for i in distances[1:6]:
#         # fetch the movie poster
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movie_posters.append(fetch_poster(movie_id))
#         recommended_movie_names.append(movies.iloc[i[0]].title)

#     return recommended_movie_names, recommended_movie_posters

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         search_query = request.form.get('selected_movie')
#         if search_query:
#             # Filter the movie_list to find movies that match the search query
#             matching_movies = [movie for movie in movie_list if search_query.lower() in movie.lower()]

#             if matching_movies:
#                 # If there are matching movies, recommend the first one in the list
#                 recommended_movie_names, recommended_movie_posters = recommend(matching_movies[0])
#             else:
#                 # If no matching movies are found, provide a message or handle it as you like
#                 recommended_movie_names = ["No recommendations found"]
#                 recommended_movie_posters = []

#             return render_template('index.html',
#                 recommended_movie_names=recommended_movie_names,
#                 recommended_movie_posters=recommended_movie_posters)

#     return render_template('index.html', movie_list=movie_list)

# if __name__ == '__main__':
#     # Load the movie data and similarity scores
#     movies = pickle.load(open('model/movie_list.pkl', 'rb'))
#     similarity = pickle.load(open('model/similarity.pkl', 'rb'))

#     # Get the list of movie titles
#     movie_list = movies['title'].values

#     app.run(debug=True)


import pickle
from flask import Flask, render_template, request, jsonify
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('selected_movie')
        if search_query:
            # Filter the movie_list to find movies that match the search query
            matching_movies = [movie for movie in movie_list if search_query.lower() in movie.lower()]

            if matching_movies:
                # If there are matching movies, recommend the first one in the list
                recommended_movie_names, recommended_movie_posters = recommend(matching_movies[0])
            else:
                # If no matching movies are found, provide a message or handle it as you like
                recommended_movie_names = ["No recommendations found"]
                recommended_movie_posters = []

            return render_template('index.html',
                recommended_movie_names=recommended_movie_names,
                recommended_movie_posters=recommended_movie_posters)

    return render_template('index.html', movie_list=movie_list)

@app.route('/suggest')
def suggest():
    query = request.args.get('query')
    matching_movies = [movie for movie in movie_list if query.lower() in movie.lower()]
    suggestions = matching_movies[:10]  # Limit the number of suggestions to 10

    return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    # Load the movie data and similarity scores
    movies = pickle.load(open('model/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))

    # Get the list of movie titles
    movie_list = movies['title'].values

    app.run(debug=True)
