"""
get_movies.py holds the logic to request the IMDb movie data sets in TSV form.
It also queries the review data and merges it.
"""
from typing import List
from dataclasses import dataclass, asdict, field
import io
import gzip
import csv
import json

import requests

from scrape_locations import Location, scrape_locations

IMDB_BASIC_FILE_URL = 'https://datasets.imdbws.com/title.basics.tsv.gz'
IMDB_RATING_FILE_URL = 'https://datasets.imdbws.com/title.ratings.tsv.gz'


@dataclass
class Rating:
    average_rating: float
    num_votes: int


@dataclass
class Movie:
    id: str
    title: str
    original_title: str
    year: str
    rating: Rating = None
    locations: List[Location] = field(default_factory=list)

    def get_locations(self) -> 'Movie':
        self.locations = scrape_locations(self.id)
        return self


def get_movies() -> List[Movie]:
    """
    Fetches movie data from public IMDb datasets.

    Returns: A list of Movies, each representing an IMDb movie
    [
        Movie(
            id = 'tt0000001',
            title = 'Movie Title',
            original_title = 'Original Movie Title',
            year = '2023',
            rating = Rating(
                average_rating = 7.5,
                num_votes = 1000
            ),
        ),
        ...
    ]
    """
    movies = get_basic_movies()
    ratings = get_movie_ratings()

    print('Merging ratings into movie data...')
    # merge movies with their ratings
    for id, movie in movies.items():
        movie.rating = ratings.get(id)
    print('Ratings merged successfully.')

    # Convert the dictionary, with movieID keys, to a flat list, with IDs as another key/value pair
    return list(movies.values())


def get_basic_movies() -> dict[str, Movie]:
    """
    Fetches basic movie data from IMDb datasets.

    Returns: A dict, with the keys being IDs and the values Movie objects
    {
        'tt0000001': Movie(
            id = 'tt0000001',
            title = 'Movie Title',
            original_title = 'Original Movie Title',
            year = '2023'
        ),
        ...
    }
    """
    print('Fetching basic movie data...')
    movies = {}

    response = requests.get(IMDB_BASIC_FILE_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch basic movie data: {response.status_code}")

    with gzip.open(io.BytesIO(response.content), 'rt', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            if row['titleType'] == 'movie':
                movies[row['tconst']] = Movie(
                    id=row['tconst'],
                    title=row['primaryTitle'],
                    original_title=row['originalTitle'],
                    year=row['startYear']
                )

    print('Basic movie data fetched successfully.')

    return movies


def get_movie_ratings() -> dict[str, Rating]:
    """
    Fetches movie ratings data from IMDb datasets.

    Returns: A dictionary of movie ratings, with the keys being IDs and the values Rating objects
    {
        'tt0000001': Rating(
            average_rating = 7.5,
            num_votes = 1000
        ),
        ...
    }
    """
    print('Fetching movie ratings data...')
    ratings = {}

    response = requests.get(IMDB_RATING_FILE_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch movie ratings data: {response.status_code}")

    with gzip.open(io.BytesIO(response.content), 'rt', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            ratings[row['tconst']] = Rating(
                average_rating=float(row['averageRating']),
                num_votes=int(row['numVotes'])
            )

    print('Movie ratings data fetched successfully.')
    return ratings


if __name__ == '__main__':
    movies = get_movies()
    print(json.dumps([asdict(movie) for movie in movies[:10]], indent=2))
