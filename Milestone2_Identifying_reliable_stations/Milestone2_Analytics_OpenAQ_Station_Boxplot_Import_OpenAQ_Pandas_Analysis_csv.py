# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

dict = {"country": ["Brazil", "Russia", "India", "China", "South Africa"],
       "capital": ["Brasilia", "Moscow", "New Dehli", "Beijing", "Pretoria"],
       "area": [8.516, 17.10, 3.286, 9.597, 1.221],
       "population": [200.4, 143.5, 1252, 1357, 52.98] }

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.dates as mdates



# dict1.plot(kind='scatter', x='rating', y='revenue_millions', title='Revenue (millions) vs Rating');
# brics = pd.DataFrame(dict1)

def Print_Info(Dataset):  
 print(Dataset.info())


def Replace_Errorous_Value(Data):
 Dataset = Data    
 Dataset = Dataset.replace(-999.0,0)

 print("Value + Errors removed \n",Dataset)

 return Dataset

def Convert_DateTime(Data):
 Dataset = Data   
 Dataset = Dataset.str.replace('{','',regex=True)
 Dataset = Dataset.str.replace('}','',regex=True)

 Dataset = Dataset.str.split(pat=',',n=1,expand=True)[0]
 Dataset = Dataset.str.replace('utc=','',regex=True)
 Dataset = pd.to_datetime(Dataset, format="%Y-%m-%dT%H:%M:%S.%fZ")
 
 print(Dataset)
 return Dataset

def Print_Result(Dataset):
 print(Dataset)


def Describe_Coloumn(Dataset):
 print(Dataset.describe())

def Visualise_BoxPlot(Dataset, xaxis_label, yaxis_label):
 Dataset.plot(kind="box");

def Visualise_BoxPlots():
 # Fixing random state for reproducibility
 np.random.seed(19680801)

 # fake up some data
 spread = np.random.rand(50) * 100
 center = np.ones(25) * 50
 flier_high = np.random.rand(10) * 100 + 100
 flier_low = np.random.rand(10) * -100
 data = np.concatenate((spread, center, flier_high, flier_low))

 fig1, ax1 = plt.subplots()
 ax1.set_title('Basic Plot')
 ax1.boxplot(data)   

 fig2, ax2 = plt.subplots()
 ax2.set_title('Notched boxes')
 ax2.boxplot(data, notch=True)

def Visualise_BoxPlot_Seaborn(Dataset):
 sns.set(style="whitegrid")
 tips = sns.load_dataset("tips")

 # sns.get_data_home("./")

 ax = sns.boxplot(x="day", y="total_bill", data=tips)
 ax = sns.swarmplot(x="day", y="total_bill", data=tips, color=".25")
   
def Visualise_SimplePlot(Dataset):
    
# t = np.arange(0.0, 2.0, 0.01)
# s = 1 + np.sin(2 * np.pi * t)

 fig, ax = plt.subplots()
 ax.plot(Dataset['date'], Dataset['value'])

 ax.set(xlabel='Sample DateTime(hrs)', ylabel='PM2.5 ug/m3',
       title='Hanoi PM2.5')
 ax.grid()

 fig.savefig("test.png")
 plt.show()

#############################################################################
#
# ------------
#
# References
# """"""""""
#
# The use of the following functions and methods is shown in this example:

 matplotlib.axes.Axes.plot
 matplotlib.pyplot.plot
# matplotlib.pyplot.subplots
 matplotlib.figure.Figure.savefig


def Visualise_StemPlot(Dataset):

 levels = np.tile([-5, 5, -3, 3, -1, 1],
                 int(np.ceil(len(Dataset['date'])/6)))[:len(Dataset['date'])]
    # Create figure and plot a stem plot with the date
 fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
 ax.set(title="PM2.5 Hanoi")

 markerline, stemline, baseline = ax.stem(Dataset['date'], levels,
                                         linefmt="C3-", basefmt="k-",
                                         use_line_collection=True)

 plt.setp(markerline, mec="k", mfc="w", zorder=3)

# Shift the markers to the baseline by replacing the y-data by zeros.
 markerline.set_ydata(np.zeros(len(Dataset['date'])))

# annotate lines
 vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
 for d, l, r, va in zip(Dataset['date'], Dataset['value'],levels, vert):
    ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),
                textcoords="offset points", va=va, ha="right")

# format xaxis with 4 month intervals
 ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=4))
 ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
 plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

# remove y axis and spines
 ax.get_yaxis().set_visible(False)
 for spine in ["left", "top", "right"]:
    ax.spines[spine].set_visible(False)

 ax.margins(y=0.1)
 plt.show()


def Convert_Unit(Dataset):
 Dataset.str.replace("Â","",regex=True)  
 
 return Dataset 

def Convert_Dataset():
 dict1 = pd.read_csv("OpenAQ_Dataset_Sample_Pm25_csv.csv")
 dict3 = pd.read_csv("OpenAQ_Dataset_Sample_Pm25_csv.csv")


   
 Print_Info(dict1)
 dict3['value'] = Replace_Errorous_Value(dict1['value'])
 Describe_Coloumn(dict3['value'])
 dict3['date'] = Convert_DateTime(dict1['date'])
 dict3['unit'] = Convert_Unit(dict1['unit'])

 Print_Result(dict3)
 Print_Info(dict3) 
 
 
 print("The -999.00 values have been removed ")
 Visualise_BoxPlot(dict3['value'],"'Hanoi PM2.5","PM25")
 
 #print("The -999.00 value not removed ")
# Visualise_BoxPlot(dict1['value'],0,0)
 
 
 #Visualise_SimplePlot(dict3)
 #Visualise_StemPlot(dict3)
# date_time = pd.to_datetime(dict1["date"]) 

# print(date_time)

# Step 1 Convert Datetime and to dataframe 

Dataset = Convert_Dataset()

#Step 2 Print result 

Print_Result(Dataset)

#Visualise_BoxPlots()

