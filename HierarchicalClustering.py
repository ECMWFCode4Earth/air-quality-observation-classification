# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 17:36:00 2020

@author: wegia
"""


import matplotlib.pyplot as plt
import pandas as pd
#%matplotlib inline
import numpy as np


customer_data = pd.read_csv('D:\AirNode\Collaborations\PublicAuthority\Inter-Governmental\ECMWF\ESoWC\Challenge24_OutlierDetection_AirQuality\Implementations\Milestone_2\example_Dataset\hierarchical-clustering-with-python-and-scikit-learn-shopping-data.csv')


customer_data.shape
customer_data.head()

data = customer_data.iloc[:, 3:5].values

import scipy.cluster.hierarchy as shc

plt.figure(figsize=(10, 7))
plt.title("Customer Dendograms")
dend = shc.dendrogram(shc.linkage(data, method='ward'))


from sklearn.cluster import AgglomerativeClustering

cluster = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')
cluster.fit_predict(data)

plt.figure(figsize=(10, 7))
plt.scatter(data[:,0], data[:,1], c=cluster.labels_, cmap='rainbow')


