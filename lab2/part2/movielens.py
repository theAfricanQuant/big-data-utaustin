from mrjob.job import MRJob
from mrjob.step import MRStep

from random import randint

def get_genre_numbers(field):
    start_index = 5
    genres = list()

    for i in xrange(18):
        index = i + start_index
        if int(field[index]) == 1:
            genres.append(i)

    return genres


def build_ratings_dict():
    dictionary = dict()

    for i in xrange(18):
        dictionary[i] = [0, 0]

    return dictionary


def random_numbers(k, upper_bound):
    numbers = list()
    for i in xrange(k):
        numbers.append(randint(0, upper_bound))

    return numbers


class MRMovielens(MRJob):

    def steps(self):
	# This function defines the steps your job will follow. If you want to chain jobs, you can just have multiple steps.
        return [
            MRStep(mapper_init=self.build_dicts, mapper=self.k_means_mapper, reducer=self.k_means_reducer),
        ]


    def build_dicts(self):
        # Builds a dict where key is User ID and value is (age, genre ratings dict) tuple
        self.users = dict()
        with open('u.user', 'r') as user_file:
            for line in user_file:
                fields = line.split("|")
                self.users[fields[0]] = (fields[1], build_ratings_dict())
      
        # Builds a dict where key is movie ID and value is tuple of genre numbers
        self.movies = dict()
        with open('u.item', 'r') as movie_file:
            for line in movie_file:
                fields = line.split("|")
                self.movies[fields[0]] = get_genre_numbers(fields)
       
        # Goes line by line and fills updates user ratings dicts accordingly
        with open('u.data', 'r') as data_file:
            for line in data_file:
                fields = line.split()

                # Get the ratings dict for the user that did this rating
                user = self.users[fields[0]]
                ratings = user[1]

                # Get the genre numbers for this movie that was rated
                genres = self.movies[fields[1]]

                # For each genre that the movie is in, add 1 to the count and the rating to the sum
                for genre in genres:
                    current = ratings[genre]
                    current[0] += 1 # count
                    current[1] += int(fields[2]) # sum of ratings
        
        print self.users
        # Get random initial centroids (user IDs)       
#        self.centroids = random_numbers(5, len(self.users))
#        print self.centroids


    def k_means_mapper(self, _, line):
        # Calculate the distance to each centroid
#        for user_id, value in self.users.iteritems():
#            smallest_distance = sys.maxint
#            closest_centroid = None
#
#            for centroid in self.centroids:
#                centroid_age = self.users[centroid][0]
        print line
        # Take the closest one, and yield (centroid, user) pair
        yield "x", 1


    def k_means_reducer(self, key, values):
        # For a given key, we have a list of users that belong to that key
        # Average their locations to get a new centroid
        yield key, sum(values)


if __name__ == '__main__':
    MRMovielens.run()
