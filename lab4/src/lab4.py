import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from time import time

from pyspark import SparkContext
from pyspark.sql import SQLContext

from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.util import MLUtils

# Reads in the arcene dataset.
# t should be either 'train' or 'test' to load the respective dataset.
def read_data(t):
    # Make sure we are loading either train or test data
    if t not in ['train', 'test']:
        raise ValueError("Not valid data type.")
    # First load the prediction data
    data = pd.read_csv(f"../dataset/arcene_{t}.data", sep=' ', header=None)
    data.drop(data.columns[[10000]], axis=1, inplace=True)

    # Then the load labels associated with them
    # Replace the class -1 with class 0 for MLLib to use
    labels = pd.read_csv(
        f"../dataset/arcene_{t}.labels", header=None, names=["class"]
    )
    labels.replace(-1.0, 0.0, inplace=True)

    # Combine the two into one dataframe
    return pd.concat([labels, data], axis=1)


# Converts a Pandas dataframe to a LabeledPoint RDD
def convertToLabeledPoint(sc, dataframe):
    sql_context = SQLContext(sc)
    df = sql_context.createDataFrame(dataframe)

    # Convert to LabeledPoint RDD
    return df.map(lambda line:LabeledPoint(line[0],[line[1:]]))


# Fits a Decision Tree using the training data and measures error against the validation data.
def fitDecisionTree(train_data, validation_data, impurity='gini', maxBins=32, maxDepth=5):
    model = DecisionTree.trainClassifier(train_data, numClasses=2, categoricalFeaturesInfo={},
                                         impurity=impurity, maxBins=maxBins, maxDepth=maxDepth, minInfoGain=0.05)

    predictions = model.predict(validation_data.map(lambda x: x.features))
    labelsAndPredictions = validation_data.map(lambda lp: lp.label).zip(predictions)
    testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(validation_data.count())
    
    accuracy = 1.0 - testErr
    print('Accuracy = ' + str(accuracy))
    #print('Learned classification tree model:')
    #print(model.toDebugString())

    return accuracy


# Plots x and y and displays it to the user.
def makePlot(x, y, xlabel, ylabel):
    plt.scatter(x, y, color='black')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


# Fits 10 decision trees, varying the number of maxBins used.
def decisionTreeVaryBins(train_data, validation_data):
    bins = [2, 6, 10, 14, 18, 22, 26, 30, 34, 38]
    accuracy = []
    for b in bins:
        print(f'maxBins={b}')
        result = fitDecisionTree(train_data, validation_data, impurity='gini', maxBins=b)
        accuracy.append(result)

    makePlot(bins, accuracy, 'maxBins', 'accuracy')


# Fits 5 decision trees, varying the max depth allowed.
# maxBins is fixed to 14, because that is the best one we saw from varying the bins.
def decisionTreeVaryDepth(train_data, validation_data):
    depth = [1, 2, 3, 4, 5]
    accuracy = []
    for d in depth:
        print(f'maxDepth={d}')
        result = fitDecisionTree(train_data, validation_data, impurity='gini', maxBins=14, maxDepth=d)
        accuracy.append(result)

    makePlot(depth, accuracy, 'maxDepth', 'accuracy')


# Fits a RandomForest model using numTrees number of trees.
def fitRandomForest(train_data, validation_data, numTrees, impurity='gini', maxBins=14, maxDepth=5):
    t0 = time()
    model = RandomForest.trainClassifier(train_data, numClasses=2, categoricalFeaturesInfo={},
                                         numTrees=numTrees, featureSubsetStrategy="auto",
                                         impurity=impurity, maxDepth=maxDepth, maxBins=maxBins)
    tt = time() - t0

    predictions = model.predict(validation_data.map(lambda x: x.features))
    labelsAndPredictions = validation_data.map(lambda lp: lp.label).zip(predictions)
    testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(validation_data.count())

    accuracy = 1.0 - testErr
    print('Accuracy = ' + str(accuracy))
    #print('Learned classification forest model:')
    #print(model.toDebugString())

    return (accuracy, tt)


# Trains multiple Random Forest models, varying the number of trees in intervals of 100.
# maxNumTrees will be multiped by 100. For example, with maxNumTrees=5, this will
# train 5 trees of size 100, 200, 300, 400, and 500.
def randomForestVaryTrees(train_data, validation_data, maxNumTrees=5):
    trees = []
    accuracy = []
    for i in range(1, maxNumTrees+1):
        numTrees = i*100
        print(f'numTrees={numTrees}')
        result, time = fitRandomForest(train_data, validation_data, numTrees)
        print(f'time to train = {time}')
        trees.append(numTrees)
        accuracy.append(result)

    makePlot(trees, accuracy, 'numTrees', 'accuracy')

##### START HERE #####
# Initalize Spark context
sc = SparkContext(appName="Lab4")
sc.setLogLevel("ERROR")

# Read data and convert
training_data = read_data('train')
allTrain = convertToLabeledPoint(sc, training_data)

testing_data = read_data('test')
allTest = convertToLabeledPoint(sc, testing_data)

# Split allTrain into train and validation
(train, validation) = allTrain.randomSplit([0.7, 0.3], seed=42)

# Start training Decision Trees!
print('Decision Tree using gini impurity')
fitDecisionTree(train, validation, impurity='gini', maxBins=32)

print('Decision Tree using entropy impurity')
fitDecisionTree(train, validation, impurity='entropy', maxBins=32)

print('Decision Trees keeping impurity as gini, but varying the number of bins')
decisionTreeVaryBins(train, validation)

print('Decision Trees keeping impurity as gini, maxBins as 14, but varying maxDepth')
decisionTreeVaryDepth(train, validation)

print('Final Decision Tree model, ran on split data and tested on validation')
fitDecisionTree(train, validation, impurity='gini', maxBins=14, maxDepth=5)

print('Final Decision Tree trained on all training data and tested on test dataset')
fitDecisionTree(allTrain, allTest, impurity='gini', maxBins=14, maxDepth=5)

print('Random Forest models, by varying the number of trees')
randomForestVaryTrees(train, validation, maxNumTrees=40)

print('Random Forest with most trees I can train, to be examined as a function of N (cores)')
accuracy, time = fitRandomForest(train, validation, 4000)
print(f'Time taken to train = {time} (seconds)')

print('Final Random Forest model, ran on split data and tested on validation')
fitRandomForest(train, validation, 2400, impurity='gini', maxBins=14, maxDepth=5)

print('Final Random Forest model, ran on all training data and tested on test dataset')
fitRandomForest(allTrain, allTest, 2400, impurity='gini', maxBins=14, maxDepth=5)

