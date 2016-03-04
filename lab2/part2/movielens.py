from mrjob.job import MRJob
from mrjob.step import MRStep

import sys
import math

from random import randint, choice

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
    return users


# Returns a tuple of attributes for a selected user. This tuple is
# (age, most_watched_genre_number, highest_rated_genre_number).
def get_attributes_for_user(user):
    age = user[0]
    genre_dict = user[1]

    average_comedy_rating = float(genre_dict[7][1]) / float(genre_dict[7][0]) if genre_dict[7][0] != 0 else 0
    avg_comedy_rating = int(average_comedy_rating)

    return (int(age), avg_comedy_rating)


# Creates k new random centroids. Writes these to k distinct files.
def create_centroids(users, k=10):
    centroids = list()

    for i in xrange(k):
        # Pick a random user ID and get that user's attributes for the centroid
        key = choice(users.keys())
        attributes = list(get_attributes_for_user(users[key]))
        attributes.append(i) # Append the index so we know what number centroid it is later
        centroids.append(attributes) # Add it to the list to return
        
        # Write to file
        filename = "centroid%s.txt" % i
        with open(filename, 'w') as f:
            f.write("%s\n" % attributes)

    return centroids


# Reads all k centroid files and puts them into a list.
def read_centroids(k=10):
    centroids = list()

    for i in xrange(k):
        filename = "centroid%s.txt" % i
        with open(filename, 'r') as f:
            for line in f:
                attributes = eval(line)
                centroids.append(attributes)

    return centroids


class MRMovielens(MRJob):

    def steps(self):
	# Start with the first job that initalizes everything
        jobs = [
            MRStep(mapper_init=self.first_step_init,
                   mapper=self.k_means_mapper,
                   reducer=self.k_means_reducer),
        ]

        # Add 49 normal MR jobs
        for i in xrange(49):
            jobs.append(
                MRStep(mapper_init=self.before_mapper,
                       mapper=self.k_means_mapper,
                       reducer=self.k_means_reducer))

        # Add the last job - final clustering and output of results
        jobs.append(
            MRStep(mapper_init=self.before_mapper,
                   mapper=self.k_means_mapper,
                   reducer=self.final_reducer))

        return jobs


    # This is the mapper_init for the first Job.
    # Builds the database and creates new centroids.
    def first_step_init(self):
        self.users = build_database()
        self.centroids = create_centroids(self.users)


    # This is the mapper_init for a normal K-means iteration.
    # Opens the user database and reads in all of the current centroids.
    def before_mapper(self):
        self.users = open_database()
        self.centroids = read_centroids()


    # This is the mapper for a K-means iteration.
    def k_means_mapper(self, _, line):
        # Calculate the distance to each centroid
        smallest_distance = sys.maxint
        closest_centroid = None

        fields = line.split("|")
        user_id = fields[0]
        attributes = get_attributes_for_user(self.users[user_id])

        for centroid in self.centroids:
            age_diff = pow(centroid[0] - attributes[0], 2)
            genre_diff = pow(centroid[1] - attributes[1], 2)

            distance = math.sqrt((2*age_diff) + genre_diff)

            if distance < smallest_distance:
                smallest_distance = distance
                closest_centroid = centroid

        # Take the closest one, and yield (centroid, (user attributes, input line)) pair
        yield closest_centroid, (attributes, line)


    # This is the reducer for a K-means iteration.
    def k_means_reducer(self, key, values):
        # For a given key, we have a list of users that belong to that key
        # Average their locations to get a new centroid
        count, age, genre_rating = 0, 0, 0
        for value in values:
            attributes = value[0]
            line = value[1]
            count += 1

            age += attributes[0]
            genre_rating += attributes[1]

            # Yield this to the mappers so they can get the users line by line again
            yield None, line

        age /= count
        genre_rating /= count

        new_centroid = (age, genre_rating, key[2])

        # Save the new centroid
        filename = "centroid%s.txt" % key[2]
        with open(filename, 'w') as f:
            f.write("%s\n" % list(new_centroid))


    def final_reducer(self, key, values):
        count = 0
        for value in values:
            attributes = value[0]
            line = value[1]
            count += 1

            yield key, line

        print "Total users under centroid %s: %s" % (key, count)

if __name__ == '__main__':
    MRMovielens.run()
