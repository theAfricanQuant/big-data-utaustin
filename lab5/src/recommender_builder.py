from pyspark import SparkContext

from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating


def read_ratings_data(sc):
    ''' Reads in the MovieLens rating data from the file
    and returns it in a Spark RDD of (user, movie, rating). '''
    data = sc.textFile('../../lab2/part2/ml-100k/u.data')
    ratings = data.map(lambda l: l.split()).map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2])))

    return ratings


def set_up_als():
    ''' Sets up MLLib ALS for training. This function was made
    in case we need to do more setup in the future. '''
    ALS.checkpointInterval = 2


def run_als(train, validation, rank=10, iterations=7):
    ''' Trains an ALS on train and reports the accuracy on validation. '''
    model = ALS.train(train, rank, iterations)

    # Evaluate model
    testData = validation.map(lambda d: (d[0], d[1]))
    predictions = model.predictAll(testData).map(lambda r: ((r[0], r[1]), r[2]))
    origAndPreds = validation.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
    correct = origAndPreds.map(lambda r: (1 if (abs(r[1][0] - r[1][1]) <= 1.0) else 0))
    accuracy = correct.mean()
    
    return accuracy


def als_vary_iterations(train, validation):
    ''' Trains multiple ALS models, varying the numIterations parameter. '''
    iterations = [2, 3, 4, 5, 6, 7]
    accuracies = []
    for i in iterations:
        accuracy = run_als(train, validation, iterations=i)
        accuracies.append(accuracy)

    # TODO plot
    print(accuracies)


def als_vary_rank(train, validation):
    ''' Trains multiple ALS models, varying the rank parameter. '''
    rank = range(5, 21)
    accuracies = []
    for r in rank:
        accuracy = run_als(train, validation, rank=r)
        accuracies.append(accuracy)

    # TODO plot
    print(accuracies)


### START HERE ###
# Initalize Spark context
sc = SparkContext(appName="Lab5")
sc.setLogLevel("ERROR")
sc.setCheckpointDir('checkpoint/')

# Read in ratings data
ratings = read_ratings_data(sc)

# Split into train and test
(ratings_train, ratings_validation) = ratings.randomSplit([0.7, 0.3], seed=42)

# Do any setup required
set_up_als()

# Train recommenders
print('Training the model by varying the number of iterations.')
als_vary_iterations(ratings_train, ratings_validation)

print('Training the model by varying the rank.')
als_vary_rank(ratings_train, ratings_validation)

