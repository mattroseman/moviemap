"""
scrape_locations.py holds the logic to scrape the location data of a movie from IMDb.
"""
from typing import List

import requests
from bs4 import BeautifulSoup

IMDB_LOCATION_URL_TEMPLATE = 'https://www.imdb.com/title/{movie_id}/locations/'


def scrape_locations(movie_id: str) -> List:
    movie_location_url = IMDB_LOCATION_URL_TEMPLATE.format(movie_id=movie_id)
    print(f'Scraping locations for movie ID: {movie_id} from {movie_location_url}...')
    response = requests.get(movie_location_url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch locations for movie ID {movie_id}. Status code: {response.status_code}")

    body = response.text

    print('Successfully scraped locations.')

    print('Parsing locations from HTML...')

    locations = []
    html = BeautifulSoup(body, 'html.parser')

    location_elements = html.select('div:has(p):has(a)')
    for location_element in location_elements:
        if (
            not location_element.find('a', recursive=False)
            or not location_element.find('p', recursive=False)
        ):
            continue

        locations.append({
            'name': location_element.find('a', recursive=False).get_text(strip=True).replace('\n', ''),
            'description': location_element.find('p', recursive=False).get_text(strip=True).replace('\n', '').strip('()')
        })

    print('Successfully parsed locations.')

    return locations


if __name__ == '__main__':
    locations = scrape_locations('tt0056172')

    print(locations)
