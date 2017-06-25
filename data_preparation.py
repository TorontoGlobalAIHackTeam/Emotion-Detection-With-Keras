import os
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
##from sklearn.model_selection import cross_val_score
##from sklearn.model_selection import KFold
##from sklearn.preprocessing import LabelEncoder
##from sklearn.pipeline import Pipeline
#from scipy.misc import imread
#from sklearn.metrics import accuracy_score
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_dim_ordering('th')

#import tensorflow as tf
#import keras

def one_hot(y):
        #convert to one-hot matrix
        s = pd.Series(y)
        return np.array(pd.get_dummies(s))
        

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

print('loading data...')

# load dataset
dataframe = pd.read_csv('train.csv', header=None)
dataset = dataframe.values

x_train = np.array(dataset[:,:-1].astype(float))
y_train = dataset[:,-1]

#load test data
dataframe = pd.read_csv('test.csv', header=None)
dataset = dataframe.values

x_test = np.array(dataset[:,:-1].astype(float))
y_test= dataset[:,-1]

#one-hot encoding
y_train = one_hot(y_train)
y_test = one_hot(y_test)


#split each image into 48 x 48
x_train = np.array([np.split(x_i,48) for x_i in x_train])
x_test = np.array([np.split(x_i,48) for x_i in x_test])

num_classes = y_train.shape[1]
x_train = np.expand_dims(x_train,axis=0)
print(x_train.shape)
print(x_train[0].shape)
print(x_train)

# Create the model
print('creating model...')
model = Sequential()
model.add(Conv2D(48, (3, 3), input_shape=(1,48,48), padding='same', activation='relu', kernel_constraint=maxnorm(3)))
model.add(Dropout(0.2))
model.add(Conv2D(48, (3, 3), activation='relu', padding='same', kernel_constraint=maxnorm(3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(576, activation='relu', kernel_constraint=maxnorm(3)))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

# Compile model
epochs = 25
lrate = 0.01
decay = lrate/epochs
sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
print(model.summary())

# Fit the model
model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=epochs, batch_size=48)
# Final evaluation of the model
"""
scores = model.evaluate(x_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

# Fit the model
model.fit(x_train, x_train, validation_data=(x_test, y_test), epochs=epochs, batch_size=48)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
"""


