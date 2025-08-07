import unittest
from unittest.mock import patch, MagicMock
import json

import scrape

with open('./test_data/title.basics.tsv.gz', 'rb') as file:
    BASICS_CONTENT = file.read()
with open('./test_data/title.ratings.tsv.gz', 'rb') as file:
    RATINGS_CONTENT = file.read()

def mock_requests_get(url, *args, **kwargs):
    if 'title.basics.tsv.gz' in url:
        return MagicMock(status_code=200, content=BASICS_CONTENT)
    elif 'title.ratings.tsv.gz' in url:
        return MagicMock(status_code=200, content=RATINGS_CONTENT)

    return MagicMock(status_code=404, content=b'')


class TestScrape(unittest.TestCase):
    @patch('requests.get', side_effect=mock_requests_get)
    def test_scrape(self, mock_get):
        movies = scrape.get_movies()
        print(json.dumps(movies[:10], indent=2))

        self.assertTrue(len(movies) > 0)
        for movie in movies:
            self.assertIn('tconst', movie)
            self.assertIn('title', movie)
            self.assertIn('year', movie)
            self.assertIn('averageRating', movie)


if __name__ == '__main__':
    unittest.main()
