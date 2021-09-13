# -*- coding: utf-8 -*-
"""neural_network_Mnist_three_layer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DsaCY0N8IDoS1FWu0CFgm6aPtc4wdrIm

Imports
"""

import tensorflow as tf
tf.config.experimental.set_memory_growth(tf.config.list_physical_devices('GPU')[0],True)
import numpy as np
from keras import initializers
from keras.layers import Input, Dense, Activation,BatchNormalization, Flatten, Conv2D, MaxPooling2D
from keras.models import Model
from keras.preprocessing import image
from keras import metrics
from keras.metrics import SparseTopKCategoricalAccuracy 
import keras.backend as K
K.set_image_data_format("channels_last")
import glob 
import matplotlib.pyplot as plt
import cv2
from sklearn.decomposition import PCA
from keras.datasets import mnist

"""Functions"""

def Create_Histogam(data):
  histogram = np.zeros(10)
  for i in range(10):
    histogram[i] = np.sum(data==i)
  return histogram

def Create_data_label(data,label,n,start,stop):
  New_data = np.zeros((1,n,n),dtype=data.dtype)
  New_label = np.zeros((1,10),dtype=label.dtype)
  for i in range(10):
      sample = np.where(label==i)[0][start:stop]
      d = data[sample]
      l = np.zeros((stop-start,10),dtype=label.dtype)
      l[:,i] = 1
      New_label = cv2.vconcat([New_label,l])
      New_data = np.concatenate((New_data,d),axis=0)
  New_data = np.delete(New_data,0,0)
  New_label = np.delete(New_label,0,0)
  return New_data,New_label

"""Loading data"""

(TrainX, TrainY), (TestX, TestY) = mnist.load_data()
train_histogram = Create_Histogam(TrainY)
test_histogram = Create_Histogam(TestY)

"""defining model"""

def My_model(n):
  tf.config.experimental.list_logical_devices('GPU')
  tf.debugging.set_log_device_placement(True)
  with tf.device(tf.test.gpu_device_name()):
      X_input = Input(shape=(n,n,1))
      X = Conv2D(32,(3,3), name="Conv", kernel_initializer=initializers.GlorotUniform())(X_input)
      X = Activation('relu')(X)
      X = MaxPooling2D((2,2), name='Max')(X)
      X = Flatten()(X)
      X = Dense(10, activation='softmax', name="Fc", kernel_initializer=initializers.GlorotUniform())(X)
      model = Model(inputs=X_input,outputs=X, name='My_Model')
      model.compile(optimizer="Adam", loss='categorical_crossentropy', metrics=['accuracy'])
      return model

"""Fitting and testing the model"""

n = 28
train_X,train_Y = Create_data_label(TrainX,TrainY,n,0,int(np.min(train_histogram)))
train_X = train_X.reshape(-1,28,28,1)
test_X,test_Y = Create_data_label(TestX,TestY,n,0,int(np.min(test_histogram)))

with tf.device(tf.test.gpu_device_name()):
  model = My_model(n)
  model.fit(train_X,train_Y, epochs=40)
  loss,precision =  model.evaluate(train_X,train_Y)

"""Final result"""

print(f'The precision of network is {precision}.')
print(f'The loss of network is {loss}.')