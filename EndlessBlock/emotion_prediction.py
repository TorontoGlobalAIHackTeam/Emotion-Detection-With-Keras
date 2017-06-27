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


json_file = open('dillion_model_final.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("dillion_model.h5")
print("Loaded model from disk")

# evaluate loaded model on test data
loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# score = loaded_model.evaluate(X_t, Y_t, verbose=0)
# print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))

# print("prediction of emotion", prediction)

# predict_1 = prediction[0]
emotion_arr = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

# def emotion(arr):
#     arr = np.array(arr)
#     arr = np.reshape(arr, (-1, 48, 48, 1));
#     index = 0
#     highest_num = 0
#     prediction = loaded_model.predict(arr, batch_size=1, verbose=0)
#
#     for i in range(len(arr)):
#         if (arr[i] > highest_num):
#             index = i
#             highest_num = arr[i]
#     return emotion_arr[index]


def emotion(arr):
   arr = np.array(arr)
   arr =np.reshape(arr,(-1,48,48,1))

   prediction = loaded_model.predict(arr, batch_size=1, verbose=0)

   predict_1 = prediction[0]

   index = 0
   highest_num = 0
   for i in range(len(predict_1)):
       if (predict_1[i] > highest_num):
           index = i
           highest_num = predict_1[i]
   return emotion_arr[index]
