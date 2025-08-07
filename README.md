# MovieMap

## Testing
The IMDb CSV files need to be downloaded to `src/test/test_data`:
```
https://datasets.imdbws.com/title.basics.tsv.gz
https://datasets.imdbws.com/title.ratings.tsv.gz
``` 

Then unittests can be run with,
```bash
docker-compose run -it --rm moviemap python -m src.test.test_get_movies
```

## Running