# MovieMap

## Testing
Before testing, the IMDb CSV files need to be downloaded.

```
https://datasets.imdbws.com/title.basics.tsv.gz
https://datasets.imdbws.com/title.ratings.tsv.gz
```

unittests can be run with,
```bash
docker-compose run -it --rm moviemap python test_scrape.py
```

## Running