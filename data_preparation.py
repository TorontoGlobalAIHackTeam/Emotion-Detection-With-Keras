import os
import numpy as np
import pandas as pd
import csv

import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
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
X = np.array(dataset[:,:-1].astype(float))
Y = np.array(dataset[:,-1])

print(X)
print(Y)

#one-hot encoding
s = pd.Series(Y)
Y = pd.get_dummies(s)

#X = np.expand_dims(X,axis = 0)
#X = np.split(X,48,axis=2)
X = np.array([np.split(x_i,48) for x_i in X])

# Create the model
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(3, 32, 32), padding='same', activation='relu', kernel_constraint=maxnorm(3)))
model.add(Dropout(0.2))
model.add(Conv2D(32, (3, 3), activation='relu', padding='same', kernel_constraint=maxnorm(3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(512, activation='relu', kernel_constraint=maxnorm(3)))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))


