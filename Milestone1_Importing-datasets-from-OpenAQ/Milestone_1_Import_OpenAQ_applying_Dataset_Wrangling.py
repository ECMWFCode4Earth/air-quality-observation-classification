# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 14:09:57 2020

@author: wegia
"""



import jsonlines
import ndjson
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pecos


data = []

with jsonlines.open('OpenAQ_1.ndjson') as reader:
    for obj in reader:
        #print(obj)
        obj1 = pd.Series(obj)
        #pd.read_csv(obj)
        data.append(obj1)

Dataset = pd.DataFrame(data)

print(Dataset)

def plot_df(df, x, y, title="", xlabel='Date', ylabel='Value', dpi=100):
    plt.figure(figsize=(16,5), dpi=dpi)
    plt.plot(x, y, color='tab:red')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()



print(Dataset[['date','value','parameter','location']])

print(Dataset.dtypes)

#How to split column into two columns
#https://www.geeksforgeeks.org/split-a-text-column-into-two-columns-in-pandas-dataframe/


Dataset[['Dateutc','Datelocal']] = Dataset.date.apply(lambda x: pd.Series(str(x).split(",")))


Dataset_split = Dataset.Dateutc.apply(lambda x: pd.Series(str(x).split(":")))

#print(Dataset_split)

Dataset['utc'] = pd.to_datetime(Dataset_split[1])

#print(Dataset.dtypes)


print(Dataset)



pd.to_datetime(Dataset['utc'])


Dataset2 = Dataset[['utc','value','parameter','location']].copy()

pd.to_datetime(Dataset2['utc'])
#Dataset2.set_index('utc')

Location_Subset = Dataset[['location']].copy()


Location_Subset.sort_values('location', ascending=False)
Location_Subset = Location_Subset.drop_duplicates(subset='location', keep='first')

#Location_Subset.drop_duplicates('location')

print(Location_Subset)


print(Location_Subset.dtypes)

print(Dataset2.dtypes)


Dataset2.index = Dataset2['utc']

print(Dataset2)

#pd.to_datetime(Dataset2.index)

#LocationId = Dataset2.groupby('location').groups


#plot_df(df, x=Dataset2.index, y=Dataset2.value, title='Monthly anti-diabetic drug sales in Australia from 1992 to 2008.')    




