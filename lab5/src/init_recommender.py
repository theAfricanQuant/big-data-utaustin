import os
import sys
import random

def get_random_movies():
    ''' Finds 10 random movies in the MovieLens dataset and returns them
    as a list of (movie_id, movie_title). '''
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
    ''' Gets an integer input by displaying prompt to the
    user and waiting for input. '''
    while True:
        value = raw_input('%s: ' % prompt)
        try:
            value = int(value)
            return value
        except ValueError:
            print('Please enter an integer number.')
            continue


def rate_movies(movies):
    ''' Asks the user to rate all the movies in the input
    movies list. Returns a list of (movie_id, user_rating)
    for all of the movies. '''
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


def save_personal_ratings(ratings):
    ''' Saves the movie ratings in a file called
    personal_ratings.txt. '''
    if not os.path.exists('target/'):
        os.makedirs('target/')

    with open('target/personal_ratings.txt', 'w') as f:
        for rating in ratings:
            f.write('%s %s\n' % (rating[0], rating[1]))


### START HERE ###
reload(sys)
sys.setdefaultencoding('utf8')

movies = get_random_movies()
ratings = rate_movies(movies)
save_personal_ratings(ratings)

