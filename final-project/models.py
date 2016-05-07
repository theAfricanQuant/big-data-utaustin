# This file trains our final models.
# No cross validation or parameter tuning is done in this file, since we
# did all of that in our Juypter notebooks. Look at our notebooks
# to see the parameter tuning and CV.

import numpy as np
import pandas as pd
import xgboost as xgb

from sklearn.grid_search import RandomizedSearchCV, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.metrics import roc_auc_score

def write_to_file(outfile, preds):
    pred_write = enumerate(preds, start=1)
    with open(outfile, 'w') as f:
        f.write('Id,Action\n')
        for instance, prediction in pred_write:
            f.write('{},{}\n'.format(instance, prediction))


# Load data
print('Loading the data...')
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv', index_col='id')

y_train = train.ACTION
X_train = train.drop(["ACTION"], axis=1)

# Drop unnecessary features
X_train = X_train.drop(["ROLE_CODE"], axis=1)
test = test.drop(["ROLE_CODE"], axis=1)

# Train XGB
print('Training the XGBoost model...')
xg = xgb.XGBClassifier(max_depth=8, learning_rate=0.3, n_estimators=155, min_child_weight=0.6, subsample=1.0, colsample_bytree=0.45)
xg.fit(X_train, y_train)
preds = xg.predict_proba(test)[:, 1]

print('Saving the XGBoost model...')
write_to_file('output/xgb_155trees_minchildweight.6_colsampletree.45_learningrate0.3_maxdepth8_.86815.csv', preds)

# Train RF
print('Training the Random Forest model...')
rf = RandomForestClassifier(n_estimators=2000, criterion='entropy', max_features='auto', bootstrap=True)
rf.fit(X_train, y_train)
preds = rf.predict_proba(test)[:, 1]

print('Saving the Random Forest model...')
write_to_file('output/rf_2ktrees_entropy_auto_bootstrapped_.863.csv', preds)

