# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 11:47:50 2020

@author: wegia
"""




import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pecos


df4 = pd.read_csv (r'openAQ_PM25_3_copy_2.csv',index_col=0)

print(df4)

# Initialize logger
pecos.logger.initialize()

# Create a Pecos PerformanceMonitoring data object
pm = pecos.monitoring.PerformanceMonitoring()

# Populate the object with a DataFrame and translation dictionary
data_file = 'simple_pecos.xlsx'

data_file1 = 'openAQ_PM25_3_copy.xlsx';

#df4 = pd.read_csv (r'openAQ_PM25_3_copy_2.csv',index_col=0)


df = pd.read_excel(data_file1, index_col=0)

print(df4.dtypes)

print(df.dtypes)

Dataset2 = df[['utc','value','parameter','value_copy','value_copy1','value_copy2']].copy()



pm.add_dataframe(Dataset2)
pm.add_translation_dictionary({'Wave': ['value_copy1','value_copy2']}) # group C and D


# Check the expected frequency of the timestamp
pm.check_timestamp(900)
 
# Generate a time filter to exclude data points early and late in the day
clock_time = pecos.utils.datetime_to_clocktime(pm.df.index)
time_filter = pd.Series((clock_time > 3*3600) & (clock_time < 21*3600), 
                        index=pm.df.index)
pm.add_time_filter(time_filter)

# Check for missing data
pm.check_missing()
        
# Check for corrupt data values
pm.check_corrupt([-999]) 

# Add a composite signal which compares measurements to a model
wave_model = np.array(np.sin(10*clock_time/86400))
wave_measurments = pm.df[pm.trans['Wave']]
wave_error = np.abs(wave_measurments.subtract(wave_model,axis=0))
wave_error.columns=['Wave Error C', 'Wave Error D']
pm.add_dataframe(wave_error)
pm.add_translation_dictionary({'Wave Error': ['Wave Error C', 'Wave Error D']})

# Check data for expected ranges
pm.check_range([0, 1], 'value')
pm.check_range([-1, 1], 'Wave')
pm.check_range([None, 0.25], 'Wave Error')

# Check for stagnant data within a 1 hour moving window
pm.check_delta([0.0001, None], 'value', 3600) 
pm.check_delta([0.0001, None], 'value', 3600) 
pm.check_delta([0.0001, None], 'Wave', 3600) 
    
# Check for abrupt changes between consecutive time steps
pm.check_increment([None, 0.6], 'Wave') 

# Check for abrupt changes between consecutive time steps
pm.check_increment([None, 0.6], 'value') 


# Compute the quality control index for A, B, C, and D
mask = pm.mask[['value','value_copy1','value_copy2','value_copy']]
QCI = pecos.metrics.qci(mask, pm.tfilter)

print(pm.df['Wave Error C'])

# Generate graphics
test_results_graphics = pecos.graphics.plot_test_results(pm.df, pm.test_results)
df.plot(ylim=[-100,100], figsize=(7.0,3.5))
plt.savefig('custom.png', format='png', dpi=500)

print(pm.test_results.dtypes)

print(pm.test_results['Error Flag'])

# Write test results and report files
pecos.io.write_test_results(pm.test_results)
pecos.io.write_monitoring_report(pm.df, pm.test_results, test_results_graphics, 
                                 ['custom.png'], QCI)


