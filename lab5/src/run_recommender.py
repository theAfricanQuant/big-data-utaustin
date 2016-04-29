import sys
import os
import shutil

import matplotlib as mpl
import matplotlib.pyplot as plt

from pyspark import SparkContext
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating

def read_ratings_data(sc):
    ''' Reads in the MovieLens rating data from the file
    and returns it in a Spark RDD of (user, movie, rating). '''
    data = sc.textFile('../../lab2/part2/ml-100k/u.data')
    ratings = data.map(lambda l: l.split()).map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2])))

    return ratings


def load_personal_ratings(sc):
    ''' Reads in personal rating data from the file and
    returns it in a Spark RDD of (user (0), movie, rating). '''
    if not os.path.exists('target/personal_ratings.txt'):
        print('If you want personal recommendations, you must first run init_recommender.py')
        sys.exit(1)

    data = sc.textFile('target/personal_ratings.txt')
    ratings = data.map(lambda l: l.split()).map(lambda l: Rating(0, int(l[0]), float(l[1])))

    return ratings


def load_movies_dict():
    ''' Creates a dictionary of movie ID to movie title
    based on the MovieLens dataset. '''
    all_movies = dict()

    with open('../../lab2/part2/ml-100k/u.item') as f:
        for line in f:
            info = line.split('|')
            movie_id = int(info[0])
            movie_title = info[1]
            
            all_movies[movie_id] = movie_title

    return all_movies


def titles_for_ids(ids):
    ''' Returns the titles for a list of given movie ids. '''
    movies = load_movies_dict()
    titles = []

    for i in ids:
        titles.append(movies[i])

    return titles


def makePlot(x, y, xlabel, ylabel):
    ''' Plots x and y and displays it to the user. '''
    plt.scatter(x, y, color='black')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def set_up():
    ''' Sets up random initalization for the program. '''
    if not os.path.exists('checkpoint/'):
        os.makedirs('checkpoint/')

    if not os.path.exists('target/'):
        os.makedirs('target/')

    reload(sys)
    sys.setdefaultencoding('utf8')

    ALS.checkpointInterval = 2


def use_personal_ratings():
    ''' Returns true if the program was run with the -r option
    and false if it was not. If it was run with any other options,
    prints an error message and exits. '''
    if len(sys.argv) >= 2:
        if len(sys.argv) == 2 and sys.argv[1] == '-r':
            return True
        else:
            print('Usage: .../spark-submit --master local[x] run_recommender.py <-r>')
            sys.exit(1)

    return False


def show_movie_titles(titles):
    ''' Prints all movie titles in the given list. '''
    print('Here are your top movie recommendations:')
    for i, title in enumerate(titles):
        num = i + 1
        print('%s. %s' % (num, title))


def run_als(train, validation, rank=10, iterations=7, l=0.01, save_model=False, sc=None):
    ''' Trains an ALS on train and reports the accuracy on validation. '''
    model = ALS.train(train, rank, iterations, lambda_=l)
    
    if save_model and sc is not None:
        if os.path.exists('target/recommender'):
            shutil.rmtree('target/recommender')
        
        model.save(sc, 'target/recommender')

    # Evaluate model
    if validation is not None:
        testData = validation.map(lambda d: (d[0], d[1]))
        predictions = model.predictAll(testData).map(lambda r: ((r[0], r[1]), r[2]))
        origAndPreds = validation.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
        correct = origAndPreds.map(lambda r: (1 if (abs(r[1][0] - r[1][1]) <= 1.0) else 0))
        accuracy = correct.mean()
        return accuracy

    return None


def als_vary_iterations(train, validation):
    ''' Trains multiple ALS models, varying the numIterations parameter. '''
    iterations = [2, 3, 4, 5, 6, 7]
    accuracies = []
    for i in iterations:
        accuracy = run_als(train, validation, iterations=i)
        accuracies.append(accuracy)

    makePlot(iterations, accuracies, 'numIterations', 'accuracy')


def als_vary_rank(train, validation):
    ''' Trains multiple ALS models, varying the rank parameter. '''
    rank = range(5, 21)
    accuracies = []
    for r in rank:
        accuracy = run_als(train, validation, rank=r)
        accuracies.append(accuracy)

    makePlot(rank, accuracies, 'rank', 'accuracy')


### START HERE ###
set_up()

# Initalize Spark context
sc = SparkContext(appName="Lab5")
sc.setLogLevel("ERROR")
sc.setCheckpointDir('checkpoint/')

# Check how we are running
if use_personal_ratings():
    print('Recommending movies to you based on results from init_recommender.py')
    personal_ratings = load_personal_ratings(sc)
    ratings = read_ratings_data(sc).union(personal_ratings)
else:
    ratings = read_ratings_data(sc)

# Split into train and test
(ratings_train, ratings_validation) = ratings.randomSplit([0.7, 0.3], seed=42)

# Don't want to train all the various models if we're recommending, only the best one
if use_personal_ratings():
    run_als(ratings, None, rank=5, iterations=7, l=0.1, save_model=True, sc=sc)
    model = MatrixFactorizationModel.load(sc, 'target/recommender')

    # Get the 20 best recommended movies for user 0 (the user)
    # Then filter out any they have already rated
    # Convert the movie ids into titles
    movies = model.recommendProducts(0, 20)
    movie_ids = [m[1] for m in movies]
    rated_movie_ids = [m[0] for m in personal_ratings.map(lambda m: (m[1], m[2])).collect() if m[1] != 0]
    unwatched_movies = [m for m in movie_ids if m not in rated_movie_ids]
    top_ten_movies = unwatched_movies[:10]
    titles = titles_for_ids(top_ten_movies)

    show_movie_titles(titles)

    # Done with the personal recommendations
    sys.exit(0)

# Train recommenders
print('Training the model by varying the number of iterations.')
als_vary_iterations(ratings_train, ratings_validation)

print('Training the model by varying the rank.')
als_vary_rank(ratings_train, ratings_validation)

print('Training the model with the best parameters.')
accuracy = run_als(ratings_train, ratings_validation, rank=5, iterations=7, l=0.1)
print('Validation set accuracy: %s' % (accuracy))

print('Training the model on all data and saving it.')
run_als(ratings, None, rank=5, iterations=7, l=0.1, save_model=True, sc=sc)

