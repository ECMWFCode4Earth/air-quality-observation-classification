# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 13:09:18 2020

@author: wegia
"""

import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.dates as mdates



def Convert_DateTime(Data):
 Dataset = Data   
 Dataset = Dataset.str.replace('{','',regex=True)
 Dataset = Dataset.str.replace('}','',regex=True)

 Dataset = Dataset.str.split(pat=',',n=1,expand=True)[0]
 Dataset = Dataset.str.replace('utc=','',regex=True)
 Dataset = pd.to_datetime(Dataset, format="%Y-%m-%dT%H:%M:%S.%fZ")
 
 print(Dataset)
 
 return Dataset

def Test_Convert_DateTime():
    
    dict1 = pd.read_csv("Dataset/AirNode_OpenAQ_Dataset_Sample.csv")
 
    Convert_DateTime(dict1['date'])
    
    
    
Test_Convert_DateTime()
    