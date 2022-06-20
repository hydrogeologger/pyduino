import py_compile
import os
import sys
import json
import pandas as pd
import numpy as np
import importlib
import matplotlib.pyplot as plt
import glob

import matplotlib
#matplotlib.use('Agg')

# os.chdir("C:\\Users\\virus\\Desktop\\UQ\\7500\\produce_video\\photos_yarwun_basin_test")

import matplotlib.pyplot as plt
plt.ioff()  # disable poping out figure automatically
# recompile post_processing in case update are required
pyduino_path = os.environ['pyduino']
print(os.environ['pyduino'])
sys.path.append(os.path.join(pyduino_path,'pyduino-master','python','post_processing'))
py_compile.compile(os.path.join(pyduino_path,'pyduino-master','python','post_processing','thingsboard_to_pandas_py3.py'))
import thingsboard_to_pandas_py3
#reload(thingsboard_to_pandas_py3)

cwd=os.getcwd()
tb_pandas=thingsboard_to_pandas_py3.tingsboard_to_pandas(cwd+'\\tb_ch.json')   # input is the location of the json file
# use the below command to show the comments on tb_credential.json
# print tb_pandas.input_json['comments'] 



tb_pandas.get_token()    # get the token associated with the account
tb_pandas.get_keys()     # list of keys in the device
tb_pandas.get_data()     # obtain data from thingsboard stored at tb_pandas['results']
tb_pandas.convert_data_to_df()  # convert each datasets to pandas dataframe
#tb_pandas.plot_df(['sa3_uv','sa3_vis'])
# small optation to the failed measurement

tb_pandas.result_df['scaleE']['value'] [ tb_pandas.result_df['scaleE']['value'] <5  ] =np.nan 

tb_pandas.result_df['delta_t_se1']['value'] [ tb_pandas.result_df['delta_t_se1']['value'] <0.5  ] =np.nan 

# merge data    
with open(cwd+'\\schedule.json') as data_file:    
    sp_input = json.load(data_file)

#sys.path.append   (os.environ['pyduino']+'/python/post_processing/')
#py_compile.compile(os.environ['pyduino']+'/python/post_processing/pandas_scale.py')
#py_compile.compile(os.environ['pyduino']+'/python/post_processing/constants.py')
#
#
#sys.path.join(os.environ['pyduino'],'python','post_processing')
#sys.path.append(os.path.join(os.environ['pyduino'],'python','post_processing'))
# py_compile.compile( os.path.join(os.environ['pyduino'],'pandas_scale.py')  )
# py_compile.compile( os.path.join(os.environ['pyduino'],'python','post_processing','constants.py')  )

# CM210730 anaconda has realieased a constants.py, which is in flict with constants here.
# so a new way of defining constants needs to be done by the following way
# https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
constants_file_path=os.path.join(pyduino_path,'pyduino-master','python','post_processing','constants.py')
spec = importlib.util.spec_from_file_location("constants", constants_file_path)
constants = importlib.util.module_from_spec(spec)

spec.loader.exec_module(constants)

# import pandas_scale
# reload(pandas_scale)
import pandas_scale_py3


sp_sch={}
plot_interpolate=True
#plot_interpolate=True

sp_sch=pandas_scale_py3.concat_data_tb(pd.datetime.strptime(sp_input['start_time'],'%Y/%b/%d %H:%M'),
    pd.datetime.strptime(sp_input['end_time'],'%Y/%b/%d %H:%M'),sp_input['delta_t_s'] );
sp_sch.start_dt = pd.datetime.strptime(sp_input['start_time'],'%Y/%b/%d %H:%M')
sp_sch.end_dt   = pd.datetime.strptime(sp_input['end_time'  ],'%Y/%b/%d %H:%M')


sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['scaleA'].index, 
        input_data_series=tb_pandas.result_df['scaleA']['value'], 
        output_time_series=sp_sch.df.index,key_name='scaleA' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['scaleB'].index, 
        input_data_series=tb_pandas.result_df['scaleB']['value'], 
        output_time_series=sp_sch.df.index,key_name='scaleB' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['scaleC'].index, 
        input_data_series=tb_pandas.result_df['scaleC']['value'], 
        output_time_series=sp_sch.df.index,key_name='scaleC' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['scaleD'].index, 
        input_data_series=tb_pandas.result_df['scaleD']['value'], 
        output_time_series=sp_sch.df.index,key_name='scaleD' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['scaleE'].index, 
        input_data_series=tb_pandas.result_df['scaleE']['value'], 
        output_time_series=sp_sch.df.index,key_name='scaleE' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)

sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['m_a1'].index, 
        input_data_series=tb_pandas.result_df['m_a1']['value'], 
        output_time_series=sp_sch.df.index,key_name='m_a1' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['m_a2'].index, 
        input_data_series=tb_pandas.result_df['m_a2']['value'], 
        output_time_series=sp_sch.df.index,key_name='m_a2' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['m_a3'].index, 
        input_data_series=tb_pandas.result_df['m_a3']['value'], 
        output_time_series=sp_sch.df.index,key_name='m_a3' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['m_b1'].index, 
        input_data_series=tb_pandas.result_df['m_b1']['value'], 
        output_time_series=sp_sch.df.index,key_name='m_b1' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['m_b2'].index, 
        input_data_series=tb_pandas.result_df['m_b2']['value'], 
        output_time_series=sp_sch.df.index,key_name='m_b2' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['m_b3'].index, 
        input_data_series=tb_pandas.result_df['m_b3']['value'], 
        output_time_series=sp_sch.df.index,key_name='m_b3' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['m_c1'].index, 
        input_data_series=tb_pandas.result_df['m_c1']['value'], 
        output_time_series=sp_sch.df.index,key_name='m_c1' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['m_c2'].index, 
        input_data_series=tb_pandas.result_df['m_c2']['value'], 
        output_time_series=sp_sch.df.index,key_name='m_c2' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['m_c3'].index, 
        input_data_series=tb_pandas.result_df['m_c3']['value'], 
        output_time_series=sp_sch.df.index,key_name='m_c3' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['m_d1'].index, 
        input_data_series=tb_pandas.result_df['m_d1']['value'], 
        output_time_series=sp_sch.df.index,key_name='m_d1' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['m_d2'].index, 
        input_data_series=tb_pandas.result_df['m_d2']['value'], 
        output_time_series=sp_sch.df.index,key_name='m_d2' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['m_d3'].index, 
        input_data_series=tb_pandas.result_df['m_d3']['value'], 
        output_time_series=sp_sch.df.index,key_name='m_d3' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['m_e1'].index, 
        input_data_series=tb_pandas.result_df['m_e1']['value'], 
        output_time_series=sp_sch.df.index,key_name='m_e1' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['m_e2'].index, 
        input_data_series=tb_pandas.result_df['m_e2']['value'], 
        output_time_series=sp_sch.df.index,key_name='m_e2' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['m_e3'].index, 
        input_data_series=tb_pandas.result_df['m_e3']['value'], 
        output_time_series=sp_sch.df.index,key_name='m_e3' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)

sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['delta_t_sa1'].index, 
        input_data_series=tb_pandas.result_df['delta_t_sa1']['value'], 
        output_time_series=sp_sch.df.index,key_name='delta_t_sa1' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['delta_t_sa2'].index, 
        input_data_series=tb_pandas.result_df['delta_t_sa2']['value'], 
        output_time_series=sp_sch.df.index,key_name='delta_t_sa2' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['delta_t_sb1'].index, 
        input_data_series=tb_pandas.result_df['delta_t_sb1']['value'], 
        output_time_series=sp_sch.df.index,key_name='delta_t_sb1' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['delta_t_sb2'].index, 
        input_data_series=tb_pandas.result_df['delta_t_sb2']['value'], 
        output_time_series=sp_sch.df.index,key_name='delta_t_sb2' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['delta_t_sc1'].index, 
        input_data_series=tb_pandas.result_df['delta_t_sc1']['value'], 
        output_time_series=sp_sch.df.index,key_name='delta_t_sc1' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['delta_t_sc2'].index, 
        input_data_series=tb_pandas.result_df['delta_t_sc2']['value'], 
        output_time_series=sp_sch.df.index,key_name='delta_t_sc2' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['delta_t_sd1'].index, 
        input_data_series=tb_pandas.result_df['delta_t_sd1']['value'], 
        output_time_series=sp_sch.df.index,key_name='delta_t_sd1' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['delta_t_sd2'].index, 
        input_data_series=tb_pandas.result_df['delta_t_sd2']['value'], 
        output_time_series=sp_sch.df.index,key_name='delta_t_sd2' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['delta_t_se1'].index, 
        input_data_series=tb_pandas.result_df['delta_t_se1']['value'], 
        output_time_series=sp_sch.df.index,key_name='delta_t_se1' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
sp_sch.merge_data_from_tb(
        input_time_series=tb_pandas.result_df['delta_t_se2'].index, 
        input_data_series=tb_pandas.result_df['delta_t_se2']['value'], 
        output_time_series=sp_sch.df.index,key_name='delta_t_se2' ,
        plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
# sp_sch.merge_data_from_tb(input_time_series=tb_pandas.result_df['temp_4'].index,
#                 input_data_series=tb_pandas.result_df['temp_4']['value'], output_time_series=sp_sch.df.index,key_name='temp_4' ,
#                         plot=plot_interpolate  ,coef=5e-5,rm_nan=True)
# sp_sch.merge_data_from_tb(input_time_series=tb_pandas.result_df['temp_3'].index,
#                 input_data_series=tb_pandas.result_df['temp_3']['value'], output_time_series=sp_sch.df.index,key_name='temp_3' ,
#                         plot=plot_interpolate  ,coef=5e-5,rm_nan=True)
# sp_sch.merge_data_from_tb(input_time_series=tb_pandas.result_df['temp_2'].index,
#                 input_data_series=tb_pandas.result_df['temp_2']['value'], output_time_series=sp_sch.df.index,key_name='temp_2' ,
#                         plot=plot_interpolate  ,coef=5e-5,rm_nan=True)
# sp_sch.merge_data_from_tb(input_time_series=tb_pandas.result_df['scale1'].index,
#                 input_data_series=tb_pandas.result_df['scale1']['value'], output_time_series=sp_sch.df.index,key_name='scale1' ,
#                         plot=plot_interpolate  ,coef=5e-8,rm_nan=True)
# sp_sch.merge_data_from_tb(input_time_series=tb_pandas.result_df['scale2'].index,
#                 input_data_series=tb_pandas.result_df['scale2']['value'], output_time_series=sp_sch.df.index,key_name='scale2' ,
#                         plot=plot_interpolate  ,coef=5e-5,rm_nan=True)



# fig = plt.figure(figsize=(16,10))
# ax = [[] for i in range(30)]
# ax[0  ] = plt.subplot2grid((2, 1), (0, 0), colspan=1)
# ax[1  ] = plt.subplot2grid((2, 1), (1, 0), colspan=1, sharex = ax[0])

# ax[0].plot(sp_sch.df.index,sp_sch.df['temp_6'])
# ax[0].plot(sp_sch.df.index,sp_sch.df['temp_4'])
# ax[0].plot(sp_sch.df.index,sp_sch.df['temp_3'])
# ax[0].plot(sp_sch.df.index,sp_sch.df['temp_2'])
# ax[1].plot(sp_sch.df.index,sp_sch.df['scale1']) #[0]-sp_sch.df['scale1'])
# ax[1].plot(sp_sch.df.index,sp_sch.df['scale2'])#[0]-sp_sch.df['scale2'])
# ax[1].plot(sp_sch.df.index,sp_sch.df['scale_plus'])

# plt.show()
sp_sch.df.to_csv('result_all.csv')
# #plt.close()
