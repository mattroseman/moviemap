from get_movies import get_movies


def main():
    movies = get_movies()

    movies.sort(key=lambda movie: movie.rating.num_votes if movie.rating else 0, reverse=True)
    for movie in movies[:10]:
        movie.get_locations()
        print(movie)


if __name__ == '__main__':
    main()
