# importing basic packages
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import pickle

data0 = pd.read_csv(r"Dataset.csv")

# Sepratating & assigning features and target columns to X & y
y = data0["Label"]
X = data0.drop("Label", axis=1)
X.shape, y.shape

# Splitting the dataset into train and test sets: 80-20 split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=12
)


# Creating holders to store the model performance results
ML_Model = []
acc_train = []
acc_test = []


# function to call for storing the results
def storeResults(model, a, b):
    ML_Model.append(model)
    acc_train.append(round(a, 3))
    acc_test.append(round(b, 3))


# XGBoost Classification model
# save XGBoost model to file

# instantiate the model
xgb = XGBClassifier(learning_rate=0.4, max_depth=7)
# fit the model
xgb.fit(X_train, y_train)

# predicting the target value from the model for the samples
y_test_xgb = xgb.predict(X_test)
y_train_xgb = xgb.predict(X_train)

# computing the accuracy of the model performance
acc_train_xgb = accuracy_score(y_train, y_train_xgb)
acc_test_xgb = accuracy_score(y_test, y_test_xgb)

print("XGBoost: Accuracy on training Data: {:.3f}".format(acc_train_xgb))
print("XGBoost : Accuracy on test Data: {:.3f}".format(acc_test_xgb))

# storing the results. The below mentioned order of parameter passing is important.
# Caution: Execute only once to avoid duplications.
storeResults("XGBoost", acc_train_xgb, acc_test_xgb)


pickle.dump(xgb, open("XGBoostClassifier.pickle.dat", "wb"))
# load model from file
loaded_model = pickle.load(open("XGBoostClassifier.pickle.dat", "rb"))
