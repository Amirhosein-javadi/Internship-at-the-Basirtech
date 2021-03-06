# -*- coding: utf-8 -*-
"""PCA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oWX1nSdmEhkBXgj7LgXeAirmo7NiSIa_
"""

from sklearn import datasets
import matplotlib.pyplot as plt
import cv2
import numpy as np
from sklearn.decomposition import PCA
def plot_func(y,x,plt_file,plt_title):
  plt.plot(x, y, color='red', marker='o', markerfacecolor='red', markersize=3)
  plt.xlabel('PCA Component')
  plt.ylabel(f'{plt_title}')
  plt.title(f'{plt_title}')
  plt.ylim(0, 1)
  plt.grid()
  plt.savefig(plt_file)
  plt.close()
  return
# loading data set
digits = datasets.load_digits()
# reshaping data
n_samples = len(digits.images)
image = digits.images
data = digits.images.reshape((n_samples, -1))
# fitting pca to the data
dim = data.shape[1]
variance = np.zeros((dim-1))
pca = PCA(n_components=dim)
pca.fit(data)
var = pca.explained_variance_ratio_
# finding the numer of component to get 0.99 of variance
variance[0] = var[0] + var[1]
for i in range(1,dim-1):
  variance[i] = variance[i-1] + var[i+1]
n = np.where(variance>0.99)[0][0]
print(f'The image size was {image[0].shape}')
print(f'For having at least 0.99 variance, We need n_component of PCA to be {n}.')

plot_func(variance,range(1,dim),'Variance_PCA.jpg','Variance')