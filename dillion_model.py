import pandas as pd
import csv
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist
from matplotlib import pyplot as plt
from keras.utils import plot_model
from keras.utils.vis_utils import model_to_dot
from keras.models import load_model
from keras.models import model_from_json

np.random.seed(123)  # for reproducibility

########## TRAINING DATA ##########

print('loading data...')
# load dataset
dataframe = pd.read_csv('train1.csv', header=None)
print('getting values...')
dataset = dataframe.values
X = np.array(dataset[:,:-1].astype(float))
Y = np.array(dataset[:,-1])

#one-hot encoding
s = pd.Series(Y)
Y = np.array(pd.get_dummies(s))

# multidim array
X = np.array([np.split(x_i,48) for x_i in X])

########## TEST DATA ##########

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

########## DATA PREPROCESSING ##########

X = X.reshape(X.shape[0],48, 48, 1 )
X_t = X_t.reshape(X_t.shape[0], 48, 48, 1)

X = X.astype('float32')
X_t = X_t.astype('float32')
X /= 255
X_t /= 255

########## KERAS ML MODEL ##########

model = Sequential()
model.add(Convolution2D(48, (3, 3), activation='relu', input_shape=(48,48, 1)))
model.add(Convolution2D(48, (3, 3), activation='relu'))
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

history = model.fit(X, Y, validation_split=0.33, batch_size=48, nb_epoch=25, verbose=1)
scores = model.evaluate(X_t, Y_t, verbose=0)

print(model.summary())
print(scores)

# output model visualization to file
plot_model(model, to_file='dillion_model.png')

# ########## SAVE MODEL ##########

print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# serialize model to JSON
model_json = model.to_json()
with open("dillion_model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("dillion_model.h5")
print("Saved model to disk")

########## LOAD MODEL ##########

# json_file = open('dillion_model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# # load weights into new model
# loaded_model.load_weights("dillion_model.h5")
# print("Loaded model from disk")
#
# # evaluate loaded model on test data
# loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# score = loaded_model.evaluate(X_t, Y_t, verbose=0)
# print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
#
# prediction = loaded_model.predict(X, batch_size=1, verbose=0)
# print("prediction of emotion", prediction)
#
# predict_1 = prediction[0]
# emotion_arr = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
#
# def emotion(arr):
#     index = 0
#     highest_num = 0
#     for i in range(7):
#         if (arr[i] > highest_num):
#             index = i
#             highest_num = arr[i]
#     return emotion_arr[index]
#
# for p in prediction:
#     print(emotion(p), p)

########## SHOW GRAPH OF RESULTS ##########

# list all data in history
print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
