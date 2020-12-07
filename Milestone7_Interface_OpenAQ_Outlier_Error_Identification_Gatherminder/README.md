  
# Air Quality Observations Quality Control  

# Description
Validating and removing errors outliers from surface air quality observations from individual sensors so that these observation can be compared to ECMWF's CAMS air quality forecasts. By clustering analysis on these observations more reliable observations can be identified. Enhancing these observations by attaching data about factors that affect air quality these observations can have more credibility about their accuracy. CAMS lacks credible surface air quality observations in many parts of the world, often in the most polluted area such as in India or Africa. Some observations are available for these areas from data harvesting efforts such as openAQ but there is no quality control applied to the data, and it is often not well known if the observations are made in a rural, urban or heavily polluted local environment. This information on the environment is important because the very locally influenced measurements are mostly not representative for the horizontal scale (40 km) of the CAMS forecasts and should therefore not be used for the evaluation of the CAMS model.

Completed for ECMWF European Centre for Medium Weather Forecast 2020 
and ESoWC 2020

# Features 

1 Plot Outliers with Dataset

2 Performance metrics of Dataset 

3 Reliability report for every Station

# Implementation 


## 1 Plot Outliers and OpenAQ dataset 

Milestone 3 Pecos Quality control plots outliers

## 2 Milestone 3 Dashboard with performance metric and link to monitoring report

## 3 Process Pecos Quality Control analysis 

Milestone 3 prints out a monitoring report

# Presentation results

The scripts output to test_results.csv and monitoring_report.html
(There are examples of these in the github)



# Dependencies

Pecos Package 

https://pecos.readthedocs.io/en/stable/overview.html
https://github.com/sandialabs/pecos

