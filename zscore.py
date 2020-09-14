# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:47:49 2020

@author: wegia
"""
import numpy as np

a = np.array([ 0.7972,  0.0767,  0.4383,  0.7866,  0.8091,
               0.1954,  0.6307,  0.6599,  0.1065,  0.0508])
from scipy import stats
print(stats.zscore(a))