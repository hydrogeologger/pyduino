import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib.image as image
from datetime import datetime
import glob
import operator

""" Information about the sample and setup"""
#
#                ---------- ---------- ---------- ---------- ----------
#Basin Position  |Basin A | |Basin B | |Basin C | |Basin D | |Basin E |
#Sample Name     |SP04    | |SP06    | |SP11    | |SP09    | |SP01    |
#                ---------- ---------- ---------- ---------- ----------
#
#Initial GWC (%) 136.1      124.8      117.5      143.61     123.9
#Initial SC  (%) 42.4       44.5       46         41.05      44.8
#SG              2.9        2.83       2.82       2.90       2.675

"""Read the csv file and create a DataFrame"""
df=pd.read_csv('result_all.csv')

"""Select durations------------------------------------------------------------
First, we need to ensure df['date_time'] is a Pandas Series with datetime64 as dtype.
Second, we make a boolean mask to select the duration we want---------------"""
df['date_time']=pd.to_datetime(df['date_time'], format='%Y/%m/%d %H:%M:%S')

start_date_A = '2022-05-24 16:20:00'
end_date_A   = '2022-06-17 12:00:00'
duration_A   = (df['date_time'] > start_date_A) & (df['date_time'] <= end_date_A)

start_date_B = '2022-05-24 16:20:00'
end_date_B   = '2022-06-17 12:00:00'
duration_B   = (df['date_time'] > start_date_B) & (df['date_time'] <= end_date_B)

start_date_C = '2022-05-24 16:20:00'
end_date_C   = '2022-06-17 12:00:00'
duration_C   = (df['date_time'] > start_date_C) & (df['date_time'] <= end_date_C)

start_date_D = '2022-06-03 16:20:00'
end_date_D   = '2022-06-17 12:00:00'
duration_D   = (df['date_time'] > start_date_D) & (df['date_time'] <= end_date_D)

start_date_E = '2022-04-14 15:30:00'
end_date_E   = '2022-06-17 12:00:00'
duration_E   = (df['date_time'] > start_date_E) & (df['date_time'] <= end_date_E)

df_A         = df.loc[duration_A]
df_B         = df.loc[duration_B]
df_C         = df.loc[duration_C]
df_D         = df.loc[duration_D]
df_E         = df.loc[duration_E]

     #--------------------Tare the index---------------------------------------

df_A.reset_index(drop=True, inplace=True)
df_B.reset_index(drop=True, inplace=True)
df_C.reset_index(drop=True, inplace=True)
df_D.reset_index(drop=True, inplace=True)
df_E.reset_index(drop=True, inplace=True)     

     #--------------------Tare the time_days-----------------------------------

df_A['time_days'] = df_A['time_days'] - df_A['time_days'].iloc[0]
df_B['time_days'] = df_B['time_days'] - df_B['time_days'].iloc[0]
df_C['time_days'] = df_C['time_days'] - df_C['time_days'].iloc[0]
df_D['time_days'] = df_D['time_days'] - df_D['time_days'].iloc[0]
df_E['time_days'] = df_E['time_days'] - df_E['time_days'].iloc[0]

""" Parameters for calculation"""
initial_weight_A = df_A['scaleA'].max() #g
initial_weight_B = df_B['scaleB'].max() #g
initial_weight_C = df_C['scaleC'].max() #g
initial_weight_D = df_D['scaleD'].max() #g
initial_weight_E = df_E['scaleE'].max() #g 

initial_GWC_A = 1.361
initial_GWC_B = 1.248
initial_GWC_C = 1.175
initial_GWC_D = 1.436
initial_GWC_E = 1.239

kgPg = 0.001
kPkg = 1000
sPday = 86400
water_density_kgPm3 = 1000
mmPm = 1000
SG_kgPm3 = 3000

delta_t_s = 600
area_basin_m2 = 0.1131 

""" Pre-processing"""
    #----------------------------cumulative evaporation------------------------
df_A['evap_cum_kg_A'] = abs(df_A['scaleA'] - initial_weight_A)*kgPg
df_A['evap_cum_mm_A'] = df_A['evap_cum_kg_A']/area_basin_m2/water_density_kgPm3*mmPm
df_B['evap_cum_kg_B'] = abs(df_B['scaleB'] - initial_weight_B)*kgPg
df_B['evap_cum_mm_B'] = df_B['evap_cum_kg_B']/area_basin_m2/water_density_kgPm3*mmPm
df_C['evap_cum_kg_C'] = abs(df_C['scaleC'] - initial_weight_C)*kgPg
df_C['evap_cum_mm_C'] = df_C['evap_cum_kg_C']/area_basin_m2/water_density_kgPm3*mmPm
df_D['evap_cum_kg_D'] = abs(df_D['scaleD'] - initial_weight_D)*kgPg
df_D['evap_cum_mm_D'] = df_D['evap_cum_kg_D']/area_basin_m2/water_density_kgPm3*mmPm
df_E['evap_cum_kg_E'] = abs(df_E['scaleE'] - initial_weight_E)*kgPg
df_E['evap_cum_mm_E'] = df_E['evap_cum_kg_E']/area_basin_m2/water_density_kgPm3*mmPm

    #----------------------------moisture content------------------------------
df_A['GWC_A'] = (initial_weight_A*initial_GWC_A/(1+initial_GWC_A)-df_A['evap_cum_kg_A']*kPkg)/(initial_weight_A/(1+initial_GWC_A))
df_B['GWC_B'] = (initial_weight_B*initial_GWC_B/(1+initial_GWC_B)-df_B['evap_cum_kg_B']*kPkg)/(initial_weight_B/(1+initial_GWC_B))
df_C['GWC_C'] = (initial_weight_C*initial_GWC_C/(1+initial_GWC_C)-df_C['evap_cum_kg_C']*kPkg)/(initial_weight_C/(1+initial_GWC_C))
df_D['GWC_D'] = (initial_weight_D*initial_GWC_D/(1+initial_GWC_D)-df_D['evap_cum_kg_D']*kPkg)/(initial_weight_D/(1+initial_GWC_D))
df_E['GWC_E'] = (initial_weight_E*initial_GWC_E/(1+initial_GWC_E)-df_E['evap_cum_kg_E']*kPkg)/(initial_weight_E/(1+initial_GWC_E))

    #---------------------------evaporation rate-------------------------------
df_A['scaleA_diff_g'] = df_A['scaleA'].diff()
df_A['scaleA_diff_g'].iloc[0] = 0
df_A['evap_kg_A'] = abs(df_A['scaleA_diff_g'])*kgPg
df_A['evap_mm_A'] = df_A['evap_kg_A']/area_basin_m2/water_density_kgPm3*mmPm   #every 600s
df_A['evap_mmPs_A'] = df_A['evap_mm_A']/delta_t_s
df_A['evap_mmPday_A'] = df_A['evap_mmPs_A']*sPday

df_B['scaleB_diff_g'] = df_B['scaleB'].diff()
df_B['scaleB_diff_g'].iloc[0] = 0
df_B['evap_kg_B'] = abs(df_B['scaleB_diff_g'])*kgPg
df_B['evap_mm_B'] = df_B['evap_kg_B']/area_basin_m2/water_density_kgPm3*mmPm   #every 600s
df_B['evap_mmPs_B'] = df_B['evap_mm_B']/delta_t_s
df_B['evap_mmPday_B'] = df_B['evap_mmPs_B']*sPday

df_C['scaleC_diff_g'] = df_C['scaleC'].diff()
df_C['scaleC_diff_g'].iloc[0] = 0
df_C['evap_kg_C'] = abs(df_C['scaleC_diff_g'])*kgPg
df_C['evap_mm_C'] = df_C['evap_kg_C']/area_basin_m2/water_density_kgPm3*mmPm   #every 600s
df_C['evap_mmPs_C'] = df_C['evap_mm_C']/delta_t_s
df_C['evap_mmPday_C'] = df_C['evap_mmPs_C']*sPday

df_D['scaleD_diff_g'] = df_D['scaleD'].diff()
df_D['scaleD_diff_g'].iloc[0] = 0
df_D['evap_kg_D'] = abs(df_D['scaleD_diff_g'])*kgPg
df_D['evap_mm_D'] = df_D['evap_kg_D']/area_basin_m2/water_density_kgPm3*mmPm   #every 600s
df_D['evap_mmPs_D'] = df_D['evap_mm_D']/delta_t_s
df_D['evap_mmPday_D'] = df_D['evap_mmPs_D']*sPday

df_E['scaleE_diff_g'] = df_E['scaleE'].diff()
df_E['scaleE_diff_g'].iloc[0] = 0
df_E['evap_kg_E'] = abs(df_E['scaleE_diff_g'])*kgPg
df_E['evap_mm_E'] = df_E['evap_kg_E']/area_basin_m2/water_density_kgPm3*mmPm   #every 600s
df_E['evap_mmPs_E'] = df_E['evap_mm_E']/delta_t_s
df_E['evap_mmPday_E'] = df_E['evap_mmPs_E']*sPday

"""
This part smoothen the evaporation rate, remove the Zig-Zag using the
MOVING AVERAGE algorithm.
The code here is a bit lumpy and needs to be improved.
"""
df_A['evap_mmPday_smooth_A'] = df_A['evap_mmPday_A'] # Initialization
for i in df_A['evap_mmPday_A']:
    index_i = int(np.where(df_A['evap_mmPday_A']==i)[0])
    if index_i >=10 and index_i <= (len(df_A['evap_mmPday_A'])-10):
        new_rate_A = (df_A['evap_mmPday_A'][index_i-1]+df_A['evap_mmPday_A'][index_i-2]+df_A['evap_mmPday_A'][index_i-3]+
                      df_A['evap_mmPday_A'][index_i-4]+df_A['evap_mmPday_A'][index_i-5]+df_A['evap_mmPday_A'][index_i-6]+
                      df_A['evap_mmPday_A'][index_i-7]+df_A['evap_mmPday_A'][index_i-8]+df_A['evap_mmPday_A'][index_i-9]+
                      df_A['evap_mmPday_A'][index_i+1]+df_A['evap_mmPday_A'][index_i+2]+df_A['evap_mmPday_A'][index_i+3]+
                      df_A['evap_mmPday_A'][index_i+4]+df_A['evap_mmPday_A'][index_i+5]+df_A['evap_mmPday_A'][index_i+6]+
                      df_A['evap_mmPday_A'][index_i+7]+df_A['evap_mmPday_A'][index_i+8]+df_A['evap_mmPday_A'][index_i+9]+
                      df_A['evap_mmPday_A'][index_i])/19
        
        df_A['evap_mmPday_smooth_A'].iloc[index_i] = new_rate_A

df_B['evap_mmPday_smooth_B'] = df_B['evap_mmPday_B'] # Initialization
for i in df_B['evap_mmPday_B']:
    index_i = int(np.where(df_B['evap_mmPday_B']==i)[0])
    if index_i >=10 and index_i <= (len(df_B['evap_mmPday_B'])-10):
        new_rate_B = (df_B['evap_mmPday_B'][index_i-1]+df_B['evap_mmPday_B'][index_i-2]+df_B['evap_mmPday_B'][index_i-3]+
                      df_B['evap_mmPday_B'][index_i-4]+df_B['evap_mmPday_B'][index_i-5]+df_B['evap_mmPday_B'][index_i-6]+
                      df_B['evap_mmPday_B'][index_i-7]+df_B['evap_mmPday_B'][index_i-8]+df_B['evap_mmPday_B'][index_i-9]+
                      df_B['evap_mmPday_B'][index_i+1]+df_B['evap_mmPday_B'][index_i+2]+df_B['evap_mmPday_B'][index_i+3]+
                      df_B['evap_mmPday_B'][index_i+4]+df_B['evap_mmPday_B'][index_i+5]+df_B['evap_mmPday_B'][index_i+6]+
                      df_B['evap_mmPday_B'][index_i+7]+df_B['evap_mmPday_B'][index_i+8]+df_B['evap_mmPday_B'][index_i+9]+
                      df_B['evap_mmPday_B'][index_i])/19
        
        df_B['evap_mmPday_smooth_B'].iloc[index_i] = new_rate_B
        
df_C['evap_mmPday_smooth_C'] = df_C['evap_mmPday_C'] # Initialization
for i in df_C['evap_mmPday_C']:
    index_i = int(np.where(df_C['evap_mmPday_C']==i)[0])
    if index_i >=10 and index_i <= (len(df_C['evap_mmPday_C'])-10):
        new_rate_C = (df_C['evap_mmPday_C'][index_i-1]+df_C['evap_mmPday_C'][index_i-2]+df_C['evap_mmPday_C'][index_i-3]+
                      df_C['evap_mmPday_C'][index_i-4]+df_C['evap_mmPday_C'][index_i-5]+df_C['evap_mmPday_C'][index_i-6]+
                      df_C['evap_mmPday_C'][index_i-7]+df_C['evap_mmPday_C'][index_i-8]+df_C['evap_mmPday_C'][index_i-9]+
                      df_C['evap_mmPday_C'][index_i+1]+df_C['evap_mmPday_C'][index_i+2]+df_C['evap_mmPday_C'][index_i+3]+
                      df_C['evap_mmPday_C'][index_i+4]+df_C['evap_mmPday_C'][index_i+5]+df_C['evap_mmPday_C'][index_i+6]+
                      df_C['evap_mmPday_C'][index_i+7]+df_C['evap_mmPday_C'][index_i+8]+df_C['evap_mmPday_C'][index_i+9]+
                      df_C['evap_mmPday_C'][index_i])/19
        
        df_C['evap_mmPday_smooth_C'].iloc[index_i] = new_rate_C
        
df_D['evap_mmPday_smooth_D'] = df_D['evap_mmPday_D'] # Initialization
for i in df_D['evap_mmPday_D']:
    index_i = int(np.where(df_D['evap_mmPday_D']==i)[0])
    if index_i >=10 and index_i <= (len(df_D['evap_mmPday_D'])-10):
        new_rate_D = (df_D['evap_mmPday_D'][index_i-1]+df_D['evap_mmPday_D'][index_i-2]+df_D['evap_mmPday_D'][index_i-3]+
                      df_D['evap_mmPday_D'][index_i-4]+df_D['evap_mmPday_D'][index_i-5]+df_D['evap_mmPday_D'][index_i-6]+
                      df_D['evap_mmPday_D'][index_i-7]+df_D['evap_mmPday_D'][index_i-8]+df_D['evap_mmPday_D'][index_i-9]+
                      df_D['evap_mmPday_D'][index_i+1]+df_D['evap_mmPday_D'][index_i+2]+df_D['evap_mmPday_D'][index_i+3]+
                      df_D['evap_mmPday_D'][index_i+4]+df_D['evap_mmPday_D'][index_i+5]+df_D['evap_mmPday_D'][index_i+6]+
                      df_D['evap_mmPday_D'][index_i+7]+df_D['evap_mmPday_D'][index_i+8]+df_D['evap_mmPday_D'][index_i+9]+
                      df_D['evap_mmPday_D'][index_i])/19
        
        df_D['evap_mmPday_smooth_D'].iloc[index_i] = new_rate_D

df_E['evap_mmPday_smooth_E'] = df_E['evap_mmPday_E'] # Initialization
for i in df_E['evap_mmPday_E']:
    index_i = int(np.where(df_E['evap_mmPday_E']==i)[0][0])
    if index_i >=10 and index_i <= (len(df_E['evap_mmPday_E'])-10):
        new_rate_E = (df_E['evap_mmPday_E'][index_i-1]+df_E['evap_mmPday_E'][index_i-2]+df_E['evap_mmPday_E'][index_i-3]+
                      df_E['evap_mmPday_E'][index_i-4]+df_E['evap_mmPday_E'][index_i-5]+df_E['evap_mmPday_E'][index_i-6]+
                      df_E['evap_mmPday_E'][index_i-7]+df_E['evap_mmPday_E'][index_i-8]+df_E['evap_mmPday_E'][index_i-9]+
                      df_E['evap_mmPday_E'][index_i+1]+df_E['evap_mmPday_E'][index_i+2]+df_E['evap_mmPday_E'][index_i+3]+
                      df_E['evap_mmPday_E'][index_i+4]+df_E['evap_mmPday_E'][index_i+5]+df_E['evap_mmPday_E'][index_i+6]+
                      df_E['evap_mmPday_E'][index_i+7]+df_E['evap_mmPday_E'][index_i+8]+df_E['evap_mmPday_E'][index_i+9]+
                      df_E['evap_mmPday_E'][index_i])/19
        
        df_E['evap_mmPday_smooth_E'].iloc[index_i] = new_rate_E    
        
"""----------------------------Plots Configuration--------------------------"""
#Overall styles
params = {'legend.fontsize': 4,
          'figure.figsize': (10, 5),
          'axes.labelsize': 11,
          'axes.titlesize':'11',
          'xtick.labelsize':'14',
          'ytick.labelsize':'14',
          'font.weight':'bold',
          'font.sans-serif':'Arial',
          'axes.labelweight':'bold',
          'lines.linewidth':2}

pylab.rcParams.update(params)

lw=2
ms=6
mew=2
grid_width=2
y_fontsize=20

"""------create 2 lists to store info about image files for later use-------"""
path_im_basin_A ='H:\\SpyderWorkingDirectory\\yarwun\\photos_yarwun_basin_test\\basinA\\'    
path_im_basin_B ='H:\\SpyderWorkingDirectory\\yarwun\\photos_yarwun_basin_test\\basinB\\'    
path_im_basin_C ='H:\\SpyderWorkingDirectory\\yarwun\\photos_yarwun_basin_test\\basinC\\'    
path_im_basin_D ='H:\\SpyderWorkingDirectory\\yarwun\\photos_yarwun_basin_test\\basinD\\'    
path_im_basin_E ='H:\\SpyderWorkingDirectory\\yarwun\\photos_yarwun_basin_test\\basinE\\'    

lst_im_path_basin_A = list(filter(os.path.isfile, glob.glob(path_im_basin_A + "*.jpg")))  # filter out the files not ending with .jpg
lst_im_path_basin_B = list(filter(os.path.isfile, glob.glob(path_im_basin_B + "*.jpg"))) 
lst_im_path_basin_C = list(filter(os.path.isfile, glob.glob(path_im_basin_C + "*.jpg")))  
lst_im_path_basin_D = list(filter(os.path.isfile, glob.glob(path_im_basin_D + "*.jpg"))) 
lst_im_path_basin_E = list(filter(os.path.isfile, glob.glob(path_im_basin_E + "*.jpg")))  

"""define a function to parse the date from the absolute directory of the jpg files"""
def get_date_taken_A(path):
    return datetime.strptime(path.split("\\")[-1], 'basinA_' + '%Y_%m_%d_%H_%M_%S.jpg')
def get_date_taken_B(path):
    return datetime.strptime(path.split("\\")[-1], 'basinB_' + '%Y_%m_%d_%H_%M_%S.jpg')
def get_date_taken_C(path):
    return datetime.strptime(path.split("\\")[-1], 'basinC_' + '%Y_%m_%d_%H_%M_%S.jpg')
def get_date_taken_D(path):
    return datetime.strptime(path.split("\\")[-1], 'basinD_' + '%Y_%m_%d_%H_%M_%S.jpg')
def get_date_taken_E(path):
    return datetime.strptime(path.split("\\")[-1], 'basinE_' + '%Y_%m_%d_%H_%M_%S.jpg')

im_name_basin_A = []
im_date_basin_A = []
for i in lst_im_path_basin_A:
    im_name_basin_A.append(i.split('\\')[-1])
    im_date_basin_A.append(get_date_taken_A(i))
    
im_name_basin_B = []
im_date_basin_B = []
for i in lst_im_path_basin_B:
    im_name_basin_B.append(i.split('\\')[-1])
    im_date_basin_B.append(get_date_taken_B(i))
    
im_name_basin_C = []
im_date_basin_C = []
for i in lst_im_path_basin_C:
    im_name_basin_C.append(i.split('\\')[-1])
    im_date_basin_C.append(get_date_taken_C(i))
    
im_name_basin_D = []
im_date_basin_D = []
for i in lst_im_path_basin_D:
    im_name_basin_D.append(i.split('\\')[-1])
    im_date_basin_D.append(get_date_taken_D(i))

im_name_basin_E = []
im_date_basin_E = []
for i in lst_im_path_basin_E:
    im_name_basin_E.append(i.split('\\')[-1])
    im_date_basin_E.append(get_date_taken_E(i))

"""
This part assigns a GWC value to each JPG file, so that we can find the data point
correspoding to that JPG file by using GWC as index.
Reason of doing this is that: name of the JPG file only contains the info about
date, but not the info about GWC; By making the JPG image file an Python Object,
we can add any attributes such as GWC to the JPG image file
"""
class IMG:    
    def __init__(self, image_path, gwc_of_the_image):
        self.gwc = gwc_of_the_image
        self.img = image.imread(image_path)
        
"""----------------Start plotting figures used for video--------------------"""
gwc_increment = 0.05
initial_gwc   = 1.4
residual_gwc  = 0.10
selected_gwc = np.arange(initial_gwc, residual_gwc, -gwc_increment)

""" Find the image we need for given GWCs
First, we find the index of the data at the current GWC (1st enumeration)
Then we can know the date_time using the index we just obtain
Second, we find the index of the image at the current date_time (2nd enumeration)
"""
for gwc in selected_gwc:
    idx_gwc_A, min_value_A = min(enumerate(abs(df_A['GWC_A']-gwc)), key=operator.itemgetter(1)) # find the index corresponding to the GWC we want
    idx_im_A, min_value_A = min(enumerate(abs(df_A.iloc[idx_gwc_A]['date_time']-pd.DataFrame(im_date_basin_A)[0])), key=operator.itemgetter(1)) # find the photo index corresponding to the GWC we want   
    current_im_basin_A = IMG(lst_im_path_basin_A[idx_im_A], gwc).img
    
    idx_gwc_B, min_value_B = min(enumerate(abs(df_B['GWC_B']-gwc)), key=operator.itemgetter(1)) # find the index corresponding to the GWC we want
    idx_im_B, min_value_B = min(enumerate(abs(df_B.iloc[idx_gwc_B]['date_time']-pd.DataFrame(im_date_basin_B)[0])), key=operator.itemgetter(1)) # find the photo index corresponding to the GWC we want   
    current_im_basin_B = IMG(lst_im_path_basin_B[idx_im_B], gwc).img

    idx_gwc_C, min_value_C = min(enumerate(abs(df_C['GWC_C']-gwc)), key=operator.itemgetter(1)) # find the index corresponding to the GWC we want
    idx_im_C, min_value_C = min(enumerate(abs(df_C.iloc[idx_gwc_C]['date_time']-pd.DataFrame(im_date_basin_C)[0])), key=operator.itemgetter(1)) # find the photo index corresponding to the GWC we want   
    current_im_basin_C = IMG(lst_im_path_basin_C[idx_im_C], gwc).img

    idx_gwc_D, min_value_D = min(enumerate(abs(df_D['GWC_D']-gwc)), key=operator.itemgetter(1)) # find the index corresponding to the GWC we want
    idx_im_D, min_value_D = min(enumerate(abs(df_D.iloc[idx_gwc_D]['date_time']-pd.DataFrame(im_date_basin_D)[0])), key=operator.itemgetter(1)) # find the photo index corresponding to the GWC we want   
    current_im_basin_D = IMG(lst_im_path_basin_D[idx_im_D], gwc).img

    idx_gwc_E, min_value_E = min(enumerate(abs(df_E['GWC_E']-gwc)), key=operator.itemgetter(1)) # find the index corresponding to the GWC we want
    idx_im_E, min_value_E = min(enumerate(abs(df_E.iloc[idx_gwc_E]['date_time']-pd.DataFrame(im_date_basin_E)[0])), key=operator.itemgetter(1)) # find the photo index corresponding to the GWC we want   
    current_im_basin_E = IMG(lst_im_path_basin_E[idx_im_E], gwc).img    
        
    """---------------Initialize the Figure and its sub-plots---------------"""
    
    fig   = plt.figure(num='Basin_all',figsize=(18,9))
    ax    = [[] for i in range(25)]   # 20+5(plots with same x axis, i.e. secondary y-axis)
    ax[0]  = plt.subplot2grid((4,5), (0, 0), colspan=1, rowspan=1)
    ax[1]  = plt.subplot2grid((4,5), (0, 1), colspan=1, rowspan=1)
    ax[2]  = plt.subplot2grid((4,5), (0, 2), colspan=1, rowspan=1)
    ax[3]  = plt.subplot2grid((4,5), (0, 3), colspan=1, rowspan=1)
    ax[4]  = plt.subplot2grid((4,5), (0, 4), colspan=1, rowspan=1)
    ax[5]  = plt.subplot2grid((4,5), (1, 0), colspan=1, rowspan=1)
    ax[6]  = plt.subplot2grid((4,5), (1, 1), colspan=1, rowspan=1)
    ax[7]  = plt.subplot2grid((4,5), (1, 2), colspan=1, rowspan=1)
    ax[8]  = plt.subplot2grid((4,5), (1, 3), colspan=1, rowspan=1)
    ax[9]  = plt.subplot2grid((4,5), (1, 4), colspan=1, rowspan=1)
    ax[10] = plt.subplot2grid((4,5), (2, 0), colspan=1, rowspan=1)
    ax[11] = plt.subplot2grid((4,5), (2, 1), colspan=1, rowspan=1)
    ax[12] = plt.subplot2grid((4,5), (2, 2), colspan=1, rowspan=1)
    ax[13] = plt.subplot2grid((4,5), (2, 3), colspan=1, rowspan=1)
    ax[14] = plt.subplot2grid((4,5), (2, 4), colspan=1, rowspan=1)
    ax[15] = plt.subplot2grid((4,5), (3, 0), colspan=1, rowspan=1)
    ax[16] = plt.subplot2grid((4,5), (3, 1), colspan=1, rowspan=1)
    ax[17] = plt.subplot2grid((4,5), (3, 2), colspan=1, rowspan=1)
    ax[18] = plt.subplot2grid((4,5), (3, 3), colspan=1, rowspan=1)
    ax[19] = plt.subplot2grid((4,5), (3, 4), colspan=1, rowspan=1)
    
    #------------adjust size and spacing of the subplot------------------------
    
    fig.subplots_adjust(left   = 0.05,  # position of the left edge of the subplots, as a fraction of the figure width
                        right  = 0.95,  # position of the right edge of the subplots, as a fraction of the figure width
                        top    = 0.95,  # position of the top edge of the subplots, as a fraction of the figure height
                        bottom = 0.05,  # position of the bottom edge of the subplots, as a fraction of the figure height
                        hspace = 0.05,  # height of the padding between subplots
                        wspace = 0.03)  # width of the padding between subplots

    # """-----------Plot Evap Rate and Cumulative Evap-----------------------"""
    
    first=ax[5].plot(df_A['time_days'][:idx_gwc_A], df_A['evap_mmPday_smooth_A'][:idx_gwc_A], '-', color='b', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='Evap rate (mm/day)', markevery=2)
    ax[20] = ax[5].twinx()
    second=ax[20].plot(df_A['time_days'][:idx_gwc_A], df_A['evap_cum_mm_A'][:idx_gwc_A], '-', color='r', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='Cumulative Evap (mm)', markevery=2)

    ax[6].plot(df_B['time_days'][:idx_gwc_B], df_B['evap_mmPday_smooth_B'][:idx_gwc_B], '-', color='b', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='Evap rate (mm/day)', markevery=2)
    ax[21] = ax[6].twinx()
    ax[21].plot(df_B['time_days'][:idx_gwc_B], df_B['evap_cum_mm_B'][:idx_gwc_B], '-', color='r', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='Cumulative Evap (mm)', markevery=2)

    ax[7].plot(df_C['time_days'][:idx_gwc_C], df_C['evap_mmPday_smooth_C'][:idx_gwc_C], '-', color='b', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='Evap rate (mm/day)', markevery=2)
    ax[22] = ax[7].twinx()
    ax[22].plot(df_C['time_days'][:idx_gwc_C], df_C['evap_cum_mm_C'][:idx_gwc_C], '-', color='r', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='Cumulative Evap (mm)', markevery=2)

    ax[8].plot(df_D['time_days'][:idx_gwc_D], df_D['evap_mmPday_smooth_D'][:idx_gwc_D], '-', color='b', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='Evap rate (mm/day)', markevery=2)
    ax[23] = ax[8].twinx()
    ax[23].plot(df_D['time_days'][:idx_gwc_D], df_D['evap_cum_mm_D'][:idx_gwc_D], '-', color='r', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='Cumulative Evap (mm)', markevery=2)

    ax[9].plot(df_E['time_days'][:idx_gwc_E], df_E['evap_mmPday_smooth_E'][:idx_gwc_E], '-', color='b', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='Evap rate (mm/day)', markevery=2)
    ax[24] = ax[9].twinx()
    ax[24].plot(df_E['time_days'][:idx_gwc_E], df_E['evap_cum_mm_E'][:idx_gwc_E], '-', color='r', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='Cumulative Evap (mm)', markevery=2)

    # """-----------Plot Moisture Sensor Readings-----------------------"""

    ax[10].plot(df_A['time_days'][:idx_gwc_A], df_A['m_a1'][:idx_gwc_A], '-', color='b', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='MO.1', markevery=2)
    ax[10].plot(df_A['time_days'][:idx_gwc_A], df_A['m_a2'][:idx_gwc_A], '-', color='r', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='MO.2', markevery=2)
    ax[10].plot(df_A['time_days'][:idx_gwc_A], df_A['m_a3'][:idx_gwc_A], '-', color='y', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='MO.3', markevery=2)

    ax[11].plot(df_B['time_days'][:idx_gwc_B], df_B['m_b1'][:idx_gwc_B], '-', color='b', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='MO.1', markevery=2)
    ax[11].plot(df_B['time_days'][:idx_gwc_B], df_B['m_b2'][:idx_gwc_B], '-', color='r', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='MO.2', markevery=2)
    ax[11].plot(df_B['time_days'][:idx_gwc_B], df_B['m_b3'][:idx_gwc_B], '-', color='y', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='MO.3', markevery=2)

    ax[12].plot(df_C['time_days'][:idx_gwc_C], df_C['m_c1'][:idx_gwc_C], '-', color='b', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='MO.1', markevery=2)
    ax[12].plot(df_C['time_days'][:idx_gwc_C], df_C['m_c2'][:idx_gwc_C], '-', color='r', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='MO.2', markevery=2)
    ax[12].plot(df_C['time_days'][:idx_gwc_C], df_C['m_c3'][:idx_gwc_C], '-', color='y', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='MO.3', markevery=2)

    ax[13].plot(df_D['time_days'][:idx_gwc_D], df_D['m_d1'][:idx_gwc_D], '-', color='b', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='MO.1', markevery=2)
    ax[13].plot(df_D['time_days'][:idx_gwc_D], df_D['m_d2'][:idx_gwc_D], '-', color='r', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='MO.2', markevery=2)
    ax[13].plot(df_D['time_days'][:idx_gwc_D], df_D['m_d3'][:idx_gwc_D], '-', color='y', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='MO.3', markevery=2)

    ax[14].plot(df_E['time_days'][:idx_gwc_E], df_E['m_e1'][:idx_gwc_E], '-', color='b', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='MO.1', markevery=2)
    ax[14].plot(df_E['time_days'][:idx_gwc_E], df_E['m_e2'][:idx_gwc_E], '-', color='r', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='MO.2', markevery=2)
    ax[14].plot(df_E['time_days'][:idx_gwc_E], df_E['m_e3'][:idx_gwc_E], '-', color='y', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='MO.3', markevery=2)
    
    # """-----------Plot Suction Sensor Readings-----------------------"""

    ax[15].plot(df_A['time_days'][:idx_gwc_A], df_A['delta_t_sa1'][:idx_gwc_A], '-', color='b', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='SUC.1', markevery=2)
    ax[15].plot(df_A['time_days'][:idx_gwc_A], df_A['delta_t_sa2'][:idx_gwc_A], '-', color='r', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='SUC.2', markevery=2)

    ax[16].plot(df_B['time_days'][:idx_gwc_B], df_B['delta_t_sb1'][:idx_gwc_B], '-', color='b', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='SUC.1', markevery=2)
    ax[16].plot(df_B['time_days'][:idx_gwc_B], df_B['delta_t_sb2'][:idx_gwc_B], '-', color='r', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='SUC.2', markevery=2)

    ax[17].plot(df_C['time_days'][:idx_gwc_C], df_C['delta_t_sc1'][:idx_gwc_C], '-', color='b', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='SUC.1', markevery=2)
    ax[17].plot(df_C['time_days'][:idx_gwc_C], df_C['delta_t_sc2'][:idx_gwc_C], '-', color='r', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='SUC.2', markevery=2)

    ax[18].plot(df_D['time_days'][:idx_gwc_D], df_D['delta_t_sd1'][:idx_gwc_D], '-', color='b', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='SUC.1', markevery=2)
    ax[18].plot(df_D['time_days'][:idx_gwc_D], df_D['delta_t_sd2'][:idx_gwc_D], '-', color='r', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='SUC.2', markevery=2)

    ax[19].plot(df_E['time_days'][:idx_gwc_E], df_E['delta_t_se1'][:idx_gwc_E], '-', color='b', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='SUC.1', markevery=2)
    ax[19].plot(df_E['time_days'][:idx_gwc_E], df_E['delta_t_se2'][:idx_gwc_E], '-', color='r', markersize=ms, markeredgewidth=mew, markeredgecolor='m', label='SUC.2', markevery=2)


    # """--------------Detailed Configurations--------------------------------"""
    #----------------Bold the border of each subplot---------------------------
    for i in ax:
        for axis in ['top','bottom','left','right']:
            i.spines[axis].set_linewidth(2)
            
    #----------------Set limits for x-axis--------------------------
    xlim_A=[df_A['time_days'].iloc[0], df_A['time_days'].iloc[-1]]
    xlim_B=[df_B['time_days'].iloc[0], df_B['time_days'].iloc[-1]]
    xlim_C=[df_C['time_days'].iloc[0], df_C['time_days'].iloc[-1]]
    xlim_D=[df_D['time_days'].iloc[0], df_D['time_days'].iloc[-1]]
    xlim_E=[df_E['time_days'].iloc[0], df_E['time_days'].iloc[-1]]

    ax[5].set_xlim(xlim_A)
    ax[6].set_xlim(xlim_B)
    ax[7].set_xlim(xlim_C)
    ax[8].set_xlim(xlim_D)
    ax[9].set_xlim(xlim_E)

    ax[10].set_xlim(xlim_A)
    ax[11].set_xlim(xlim_B)
    ax[12].set_xlim(xlim_C)
    ax[13].set_xlim(xlim_D)
    ax[14].set_xlim(xlim_E)

    ax[15].set_xlim(xlim_A)
    ax[16].set_xlim(xlim_B)
    ax[17].set_xlim(xlim_C)
    ax[18].set_xlim(xlim_D)
    ax[19].set_xlim(xlim_E)
        
    #----------------Set limits for y-axis--------------------------

    ax[5].set_ylim([0, 6])  # limits for daily evaporation rate
    ax[6].set_ylim([0, 6])
    ax[7].set_ylim([0, 6])
    ax[8].set_ylim([0, 6])
    ax[9].set_ylim([0, 6])
    
    ax[20].set_ylim([0, 80])  # limits for cumulative evaporation
    ax[21].set_ylim([0, 80])
    ax[22].set_ylim([0, 80])
    ax[23].set_ylim([0, 80])
    ax[24].set_ylim([0, 80])
    
    ax[10].set_ylim([100, 500])  # limits for daily moisture sensor
    ax[11].set_ylim([100, 500])
    ax[12].set_ylim([100, 500])
    ax[13].set_ylim([100, 500])
    ax[14].set_ylim([100, 500])
        
    ax[15].set_ylim([5, 15])  # limits for daily suction sensor
    ax[16].set_ylim([5, 15])
    ax[17].set_ylim([5, 15])
    ax[18].set_ylim([5, 15])
    ax[19].set_ylim([5, 15])
    
    #---------------Set labels for x-axis--------------------------------------
    
    ax[15].set_xlabel('TIME (DAYS)', fontsize=y_fontsize,labelpad=3)
    ax[16].set_xlabel('TIME (DAYS)', fontsize=y_fontsize,labelpad=3)
    ax[17].set_xlabel('TIME (DAYS)', fontsize=y_fontsize,labelpad=3)
    ax[18].set_xlabel('TIME (DAYS)', fontsize=y_fontsize,labelpad=3)
    ax[19].set_xlabel('TIME (DAYS)', fontsize=y_fontsize,labelpad=3)

    #---------------Set labels for x-axis--------------------------------------    
    
    ax[5].set_ylabel('EVAP RATE\n(mm/day)', fontsize=y_fontsize, labelpad=20, color='b')  
    ax[10].set_ylabel('MOISTURE\nSENSOR', fontsize=y_fontsize, labelpad=2)    
    ax[15].set_ylabel('SUCTION\nSENSOR', fontsize=y_fontsize, labelpad=9)
    ax[24].set_ylabel('CUMULATIVE\nEVAP (mm)', fontsize=y_fontsize, labelpad=3, color='r')
  
    #---------------Set ticks for x-axis and y-axis----------------------------
    
    ax[5].set_yticks([1, 2, 3, 4, 5, 6])
    ax[6].set_yticks([1, 2, 3, 4, 5, 6])
    ax[7].set_yticks([1, 2, 3, 4, 5, 6])
    ax[8].set_yticks([1, 2, 3, 4, 5, 6])
    ax[9].set_yticks([1, 2, 3, 4, 5, 6])
    
    ax[10].set_yticks([150, 250, 350, 450])
    ax[11].set_yticks([150, 250, 350, 450])
    ax[12].set_yticks([150, 250, 350, 450])
    ax[13].set_yticks([150, 250, 350, 450])
    ax[14].set_yticks([150, 250, 350, 450])

    ax[15].set_yticks([6, 8, 10, 12, 14])
    ax[16].set_yticks([6, 8, 10, 12, 14])
    ax[17].set_yticks([6, 8, 10, 12, 14])
    ax[18].set_yticks([6, 8, 10, 12, 14])
    ax[19].set_yticks([6, 8, 10, 12, 14])
        
    #-----------------------Remove labels and ticks----------------------------

    plt.setp(ax[5].get_xticklabels(), visible=False)
    plt.setp(ax[5].get_yticklabels(), visible=True, color='b', fontsize=18)
    ax[5].tick_params(axis='both', which='both', length=0)
    
    plt.setp(ax[6].get_xticklabels(), visible=False)
    plt.setp(ax[6].get_yticklabels(), visible=False)
    ax[6].tick_params(axis='both', which='both', length=0)

    plt.setp(ax[7].get_xticklabels(), visible=False)
    plt.setp(ax[7].get_yticklabels(), visible=False)
    ax[7].tick_params(axis='both', which='both', length=0)
    
    plt.setp(ax[8].get_xticklabels(), visible=False)
    plt.setp(ax[8].get_yticklabels(), visible=False)
    ax[8].tick_params(axis='both', which='both', length=0)
    
    plt.setp(ax[9].get_xticklabels(), visible=False)
    plt.setp(ax[9].get_yticklabels(), visible=False)
    ax[9].tick_params(axis='both', which='both', length=0)
    
    plt.setp(ax[10].get_xticklabels(), visible=False)
    plt.setp(ax[10].get_yticklabels(), visible=True, fontsize=18)
    ax[10].tick_params(axis='both', which='both', length=0)
    
    plt.setp(ax[11].get_xticklabels(), visible=False)
    plt.setp(ax[11].get_yticklabels(), visible=False)
    ax[11].tick_params(axis='both', which='both', length=0)
    
    plt.setp(ax[12].get_xticklabels(), visible=False)
    plt.setp(ax[12].get_yticklabels(), visible=False)
    ax[12].tick_params(axis='both', which='both', length=0)
    
    plt.setp(ax[13].get_xticklabels(), visible=False)
    plt.setp(ax[13].get_yticklabels(), visible=False)
    ax[13].tick_params(axis='both', which='both', length=0)
    
    plt.setp(ax[14].get_xticklabels(), visible=False)
    plt.setp(ax[14].get_yticklabels(), visible=False)
    ax[14].tick_params(axis='both', which='both', length=0)
    
    #--------------------------------------------------------------------------
    
    plt.setp(ax[15].get_xticklabels(), visible=True, fontsize=18)
    plt.setp(ax[15].get_yticklabels(), visible=True, fontsize=18)
    ax[15].tick_params(axis='both', which='both', length=0)    
    
    plt.setp(ax[16].get_xticklabels(), visible=True, fontsize=18)
    plt.setp(ax[16].get_yticklabels(), visible=False)
    ax[16].tick_params(axis='both', which='both', length=0)
    
    plt.setp(ax[17].get_xticklabels(), visible=True, fontsize=18)
    plt.setp(ax[17].get_yticklabels(), visible=False)
    ax[17].tick_params(axis='both', which='both', length=0)
    
    plt.setp(ax[18].get_xticklabels(), visible=True, fontsize=18)
    plt.setp(ax[18].get_yticklabels(), visible=False)
    ax[18].tick_params(axis='both', which='both', length=0)
    
    plt.setp(ax[19].get_xticklabels(), visible=True, fontsize=18)
    plt.setp(ax[19].get_yticklabels(), visible=False)
    ax[19].tick_params(axis='both', which='both', length=0)
      
    #--------------------------------------------------------------------------
    
    plt.setp(ax[20].get_xticklabels(), visible=True)
    plt.setp(ax[20].get_yticklabels(), visible=False)
    ax[20].tick_params(axis='both', which='minor', length=0)
    
    plt.setp(ax[21].get_xticklabels(), visible=True)
    plt.setp(ax[21].get_yticklabels(), visible=False)
    ax[21].tick_params(axis='both', which='minor', length=0)
    
    plt.setp(ax[22].get_xticklabels(), visible=True)
    plt.setp(ax[22].get_yticklabels(), visible=False)
    ax[22].tick_params(axis='both', which='minor', length=0)
    
    plt.setp(ax[23].get_xticklabels(), visible=True)
    plt.setp(ax[23].get_yticklabels(), visible=False)
    ax[23].tick_params(axis='both', which='minor', length=0)
        
    plt.setp(ax[24].get_xticklabels(), visible=False)
    plt.setp(ax[24].get_yticklabels(), visible=True, color='r', fontsize=18)
    ax[24].tick_params(axis='both', which='minor', length=0)
    
    #---------------Set gridlines----------------------------------------------
    
    ax[5].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[6].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[7].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[8].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[9].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    
    ax[10].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[11].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[12].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[13].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[14].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    
    ax[15].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[16].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[17].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[18].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[19].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    
    #---------------Set legends------------------------------------------------
    
    # ax[5].legend(loc='upper right', borderaxespad=0.8, fontsize=14, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)    
    # ax[6].legend(loc='upper right', borderaxespad=0.8, fontsize=14, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    # ax[7].legend(loc='upper right', borderaxespad=0.8, fontsize=14, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    # ax[8].legend(loc='upper right', borderaxespad=0.8, fontsize=14, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    # ax[9].legend(loc='upper right', borderaxespad=0.8, fontsize=14, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)

    ax[10].legend(loc='lower left', borderaxespad=0.8, fontsize=16, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    # ax[11].legend(loc='lower left', borderaxespad=0.8, fontsize=14, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    # ax[12].legend(loc='lower left', borderaxespad=0.8, fontsize=14, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    # ax[13].legend(loc='lower left', borderaxespad=0.8, fontsize=14, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    # ax[14].legend(loc='lower left', borderaxespad=0.8, fontsize=14, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)

    ax[15].legend(loc='upper left', borderaxespad=0.8, fontsize=16, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    # ax[16].legend(loc='lower right', borderaxespad=0.8, fontsize=14, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    # ax[17].legend(loc='lower right', borderaxespad=0.8, fontsize=14, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    # ax[18].legend(loc='lower right', borderaxespad=0.8, fontsize=14, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    # ax[19].legend(loc='lower right', borderaxespad=0.8, fontsize=14, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)

    
    """--------Add the JPG file to the figure and label the image-----------"""
    ax[0].imshow(current_im_basin_A)
    ax[0].axis('off')
    ax[0].set_title('Basin A (SP04)', x=0.01, y=0.75, fontweight='bold', fontsize=24, color='r', loc='left')
    
    ax[1].imshow(current_im_basin_B)
    ax[1].axis('off')
    ax[1].set_title('Basin B (SP06)', x=0.01, y=0.75, fontweight='bold', fontsize=24, color='r', loc='left')
    
    ax[2].imshow(current_im_basin_C)
    ax[2].axis('off')
    ax[2].set_title('Basin C (SP11)', x=0.01, y=0.75, fontweight='bold', fontsize=24, color='r', loc='left')
    
    ax[3].imshow(current_im_basin_D)
    ax[3].axis('off')
    ax[3].set_title('Basin D (SP09)', x=0.01, y=0.75, fontweight='bold', fontsize=24, color='r', loc='left')

    ax[4].imshow(current_im_basin_E)
    ax[4].axis('off')
    ax[4].set_title('Basin E (SP01)', x=0.01, y=0.75, fontweight='bold', fontsize=24, color='r', loc='left')
    
    """-----------Add the Moisture Content to the figure--------------------"""
    
    GWC_basin_A = str(round(IMG(lst_im_path_basin_A[idx_im_A], gwc).gwc,2))
    text = "GWC\n= " + GWC_basin_A
    fig.text(0.0, 0.82, text, fontsize=24, bbox=dict(boxstyle="square",
                                                       ec=(1., 0.2, 0.2),
                                                       fc=(1., 0.2, 0.2),))
    
    """--------Save the figure----------------------------------------------"""
    plt.show(block=False)
    output_name = os.getcwd() + '\\photos_for_video' + '\\' + str(round(gwc*100,2))+'.jpg'
    fig.savefig(output_name, format='jpg', dpi=100, bbox_inches='tight', pad_inches=0.01 )
    # plt.close()

"""-------------------Converting images to video----------------------------------"""
"""The sequence of the images is important because the video plays images in 
order. However, by default, 10.jpg will be displayed before 2.jpg because
'10' < '2' in str comparison. Thus we need to convert them to floats and then 
we can sort them mathematically."""

def get_jpg_number(jpg_name):
    return float(jpg_name.split('.')[-3])

image_folder = os.getcwd() + '\\photos_for_video'
video_name = 'basin_all.avi'
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
images.sort(key=lambda x: get_jpg_number(x), reverse=True)
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape
video = cv2.VideoWriter(video_name, 0, 2, (width,height))

for img in images:
    video.write(cv2.imread(os.path.join(image_folder, img)))

cv2.destroyAllWindows()
video.release()

























