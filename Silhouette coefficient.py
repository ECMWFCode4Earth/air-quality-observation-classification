# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 17:33:05 2020

@author: wegia
"""


import numpy as np
from sklearn.metrics import silhouette_score
from sklearn import datasets
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# Generate feature matrix
X, _ = make_blobs(n_samples = 1000,
                  n_features = 10,
                  centers = 2,
                  cluster_std = 0.5,
                  shuffle = True,
                  random_state = 1)


# Cluster data using k-means to predict classes
model = KMeans(n_clusters=2, random_state=1).fit(X)

# Get predicted classes
y_hat = model.labels_

# Evaluate model
print(silhouette_score(X, y_hat))

