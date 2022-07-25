# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 17:03:16 2022

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
          'lines.linewidth':2}

pylab.rcParams.update(params)

lw=2
ms=4
mew=2
grid_width=2
label_fontsize=16
legend_fontsize=10

"""---------------Initialize the Figure and its sub-plots---------------"""
    
fig   = plt.figure(num='Calibration',figsize=(18,9))
ax    = [[] for i in range(20)]   # 20+5(plots with same x axis, i.e. secondary y-axis)
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
ax[10]  = plt.subplot2grid((4,5), (2, 0), colspan=1, rowspan=1)
ax[11]  = plt.subplot2grid((4,5), (2, 1), colspan=1, rowspan=1)
ax[12]  = plt.subplot2grid((4,5), (2, 2), colspan=1, rowspan=1)
ax[13]  = plt.subplot2grid((4,5), (2, 3), colspan=1, rowspan=1)
ax[14]  = plt.subplot2grid((4,5), (2, 4), colspan=1, rowspan=1)
ax[15]  = plt.subplot2grid((4,5), (3, 0), colspan=1, rowspan=1)
ax[16]  = plt.subplot2grid((4,5), (3, 1), colspan=1, rowspan=1)
ax[17]  = plt.subplot2grid((4,5), (3, 2), colspan=1, rowspan=1)
ax[18]  = plt.subplot2grid((4,5), (3, 3), colspan=1, rowspan=1)
ax[19]  = plt.subplot2grid((4,5), (3, 4), colspan=1, rowspan=1)

"""Select durations------------------------------------------------------------
start from the time sensors showed response (around liquid limit/DoS=1)-----"""

start_date_A = '2022-05-25 16:20:00'
end_date_A   = '2022-07-07 12:00:00'
duration_A   = (df_A['date_time'] > start_date_A) & (df_A['date_time'] <= end_date_A)

start_date_B = '2022-05-25 16:20:00'
end_date_B   = '2022-07-7 12:00:00'
duration_B   = (df_B['date_time'] > start_date_B) & (df_B['date_time'] <= end_date_B)

start_date_C = '2022-05-25 16:20:00'
end_date_C   = '2022-07-07 12:00:00'
duration_C   = (df_C['date_time'] > start_date_C) & (df_C['date_time'] <= end_date_C)

start_date_D = '2022-06-03 16:20:00'
end_date_D   = '2022-07-07 12:00:00'
duration_D   = (df_D['date_time'] > start_date_D) & (df_D['date_time'] <= end_date_D)

start_date_E = '2022-04-10 15:30:00'
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
depth_basinA_m = 0.1 # m
depth_basinB_m = 0.1 # m
depth_basinC_m = 0.1 # m
depth_basinD_m = 0.1 # m
depth_basinE_m = 0.1 # m

df_A['total_volume'] = area_basin_m2*depth_basinA_m  # assume volume does not change
df_A['VWC_A'] = df_A['GWC_A']*(0.424*initial_weight_A/1000/df_A['total_volume'])/water_density
df_B['total_volume'] = area_basin_m2*depth_basinB_m  # assume volume does not change
df_B['VWC_B'] = df_B['GWC_B']*(0.445*initial_weight_B/1000/df_B['total_volume'])/water_density
df_C['total_volume'] = area_basin_m2*depth_basinC_m  # assume volume does not change
df_C['VWC_C'] = df_C['GWC_C']*(0.460*initial_weight_C/1000/df_C['total_volume'])/water_density
df_D['total_volume'] = area_basin_m2*depth_basinD_m  # assume volume does not change
df_D['VWC_D'] = df_D['GWC_D']*(0.411*initial_weight_D/1000/df_D['total_volume'])/water_density
df_E['total_volume'] = area_basin_m2*depth_basinE_m  # assume volume does not change
df_E['VWC_E'] = df_E['GWC_E']*(0.448*initial_weight_E/1000/df_E['total_volume'])/water_density

""" Normalize data """
alpha = 1
df_A['m_a1_norm'] = (df_A['m_a1']**alpha-mo_a1_min**alpha)/(mo_a1_max**alpha-mo_a1_min**alpha)
df_A['m_a2_norm'] = (df_A['m_a2']**alpha-mo_a2_min**alpha)/(mo_a2_max**alpha-mo_a2_min**alpha)
df_A['m_a3_norm'] = (df_A['m_a3']**alpha-mo_a3_min**alpha)/(mo_a3_max**alpha-mo_a3_min**alpha)
df_B['m_b1_norm'] = (df_B['m_b1']**alpha-mo_b1_min**alpha)/(mo_b1_max**alpha-mo_b1_min**alpha)
df_B['m_b2_norm'] = (df_B['m_b2']**alpha-mo_b2_min**alpha)/(mo_b2_max**alpha-mo_b2_min**alpha)
df_B['m_b3_norm'] = (df_B['m_b3']**alpha-mo_b3_min**alpha)/(mo_b3_max**alpha-mo_b3_min**alpha)
df_C['m_c1_norm'] = (df_C['m_c1']**alpha-mo_c1_min**alpha)/(mo_c1_max**alpha-mo_c1_min**alpha)
df_C['m_c2_norm'] = (df_C['m_c2']**alpha-mo_c2_min**alpha)/(mo_c2_max**alpha-mo_c2_min**alpha)
df_C['m_c3_norm'] = (df_C['m_c3']**alpha-mo_c3_min**alpha)/(mo_c3_max**alpha-mo_c3_min**alpha)
df_D['m_d1_norm'] = (df_D['m_d1']**alpha-mo_d1_min**alpha)/(mo_d1_max**alpha-mo_d1_min**alpha)
df_D['m_d2_norm'] = (df_D['m_d2']**alpha-mo_d2_min**alpha)/(mo_d2_max**alpha-mo_d2_min**alpha)
df_D['m_d3_norm'] = (df_D['m_d3']**alpha-mo_d3_min**alpha)/(mo_d3_max**alpha-mo_d3_min**alpha)
df_E['m_e1_norm'] = (df_E['m_e1']**alpha-mo_e1_min**alpha)/(mo_e1_max**alpha-mo_e1_min**alpha)
df_E['m_e2_norm'] = (df_E['m_e2']**alpha-mo_e2_min**alpha)/(mo_e2_max**alpha-mo_e2_min**alpha)
df_E['m_e3_norm'] = (df_E['m_e3']**alpha-mo_e3_min**alpha)/(mo_e3_max**alpha-mo_e3_min**alpha)
""" Moisture Sensor fitting parameters """
# l, m and n
# y = l*(x**m) + n
(l_a1, m_a1, n_a1) = (0.3, 0.3, 0.1)
(l_a2, m_a2, n_a2) = (0.3, 0.2, 0.1)
(l_a3, m_a3, n_a3) = (0.3, 0.7, 0.1)

(l_b1, m_b1, n_b1) = (0.3, 0.1, 0.1) #done
(l_b2, m_b2, n_b2) = (0.3, 0.1, 0.1)
(l_b3, m_b3, n_b3) = (0.4, 0.1, 0.0)

(l_c1, m_c1, n_c1) = (0.4, 0.1, 0.0)
(l_c2, m_c2, n_c2) = (0.4, 0.1, 0.0)
(l_c3, m_c3, n_c3) = (0.4, 0.1, 0.0)

(l_d1, m_d1, n_d1) = (0.3, 0.3, 0.1)
(l_d2, m_d2, n_d2) = (0.3, 0.5, 0.1)
(l_d3, m_d3, n_d3) = (0.3, 0.7, 0.1)

(l_e1, m_e1, n_e1) = (0.2, 0.3, 0.1) #done
(l_e2, m_e2, n_e2) = (0.2, 0.3, 0.1)
(l_e3, m_e3, n_e3) = (0.2, 0.3, 0.1)

curve_label_a1 = "y="+f"{l_a1}"+"x$^{%s}$+" % m_a1 +f"{n_a1}"
curve_label_a2 = "y="+f"{l_a2}"+"x$^{%s}$+" % m_a2 +f"{n_a2}"
curve_label_a3 = "y="+f"{l_a3}"+"x$^{%s}$+" % m_a3 +f"{n_a3}"
curve_label_b1 = "y="+f"{l_b1}"+"x$^{%s}$+" % m_b1 +f"{n_b1}"
curve_label_b2 = "y="+f"{l_b2}"+"x$^{%s}$+" % m_b2 +f"{n_b2}"
curve_label_b3 = "y="+f"{l_b3}"+"x$^{%s}$+" % m_b3 +f"{n_b3}"
curve_label_c1 = "y="+f"{l_c1}"+"x$^{%s}$+" % m_c1 +f"{n_c1}"
curve_label_c2 = "y="+f"{l_c2}"+"x$^{%s}$+" % m_c2 +f"{n_c2}"
curve_label_c3 = "y="+f"{l_c3}"+"x$^{%s}$+" % m_c3 +f"{n_c3}"
curve_label_d1 = "y="+f"{l_d1}"+"x$^{%s}$+" % m_d1 +f"{n_d1}"
curve_label_d2 = "y="+f"{l_d2}"+"x$^{%s}$+" % m_d2 +f"{n_d2}"
curve_label_d3 = "y="+f"{l_d3}"+"x$^{%s}$+" % m_d3 +f"{n_d3}"
curve_label_e1 = "y="+f"{l_e1}"+"x$^{%s}$+" % m_e1 +f"{n_e1}"
curve_label_e2 = "y="+f"{l_e2}"+"x$^{%s}$+" % m_e2 +f"{n_e2}"
curve_label_e3 = "y="+f"{l_e3}"+"x$^{%s}$+" % m_e3 +f"{n_e3}"

df_A['VWC_a1_cali'] = l_a1*(df_A['m_a1_norm']**m_a1)+n_a1
df_A['VWC_a2_cali'] = l_a2*(df_A['m_a2_norm']**m_a2)+n_a2
df_A['VWC_a3_cali'] = l_a3*(df_A['m_a3_norm']**m_a3)+n_a3
df_B['VWC_b1_cali'] = l_b1*(df_B['m_b1_norm']**m_b1)+n_b1
df_B['VWC_b2_cali'] = l_b2*(df_B['m_b2_norm']**m_b2)+n_b2
df_B['VWC_b3_cali'] = l_b3*(df_B['m_b3_norm']**m_b3)+n_b3
df_C['VWC_c1_cali'] = l_c1*(df_C['m_c1_norm']**m_c1)+n_c1
df_C['VWC_c2_cali'] = l_c2*(df_C['m_c2_norm']**m_c2)+n_c2
df_C['VWC_c3_cali'] = l_c3*(df_C['m_c3_norm']**m_c3)+n_c3
df_D['VWC_d1_cali'] = l_d1*(df_D['m_d1_norm']**m_d1)+n_d1
df_D['VWC_d2_cali'] = l_d2*(df_D['m_d2_norm']**m_d2)+n_d2
df_D['VWC_d3_cali'] = l_d3*(df_D['m_d3_norm']**m_d3)+n_d3
df_E['VWC_e1_cali'] = l_e1*(df_E['m_e1_norm']**m_e1)+n_e1
df_E['VWC_e2_cali'] = l_e2*(df_E['m_e2_norm']**m_e2)+n_e2
df_E['VWC_e3_cali'] = l_e3*(df_E['m_e3_norm']**m_e3)+n_e3

ax[0].plot(df_A['m_a1'], df_A['VWC_A'], '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='MO1 - RAW')
ax[0].plot(df_A['m_a2'], df_A['VWC_A'], '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='MO2 - RAW')
ax[0].plot(df_A['m_a3'], df_A['VWC_A'], '-', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label='MO3 - RAW')
ax[1].plot(df_B['m_b1'], df_B['VWC_B'], '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='MO1 - RAW')
ax[1].plot(df_B['m_b2'], df_B['VWC_B'], '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='MO2 - RAW')
ax[1].plot(df_B['m_b3'], df_B['VWC_B'], '-', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label='MO3 - RAW')
ax[2].plot(df_C['m_c1'], df_C['VWC_C'], '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='MO1 - RAW')
ax[2].plot(df_C['m_c2'], df_C['VWC_C'], '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='MO2 - RAW')
ax[2].plot(df_C['m_c3'], df_C['VWC_C'], '-', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label='MO3 - RAW')
ax[3].plot(df_D['m_d1'], df_D['VWC_D'], '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='MO1 - RAW')
ax[3].plot(df_D['m_d2'], df_D['VWC_D'], '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='MO2 - RAW')
ax[3].plot(df_D['m_d3'], df_D['VWC_D'], '-', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label='MO3 - RAW')
ax[4].plot(df_E['m_e1'], df_E['VWC_E'], '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='MO1 - RAW')
ax[4].plot(df_E['m_e2'], df_E['VWC_E'], '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='MO2 - RAW')
ax[4].plot(df_E['m_e3'], df_E['VWC_E'], '-', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label='MO3 - RAW')

k = 1
ax[5].plot(df_A['m_a1_norm'][::k], df_A['VWC_A'][::k],  '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='MO1 - NORM.')
ax[5].plot(df_A['m_a2_norm'][::k], df_A['VWC_A'][::k],  '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='MO2 - NORM.')
ax[5].plot(df_A['m_a3_norm'][::k], df_A['VWC_A'][::k],  '-', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label='MO3 - NORM.')
ax[6].plot(df_B['m_b1_norm'][::k], df_B['VWC_B'][::k],  '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='MO1 - NORM.')
ax[6].plot(df_B['m_b2_norm'][::k], df_B['VWC_B'][::k],  '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='MO2 - NORM.')
ax[6].plot(df_B['m_b3_norm'][::k], df_B['VWC_B'][::k],  '-', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label='MO3 - NORM.')
ax[7].plot(df_C['m_c1_norm'][::k], df_C['VWC_C'][::k],  '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='MO1 - NORM.')
ax[7].plot(df_C['m_c2_norm'][::k], df_C['VWC_C'][::k],  '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='MO2 - NORM.')
ax[7].plot(df_C['m_c3_norm'][::k], df_C['VWC_C'][::k],  '-', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label='MO3 - NORM.')
ax[8].plot(df_D['m_d1_norm'][::k], df_D['VWC_D'][::k],  '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='MO1 - NORM.')
ax[8].plot(df_D['m_d2_norm'][::k], df_D['VWC_D'][::k],  '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='MO2 - NORM.')
ax[8].plot(df_D['m_d3_norm'][::k], df_D['VWC_D'][::k],  '-', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label='MO3 - NORM.')
ax[9].plot(df_E['m_e1_norm'][::k], df_E['VWC_E'][::k],  '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='MO1 - NORM.')
ax[9].plot(df_E['m_e2_norm'][::k], df_E['VWC_E'][::k],  '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='MO2 - NORM.')
ax[9].plot(df_E['m_e3_norm'][::k], df_E['VWC_E'][::k],  '-', color='y', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='y', label='MO3 - NORM.')

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

# labels
curve_label_swcc_sa1 = ''
curve_label_swcc_sa2 = ''
curve_label_swcc_sb1 = ''
curve_label_swcc_sb2 = ''
curve_label_swcc_sc1 = ''
curve_label_swcc_sc2 = ''
curve_label_swcc_sd1 = ''
curve_label_swcc_sd2 = ''
curve_label_swcc_se1 = ''
curve_label_swcc_se2 = ''

ax[10].plot(df_A['delta_t_sa1'], df_A['VWC_A'], '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='SU1 - RAW')
ax[10].plot(df_A['delta_t_sa2'], df_A['VWC_A'], '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='SU2 - RAW')
ax[11].plot(df_B['delta_t_sb1'], df_B['VWC_B'], '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='SU1 - RAW')
ax[11].plot(df_B['delta_t_sb2'], df_B['VWC_B'], '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='SU2 - RAW')
ax[12].plot(df_C['delta_t_sc1'], df_C['VWC_C'], '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='SU1 - RAW')
ax[12].plot(df_C['delta_t_sc2'], df_C['VWC_C'], '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='SU2 - RAW')
ax[13].plot(df_D['delta_t_sd1'], df_D['VWC_D'], '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='SU1 - RAW')
ax[13].plot(df_D['delta_t_sd2'], df_D['VWC_D'], '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='SU2 - RAW')
ax[14].plot(df_E['delta_t_se1'], df_E['VWC_E'], '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='SU1 - RAW')
ax[14].plot(df_E['delta_t_se2'], df_E['VWC_E'], '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='SU2 - RAW')
ax[15].plot(df_A['delta_t_sa1_norm'][::k], df_A['VWC_A'][::k],  '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='SU1 - NORM.')
ax[15].plot(df_A['delta_t_sa2_norm'][::k], df_A['VWC_A'][::k],  '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='SU2 - NORM.')
ax[16].plot(df_B['delta_t_sb1_norm'][::k], df_B['VWC_B'][::k],  '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='SU1 - NORM.')
ax[16].plot(df_B['delta_t_sb2_norm'][::k], df_B['VWC_B'][::k],  '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='SU2 - NORM.')
ax[17].plot(df_C['delta_t_sc1_norm'][::k], df_C['VWC_C'][::k],  '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='SU1 - NORM.')
ax[17].plot(df_C['delta_t_sc2_norm'][::k], df_C['VWC_C'][::k],  '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='SU2 - NORM.')
ax[18].plot(df_D['delta_t_sd1_norm'][::k], df_D['VWC_D'][::k],  '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='SU1 - NORM.')
ax[18].plot(df_D['delta_t_sd2_norm'][::k], df_D['VWC_D'][::k],  '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='SU2 - NORM.')
ax[19].plot(df_E['delta_t_se1_norm'][::k], df_E['VWC_E'][::k],  '-', color='b', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='b', label='SU1 - NORM.')
ax[19].plot(df_E['delta_t_se2_norm'][::k], df_E['VWC_E'][::k],  '-', color='r', markersize=ms, markeredgewidth=mew, fillstyle='full', markeredgecolor='r', label='SU2 - NORM.')

# """--------------Detailed Configurations--------------------------------"""
#----------------Bold the border of each subplot---------------------------
for i in ax:
    for axis in ['top','bottom','left','right']:
        i.spines[axis].set_linewidth(2)
            
    #----------------Set limits for x-axis--------------------------
    
    ax[0].set_xlim([150, 450])
    ax[1].set_xlim([150, 450])
    ax[2].set_xlim([150, 450])
    ax[3].set_xlim([150, 450])
    ax[4].set_xlim([150, 450])  
    ax[5].set_xlim([0, 1])
    ax[6].set_xlim([0, 1])
    ax[7].set_xlim([0, 1])
    ax[8].set_xlim([0, 1])
    ax[9].set_xlim([0, 1])
    ax[10].set_xlim([5, 14])
    ax[11].set_xlim([5, 14])
    ax[12].set_xlim([5, 14])
    ax[13].set_xlim([5, 14])
    ax[14].set_xlim([5, 14])
    ax[15].set_xlim([0, 1])
    ax[16].set_xlim([0, 1])
    ax[17].set_xlim([0, 1])
    ax[18].set_xlim([0, 1])
    ax[19].set_xlim([0, 1])
        
    #----------------Set limits for y-axis--------------------------

    ax[0].set_ylim([0, 0.8])
    ax[1].set_ylim([0, 0.8])
    ax[2].set_ylim([0, 0.8])
    ax[3].set_ylim([0, 0.8])
    ax[4].set_ylim([0, 0.8])
    ax[5].set_ylim([0, 0.8])
    ax[6].set_ylim([0, 0.8])
    ax[7].set_ylim([0, 0.8])
    ax[8].set_ylim([0, 0.8])
    ax[9].set_ylim([0, 0.8])
    ax[10].set_ylim([0, 0.8])
    ax[11].set_ylim([0, 0.8])
    ax[12].set_ylim([0, 0.8])
    ax[13].set_ylim([0, 0.8])
    ax[14].set_ylim([0, 0.8])
    ax[15].set_ylim([0, 0.8])
    ax[16].set_ylim([0, 0.8])
    ax[17].set_ylim([0, 0.8])
    ax[18].set_ylim([0, 0.8])
    ax[19].set_ylim([0, 0.8])
    
    #---------------Set labels for x-axis--------------------------------------
    
    # ax[0].set_xlabel('MO. READING', fontsize=label_fontsize,labelpad=3)
    # ax[1].set_xlabel('MO. READING', fontsize=label_fontsize,labelpad=3)
    # ax[2].set_xlabel('MO. READING', fontsize=label_fontsize,labelpad=3)
    # ax[3].set_xlabel('MO. READING', fontsize=label_fontsize,labelpad=3)
    # ax[4].set_xlabel('MO. READING', fontsize=label_fontsize,labelpad=3)
    # ax[5].set_xlabel('NORM. MO. READING', fontsize=label_fontsize,labelpad=3)
    # ax[6].set_xlabel('NORM. MO. READING', fontsize=label_fontsize,labelpad=3)
    # ax[7].set_xlabel('NORM. MO. READING', fontsize=label_fontsize,labelpad=3)
    # ax[8].set_xlabel('NORM. MO. READING', fontsize=label_fontsize,labelpad=3)
    # ax[9].set_xlabel('NORM. MO. READING', fontsize=label_fontsize,labelpad=3)
    # ax[10].set_xlabel('SU. READING', fontsize=label_fontsize,labelpad=3)
    # ax[11].set_xlabel('SU. READING', fontsize=label_fontsize,labelpad=3)
    # ax[12].set_xlabel('SU. READING', fontsize=label_fontsize,labelpad=3)
    # ax[13].set_xlabel('SU. READING', fontsize=label_fontsize,labelpad=3)
    # ax[14].set_xlabel('SU. READING', fontsize=label_fontsize,labelpad=3)
    ax[15].set_xlabel('SENSOR READING\nBASIN A (SP04)', fontsize=label_fontsize,labelpad=3)
    ax[16].set_xlabel('SENSOR READING\nBASIN B (SP06)', fontsize=label_fontsize,labelpad=3)
    ax[17].set_xlabel('SENSOR READING\nBASIN C (SP11)', fontsize=label_fontsize,labelpad=3)
    ax[18].set_xlabel('SENSOR READING\nBASIN D (SP09)', fontsize=label_fontsize,labelpad=3)
    ax[19].set_xlabel('SENSOR READING\nBASIN E (SP01)', fontsize=label_fontsize,labelpad=3)

    #---------------Set labels for x-axis--------------------------------------    

    ax[0].set_ylabel('VWC', fontsize=label_fontsize, labelpad=3)    
    ax[5].set_ylabel('VWC', fontsize=label_fontsize, labelpad=3)
    ax[10].set_ylabel('VWC', fontsize=label_fontsize, labelpad=3)  
    ax[15].set_ylabel('VWC', fontsize=label_fontsize, labelpad=3)    

    #---------------Set ticks for x-axis and y-axis----------------------------

    ax[0].set_xticks([150, 250, 350, 450])
    ax[1].set_xticks([150, 250, 350, 450])
    ax[2].set_xticks([150, 250, 350, 450])
    ax[3].set_xticks([150, 250, 350, 450])
    ax[4].set_xticks([150, 250, 350, 450])
    ax[5].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[6].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[7].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[8].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[9].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[10].set_xticks([6, 8, 10, 12, 14])
    ax[11].set_xticks([6, 8, 10, 12, 14])
    ax[12].set_xticks([6, 8, 10, 12, 14])
    ax[13].set_xticks([6, 8, 10, 12, 14])
    ax[14].set_xticks([6, 8, 10, 12, 14])
    ax[15].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[16].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[17].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[18].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[19].set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])

    ax[0].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[1].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[2].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[3].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[4].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[5].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[6].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[7].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[8].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[9].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[10].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[11].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[12].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[13].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[14].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[15].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[16].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[17].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[18].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax[19].set_yticks([0, 0.2, 0.4, 0.6, 0.8])

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
    ax[15].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[16].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[17].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[18].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')
    ax[19].grid(True, which="both", ls=":", linewidth=grid_width, color = '0.5')    
    #---------------Set legends------------------------------------------------
    ax[0].legend(loc='upper left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)    
    ax[1].legend(loc='upper left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[2].legend(loc='upper left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[3].legend(loc='upper left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[4].legend(loc='upper left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[5].legend(loc='upper left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)    
    ax[6].legend(loc='upper left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[7].legend(loc='upper left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[8].legend(loc='upper left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[9].legend(loc='upper left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[10].legend(loc='lower left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)    
    ax[11].legend(loc='lower left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[12].legend(loc='lower left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[13].legend(loc='lower left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[14].legend(loc='lower left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[15].legend(loc='lower left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[16].legend(loc='lower left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[17].legend(loc='lower left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[18].legend(loc='lower left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)
    ax[19].legend(loc='lower left', borderaxespad=0.8, fontsize=legend_fontsize, handletextpad=0.5, labelspacing=0.1, ncol=1, columnspacing=0.4)

plt.show(block=False)
output_name = os.getcwd() + '_sensor_normalized.jpg'
fig.savefig(output_name, format='jpg', dpi=100, bbox_inches='tight', pad_inches=0.05 )
















