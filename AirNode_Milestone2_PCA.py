# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 21:04:21 2020

@author: wegia
"""


from numpy import array
from numpy import mean
from numpy import cov
from numpy.linalg import eig

# define a small 3×2 matrix
matrix = array([[5, 6], [8, 10], [12, 18]])
print("original Matrix: ")
print(matrix)

# calculate the mean of each column
Mean_col = mean(matrix.T, axis=1)
print("Mean of each column: ")
print(Mean_col)

# center columns by subtracting column means
Centre_col = matrix - Mean_col
print("Covariance Matrix: ")
print(Centre_col)

# calculate covariance matrix of centered matrix
cov_matrix = cov(Centre_col.T)
print(cov_matrix)

# eigendecomposition of covariance matrix
values, vectors = eig(V)
print("Eigen vectors: ",vectors)
print("Eigen values: ",values)

# project data on the new axes
projected_data = e_vectors.T.dot(Centre_col.T)
print(projected_data.T)