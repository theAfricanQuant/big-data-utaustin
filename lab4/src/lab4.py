import pandas as pd

from pyspark import SparkContext
from pyspark.sql import SQLContext

from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.util import MLUtils

def read_train_data():
    # First the prediction data
    data = pd.read_csv("../dataset/arcene_train.data", sep=' ', header=None)
    data.drop(data.columns[[10000]], axis=1, inplace=True)

    # Then the labels associated with them
    # Replace the class -1 with class 0 for MLLib to use
    labels = pd.read_csv("../dataset/arcene_train.labels", header=None, names=["class"])
    labels.replace(-1.0, 0.0, inplace=True)

    # Combine the two into one dataframe
    return pd.concat([labels, data], axis=1)

def fitDecisionTree(train_data, validation_data, impurity='gini', maxBins=32, maxDepth=5):
    # Fit the model
    model = DecisionTree.trainClassifier(train_data, numClasses=2, categoricalFeaturesInfo={}, impurity=impurity, maxBins=maxBins, maxDepth=maxDepth)

    # Make predictions on validation set and get error
    predictions = model.predict(validation_data.map(lambda x: x.features))
    labelsAndPredictions = validation_data.map(lambda lp: lp.label).zip(predictions)
    testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(validation_data.count())
    print('Error = ' + str(testErr))
    #print('Learned classification tree model:')
    #print(model.toDebugString())

##### START HERE #####
# Initalize Spark context
sc = SparkContext(appName="Lab4")
sc.setLogLevel("ERROR")

# Convert our Pandas dataframe to a Spark dataframe
training_data = read_train_data()
sql_context = SQLContext(sc)
df = sql_context.createDataFrame(training_data)

# Convert Spark dataframe to LabeledPoint RDD
temp = df.map(lambda line:LabeledPoint(line[0],[line[1:]]))

# Split into train and validation
(train, validation) = temp.randomSplit([0.7, 0.3], seed=42)

# Fit the model - gini
print('Gini impurity classifier')
fitDecisionTree(train, validation, impurity='gini', maxBins=32)

# Model with entropy
print('Entropy impurity classifier')
fitDecisionTree(train, validation, impurity='entropy', maxBins=32)

# Vary number of bins
bins = [2, 6, 10, 14, 18, 22, 26, 30, 34, 38]
for b in bins:
    print('accuracy for maxBins=%s' % (b))
    fitDecisionTree(train, validation, maxBins=b)

# TODO plot

# Vary maxDepth
depth = [1, 2, 3, 4, 5]
for d in depth:
    print('accuracy for maxDepth=%s' % (d))
    fitDecisionTree(train, validation, maxDepth=d)

# TODO plot
