# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 14:36:28 2020

@author: wegia
"""



import matplotlib.pyplot as plt

import pandas as pd

import numpy as np


def Milestone1_Import_OpenAQ_Csv():
    
   df4 = pd.read_csv (r'openAQ_PM25_3.csv')

   return df4


Milestone1_Import_OpenAQ_Csv()
