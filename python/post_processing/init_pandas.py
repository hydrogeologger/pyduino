#import sys
#sys.modules[__name__].__dict__.clear()
import os
import numpy as np
#http://stackoverflow.com/questions/5607283/how-can-i-manually-generate-a-pyc-file-from-a-py-file
import py_compile
import sys
import matplotlib.pyplot as plt
import pandas as pd

################################get scale data####################################################################



scale=1
del scale
#os.path.dirname(os.path.realpath(__file__))
current_path=os.getcwd()
sys.path.append(current_path+'/python')
py_compile.compile(current_path+'/python/pandas_scale.py')
py_compile.compile(current_path+'/python/constants.py')

import pandas_scale
import constants
reload(pandas_scale)
reload(constants)



#data_list_weather_roof=os.listdir(current_path+'/data/weather_roof/')
weather_roof_file_path=current_path+'/data/weather_roof/'
weather_roof_header=['date_time','reading_no','voltage','T','hr','patm',
        'rain1','rain2','rain3','rain4','rain5','rain6','wind2','wind5','R_up','R_down']
weather_date_time=['date_time']
dateparse =  lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
weather_roof=pandas_scale.pandas_scale(file_path=weather_roof_file_path,
    source='raw',
    sep=',',
    header=4,
    names=weather_roof_header,
    parse_dates=weather_date_time,
    date_parser=dateparse
    )

dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%Y %H:%M')


weather_roof.append_file(file_path=weather_roof_file_path+'append_files/',
    sep=',',
    header=4,
    names=weather_roof_header,
    parse_dates=weather_date_time,
    date_parser=dateparse
    )


# convert string column to float column, current
# http://stackoverflow.com/questions/15891038/pandas-change-data-type-of-columns
weather_roof.df['R_up']=pd.to_numeric(weather_roof.df['R_up'],errors='coerce')
# remove the row that has NAN inside
# the reason it needs to be droped is because SmoothSpline does not like NaN. which is bad
#http://stackoverflow.com/questions/13413590/how-to-drop-rows-of-pandas-dataframe-whose-value-of-certain-column-is-nan
weather_roof.df=weather_roof.df.dropna()

weather_roof.save_as_csv (fn='weather_roof_merged.csv')
#weather_roof.save_as_hdf5(fn='weather_roof_merged.hd5')




###################################reading scale class#################################################################
column_roof_file_path=current_path+'/data/column_roof/'
scale_header=['date','time','scale','stable']
scale_date_time_merge=[['date','time']]


## using raw material for parsing
scale=pandas_scale.pandas_scale(file_path=column_roof_file_path,
    source='raw',
    sep='\s+',
    names=scale_header,
    parse_dates=scale_date_time_merge
    )
## using csv file for parsing
#scale=pandas_scale.pandas_scale(file_path=column_roof_file_path,
#    source='csv',
#    sep='\s+',
#    names=scale_header,
#    parse_dates=scale_date_time_merge
#    )
#scale=pandas_scale.pandas_scale(file_path=column_roof_file_path,sep='\s+',source='csv',fn_csv='scale_merged.csv',fn_hd5='scale_merged.hd5')
#scale=pandas_scale.pandas_scale(file_path=column_roof_file_path,sep='\s+',source='hd5',fn_csv='scale_merged.csv',fn_hd5='scale_merged.hd5')
#scale.df['scale']=scale.df['scale']*constants.g2kg   # convert g to kg
# here is the place to play with the accuracy of the scales...
# below is 50g accuracy
#scale.df['scale']=np.around(scale.df['scale']*constants.g2kg*2,1)/2.0   # round 
# 100g accuracy
scale.df['scale']=np.around(scale.df['scale']*constants.g2kg,1)   # round 

scale.surf_area1=np.pi*(0.265/2)**2

scale.save_as_csv(fn='scale_merged.csv')
#scale.save_as_hdf5(fn='scale_merged.hd5')
self=scale

####################################################################################################
sp=1
del sp
sp=pandas_scale.concat_data_roof()
sp.merge_data( df=scale.df, keys=['scale'] ,plot=True ,coef=5e-15)

#sp.merge_data( df=scale.df, keys=['scale'] ,plot=True ,coef=1e-9)
#sp.merge_data( df=scale.df, keys=['scale'] ,plot=True ,coef=1e-14)
#sp.surf_area1=np.pi*(0.265/2)**2
#sp.surf_area1=np.pi*(0.265/2)**2
sp.surf_area1=np.pi*(0.22/2)**2
# get cumulative evaporation
sp.df['cum_evap']=(sp.df['scale'][0]-sp.df['scale'])/sp.surf_area1/constants.rhow_pure_water
sp.get_derivative(key='cum_evap',deri_key='evap')


#sp.df.plot(x='date_time', y='cum_evap')
#sp.df.plot(x='date_time', y='evap')
#plt.plot(sp.df['date_time'],sp.df['evap']*constants.ms2mmday)
#plt.show(block=False)

# incorporate data from weather_roof with plotting
#sp.merge_data(df=weather_roof.df, keys=['T','hr','patm',
#        'rain1','rain2','rain3','wind2','wind5','R_up','R_down'] ,plot=True,coef=1e-9 )

### basically this means the SmoothSpline does not like Nan at all, even the source nan has nothing to do with 
### the splined location
sp.merge_data(df=weather_roof.df, keys=['T','hr','patm',
        'rain1','rain2','rain3','wind2','wind5','R_up','R_down'] ,plot=False,coef=1e-9 )
### post processing
# relative humidity
sp.df['hr']=sp.df['hr']*0.01


##############################calculate potential evaporation########################################################
sp.df['Tk']= sp.df['T']+constants.kelvin
sp.df['Rn']= sp.df['R_up']-sp.df['R_down']   # w/m2
sp.df['lv']= constants.lhv(sp.df['Tk'])
sp.df['Er']= sp.df['Rn']/sp.df['lv']/constants.rhow_pure_water  # m/s
sp.df['rhowv_sat']= constants.svp(sp.df['Tk']) #pascal 
sp.df['rhowv_air']= constants.svp(sp.df['Tk'])*sp.df['hr'] #pascal

#sp.df['B']=0.102*sp.df['wind5']/ np.log( 2/0.00000001   )**2
sp.df['B']=0.102*sp.df['wind5']/ np.log( 2/0.0001   )**2
#sp.df['B']=6430.*(1+0.536*sp.df['wind5'])  
sp.df['Ea']=sp.df['B']*(sp.df['rhowv_sat']-sp.df['rhowv_air'])/sp.df['lv']


#sp.df['Ea']=sp.df['B']*(constants.svp(273.15+7)-sp.df['rhowv_air'])/sp.df['lv']
sp.df['drhowv_sat_dt']=constants.dsvp_dtk(  sp.df['Tk']   )

sp.df['evap_weather']=sp.df['drhowv_sat_dt']/(sp.df['drhowv_sat_dt']+constants.psych)*sp.df['Er'
    ] + constants.psych/(sp.df['drhowv_sat_dt']+constants.psych)*sp.df['Ea']

fig=plt.figure(figsize=(20,25))
plt.plot(sp.df['date_time'],sp.df['Ea']*constants.ms2mmday,'r-')
plt.plot(sp.df['date_time'],sp.df['Er']*constants.ms2mmday,'g-')
plt.plot(sp.df['date_time'],sp.df['evap_weather']*constants.ms2mmday,'b-')
plt.plot(sp.df['date_time'],sp.df['evap']*constants.ms2mmday,'k-')



fig=plt.figure(figsize=(20,25))
plt.plot(sp.df['date_time'],sp.df['T'],'k-')

fig=plt.figure(figsize=(20,25))
plt.plot(sp.df['date_time'],sp.df['rhowv_air'],'k-')
plt.plot(sp.df['date_time'],sp.df['rhowv_sat'],'r-')
fig=plt.figure(figsize=(20,25))
plt.plot(sp.df['date_time'],sp.df['wind5'],'r-')
#fig=plt.figure(figsize=(20,25))
#plt.plot(sp.df['date_time'],sp.df['B']*constants.ms2mmday,'k-')
##sp.df['B2']=0.102*sp.df['wind5']/ np.log( 2/0.001   )**2
#sp.df['B2']=0.102*sp.df['wind5']/ np.log( 2/0.005   )**2


# two issues currently for the model
#(1) we assumed a water temperature as 10 celsius
#(2) the surface temp is set as 10 celsius



####################################################################################################
plt.plot(sp.df['date_time'],sp.df['B2']*constants.ms2mmday,'r-')
fig=plt.figure(figsize=(20,25))
plt.plot(sp.df['date_time'],sp.df['wind5'],'r-')
#



#
#for n in np.arange(len(file_list_column_roof)):
#    a.append_file(path_data_column_roof+file_list_column_roof[n])
#
#a.export_data_as_csv('2016-06-25_2016-07-11.dat')
##a.spline_scale_readings(coef=0.001,time_interval_sec_sp=600)
##a.spline_scale_readings(coef=0.0000001,time_interval_sec_sp=600)
##a.spline_scale_readings(coef=1e-8,time_interval_sec_sp=600)
##a.spline_scale_readings(coef=1e-10,time_interval_sec_sp=600)
##a.spline_scale_readings(coef=1e-13,time_interval_sec_sp=600)
#a.spline_scale_readings(coef=1e-14,time_interval_sec_sp=600)
##a.spline_scale_readings(coef=1e-15,time_interval_sec_sp=600)
