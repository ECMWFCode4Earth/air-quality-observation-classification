  
# Air Quality Observations Quality Control  

Description
Validating and removing errors outliers from surface air quality observations from individual sensors so that these observation can be compared to ECMWF's CAMS air quality forecasts. By clustering analysis on these observations more reliable observations can be identified. Enhancing these observations by attaching data about factors that affect air quality these observations can have more credibility about their accuracy. CAMS lacks credible surface air quality observations in many parts of the world, often in the most polluted area such as in India or Africa. Some observations are available for these areas from data harvesting efforts such as openAQ but there is no quality control applied to the data, and it is often not well known if the observations are made in a rural, urban or heavily polluted local environment. This information on the environment is important because the very locally influenced measurements are mostly not representative for the horizontal scale (40 km) of the CAMS forecasts and should therefore not be used for the evaluation of the CAMS model.

Completed for ECMWF European Centre for Medium Weather Forecast 2020 
and ESoWC 2020

# Aims

1 Data Wrangling so can be applied to further analysis 

2 Visual Analytics of Histograms, Line Plots or Boxplots of Stations, Cities, Country or Choosen Coordinate Centre and Radius


# User Manual 

Step 1 Download Dataset for one AQ Station from the dataset from openAQ.org using Milestone 1

Step 2 Change the csv requested in the "Milestone2_VisualAnalytics_Evaluate_Coordinates_OpenAQ_Deployed.py" script to chosen OpenAQ Stations 



# Implementation 

Aim 2 Visual Analytics for Identifying reliable stations

1 Histogram and Line graph of OpenAQ stations or OpenAQ download 

"Milestone2_VisualAnalytics_Evaluate_Coordinates_OpenAQ_Deployed.py"


# Python Scripts 

1 Histogram and line graph of OpenAQ stations  

"Milestone2_VisualAnalytics_Evaluate_Coordinates_OpenAQ_Deployed.py"


# Dependencies

matplotlib.pyplot

pandas

numpy 

Seaborn
