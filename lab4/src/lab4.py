import pandas as pd

from pyspark import SparkContext
from pyspark.sql import SQLContext

from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.util import MLUtils

# Read in the data
# First the prediction data
data = pd.read_csv("../dataset/arcene_train.data", sep=' ', header=None)
data.drop(data.columns[[10000]], axis=1, inplace=True)

# Then the labels associated with them
# Replace the class -1 with class 0 for MLLib to use
labels = pd.read_csv("../dataset/arcene_train.labels", header=None, names=["class"])
labels.replace(-1.0, 0.0, inplace=True)

# Combine the two into one dataframe
combined = pd.concat([labels, data], axis=1)

#print(combined.shape)
#print(combined.head())

# Initalize Spark context
sc = SparkContext(appName="Lab4")
sc.setLogLevel("ERROR")

# Convert our Pandas dataframe to a Spark dataframe
sql_context = SQLContext(sc)
df = sql_context.createDataFrame(combined)

# Convert Spark dataframe to LabeledPoint RDD
temp = df.map(lambda line:LabeledPoint(line[0],[line[1:]]))

# Split into train and validation
(train, validation) = temp.randomSplit([0.7, 0.3], seed=42)

# Fit the model
model = DecisionTree.trainClassifier(train, numClasses=2, categoricalFeaturesInfo={}, impurity='gini', maxBins=32)

# Make predictions on validation set and get error
predictions = model.predict(validation.map(lambda x: x.features))
labelsAndPredictions = validation.map(lambda lp: lp.label).zip(predictions)
testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(validation.count())
print('Test Error = ' + str(testErr))
print('Learned classification tree model:')
print(model.toDebugString())

