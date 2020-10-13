# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 14:40:37 2020

@author: Gordon
"""

import matplotlib.pyplot as plt

import pandas as pd

df = pd.read_csv (r'2018-04-06.csv')

 
Dataset5 = [89,90,90,91]

plt.hist(df['value'], bins=[0,10,20,30,40,50,60,70,80,90,99])
plt.show()