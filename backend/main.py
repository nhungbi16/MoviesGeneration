from flask import Flask

api = Flask(__name__)

# model imports
from transformers import ViTImageProcessor
from transformers import ViTForImageClassification
from PIL import Image
import requests
import numpy

from datasets import load_dataset

dataset = load_dataset("csv", data_files="imdb_top_1000.csv")
database = dataset['train']


# import random
import random
 
# prints a random value from the list
all_movies = [i for i in range(len(database))]

from flask import request, jsonify

# global var think if this as the database
label2id = {
    "Action": 2,
    "Adventure": 3,
    "Animation": 12,
    "Biography": 4,
    "Comedy": 10,
    "Crime": 1,
    "Drama": 0,
    "Family": 13,
    "Fantasy": 9,
    "Film-Noir": 19,
    "History": 5,
    "Horror": 17,
    "Music": 16,
    "Musical": 18,
    "Mystery": 15,
    "Romance": 7,
    "Sci-Fi": 6,
    "Sport": 20,
    "Thriller": 11,
    "War": 14,
    "Western": 8}

id2label =  {
    0: "Drama",
    1: "Crime",
    10: "Comedy",
    11: "Thriller",
    12: "Animation",
    13: "Family",
    14: "War",
    15: "Mystery",
    16: "Music",
    17: "Horror",
    18: "Musical",
    19: "Film-Noir",
    2: "Action",
    20: "Sport",
    3: "Adventure",
    4: "Biography",
    5: "History",
    6: "Sci-Fi",
    7: "Romance",
    8: "Western",
    9: "Fantasy"
  }

def get_results(logits: list):
    rounded_logs = [round(num) for num in logits]
    filtered1 = [1 if abs(num) == 1  else 0 for num in rounded_logs]
    filtered2 = [1 if num > 0 else 0 for num in rounded_logs]
    ids = [num1 if num1 == 1 else num2 for (num1, num2) in zip(filtered1, filtered2)]
    return [id2label[i] for i in range(len(id2label)) if ids[i] == 1]

def extract_ids(link:str) :
    im = Image.open(requests.get(link, stream=True).raw).convert('RGB')
    new_feature_extractor = ViTImageProcessor.from_pretrained('MoviesModel/movies_generation')
    inputs = new_feature_extractor(im, return_tensors='pt')

    new_model = ViTForImageClassification.from_pretrained('MoviesModel/movies_generation', problem_type="multi_label_classification")
    output = new_model(**inputs)
    return output.logits[0].detach().numpy()

@api.route('/get_categories', methods = ["POST"])
def get_ids():
    """
    args: {
        inputURL: str
    }
    returns: list of genres
    """
    link = request.get_json().get('inputURL')
    output = extract_ids(link)
    results = get_results(output)

    return results

@api.route('/get_movies_recommendations', methods = ["POST"])
def get_movies():
    """
    args: {
        inputURL: str
    }
    returns: list of movie dicts
    """
    link = request.get_json().get('inputURL')
    output = extract_ids(link)
    genres = get_results(output) 
    if len(genres) == 0: #just find random
        genres = [label for label in label2id.keys()]

    return jsonify({'movies': find_ten_movies(genres), 'genres': genres})

#{'Poster_Link': 'https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX67_CR0,0,67,98_AL_.jpg', 
# 'Series_Title': 'The Shawshank Redemption',
#  'Released_Year': '1994', 
# 'Certificate': 'A', 
# 'Runtime': '142 min', 
# 'Genre': 'Drama', 
# 'IMDB_Rating': 9.3, 
# 'Overview': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', 
# 'Meta_score': 80.0, 
# 'Director': 'Frank Darabont',
# 'Star1': 'Tim Robbins', 
# 'Star2': 'Morgan Freeman',
#  'Star3': 'Bob Gunton', 
# 'Star4': 'William Sadler', 
# 'No_of_Votes': 2343110, 
# 'Gross': '28,341,469'}

def clean_genre(data):
    genre_list = data['Genre'].split(',')
    genre_list = [genre.strip() for genre in genre_list]
    return genre_list

def find_ten_movies(genres: list):
    movies = [] #dicts
    seen = set()
    while len(movies) < 10:
        current_movie = random.choice(all_movies)
        if current_movie not in seen:
            movie = database[current_movie] #dict of movie o
            movie_genres = clean_genre(movie)
            similar_genres = [genre for genre in movie_genres if genre in genres]
            if similar_genres: #nonempty
                movies.append(movie)

            seen.add(current_movie)
    
    return movies
