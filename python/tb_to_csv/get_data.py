import py_compile
import os
import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
#matplotlib.use('Agg')


# recompile post_processing in case update are required
pyduino_path = os.environ['pyduino']
print(os.environ['pyduino'])
sys.path.append(os.path.join(pyduino_path,'python','post_processing'))
py_compile.compile(os.path.join(pyduino_path,'python','post_processing','thingsboard_to_pandas.py'))
import thingsboard_to_pandas
reload(thingsboard_to_pandas)


tb_pandas=thingsboard_to_pandas.tingsboard_to_pandas('tb_credential.json')   # input is the location of the json file
# use the below command to show the comments on tb_credential.json
# print tb_pandas.input_json['comments'] 



tb_pandas.get_token()    # get the token associated with the account
tb_pandas.get_keys()     # list of keys in the device
tb_pandas.get_data()     # obtain data from thingsboard stored at tb_pandas['results']
tb_pandas.convert_data_to_df()  # convert each datasets to pandas dataframe
tb_pandas.plot_df(['scale1','scale2'])

# small optation to the failed measurement

tb_pandas.result_df['temp_2']['value'] [ tb_pandas.result_df['temp_2']['value'] <5  ] =np.nan 

tb_pandas.result_df['scale1']['value'] [ tb_pandas.result_df['scale1']['value'] <5  ] =np.nan 

# merge data    
with open('schedule.json') as data_file:    
    sp_input = json.load(data_file)

#sys.path.append   (os.environ['pyduino']+'/python/post_processing/')
#py_compile.compile(os.environ['pyduino']+'/python/post_processing/pandas_scale.py')
#py_compile.compile(os.environ['pyduino']+'/python/post_processing/constants.py')
#
#
#sys.path.join(os.environ['pyduino'],'python','post_processing')
#sys.path.append(os.path.join(os.environ['pyduino'],'python','post_processing'))
py_compile.compile( os.path.join(os.environ['pyduino'],'python','post_processing','pandas_scale.py')  )
py_compile.compile( os.path.join(os.environ['pyduino'],'python','post_processing','constants.py')  )

import pandas_scale
import constants
reload(pandas_scale)
reload(constants)

sp_sch={}
plot_interpolate=False
#plot_interpolate=True

sp_sch=pandas_scale.concat_data_tb(pd.datetime.strptime(sp_input['start_time'],'%Y/%b/%d %H:%M'),
    pd.datetime.strptime(sp_input['end_time'],'%Y/%b/%d %H:%M'),sp_input['delta_t_s'] );

sp_sch.start_dt = pd.datetime.strptime(sp_input['start_time'],'%Y/%b/%d %H:%M')
sp_sch.end_dt   = pd.datetime.strptime(sp_input['end_time'  ],'%Y/%b/%d %H:%M')

sp_sch.merge_data_from_tb(input_time_series=tb_pandas.result_df['temp_6'].index, 
        input_data_series=tb_pandas.result_df['temp_6']['value'], output_time_series=sp_sch.df.index,key_name='temp_6' ,
        plot=plot_interpolate  ,coef=5e-5,rm_nan=True)
sp_sch.merge_data_from_tb(input_time_series=tb_pandas.result_df['temp_4'].index,
                input_data_series=tb_pandas.result_df['temp_4']['value'], output_time_series=sp_sch.df.index,key_name='temp_4' ,
                        plot=plot_interpolate  ,coef=5e-5,rm_nan=True)
sp_sch.merge_data_from_tb(input_time_series=tb_pandas.result_df['temp_3'].index,
                input_data_series=tb_pandas.result_df['temp_3']['value'], output_time_series=sp_sch.df.index,key_name='temp_3' ,
                        plot=plot_interpolate  ,coef=5e-5,rm_nan=True)
sp_sch.merge_data_from_tb(input_time_series=tb_pandas.result_df['temp_2'].index,
                input_data_series=tb_pandas.result_df['temp_2']['value'], output_time_series=sp_sch.df.index,key_name='temp_2' ,
                        plot=plot_interpolate  ,coef=5e-5,rm_nan=True)
sp_sch.merge_data_from_tb(input_time_series=tb_pandas.result_df['scale1'].index,
                input_data_series=tb_pandas.result_df['scale1']['value'], output_time_series=sp_sch.df.index,key_name='scale1' ,
                        plot=plot_interpolate  ,coef=5e-5,rm_nan=True)
sp_sch.merge_data_from_tb(input_time_series=tb_pandas.result_df['scale2'].index,
                input_data_series=tb_pandas.result_df['scale2']['value'], output_time_series=sp_sch.df.index,key_name='scale2' ,
                        plot=plot_interpolate  ,coef=5e-5,rm_nan=True)



fig = plt.figure(figsize=(16,10))
ax = [[] for i in range(30)]
ax[0  ] = plt.subplot2grid((2, 1), (0, 0), colspan=1)
ax[1  ] = plt.subplot2grid((2, 1), (1, 0), colspan=1, sharex = ax[0])


#ax[0].plot(sp_sch.df['time_days']*constants.minutePday,sp_sch.df['temp_6'])
#ax[0].plot(sp_sch.df['time_days']*constants.minutePday,sp_sch.df['temp_4'])
#ax[0].plot(sp_sch.df['time_days']*constants.minutePday,sp_sch.df['temp_3'])
#ax[0].plot(sp_sch.df['time_days']*constants.minutePday,sp_sch.df['temp_2'])
#
#ax[1].plot(sp_sch.df['time_days']*constants.minutePday,sp_sch.df['scale1'][0]-sp_sch.df['scale1'])
#ax[1].plot(sp_sch.df['time_days']*constants.minutePday,sp_sch.df['scale2'][0]-sp_sch.df['scale2'])

ax[0].plot(sp_sch.df.index,sp_sch.df['temp_6'])
ax[0].plot(sp_sch.df.index,sp_sch.df['temp_4'])
ax[0].plot(sp_sch.df.index,sp_sch.df['temp_3'])
ax[0].plot(sp_sch.df.index,sp_sch.df['temp_2'])
ax[1].plot(sp_sch.df.index,sp_sch.df['scale1'][0]-sp_sch.df['scale1'])
ax[1].plot(sp_sch.df.index,sp_sch.df['scale2'][0]-sp_sch.df['scale2'])

#plt.show()
sp_sch.df.to_csv('result.csv')
#plt.close()
