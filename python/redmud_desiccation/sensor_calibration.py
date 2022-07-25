# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 19:51:07 2022

@author: uqzzhao7
"""

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

SG_A = 2.9
SG_B = 2.83
SG_C = 2.82
SG_D = 2.90
SG_E = 2.675

SC_A = 0.424
SC_B = 0.445
SC_C = 0.460
SC_D = 0.411
SC_E = 0.448

def swcc_reverse_fredlund_xing_1994(**kwargs):
    '''Soil water retention curve from Fredlund and Xing [1994]
      reversing calculating from content to suction
      input should be volumetric water content
      output unit is kpa
      input:
      input explanation:
      af -- [kpa] a soil parameter which is primarily a function of air entry value
      nf -- a soil parameter which is primarily a function of the rate of water extraction from the soil once the air-entry value has been exceeded
      mf -- a soil parameter which is primarily a function of the residual water content
      hr -- [kpa] suction at which residual water contents occurrs 
      por-- porosity
      psi_0  -- the suction kpa when volumetric water content is saturated
      '''
    arg_defaults = {
                'nf'  :0.85,
                'mf'  :0.31,
                'af'  :24.9999,
                'hr'  :223873.8,
                'por':0.54,
                'vwc':0.1,
                'psi_0':1e-1,
                'psi_1':0.02  
                }

    arg=arg_defaults
    for d in kwargs:
        arg[d]= kwargs.get(d)

    psi_outcome=np.zeros(len(np.atleast_1d(arg['vwc'])))

    for i,k in enumerate(np.atleast_1d(arg['vwc'])) :
        #import pdb
#        psi_1=0.02  # after a testing, the starting point would be good to be near the saturation level
        psi_1=arg['psi_1'] #2020-01-03 
#        psi_1=arg['af']  #2017-07-08 16:27 turns out the air entry pressure is the best start guessing point 
        psi_0=arg['psi_0'] #2020-01-03
        
        #pdb.set_trace()
        if k>=arg['por']:
            psi_1=arg['psi_0']
        else:
            while abs(psi_0-psi_1)>0.0001:
                psi_0=psi_1

                psi_on_af  = psi_0/arg['af']
                log_on_log =  np.log(1+psi_0/arg['hr']) / np.log(1+1.e6/arg['hr']) 

                e_plus    = np.e+psi_on_af**arg['nf']
                log_e      = np.log(e_plus) 
                dw_dpsi_0   =  - arg['mf']*arg['nf']*psi_on_af**(-1+arg['nf']) * arg['por'] * (1- log_on_log) * log_e **(-1-arg['mf']) /  arg['af'] / e_plus - arg['por']* log_e**(-arg['mf'])/arg['hr']/(1+psi_0/arg['hr'])/np.log(1+1.e6/arg['hr'])


                tmp1=1  -  np.log(1+psi_0/arg['hr'])  /  np.log(1+1.0e6/arg['hr'])
                tmp2=np.exp(1)+(psi_0/arg['af'])**arg['nf']
                tmp3=np.log(tmp2)**arg['mf']
                w_0=arg['por']*tmp1*(1/tmp3)-k


                psi_1= psi_0 - w_0/dw_dpsi_0
        #print psi_1
        psi_outcome[i] = psi_1


    return psi_outcome

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

""" Moisture Sensor Calibration"""
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
          'lines.linewidth':2,
          'figure.subplot.hspace':0.3}

pylab.rcParams.update(params)

lw=2
ms=2
mew=2
grid_width=2
label_fontsize=16
legend_fontsize=10

"""---------------Initialize the Figure and its sub-plots---------------"""
    
fig   = plt.figure(num='Calibration',figsize=(18,9))
ax    = [[] for i in range(15)]   # 20+5(plots with same x axis, i.e. secondary y-axis)
ax[0]  = plt.subplot2grid((3,5), (0, 0), colspan=1, rowspan=1)
ax[1]  = plt.subplot2grid((3,5), (0, 1), colspan=1, rowspan=1)
ax[2]  = plt.subplot2grid((3,5), (0, 2), colspan=1, rowspan=1)
ax[3]  = plt.subplot2grid((3,5), (0, 3), colspan=1, rowspan=1)
ax[4]  = plt.subplot2grid((3,5), (0, 4), colspan=1, rowspan=1)
ax[5]  = plt.subplot2grid((3,5), (1, 0), colspan=1, rowspan=1)
ax[6]  = plt.subplot2grid((3,5), (1, 1), colspan=1, rowspan=1)
ax[7]  = plt.subplot2grid((3,5), (1, 2), colspan=1, rowspan=1)
ax[8]  = plt.subplot2grid((3,5), (1, 3), colspan=1, rowspan=1)
ax[9]  = plt.subplot2grid((3,5), (1, 4), colspan=1, rowspan=1)
ax[10]  = plt.subplot2grid((3,5), (2, 0), colspan=1, rowspan=1)
ax[11]  = plt.subplot2grid((3,5), (2, 1), colspan=1, rowspan=1)
ax[12]  = plt.subplot2grid((3,5), (2, 2), colspan=1, rowspan=1)
ax[13]  = plt.subplot2grid((3,5), (2, 3), colspan=1, rowspan=1)
ax[14]  = plt.subplot2grid((3,5), (2, 4), colspan=1, rowspan=1)

"""Select durations------------------------------------------------------------
start from the time sensors showed response (around liquid limit/DoS=1)-----"""

start_date_A = '2022-05-30 16:20:00'
end_date_A   = '2022-07-07 12:00:00'
duration_A   = (df_A['date_time'] > start_date_A) & (df_A['date_time'] <= end_date_A)

start_date_B = '2022-05-30 16:20:00'
end_date_B   = '2022-07-7 12:00:00'
duration_B   = (df_B['date_time'] > start_date_B) & (df_B['date_time'] <= end_date_B)

start_date_C = '2022-05-30 16:20:00'
end_date_C   = '2022-07-07 12:00:00'
duration_C   = (df_C['date_time'] > start_date_C) & (df_C['date_time'] <= end_date_C)

start_date_D = '2022-06-08 16:20:00'
end_date_D   = '2022-07-07 12:00:00'
duration_D   = (df_D['date_time'] > start_date_D) & (df_D['date_time'] <= end_date_D)

start_date_E = '2022-04-15 15:30:00'
end_date_E   = '2022-07-07 12:00:00'
duration_E   = (df_E['date_time'] > start_date_E) & (df_E['date_time'] <= end_date_E)

df_A         = df_A.loc[duration_A]
df_B         = df_B.loc[duration_B]
df_C         = df_C.loc[duration_C]
df_D         = df_D.loc[duration_D]
df_E         = df_E.loc[duration_E]

""" Moisture Sensor Calibration """
# moisture sensor upper and lower bounds
mo_a1_min, mo_a1_max = (df_A['m_a1'].min(), df_A['m_a1'].max())
mo_a2_min, mo_a2_max = (df_A['m_a2'].min(), df_A['m_a2'].max())
mo_a3_min, mo_a3_max = (df_A['m_a3'].min(), df_A['m_a3'].max())
mo_b1_min, mo_b1_max = (df_B['m_b1'].min(), df_B['m_b1'].max())
mo_b2_min, mo_b2_max = (df_B['m_b2'].min(), df_B['m_b2'].max())
mo_b3_min, mo_b3_max = (df_B['m_b3'].min(), df_B['m_b3'].max())
mo_c1_min, mo_c1_max = (df_C['m_c1'].min(), df_C['m_c1'].max())
mo_c2_min, mo_c2_max = (df_C['m_c2'].min(), df_C['m_c2'].max())
mo_c3_min, mo_c3_max = (df_C['m_c3'].min(), df_C['m_c3'].max())
mo_d1_min, mo_d1_max = (df_D['m_d1'].min(), df_D['m_d1'].max())
mo_d2_min, mo_d2_max = (df_D['m_d2'].min(), df_D['m_d2'].max())
mo_d3_min, mo_d3_max = (df_D['m_d3'].min(), df_D['m_d3'].max())
mo_e1_min, mo_e1_max = (df_E['m_e1'].min(), df_E['m_e1'].max())
mo_e2_min, mo_e2_max = (df_E['m_e2'].min(), df_E['m_e2'].max())
mo_e3_min, mo_e3_max = (df_E['m_e3'].min(), df_E['m_e3'].max())

""" Convert GWC to VWC """
# VWC = GWC*DD/WD (DD is dry density, WD is water density)

water_density = 1000 # kg/m3
# depth_basinA_m = 0.098 # m
# depth_basinB_m = 0.088 # m
# depth_basinC_m = 0.089 # m
# depth_basinD_m = 0.085 # m
# depth_basinE_m = 0.094 # m
depth_basinA_m = 0.1 # m
depth_basinB_m = 0.1 # m
depth_basinC_m = 0.1 # m
depth_basinD_m = 0.1 # m
depth_basinE_m = 0.1 # m


df_A['total_volume'] = area_basin_m2*depth_basinA_m  # assume volume does not change
df_A['VWC_A'] = df_A['GWC_A']*(SC_A*initial_weight_A/1000/df_A['total_volume'])/water_density
df_B['total_volume'] = area_basin_m2*depth_basinB_m  # assume volume does not change
df_B['VWC_B'] = df_B['GWC_B']*(SC_B*initial_weight_B/1000/df_B['total_volume'])/water_density
df_C['total_volume'] = area_basin_m2*depth_basinC_m  # assume volume does not change
df_C['VWC_C'] = df_C['GWC_C']*(SC_C*initial_weight_C/1000/df_C['total_volume'])/water_density
df_D['total_volume'] = area_basin_m2*depth_basinD_m  # assume volume does not change
df_D['VWC_D'] = df_D['GWC_D']*(SC_D*initial_weight_D/1000/df_D['total_volume'])/water_density
df_E['total_volume'] = area_basin_m2*depth_basinE_m  # assume volume does not change
df_E['VWC_E'] = df_E['GWC_E']*(SC_E*initial_weight_E/1000/df_E['total_volume'])/water_density

""" Convert VWC to DoS """
# VWC = DoS * n
# DoS = GWC*DD/WD/n
# n = 1- rho(bulk)/rho(grain)
df_A['porosity'] = 1 - (initial_weight_A/df_A['total_volume']/1000)/(SG_A*1000)
df_A['DoS_A'] = df_A['GWC_A']*(SC_A*initial_weight_A/1000/df_A['total_volume'])/water_density/df_A['porosity']
df_B['porosity'] = 1 - (initial_weight_B/df_B['total_volume']/1000)/(SG_B*1000)
df_B['DoS_B'] = df_B['GWC_B']*(SC_B*initial_weight_B/1000/df_B['total_volume'])/water_density/df_B['porosity']
df_C['porosity'] = 1 - (initial_weight_C/df_C['total_volume']/1000)/(SG_C*1000)
df_C['DoS_C'] = df_C['GWC_C']*(SC_C*initial_weight_C/1000/df_C['total_volume'])/water_density/df_C['porosity']
df_D['porosity'] = 1 - (initial_weight_D/df_D['total_volume']/1000)/(SG_D*1000)
df_D['DoS_D'] = df_D['GWC_D']*(SC_D*initial_weight_D/1000/df_D['total_volume'])/water_density/df_D['porosity']
df_E['porosity'] = 1 - (initial_weight_E/df_E['total_volume']/1000)/(SG_E*1000)
df_E['DoS_E'] = df_E['GWC_E']*(SC_E*initial_weight_E/1000/df_E['total_volume'])/water_density/df_E['porosity']

""" Normalize data """
df_A['m_a1_norm'] = (df_A['m_a1']-mo_a1_min)/(mo_a1_max-mo_a1_min)
df_A['m_a2_norm'] = (df_A['m_a2']-mo_a2_min)/(mo_a2_max-mo_a2_min)
df_A['m_a3_norm'] = (df_A['m_a3']-mo_a3_min)/(mo_a3_max-mo_a3_min)
df_B['m_b1_norm'] = (df_B['m_b1']-mo_b1_min)/(mo_b1_max-mo_b1_min)
df_B['m_b2_norm'] = (df_B['m_b2']-mo_b2_min)/(mo_b2_max-mo_b2_min)
df_B['m_b3_norm'] = (df_B['m_b3']-mo_b3_min)/(mo_b3_max-mo_b3_min)
df_C['m_c1_norm'] = (df_C['m_c1']-mo_c1_min)/(mo_c1_max-mo_c1_min)
df_C['m_c2_norm'] = (df_C['m_c2']-mo_c2_min)/(mo_c2_max-mo_c2_min)
df_C['m_c3_norm'] = (df_C['m_c3']-mo_c3_min)/(mo_c3_max-mo_c3_min)
df_D['m_d1_norm'] = (df_D['m_d1']-mo_d1_min)/(mo_d1_max-mo_d1_min)
df_D['m_d2_norm'] = (df_D['m_d2']-mo_d2_min)/(mo_d2_max-mo_d2_min)
df_D['m_d3_norm'] = (df_D['m_d3']-mo_d3_min)/(mo_d3_max-mo_d3_min)
df_E['m_e1_norm'] = (df_E['m_e1']-mo_e1_min)/(mo_e1_max-mo_e1_min)
df_E['m_e2_norm'] = (df_E['m_e2']-mo_e2_min)/(mo_e2_max-mo_e2_min)
df_E['m_e3_norm'] = (df_E['m_e3']-mo_e3_min)/(mo_e3_max-mo_e3_min)

""" Moisture Sensor fitting parameters """
# Method 1 - exponential 
# l, m and n
# y = l*(x**m) + n
# (l_a1, m_a1, n_a1) = (0.5, 0.4, 0.0)
# (l_a2, m_a2, n_a2) = (0.5, 0.3, 0.0) # best
# (l_a3, m_a3, n_a3) = (0.4, 0.3, 0.0)

# (l_b1, m_b1, n_b1) = (0.5, 0.5, 0.1) 
# (l_b2, m_b2, n_b2) = (0.5, 0.2, 0.0) # best
# (l_b3, m_b3, n_b3) = (0.6, 0.4, 0.0)

# (l_c1, m_c1, n_c1) = (0.5, 0.3, 0.0) # best
# (l_c2, m_c2, n_c2) = (0.5, 0.4, 0.0)  
# (l_c3, m_c3, n_c3) = (0.6, 0.4, 0.0)

# (l_d1, m_d1, n_d1) = (0.45, 0.3, 0.0)
# (l_d2, m_d2, n_d2) = (0.35, 0.3, 0.1)
# (l_d3, m_d3, n_d3) = (0.45, 0.7, 0.0) # best

# (l_e1, m_e1, n_e1) = (0.6, 0.5, 0.0) 
# (l_e2, m_e2, n_e2) = (0.6, 0.4, 0.0) # best
# (l_e3, m_e3, n_e3) = (0.6, 0.3, 0.0) 

# curve_label_a1 = "y="+f"{l_a1}"+"x$^{%s}$+" % m_a1 +f"{n_a1}"
# curve_label_a2 = "y="+f"{l_a2}"+"x$^{%s}$+" % m_a2 +f"{n_a2}"
# curve_label_a3 = "y="+f"{l_a3}"+"x$^{%s}$+" % m_a3 +f"{n_a3}"
# curve_label_b1 = "y="+f"{l_b1}"+"x$^{%s}$+" % m_b1 +f"{n_b1}"
# curve_label_b2 = "y="+f"{l_b2}"+"x$^{%s}$+" % m_b2 +f"{n_b2}"
# curve_label_b3 = "y="+f"{l_b3}"+"x$^{%s}$+" % m_b3 +f"{n_b3}"
# curve_label_c1 = "y="+f"{l_c1}"+"x$^{%s}$+" % m_c1 +f"{n_c1}"
# curve_label_c2 = "y="+f"{l_c2}"+"x$^{%s}$+" % m_c2 +f"{n_c2}"
# curve_label_c3 = "y="+f"{l_c3}"+"x$^{%s}$+" % m_c3 +f"{n_c3}"
# curve_label_d1 = "y="+f"{l_d1}"+"x$^{%s}$+" % m_d1 +f"{n_d1}"
# curve_label_d2 = "y="+f"{l_d2}"+"x$^{%s}$+" % m_d2 +f"{n_d2}"
# curve_label_d3 = "y="+f"{l_d3}"+"x$^{%s}$+" % m_d3 +f"{n_d3}"
# curve_label_e1 = "y="+f"{l_e1}"+"x$^{%s}$+" % m_e1 +f"{n_e1}"
# curve_label_e2 = "y="+f"{l_e2}"+"x$^{%s}$+" % m_e2 +f"{n_e2}"
# curve_label_e3 = "y="+f"{l_e3}"+"x$^{%s}$+" % m_e3 +f"{n_e3}"

# Method 2 - linear 
# m and n
# y = mx+n
(m_a1, n_a1) = (0.003, -0.35)
(m_a2, n_a2) = (0.003, -0.35) # best
(m_a3, n_a3) = (0.003, -0.35)

(m_b1, n_b1) = (0.0027, -0.2) 
(m_b2, n_b2) = (0.0027, -0.2) # best
(m_b3, n_b3) = (0.0027, -0.2)

(m_c1, n_c1) = (0.0027, -0.2) # best
(m_c2, n_c2) = (0.0027, -0.2)  
(m_c3, n_c3) = (0.0027, -0.2)

(m_d1, n_d1) = (0.0028, -0.275)
(m_d2, n_d2) = (0.0028, -0.275)
(m_d3, n_d3) = (0.0028, -0.275) # best

(m_e1, n_e1) = (0.0046, -1.05) 
(m_e2, n_e2) = (0.0046, -1.05) # best
(m_e3, n_e3) = (0.0046, -1.05) 

curve_label_a1 = f"y={m_a1}x+{n_a1}"
curve_label_a2 = f"y={m_a2}x+{n_a2}"
curve_label_a3 = f"y={m_a3}x+{n_a3}"
curve_label_b1 = f"y={m_b1}x+{n_b1}"
curve_label_b2 = f"y={m_b2}x+{n_b2}"
curve_label_b3 = f"y={m_b3}x+{n_b3}"
curve_label_c1 = f"y={m_c1}x+{n_c1}"
curve_label_c2 = f"y={m_c2}x+{n_c2}"
curve_label_c3 = f"y={m_c3}x+{n_c3}"
curve_label_d1 = f"y={m_d1}x+{n_d1}"
curve_label_d2 = f"y={m_d2}x+{n_d2}"
curve_label_d3 = f"y={m_d3}x+{n_d3}"
curve_label_e1 = f"y={m_e1}x+{n_e1}"
curve_label_e2 = f"y={m_e2}x+{n_e2}"
curve_label_e3 = f"y={m_e3}x+{n_e3}"

# df_A['VWC_a1_cali'] = l_a1*(df_A['m_a1_norm']**m_a1)+n_a1
# df_A['VWC_a2_cali'] = l_a2*(df_A['m_a2_norm']**m_a2)+n_a2
# df_A['VWC_a3_cali'] = l_a3*(df_A['m_a3_norm']**m_a3)+n_a3
# df_B['VWC_b1_cali'] = l_b1*(df_B['m_b1_norm']**m_b1)+n_b1
# df_B['VWC_b2_cali'] = l_b2*(df_B['m_b2_norm']**m_b2)+n_b2
# df_B['VWC_b3_cali'] = l_b3*(df_B['m_b3_norm']**m_b3)+n_b3
# df_C['VWC_c1_cali'] = l_c1*(df_C['m_c1_norm']**m_c1)+n_c1
# df_C['VWC_c2_cali'] = l_c2*(df_C['m_c2_norm']**m_c2)+n_c2
# df_C['VWC_c3_cali'] = l_c3*(df_C['m_c3_norm']**m_c3)+n_c3
# df_D['VWC_d1_cali'] = l_d1*(df_D['m_d1_norm']**m_d1)+n_d1
# df_D['VWC_d2_cali'] = l_d2*(df_D['m_d2_norm']**m_d2)+n_d2
# df_D['VWC_d3_cali'] = l_d3*(df_D['m_d3_norm']**m_d3)+n_d3
# df_E['VWC_e1_cali'] = l_e1*(df_E['m_e1_norm']**m_e1)+n_e1
# df_E['VWC_e2_cali'] = l_e2*(df_E['m_e2_norm']**m_e2)+n_e2
# df_E['VWC_e3_cali'] = l_e3*(df_E['m_e3_norm']**m_e3)+n_e3

df_A['DoS_a2_cali'] = m_a2*df_A['m_a2']+n_a2
df_B['DoS_b1_cali'] = m_b1*df_B['m_b1']+n_b1
df_C['DoS_c3_cali'] = m_c3*df_C['m_c3']+n_c3
df_D['DoS_d3_cali'] = m_d3*df_D['m_d3']+n_d3
df_E['DoS_e2_cali'] = m_e2*df_E['m_e2']+n_e2

k = 80
ax[0].plot(df_A['m_a1'][::k], df_A['DoS_A'][::k],   '^', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='MO1-Experiment')
ax[0].plot(df_A['m_a2'][::k], df_A['DoS_A'][::k],   '8', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='MO2-Experiment')
ax[0].plot(df_A['m_a3'][::k], df_A['DoS_A'][::k],   's', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label='MO3-Experiment')
ax[0].plot(df_A['m_a2'],      df_A['DoS_a2_cali'], '--', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label=curve_label_a2)

ax[1].plot(df_B['m_b1'][::k], df_B['DoS_B'][::k],  '^', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='MO1-Experiment')
ax[1].plot(df_B['m_b2'][::k], df_B['DoS_B'][::k],  '8', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='MO2-Experiment')
ax[1].plot(df_B['m_b3'][::k], df_B['DoS_B'][::k],  's', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label='MO3-Experiment')
ax[1].plot(df_B['m_b1'],      df_B['DoS_b1_cali'], '--', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label=curve_label_b1)

ax[2].plot(df_C['m_c1'][::k], df_C['DoS_C'][::k],  '^', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='MO1-Experiment')
ax[2].plot(df_C['m_c2'][::k], df_C['DoS_C'][::k],  '8', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='MO2-Experiment')
ax[2].plot(df_C['m_c3'][::k], df_C['DoS_C'][::k],  's', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label='MO3-Experiment')
ax[2].plot(df_C['m_c3'],      df_C['DoS_c3_cali'], '--', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label=curve_label_c3)

ax[3].plot(df_D['m_d1'][::k], df_D['DoS_D'][::k],  '^', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='MO1-Experiment')
ax[3].plot(df_D['m_d2'][::k], df_D['DoS_D'][::k],  '8', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='MO2-Experiment')
ax[3].plot(df_D['m_d3'][::k], df_D['DoS_D'][::k],  's', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label='MO3-Experiment')
ax[3].plot(df_D['m_d3'],      df_D['DoS_d3_cali'], '--', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label=curve_label_d3)

ax[4].plot(df_E['m_e1'][::k], df_E['DoS_E'][::k],  '^', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='MO1-Experiment')
ax[4].plot(df_E['m_e2'][::k], df_E['DoS_E'][::k],  '8', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='MO2-Experiment')
ax[4].plot(df_E['m_e3'][::k], df_E['DoS_E'][::k],  's', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label='MO3-Experiment')
ax[4].plot(df_E['m_e2'],      df_E['DoS_e2_cali'], '--', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label=curve_label_e2)

""" Suction Sensor Calibration"""
# suction sensor upper and lower bounds
su_a1_min, su_a1_max = (df_A['delta_t_sa1'].min(), df_A['delta_t_sa1'].max())
su_a2_min, su_a2_max = (df_A['delta_t_sa2'].min(), df_A['delta_t_sa2'].max())
su_b1_min, su_b1_max = (df_B['delta_t_sb1'].min(), df_B['delta_t_sb1'].max())
su_b2_min, su_b2_max = (df_B['delta_t_sb2'].min(), df_B['delta_t_sb2'].max())
su_c1_min, su_c1_max = (df_C['delta_t_sc1'].min(), df_C['delta_t_sc1'].max())
su_c2_min, su_c2_max = (df_C['delta_t_sc2'].min(), df_C['delta_t_sc2'].max())
su_d1_min, su_d1_max = (df_D['delta_t_sd1'].min(), df_D['delta_t_sd1'].max())
su_d2_min, su_d2_max = (df_D['delta_t_sd2'].min(), df_D['delta_t_sd2'].max())
su_e1_min, su_e1_max = (df_E['delta_t_se1'].min(), df_E['delta_t_se1'].max())
su_e2_min, su_e2_max = (df_E['delta_t_se2'].min(), df_E['delta_t_se2'].max())

# normalize suction data
df_A['delta_t_sa1_norm'] = (df_A['delta_t_sa1']-su_a1_min)/(su_a1_max-su_a1_min)
df_A['delta_t_sa2_norm'] = (df_A['delta_t_sa2']-su_a2_min)/(su_a2_max-su_a2_min)
df_B['delta_t_sb1_norm'] = (df_B['delta_t_sb1']-su_b1_min)/(su_b1_max-su_b1_min)
df_B['delta_t_sb2_norm'] = (df_B['delta_t_sb2']-su_b2_min)/(su_b2_max-su_b2_min)
df_C['delta_t_sc1_norm'] = (df_C['delta_t_sc1']-su_c1_min)/(su_c1_max-su_c1_min)
df_C['delta_t_sc2_norm'] = (df_C['delta_t_sc2']-su_c2_min)/(su_c2_max-su_c2_min)
df_D['delta_t_sd1_norm'] = (df_D['delta_t_sd1']-su_d1_min)/(su_d1_max-su_d1_min)
df_D['delta_t_sd2_norm'] = (df_D['delta_t_sd2']-su_d2_min)/(su_d2_max-su_d2_min)
df_E['delta_t_se1_norm'] = (df_E['delta_t_se1']-su_e1_min)/(su_e1_max-su_e1_min)
df_E['delta_t_se2_norm'] = (df_E['delta_t_se2']-su_e2_min)/(su_e2_max-su_e2_min)

# SWCC curve fitting
# For Basin A,B,C,D
nf_1 = 0.9311
af_1 = 2.7090
mf_1 = 0.1229
hr_1 = 238968
por_1 = 0.5  # equals to saturated VWC
residual_1 = 0.03

# For Basin E
nf_2 = 0.9311
af_2 = 2.7090
mf_2 = 0.1229
hr_2 = 238968
por_2 = 0.5  # equals to saturated VWC
residual_2 = 0.03

# por=0.5,nf=0.9311,mf=0.1229,hr=238968.16,af=2.7090
# vwc_cali = np.arange(0,100)/100
# calculated_suction = lambda x: swcc_reverse_fredlund_xing_1994(nf = nf_1,
#                                                                 mf = mf_1,
#                                                                 af = af_1,
#                                                                 hr = hr_1,
#                                                                 por = por_1,
#                                                                 vwc = x)
# calculated_suction = np.array([calculated_suction(i) for i in vwc_cali])
# plt.semilogy(vwc_cali, calculated_suction)

df_A['suction_sa1_swcc'] = df_A['VWC_A'].apply(lambda x : swcc_reverse_fredlund_xing_1994(nf  = nf_1,
                                                                                          mf  = mf_1,
                                                                                          af  = af_1,
                                                                                          hr  = hr_1,
                                                                                          por = por_1,
                                                                                          vwc = x))
df_A['suction_sa2_swcc'] = df_A['VWC_A'].apply(lambda x : swcc_reverse_fredlund_xing_1994(nf  = nf_1,
                                                                                          mf  = mf_1,
                                                                                          af  = af_1,
                                                                                          hr  = hr_1,
                                                                                          por = por_1,
                                                                                          vwc = x))
df_B['suction_sb1_swcc'] = df_B['VWC_B'].apply(lambda x : swcc_reverse_fredlund_xing_1994(nf  = nf_1,
                                                                                          mf  = mf_1,
                                                                                          af  = af_1,
                                                                                          hr  = hr_1,
                                                                                          por = por_1,
                                                                                          vwc = x))
df_B['suction_sb2_swcc'] = df_B['VWC_B'].apply(lambda x : swcc_reverse_fredlund_xing_1994(nf  = nf_1,
                                                                                          mf  = mf_1,
                                                                                          af  = af_1,
                                                                                          hr  = hr_1,
                                                                                          por = por_1,
                                                                                          vwc = x))
df_C['suction_sc1_swcc'] = df_C['VWC_C'].apply(lambda x : swcc_reverse_fredlund_xing_1994(nf  = nf_1,
                                                                                          mf  = mf_1,
                                                                                          af  = af_1,
                                                                                          hr  = hr_1,
                                                                                          por = por_1,
                                                                                          vwc = x))
df_C['suction_sc2_swcc'] = df_C['VWC_C'].apply(lambda x : swcc_reverse_fredlund_xing_1994(nf  = nf_1,
                                                                                          mf  = mf_1,
                                                                                          af  = af_1,
                                                                                          hr  = hr_1,
                                                                                          por = por_1,
                                                                                          vwc = x))
df_D['suction_sd1_swcc'] = df_D['VWC_D'].apply(lambda x : swcc_reverse_fredlund_xing_1994(nf  = nf_1,
                                                                                          mf  = mf_1,
                                                                                          af  = af_1,
                                                                                          hr  = hr_1,
                                                                                          por = por_1,
                                                                                          vwc = x))
df_D['suction_sd2_swcc'] = df_D['VWC_D'].apply(lambda x : swcc_reverse_fredlund_xing_1994(nf  = nf_1,
                                                                                          mf  = mf_1,
                                                                                          af  = af_1,
                                                                                          hr  = hr_1,
                                                                                          por = por_1,
                                                                                          vwc = x))

df_E['suction_se1_swcc'] = df_E['VWC_E'].apply(lambda x : swcc_reverse_fredlund_xing_1994(nf  = nf_2,
                                                                                          mf  = mf_2,
                                                                                          af  = af_2,
                                                                                          hr  = hr_2,
                                                                                          por = por_2,
                                                                                          vwc = x))
df_E['suction_se2_swcc'] = df_E['VWC_E'].apply(lambda x : swcc_reverse_fredlund_xing_1994(nf  = nf_2,
                                                                                          mf  = mf_2,
                                                                                          af  = af_2,
                                                                                          hr  = hr_2,
                                                                                          por = por_2,
                                                                                          vwc = x))

# labels
curve_label_swcc_sa1 = 'SU1-Fredlund_Xing'
curve_label_swcc_sa2 = 'SU2-Fredlund_Xing'
curve_label_swcc_sb1 = 'SU1-Fredlund_Xing'
curve_label_swcc_sb2 = 'SU2-Fredlund_Xing'
curve_label_swcc_sc1 = 'SU1-Fredlund_Xing'
curve_label_swcc_sc2 = 'SU2-Fredlund_Xing'
curve_label_swcc_sd1 = 'SU1-Fredlund_Xing'
curve_label_swcc_sd2 = 'SU2-Fredlund_Xing'
curve_label_swcc_se1 = 'SU1-Fredlund_Xing'
curve_label_swcc_se2 = 'SU2-Fredlund_Xing'

(alpha_A, beta_A) = (21,-7)
(alpha_B, beta_B) = (21,-7)
(alpha_C, beta_C) = (24,-7)
(alpha_D, beta_D) = (16,-2)
(alpha_E, beta_E) = (48,-32)

df_A['suction_sa1_cali'] = np.exp(alpha_A*df_A['delta_t_sa1_norm']+beta_A)
df_A['suction_sa2_cali'] = np.exp(alpha_A*df_A['delta_t_sa2_norm']+beta_A)
df_B['suction_sb1_cali'] = np.exp(alpha_B*df_B['delta_t_sb1_norm']+beta_B)
df_B['suction_sb2_cali'] = np.exp(alpha_B*df_B['delta_t_sb2_norm']+beta_B)
df_C['suction_sc1_cali'] = np.exp(alpha_C*df_C['delta_t_sc1_norm']+beta_C)
df_C['suction_sc2_cali'] = np.exp(alpha_C*df_C['delta_t_sc2_norm']+beta_C)
df_D['suction_sd1_cali'] = np.exp(alpha_D*df_D['delta_t_sd1_norm']+beta_D)
df_D['suction_sd2_cali'] = np.exp(alpha_D*df_D['delta_t_sd2_norm']+beta_D)
df_E['suction_se1_cali'] = np.exp(alpha_E*df_E['delta_t_se1_norm']+beta_E)
df_E['suction_se2_cali'] = np.exp(alpha_E*df_E['delta_t_se2_norm']+beta_E)

curve_label_cali_sa1 = "y="+"e$^{%sx%s}$" % (alpha_A, beta_A) 
curve_label_cali_sb1 = "y="+"e$^{%sx%s}$" % (alpha_B, beta_B)
curve_label_cali_sc1 = "y="+"e$^{%sx%s}$" % (alpha_C, beta_C)
curve_label_cali_sd1 = "y="+"e$^{%sx+%s}$" % (alpha_D, beta_D)
curve_label_cali_se1 = "y="+"e$^{%sx%s}$" % (alpha_E, beta_E)

k = 80
ax[5].plot(df_A['delta_t_sa1_norm'][::k], df_A['VWC_A'][::k],  '^', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='SU1-Experiment')
ax[5].plot(df_A['delta_t_sa2_norm'][::k], df_A['VWC_A'][::k],  '8', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='SU2-Experiment')
ax[6].plot(df_B['delta_t_sb1_norm'][::k], df_B['VWC_B'][::k],  '^', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='SU1-Experiment')
ax[6].plot(df_B['delta_t_sb2_norm'][::k], df_B['VWC_B'][::k],  '8', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='SU2-Experiment')
ax[7].plot(df_C['delta_t_sc1_norm'][::k], df_C['VWC_C'][::k],  '^', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='SU1-Experiment')
ax[7].plot(df_C['delta_t_sc2_norm'][::k], df_C['VWC_C'][::k],  '8', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='SU2-Experiment')
ax[8].plot(df_D['delta_t_sd1_norm'][::k], df_D['VWC_D'][::k],  '^', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='SU1-Experiment')
ax[8].plot(df_D['delta_t_sd2_norm'][::k], df_D['VWC_D'][::k],  '8', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='SU2-Experiment')
ax[9].plot(df_E['delta_t_se1_norm'][::k], df_E['VWC_E'][::k],  '^', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='SU1-Experiment')
ax[9].plot(df_E['delta_t_se2_norm'][::k], df_E['VWC_E'][::k],  '8', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='SU2-Experiment')
ax[10].semilogy(df_A['delta_t_sa1_norm'], df_A['suction_sa1_swcc'], '^', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label=curve_label_swcc_sa1)
ax[10].semilogy(df_A['delta_t_sa2_norm'], df_A['suction_sa2_swcc'], 's', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label=curve_label_swcc_sa2)
ax[10].semilogy(df_A['delta_t_sa1_norm'], df_A['suction_sa1_cali'], '--', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label=curve_label_cali_sa1)

ax[11].semilogy(df_B['delta_t_sb1_norm'], df_B['suction_sb1_swcc'], '^', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label=curve_label_swcc_sb1)
ax[11].semilogy(df_B['delta_t_sb2_norm'], df_B['suction_sb2_swcc'], 's', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label=curve_label_swcc_sb2)
ax[11].semilogy(df_B['delta_t_sb1_norm'], df_B['suction_sb1_cali'], '--', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label=curve_label_cali_sb1)

ax[12].semilogy(df_C['delta_t_sc1_norm'], df_C['suction_sc1_swcc'], '^', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label=curve_label_swcc_sc1)
ax[12].semilogy(df_C['delta_t_sc2_norm'], df_C['suction_sc2_swcc'], 's', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label=curve_label_swcc_sc2)
ax[12].semilogy(df_C['delta_t_sc1_norm'], df_C['suction_sc1_cali'], '--', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label=curve_label_cali_sc1)

ax[13].semilogy(df_D['delta_t_sd1_norm'], df_D['suction_sd1_swcc'], '^', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label=curve_label_swcc_sd1)
ax[13].semilogy(df_D['delta_t_sd2_norm'], df_D['suction_sd2_swcc'], 's', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label=curve_label_swcc_sd2)
ax[13].semilogy(df_D['delta_t_sd1_norm'], df_D['suction_sd1_cali'], '--', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label=curve_label_cali_sd1)

ax[14].semilogy(df_E['delta_t_se1_norm'], df_E['suction_se1_swcc'], '^', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label=curve_label_swcc_se1)
ax[14].semilogy(df_E['delta_t_se2_norm'], df_E['suction_se2_swcc'], 's', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label=curve_label_swcc_se2)
ax[14].semilogy(df_E['delta_t_se1_norm'], df_E['suction_se1_cali'], '--', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label=curve_label_cali_se1)


# """--------------Detailed Configurations--------------------------------"""
#----------------Bold the border of each subplot---------------------------
for i in ax:
    for axis in ['top','bottom','left','right']:
        i.spines[axis].set_linewidth(2)
            
    #----------------Set limits for x-axis--------------------------
    
    ax[0].set_xlim([100, 450])
    ax[1].set_xlim([100, 450])
    ax[2].set_xlim([100, 450])
    ax[3].set_xlim([100, 450])
    ax[4].set_xlim([100, 450])
    ax[5].set_xlim([0, 1])
    ax[6].set_xlim([0, 1])
    ax[7].set_xlim([0, 1])
    ax[8].set_xlim([0, 1])
    ax[9].set_xlim([0, 1])
    ax[10].set_xlim([0, 1])
    ax[11].set_xlim([0, 1])
    ax[12].set_xlim([0, 1])
    ax[13].set_xlim([0, 1])
    ax[14].set_xlim([0, 1])
        
    #----------------Set limits for y-axis--------------------------

    ax[0].set_ylim([-0.05, 1.05])
    ax[1].set_ylim([-0.05, 1.05])
    ax[2].set_ylim([-0.05, 1.05])
    ax[3].set_ylim([-0.05, 1.05])
    ax[4].set_ylim([-0.05, 1.05])
    ax[5].set_ylim([0, 0.6])
    ax[6].set_ylim([0, 0.6])
    ax[7].set_ylim([0, 0.6])
    ax[8].set_ylim([0, 0.6])
    ax[9].set_ylim([0, 0.8])
    ax[10].set_ylim([1, 1e6])
    ax[11].set_ylim([1, 1e6])
    ax[12].set_ylim([1, 1e6])
    ax[13].set_ylim([1, 1e6])
    ax[14].set_ylim([1, 1e6])
    
    
    #---------------Set labels for x-axis--------------------------------------
    
    ax[0].set_xlabel('MO. READING', fontsize=label_fontsize,labelpad=3)
    ax[1].set_xlabel('MO. READING', fontsize=label_fontsize,labelpad=3)
    ax[2].set_xlabel('MO. READING', fontsize=label_fontsize,labelpad=3)
    ax[3].set_xlabel('MO. READING', fontsize=label_fontsize,labelpad=3)
    ax[4].set_xlabel('MO. READING', fontsize=label_fontsize,labelpad=3)
    
    ax[5].set_xlabel('NORM. SU. READING', fontsize=label_fontsize,labelpad=3)
    ax[6].set_xlabel('NORM. SU. READING', fontsize=label_fontsize,labelpad=3)
    ax[7].set_xlabel('NORM. SU. READING', fontsize=label_fontsize,labelpad=3)
    ax[8].set_xlabel('NORM. SU. READING', fontsize=label_fontsize,labelpad=3)
    ax[9].set_xlabel('NORM. SU. READING', fontsize=label_fontsize,labelpad=3)
    
    ax[10].set_xlabel('NORM. SU. READING', fontsize=label_fontsize,labelpad=3)
    ax[11].set_xlabel('NORM. SU. READING', fontsize=label_fontsize,labelpad=3)
    ax[12].set_xlabel('NORM. SU. READING', fontsize=label_fontsize,labelpad=3)
    ax[13].set_xlabel('NORM. SU. READING', fontsize=label_fontsize,labelpad=3)
    ax[14].set_xlabel('NORM. SU. READING', fontsize=label_fontsize,labelpad=3)

    #---------------Set labels for x-axis--------------------------------------    
    
    ax[0].set_ylabel('DEGREE OF\nSATURATION', fontsize=label_fontsize, labelpad=5)  
    ax[5].set_ylabel('VOLUMETRIC WATER\nCONTENT', fontsize=label_fontsize, labelpad=5)
    ax[10].set_ylabel('MATRIC\nSUCTION (kPa)',    fontsize=label_fontsize, labelpad=5)

    #---------------Set ticks for x-axis and y-axis----------------------------
    
    # ax[0].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    # ax[1].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    # ax[2].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    # ax[3].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    # ax[4].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[5].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[6].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[7].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[8].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[9].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])  
    ax[10].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0]) 
    ax[11].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0]) 
    ax[12].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0]) 
    ax[13].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0]) 
    ax[14].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0]) 
    ax[0].set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[1].set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[2].set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[3].set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[4].set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    
    #---------------Set gridlines----------------------------------------------
    
    ax[0].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[1].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[2].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[3].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[4].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
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
    
    #---------------Set legends------------------------------------------------
    
    ax[0].legend(loc='best', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)    
    ax[1].legend(loc='best', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[2].legend(loc='best', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[3].legend(loc='lower right', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[4].legend(loc='best', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[5].legend(loc='best', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[6].legend(loc='best', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[7].legend(loc='best', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[8].legend(loc='lower left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[9].legend(loc='best', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[10].legend(loc='upper left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[11].legend(loc='upper left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[12].legend(loc='best', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[13].legend(loc='upper left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[14].legend(loc='best', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    
plt.show(block=False)
output_name = os.getcwd() + '_sensor_calibration.jpg'
fig.savefig(output_name, format='jpg', dpi=100, bbox_inches='tight', pad_inches=0.01 )