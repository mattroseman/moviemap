from typing import List
import io
import gzip
import csv

import requests

IMDB_BASIC_FILE_URL = 'https://datasets.imdbws.com/title.basics.tsv.gz';
IMDB_RATING_FILE_URL = 'https://datasets.imdbws.com/title.ratings.tsv.gz';

def get_movies() -> List[dict]:
    movies = get_basic_movies()
    ratings = get_movie_ratings()

    print('Merging ratings into movie data...')
    # merge movies with their ratings
    for tconst in movies.keys():
        movies[tconst].update(ratings.get(tconst, {}))
    print('Ratings merged successfully.')

    movies_list = []
    for movie_id in movies.keys():
        movies_list.append({
            'tconst': movie_id,
            'title': movies[movie_id]['title'],
            'originalTitle': movies[movie_id]['originalTitle'],
            'year': movies[movie_id]['year'],
            'averageRating': movies[movie_id].get('averageRating', None)
        })

    return movies_list

def get_basic_movies() -> dict:
    print('Fetching basic movie data...')
    movies = {}

    response = requests.get(IMDB_BASIC_FILE_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch basic movie data: {response.status_code}")

    with gzip.open(io.BytesIO(response.content), 'rt', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            if row['titleType'] == 'movie':
                movies[row['tconst']] = {
                    'title': row['primaryTitle'],
                    'originalTitle': row['originalTitle'],
                    'year': row['startYear']
                }

    print('Basic movie data fetched successfully.')

    return movies

def get_movie_ratings() -> dict:
    print('Fetching movie ratings data...')
    ratings = {} 

    response = requests.get(IMDB_RATING_FILE_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch movie ratings data: {response.status_code}")

    with gzip.open(io.BytesIO(response.content), 'rt', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            ratings[row['tconst']] = {
                'averageRating': float(row['averageRating']),
                'numVotes': int(row['numVotes'])
            }

    print('Movie ratings data fetched successfully.')
    return ratings


if __name__ == '__main__':
    movies = get_movies()
    print(movies[0:10])