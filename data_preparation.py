import os
import numpy as np
import pandas as pd
import csv
#from scipy.misc import imread
#from sklearn.metrics import accuracy_score

#import tensorflow as tf
#import keras

def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(8, input_dim=4, activation='relu'))
	model.add(Dense(3, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model


# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

print('loading data...')
# load dataset
dataframe = pd.read_csv('train.csv', header=None)
print('getting values...')
dataset = dataframe.values
print(dataset)
print(len(dataset[0]))
X = dataset[:,:-1].astype(float)
Y = dataset[:,-1]

print(X)
print(Y)

#one-hot encoding
s = pd.Series(Y)
Y = pd.get_dummies(s)
print(Y)

#X = np.expand_dims(X,axis = 0)
#X = np.split(X,48,axis=2)
X = np.array([np.split(x_i,48) for x_i in X])
print(X)


