"""
In this example, a dashboard is generated to view quality control analysis 
results using analysis from several systems and locations.  Each system and 
location links to a detailed report which includes test failures.
For illustrative purposes, the data used in this example is generated within 
the script, using a sine wave function.
"""
import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import pecos
import openaq
from datetime import date, time, timezone




api = openaq.OpenAQ()

status, resp = api.cities()


dt_begin = date(2020,3,1)
dt_end = date(2020,9,1)

dt_start = date.today()

#date_to

print(dt_begin)
print(dt_end)

OpenAQ_station2 = ['Agartala']

def Get_OpenAQ_Dataset_API_Location_parameter(dt_begin, dt_end, OpenAQ_station2):

#Step 1 Choose the measurement country to import and parameter
   res_1 = api.measurements(country='IN', parameter='pm25', date_to=dt_end, date_from=dt_begin, limit=10000, df=True)
   
   print(OpenAQ_station2) 
    
 #  res_1 = api.measurements(location=OpenAQ_station2, parameter='pm25', date_to=dt_end, date_from=dt_begin, limit=10000, df=True)

# 
   print(res_1.dtypes)

   return res_1



def Milestone2_OpenAQ_Dataset_Remove_Neg(OpenAQ_Dataset_ImportAPI):
     
   OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI[OpenAQ_Dataset_ImportAPI.value != -999.00]

   return OpenAQ_Dataset_ImportAPI


def Get_OpenAQ_Dataset_Wrangling_utc_index(OpenAQ_Dataset_ImportAPI):

   format = '%Y-%m-%d %H:%M:%S'
    
   OpenAQ_Dataset_ImportAPI['date.utc'] = pd.to_datetime(OpenAQ_Dataset_ImportAPI['date.utc'], format=format).dt.tz_localize(None)

   Formating = pd.DatetimeIndex(OpenAQ_Dataset_ImportAPI['date.utc'])
                 

   
   OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI.set_index(Formating)

  # OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI.set_index('date.utc')

   print(OpenAQ_Dataset_ImportAPI)

   print(OpenAQ_Dataset_ImportAPI['value'])

   print(OpenAQ_Dataset_ImportAPI['date.utc'])


 #  print(OpenAQ_Dataset_ImportAPI['value'])

   return OpenAQ_Dataset_ImportAPI
   

OpenAQ_Dataset_ImportAPI = Get_OpenAQ_Dataset_API_Location_parameter(dt_begin, dt_end, OpenAQ_station2[0])

# OpenAQ_Dataset_ImportAPI = Get_OpenAQ_Dataset_Wrangling_utc_index(OpenAQ_Dataset_ImportAPI)


# Initialize logger
pecos.logger.initialize()

# Define system names, location names, and analysis date
systems = ['system1', 'system2', 'system3']
locations = ['location1', 'location2']
analysis_date = datetime.date.today()-datetime.timedelta(days=1)

dashboard_content = {} # Initialize the dashboard content dictionary
np.random.seed(500) # Set a random seed for sine wave function

for OpenAQImportAPIdataset in OpenAQ_station2:
    for system_name in systems:
        # Open config file and extract information
        config_file = system_name + '_config.yml'
        fid = open(config_file, 'r')
        config = yaml.load(fid)
        fid.close()
        trans = config['Translation']
        specs = config['Specifications']
        range_bounds = config['Range Bounds']
    
        # Create a Pecos PerformanceMonitoring data object
        pm = pecos.monitoring.PerformanceMonitoring()
        
        # Populate the object with a dataframe and translation dictionary
        # In this example, fake data is generated using a sin wave function
        index = pd.date_range(analysis_date, periods=24, freq='H')
        
        
        OpenAQ_Dataset_ImportAPI = Get_OpenAQ_Dataset_API_Location_parameter(dt_begin, dt_end, OpenAQImportAPIdataset)

        OpenAQ_Dataset_ImportAPI = Get_OpenAQ_Dataset_Wrangling_utc_index(OpenAQ_Dataset_ImportAPI)
        
        OpenAQ_Dataset_ImportAPI = Milestone2_OpenAQ_Dataset_Remove_Neg(OpenAQ_Dataset_ImportAPI)
 
        
        OpenAQ_API_Highest = OpenAQ_Dataset_ImportAPI['value'].max()
        
        print(OpenAQ_API_Highest)
        
        print(index) 
    #    dataset_df_2 = np.sin(np.random.random_integers(0,OpenAQ_API_Highest,size=(3,1)))
        
     #   print(dataset_df_2)
        
      #  print(np.random.rand(3,1))
     #   print(np.arange(0,96,1))
        data=np.sin(np.random.rand(3,1)*np.arange(0,24,1))
       
        print(data)

        index_df2 = pd.date_range(dt_begin, periods=96, freq='24h')
        
   #     print(np.arange(0,96,1))
        
  #      dataset2 = (np.array((0., 30., 45., 60., 90.)) * np.pi / 180. )
        
        dataset_df3 = np.array([[(0. * np.pi / 180.) ], [(30. * np.pi / 180.) ], [(45. * np.pi / 180.)], [(60. * np.pi / 180.)], [(90. * np.pi / 180. )]])
        
    #    dataset2_df3 = np.empty([3,1])
        
        
        
    #    print(dataset_df3 * np.arange(0,96,1))
        
        #dataset2_df3 = np.append(dataset2_df3, dataset_df3)
        
      #  print(dataset2_df3 * np.arange(0,96,1))
        
      #  print(np.random.rand(3,1))
        
        
     #   print(dataset2)
        
    #    dataset2_df2 = np.sin(np.array((0., 30., 45., 60., 90.)) * np.pi / 180. )   
         
        dataset3_df2 = np.sin(dataset_df3 * np.arange(0,96,1)) * OpenAQ_API_Highest
        
        
       
        
        print(dataset3_df2)
        
        
    #    dataset3_df = np.ndarray(shape=(2,2), dtype=float, order='F')

    #    print(dataset2_df2)

        
        print(index_df2)

      #  print(dataset3_df)
        
      #  print(data)
     #   
      #  df = pd.DataFrame(data=data.transpose(), index=index, columns=['A', 'B', 'C'])
        
      #  df2 = pd.DataFrame(data=OpenAQ_Dataset_ImportAPI, index=OpenAQ_Dataset_ImportAPI['date.utc'], columns=['location','parameter','value','unit','country','city','coordinates.latitude','coordinates.longitude'])
        
      #  df3 = pd.DataFrame(data=OpenAQ_Dataset_ImportAPI, index=OpenAQ_Dataset_ImportAPI['date.utc'], columns=['value'])
        
        df2 = OpenAQ_Dataset_ImportAPI['value']
        
        print(df2)
        
        df2_dataset = pd.DataFrame(data=dataset3_df2.transpose(), index=index_df2, columns=['0','30degrees','45degrees','60degrees','90degrees'])
        
        OpenAQ_Dataset_ImportAPIdf = pd.DataFrame(data=OpenAQ_Dataset_ImportAPI['value'], index=OpenAQ_Dataset_ImportAPI['date.utc'], columns=['value'])
        
        
               
        print(df2_dataset)
        
        df2_dataset.plot()
        
       # print(df2)
        pm.add_dataframe(df2_dataset)
        
        Amountdf = (len(OpenAQ_Dataset_ImportAPI))/96
      
        print(Amountdf)
        
        pm.add_dataframe(OpenAQ_Dataset_ImportAPIdf)
    
    #    pm.add_dataframe(df3)
    #  pm.add_translation_dictionary(trans)

      #  print(df.dtypes)
        
        print(OpenAQ_Dataset_ImportAPI.dtypes)

        print(pm.df['value'])

        # Check timestamp
        
        print(specs['Frequency']) 
        pm.check_timestamp(specs['Frequency']) 
        
        # Generate a time filter
        clock_time = pecos.utils.datetime_to_clocktime(pm.df.index)
        time_filter = pd.Series((clock_time > specs['Time Filter Min']*3600) & \
                                (clock_time < specs['Time Filter Max']*3600),
                                index=pm.df.index)
      #  pm.add_time_filter(time_filter)
        
        # Check missing
        pm.check_missing()
        
        # Check range
        for key,value in range_bounds.items():
            pm.check_range(value, key) 
            
            print(value)
            
        # Compute metrics
        QCI = pecos.metrics.qci(pm.mask)
        
        # Define output files and subdirectories
        results_directory = 'example_1'
        results_subdirectory = os.path.join(results_directory, OpenAQImportAPIdataset+'_'+system_name)
        if not os.path.exists(results_subdirectory):
            os.makedirs(results_subdirectory)
        graphics_file_rootname = os.path.join(results_subdirectory, 'test_results')
        custom_graphics_file = os.path.abspath(os.path.join(results_subdirectory, 'custom.png'))
        test_results_file = os.path.join(results_subdirectory, 'test_results.csv')
        report_file =  os.path.join(results_subdirectory, 'monitoring_report.html')
        
        # Generate graphics
        test_results_graphics = pecos.graphics.plot_test_results(pm.df, 
                                        pm.test_results, filename_root=graphics_file_rootname)
        
        
      #  df.plot()
      #  df3.plot()
        
        
        
        plt.savefig(custom_graphics_file, format='png', dpi=500)

        # Write test results and report files
        pecos.io.write_test_results(pm.test_results, test_results_file)
        pecos.io.write_monitoring_report(pm.df, pm.test_results, test_results_graphics, 
                                         [custom_graphics_file], QCI, filename=report_file)
        
        # Store content to be displayed in the dashboard
        content = {'text': "Example text for " + OpenAQImportAPIdataset+'_'+system_name, 
                   'graphics': [custom_graphics_file], 
                   'table':  QCI.to_frame('QCI').transpose().to_html(), 
                   'link': {'Link to Report': os.path.abspath(report_file)}}
        dashboard_content[(system_name, OpenAQImportAPIdataset)] = content

# Create dashboard   
pecos.io.write_dashboard(OpenAQ_station2, systems, dashboard_content, 
                         filename='dashboard_example_1.html')
