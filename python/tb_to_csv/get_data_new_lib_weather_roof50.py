import sys
sys.path.append("/home/osboxes/pyduino/python/lib")
import thingsboard_api
import thingsboard_api.tb_pandas as tb_pandas
import datetime
import pandas as pd
import json
import os
import py_compile
import numpy as np

pyduino_path = "/home/osboxes/pyduino/python"
sys.path.append(os.path.join(pyduino_path,'python','post_processing'))

START_TIME = datetime.datetime.today() - datetime.timedelta(days=5)
#START_TIME = datetime.datetime(2021,9,15)
END_TIME = datetime.datetime.today()
DELTA_TS = 3600

account = thingsboard_api.Account(url="http://monitoring.uqgec.org")
account.authenticate(username="xxxx", password="xxxx")

## Normal, without manually requesting keys
#device = thingsboard_api.Device(account, name="Weather_station_Roof50_1", device_id="555f0d40-2d48-11eb-a6b8-9bd3ee7f132e")
#device.get_keys()
#result_df = device.get_data2(start_time=datetime.datetime(2021,1,4), end_time=datetime.datetime.now(), keys=None, limit=1000, tz_offset=10)

## Normal with requesting for specific keys
#device = thingsboard_api.Device(account, name="DeviceName", device_id="55f0d405-248d-eb11-8a6b-9b13d3e7fe2e")
#result = device.get_data2(start_time=datetime.datetime(2022,6,1), end_time=datetime.datetime.now(), keys=['a', 'b'], limit=1000, tz_offset=10)

# With thingsboard_api.tb_pandas, specific keys for data frame
#------------------------------Device 1 from Thingsboard---------------------------------------------------------
device = tb_pandas.Device(account, name="WEATHER_STATION_ROOF50_2", device_id="791a7850-2feb-11eb-a6b8-9bd3ee7f132e")
result = device.get_data2(start_time=START_TIME, end_time=END_TIME, keys=['ir','uv','sht31_humidity_1','dht22_rh','dht22_t','sht31_temp_1'], tz_offset=10)
result_df = device.get_dataframe(keys=None, tz_offset=10)

result_df['Solar_radiation'] = result_df.pop('ir') #Rename keys in the dict, which could be used as new column headings in the Excel file 
result_df['UV'] = result_df.pop('uv')/100 #Transfer raw data to normal UV index
result_df['Relative_humidity_air'] = result_df.pop('sht31_humidity_1')
result_df['Relative_humidity_enclosure'] = result_df.pop('dht22_rh')
result_df['Temperature_enclosure'] = result_df.pop('dht22_t')
result_df['Temperature_air'] = result_df.pop('sht31_temp_1')

#------------------------------Device 2 from Thingsborad--------------------------------------------------------
device2 = tb_pandas.Device(account, name="WEATHER_STATION_ROOF50_1", device_id="555f0d40-2d48-11eb-a6b8-9bd3ee7f132e")
#device2.get_keys()
result2 = device2.get_data2(start_time=START_TIME, end_time=END_TIME, keys=['rain_roof','wind_speed'], tz_offset=10)
result_df2 = device2.get_dataframe(keys=None, tz_offset=10)
result_df2['Rainfall'] = result_df2.pop('rain_roof')
result_df2['Wind_speed'] = result_df2.pop('wind_speed')

def Merge(result_df,result_df2):
    return(result_df2.update(result_df))

Merge(result_df,result_df2) #Merge data from two devices

##------------------------------Put data into Excel, separated in sheets---------------------------------------
#writer_1 = pd.ExcelWriter('weather_rawdata_PinjarraHills_device1.xlsx', engine='xlsxwriter') #If there is no module named "xlsxwriter", just sudo pip install xlsxwriter.
#j=0
#k=0
#for i in result_df.keys():
#    j+=1
#    if len(result_df[i])>100:
#        k+=1
#        result_df[i]=result_df[i].rename(columns={'value':str(i)})
#        result_df[i].to_excel(writer_1, sheet_name = i) #Put all keys and values into different sheets in one Excel file.
#        worksheet = writer_1.sheets[i]
#        worksheet.set_column('A:A', 25) #Set the width of the first column
#        workbook = writer_1.book
#        chart = workbook.add_chart({'type': 'scatter'})
#        chart.add_series({
#            'name':       [i, 0, 1],
#            #'categories': [i, 1, 0, 1950, 0], #1950 means the maximum row number for plotting the data
#            #'values':     [i, 1, 1, 1950, 1], #1950 means the maximum row number for plotting the data
#            'categories': [i, 1, 0, 100000, 0],
#            'values':     [i, 1, 1, 100000, 1],
#            'marker':     {'type': 'circle', 'size': 2},
#        })
#
#        chart.set_title({
#            'name': i,
#        })
#
#        chart.set_x_axis({
#            'name': 'Date_time',
#            'name_font': {
#                'name': 'Century',
#                'color': 'black',
#            },
#            'num_format': 'dd/mm/yyyy',
#            'num_font': {
#                #'size': '5',
#                'bold': True,
#                'rotation':-45,
#            },
#
#        })
#
#        chart.set_y_axis({
#           'min': 0,
#            'num_font': {
#                'bold': True,
#               'italic': False,
#            },
#
#        })
#        chart.set_legend({'font': {'bold':1, 'italic':1}})
#        worksheet.insert_chart('D2', chart)
#    print ( i + '  ' +str(j) +'/ '+ str(k)+ '/' + str( len(result_df.keys())) )
#
#writer_1.save()

writer_2 = pd.ExcelWriter('weather_rawdata_Roof50_UQ_'+str(END_TIME.strftime("%d_%m_%Y"))+'.xlsx', engine='xlsxwriter') #If there is no module named "xlsxwriter", just sudo pip install xlsxwriter.
j=0
k=0
for i in result_df2.keys():
    j+=1
    if len(result_df2[i])>100:
        k+=1
        result_df2[i]=result_df2[i].rename(columns={'value':str(i)})
        result_df2[i].to_excel(writer_2, sheet_name = i) #Put all keys and values into different sheets in one Excel file.
        worksheet = writer_2.sheets[i]
        worksheet.set_column('A:A', 25) #Set the width of the first column
        workbook = writer_2.book
        chart = workbook.add_chart({'type': 'scatter'})
        chart.add_series({
            'name':       [i, 0, 1],
            #'categories': [i, 1, 0, 1950, 0], #1950 means the maximum row number for plotting the data
            #'values':     [i, 1, 1, 1950, 1], #1950 means the maximum row number for plotting the data
            'categories': [i, 1, 0, 100000, 0],
            'values':     [i, 1, 1, 100000, 1],
            'marker':     {'type': 'circle', 'size': 2},
        })

        chart.set_title({
            'name': i,
        })

        chart.set_x_axis({
            'name': 'Date_time',
            'name_font': {
                'name': 'Century',
                'color': 'black',
            },
            'num_format': 'dd/mm/yyyy',
            'num_font': {
                #'size': '5',
                'bold': True,
                'rotation':-45,
            },

        })

        chart.set_y_axis({
           'min': 0,
            'num_font': {
                'bold': True,
               'italic': False,
            },

        })
        chart.set_legend({'font': {'bold':1, 'italic':1}})
        worksheet.insert_chart('D2', chart)
    print ( i + '  ' +str(j) +'/ '+ str(k)+ '/' + str( len(result_df2.keys())) )

writer_2.save()
