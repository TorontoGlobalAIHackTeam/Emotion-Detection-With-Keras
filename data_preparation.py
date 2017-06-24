import os
import numpy as np
import pandas as pd
import csv
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline


# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

print('loading data...')
# load dataset
dataframe = pd.read_csv('train.csv', header=None)
print('getting values...')
dataset = dataframe.values
# print(dataset)
# print(len(dataset[0]))
X = np.array(dataset[:,:-1].astype(float))
Y = np.array(dataset[:,-1])

#one-hot encoding
s = pd.Series(Y)
Y = np.array(pd.get_dummies(s))

print(X)

#X = np.expand_dims(X,axis = 0)
#X = np.split(X,48,axis=2)
# X = np.array([np.split(x_i,48) for x_i in X])

# X = X.reshape(X.shape[0], 1, 48, 48)
# print(Y)

# print (Y.shape)

def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(7, activation='relu', input_dim=2304))
	model.add(Dense(7, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

# print(model.summary())

estimator = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5, verbose=0)
kfold = KFold(n_splits=5, shuffle=True, random_state=seed)

results = cross_val_score(estimator, X, Y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
