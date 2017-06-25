from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys


import tensorflow as tf
import pandas as pd
import numpy as np

from tensorflow.examples.tutorials.mnist import input_data

FLAGS = None

print("Retrieving data...")
dataframe = pd.read_csv('train.csv', header=None)
dataset = dataframe.values

x_train = np.array(dataset[:,:-1].astype(float))
y_train = dataset[:,-1]

#load test data
dataframe = pd.read_csv('test.csv', header=None)
dataset = dataframe.values

x_test = np.array(dataset[:,:-1].astype(float))
y_test= dataset[:,-1]


print("Changing Data...")

y_temp = []
for i in range(len(y_train)):
  row = [0]*7;
  row[y_train[i]] = 1
  y_temp.append(row)
  
y_train = np.array(y_temp)

y_temp = []
for i in range(len(y_test)):
  row = [0]*7;
  row[y_test[i]] = 1
  y_temp.append(row)

y_test = np.array(y_temp)

for i in range(len(x_test)):
  for j in range(len(x_test[i])):
    x_test[i][j] /= 255
for i in range(len(x_train)):
  for j in range(len(x_train[i])):
    x_train[i][j] /= 255
print(len(x_train))
print(len(y_train))
print(len(x_test))
print(len(y_test))
print(len(x_train[0])//100)

x_train = np.expand_dims(x_train,axis=0)
x_test = np.expand_dims(x_test,axis=0)
y_train = np.expand_dims(y_train,axis=0)
y_test = np.expand_dims(y_test,axis=0)


###

def deepnn(x):

  x_image = tf.reshape(x, [-1, 48, 48, 1])
  
  # First convolutional layer - maps one grayscale image to 32 feature maps.
  W_conv1 = weight_variable([5, 5, 1, 32])
  b_conv1 = bias_variable([32])
  h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

  # Pooling layer - downsamples by 2X.
  h_pool1 = max_pool_2x2(h_conv1)

  # Second convolutional layer -- maps 32 feature maps to 64.
  W_conv2 = weight_variable([5, 5, 32, 64])
  b_conv2 = bias_variable([64])
  h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

  # Second pooling layer.
  h_pool2 = max_pool_2x2(h_conv2)

  # Fully connected layer 1 
  W_fc1 = weight_variable([12 * 12 * 64, 1024])
  b_fc1 = bias_variable([1024])

  h_pool2_flat = tf.reshape(h_pool2, [-1, 12*12*64])
  h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

  # Dropout 
  keep_prob = tf.placeholder(tf.float32)
  h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

  # Map the 1024 features to 7 classes
  W_fc2 = weight_variable([1024, 7])
  b_fc2 = bias_variable([7])

  y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
  return y_conv, keep_prob


def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')


def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)


def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)


def main(_):
  # Import data
  #mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

  # Create the model
  x = tf.placeholder(tf.float32, [None, 2304])

  # Define loss and optimizer
  y_ = tf.placeholder(tf.float32, [None, 7])

  # Build the graph for the deep net
  y_conv, keep_prob = deepnn(x)

  cross_entropy = tf.reduce_mean(
      tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
  train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
  correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

  with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print(len(x_train[0])//50)
    for i in range(len(x_train[0])//50):
      #batch = mnist.train.next_batch(10)
      if i % 1 == 0:
        train_accuracy = accuracy.eval(feed_dict={
            x: x_train[0,i*50:(i+1)*50], y_: y_train[0,i*50:(i+1)*50], keep_prob: 1.0})
        print('step %d, training accuracy %g' % (i, train_accuracy))
      train_step.run(feed_dict={x: x_train[0], y_: y_train[0], keep_prob: 0.5})

    print("Testing...")
    print('test accuracy %g' % accuracy.eval(feed_dict={
        x: np.array(x_test[0]), y_: np.array(y_test[0]), keep_prob: 1.0}))

#if __name__ == '__main__':
  #parser = argparse.ArgumentParser()
  #parser.add_argument('--data_dir', type=str,
   #                   default='/tmp/tensorflow/mnist/input_data',
   #                   help='Directory for storing input data')
 # FLAGS, unparsed = parser.parse_known_args()
print("Training...")
tf.app.run(main=main)
