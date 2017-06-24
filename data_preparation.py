import os
import numpy as np
import pandas as pd
import csv
#from scipy.misc import imread
#from sklearn.metrics import accuracy_score

#import tensorflow as tf
#import keras

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

print('loading data...')
# load dataset
dataframe = pd.read_csv('train.csv', header=None)
print('getting values...')
dataset = dataframe.values
print(dataset)
X = dataset[:,0:len(dataset[0])-2].astype(float)
Y = dataset[:,len(dataset[0])-1]

p = np.zeros(Y.shape)

