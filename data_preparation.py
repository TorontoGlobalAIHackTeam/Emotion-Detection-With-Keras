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
X = dataset[:,0:len(dataset[0])-1].astype(float)
Y = dataset[:,len(dataset[0])-1]
print(Y)
B = []
print(X)
for i in range(3):
    print i
for x in X:
    pic = []
    for i in range(48):
        row = []
        for j in range(48):
            row.append(x[i*48 + j])
        pic.append(row)
    B.append(pic)

print "Printing B"

f = open("./out.txt", 'w+')

for i in range(len(B)):
    f.write("[")
    for j in range(48):
        f.write("[")
        for k in range(48):
            f.write(str(B[i][j][k]))
            f.write(" ")
        f.write("],")
        f.write("\n")
    f.write("],")
    f.write("\n")
f.close()
p = np.zeros(Y.shape)

