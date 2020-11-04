  
# Air Quality Observations Quality Control  

Description
Validating and removing errors outliers from surface air quality observations from individual sensors so that these observation can be compared to ECMWF's CAMS air quality forecasts. By clustering analysis on these observations more reliable observations can be identified. Enhancing these observations by attaching data about factors that affect air quality these observations can have more credibility about their accuracy. CAMS lacks credible surface air quality observations in many parts of the world, often in the most polluted area such as in India or Africa. Some observations are available for these areas from data harvesting efforts such as openAQ but there is no quality control applied to the data, and it is often not well known if the observations are made in a rural, urban or heavily polluted local environment. This information on the environment is important because the very locally influenced measurements are mostly not representative for the horizontal scale (40 km) of the CAMS forecasts and should therefore not be used for the evaluation of the CAMS model.

Completed for ECMWF European Centre for Medium Weather Forecast 2020 
and ESoWC 2020

# Implementation 

Milestone 1 Identifying reliable stations

1 Histogram of OpenAQ Stations

(Milestone_2_Import_OpenAQ_Dataset_Histogram.py)

Default is 

2 Boxplot of OpenAQ stations 

(Milestone2_Analytics_OpenAQ_Station_Boxplot_Import_OpenAQ_Pandas_Analysis_csv.py )

Defualt openAQ dataset download is OpenAQ_Dataset_Sample_Pm25_csv.csv

a. From Csv import 



Python Scripts 

1 Milestone_2_Import_OpenAQ_Dataset_Histogram.py

Histogram of OpenAQ stations 

2 Milestone2_Analytics_OpenAQ_Station_Boxplot_Import_OpenAQ_Pandas_Analysis_csv.py 

Box plot OpenAQ Station


# User Manual 

2 Milestone2_Analytics_OpenAQ_Station_Boxplot_Import_OpenAQ_Pandas_Analysis_csv.py 

Step 1 Download Dataset for one AQ Station from the dataset from openAQ.org

Step 2 Convert to csv 

Step 3 Change the csv requested in the script to chosen OpenAQ Stations 


# Dependencies


