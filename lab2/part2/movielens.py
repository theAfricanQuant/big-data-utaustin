from mrjob.job import MRJob
from mrjob.step import MRStep

from random import randint

# Given an input line from a movie item, this will return a list of
# numbers that correspond to the genres that the movie item belongs to.
def get_genre_numbers(movie):
    genres = list()
    start_index = 5 # Movie genres start at index 5

    # There are 18 genres
    for i in xrange(18):
        index = i + start_index

        # If the movie is in this genre, add the number to the list
        if int(movie[index]) == 1:
            genres.append(i)

    return genres


# Builds a dict where the keys are all of the genre numbers
# and the values are a 2-element list.
# The first element is the count of movies in a particular genere
# and the second is the sum of all the ratings in a particular genre.
def build_ratings_dict():
    dictionary = dict()

    for i in xrange(18):
        dictionary[i] = [0, 0]

    return dictionary


# Gives a list of k random numbers between 0 and upper_bound.
def random_numbers(k, upper_bound):
    numbers = list()
    for i in xrange(k):
        numbers.append(randint(0, upper_bound))

    return numbers


# Opens the database.txt file and returns it as a dict.
def open_database():
    with open('database.txt', 'r') as f:
        for line in f:
            return eval(line)


# Writes the database dict to a file.
def write_to_file(db):
    with open('database.txt', 'w') as f:
        f.write("%s" % db)


# Builds the user database.
def build_database():
    # Builds a dict where key is User ID and value is (age, genre ratings dict) tuple
    users = dict()
    with open('u.user', 'r') as user_file:
       for line in user_file:
            fields = line.split("|")
            users[fields[0]] = (fields[1], build_ratings_dict())
      
    # Builds a dict where key is movie ID and value is tuple of genre numbers
    movies = dict()
    with open('u.item', 'r') as movie_file:
        for line in movie_file:
            fields = line.split("|")
            movies[fields[0]] = get_genre_numbers(fields)
       
    # Goes line by line and fills updates user ratings dicts accordingly
    with open('u.data', 'r') as data_file:
        for line in data_file:
            fields = line.split()

            # Get the ratings dict for the user that did this rating
            user = users[fields[0]]
            ratings = user[1]

            # Get the genre numbers for this movie that was rated
            genres = movies[fields[1]]

            # For each genre that the movie is in, add 1 to the count and the rating to the sum
            for genre in genres:
                current = ratings[genre]
                current[0] += 1 # count
                current[1] += int(fields[2]) # sum of ratings
    
    # Finally write this to the database file so we can use it later
    write_to_file(users)


class MRMovielens(MRJob):

    def steps(self):
	# This function defines the steps your job will follow. If you want to chain jobs, you can just have multiple steps.
        return [
            MRStep(mapper_init=self.first_step_init, mapper=self.k_means_mapper, reducer=self.k_means_reducer),
        ]


    def first_step_init(self):
        print "First Step Init"
        build_database()


    def k_means_mapper(self, _, line):
        # Calculate the distance to each centroid
        
        # Take the closest one, and yield (centroid, user) pair
        yield "x", 1


    def k_means_reducer(self, key, values):
        # For a given key, we have a list of users that belong to that key
        # Average their locations to get a new centroid
        yield key, sum(values)


if __name__ == '__main__':
    MRMovielens.run()
