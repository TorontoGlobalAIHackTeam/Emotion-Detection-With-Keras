import pandas as pd
import csv
import numpy as np
np.random.seed(123)  # for reproducibility

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist
from matplotlib import pyplot as plt


# (X_train, y_train), (X_test, y_test) = mnist.load_data()
#
# print ("y test")
# print( y_test)


# TRAINING DATA
print('loading data...')
# load dataset
dataframe = pd.read_csv('train.csv', header=None)
print('getting values...')
dataset = dataframe.values
X = np.array(dataset[:,:-1].astype(float))
Y = np.array(dataset[:,-1])

#one-hot encoding
s = pd.Series(Y)
Y = np.array(pd.get_dummies(s))

# multidim array
X = np.array([np.split(x_i,48) for x_i in X])



# TEST DATA
print('loading data...')
# load dataset
dataframe = pd.read_csv('test.csv', header=None)
print('getting values...')
dataset = dataframe.values
X_t = np.array(dataset[:,:-1].astype(float))
Y_t = np.array(dataset[:,-1])

#one-hot encoding
s = pd.Series(Y_t)
Y_t = np.array(pd.get_dummies(s))

# multidim array
X_t = np.array([np.split(x_i,48) for x_i in X_t])


X = X.reshape(X.shape[0],48, 48, 1 )
X_t = X_t.reshape(X_t.shape[0], 48, 48, 1)

X = X.astype('float32')
X_t = X_t.astype('float32')
X /= 255
X_t /= 255



model = Sequential()
model.add(Convolution2D(32, (3, 3), activation='relu', input_shape=(48,48, 1)))
model.add(Convolution2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

# print (model.output_shape)

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(X, Y,
          batch_size=32, nb_epoch=10, verbose=1)

score = model.evaluate(X_t, Y_t, verbose=0)

print(model.summary())
print(score)
