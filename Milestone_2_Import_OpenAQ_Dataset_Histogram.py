# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 11:33:36 2020

@author: wegia
"""



import matplotlib.pyplot as plt

import pandas as pd

import numpy as np

# df = pd.read_csv (r'2018-04-06.csv')

# Step 1 Import OpenAQ pm25 datasets  
df2 = pd.read_csv (r'openAQ.csv')


df3 = pd.read_csv (r'openAQ_PM25_2.csv')


df4 = pd.read_csv (r'openAQ_PM25_year.csv')

df5 = pd.read_csv (r'openAQ_compare.csv')


#print(df4['value']) 

#print(np.arange(1,1001))

# Step 2 Create a Histogram of the OpenAQ Dataset for pm25
plt.hist(df4['value'], bins=np.arange(1,170))
plt.show()

# Step 2 Create a Histogram of the OpenAQ Dataset

plt.hist(df5['value'], bins=np.arange(1,170))
plt.show()

plt.hist(df4['value'], bins=[0,0.0001,0.0002,0.0003,0.0004,0.0005,0.0006,0.0007,0.0008,0.0009,0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,50,60,70,80,90,99])
plt.show()

