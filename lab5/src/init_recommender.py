import random

def get_random_movies():
    all_movies = []

    with open('../../lab2/part2/ml-100k/u.item') as f:
        for line in f:
            info = line.split('|')
            movie_id = info[0]
            movie_title = info[1]
            
            all_movies.append((movie_id, movie_title))

    random_movies = set()

    while len(random_movies) < 10:
        random_movies.add(random.choice(all_movies))

    return list(random_movies)


def get_input_for_prompt(prompt):
    while True:
        value = raw_input('%s: ' % prompt)
        try:
            value = int(value)
            return value
        except ValueError:
            print('Please enter an integer number.')
            continue


def rate_movies(movies):
    ratings = []

    print('Please rate the following 10 movies from 1 to 5.')
    print('Enter a 0 if you have not seen the movie.')
    for movie in movies:
        rating = get_input_for_prompt(movie[1])
        while rating > 5 or rating < 0:
            print('Please rate from 1 to 5, or 0 if you have not seen it.')
            rating = get_input_for_prompt(movie[1])

        ratings.append((movie[0], rating))

    return ratings


### START HERE ###
movies = get_random_movies()
ratings = rate_movies(movies)
print(ratings)

