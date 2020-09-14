# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 17:44:18 2020

@author: wegia
"""


from sklearn.metrics.cluster import fowlkes_mallows_score
print(fowlkes_mallows_score([0, 0, 1, 1], [0, 0, 1, 1]))