#!/usr/bin/python
# this script reads all equipment from column grange_1, including sensors and weather stations, uv sensors. 
# mount specification: mega with ec5, eps2, ds18, loadcell, 
import serial
import time
import numpy as np
import sys
from phant import Phant
import serial_openlock
import get_ip
import csv_tools
from upload_phant import upload_phant



with open('/home/pi/script/pass/public_grange_ad_weather_nectar', 'r') as myfile:
    public_grange_ad_weather=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_grange_ad_weather_nectar', 'r') as myfile:
    private_grange_ad_weather=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')



field_name_weather=['aet','batt','dlyrainmm','ir_down','ir_up','lt','mo_soil','p','pet','rainmm','rh','tc','temp_soil','uv_down','uv_up','vis_down','vis_up','wddir','wddiravg2m','wdgstdir','wdgstdir10m','wdgstkph','wdgstkph10m','wdspdkph','wdspdkphavg2m','tp_box_6','tp_box_7','rh_box_6','rh_box_7','ip']
parsed_data_weather=dict((el,0.0) for el in field_name_weather)
pht_weather = Phant(publicKey=public_grange_ad_weather, fields=field_name_weather ,privateKey=private_grange_ad_weather,baseUrl=nectar_address)
port_weather = 'USB VID:PID=0403:6015 SNR=DN01J0QU'
#------------------------- below are definations for the weather station ---------------------------------

# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'weather_grange_ad_nectar.csv'

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)

#ard = serial.Serial(port,9600,timeout=None)
[opencondition,ard]=serial_openlock.open_port(port_weather)
# the first reading is dummy readings
msg = ard.readline()


while True: 
    
    # the first five ones are not going to post online, but it may be needed as the rain can be better monitored
    for i in range(7):
        msg_weather = ard.readline()
        # save to file
        time_now=time.strftime("%d/%b/%Y %H:%M:%S")
        if screen_display: print time_now+delimiter+msg_weather
        if save_to_file: fid.write(time_now+delimiter+msg_weather)
    

    #current_read_column=msg_column_file.split(',')[0:-1]

    #SaltRH_ind=[i for i,x in enumerate(current_read_column) if x == 'SaltRH']
    #for i in SaltRH_ind:
    #    parsed_data_weather['tp_box_'+current_read_column[i+1]]=float(current_read_column[i+2])
    #    parsed_data_weather['rh_box_'+current_read_column[i+1]]=float(current_read_column[i+3])

    #vis_ind=[i for i,x in enumerate(current_read_column) if x == 'Vis']
    #parsed_data_weather['vis_up']=float(current_read_column[vis_ind[0]+1])
    #parsed_data_weather['vis_down']=float(current_read_column[vis_ind[1]+1])

    #uv_ind=[i for i,x in enumerate(current_read_column) if x == 'UV']
    #parsed_data_weather['uv_up']=float(current_read_column[uv_ind[0]+1])
    #parsed_data_weather['uv_down']=float(current_read_column[uv_ind[1]+1])
    #
    #ir_ind=[i for i,x in enumerate(current_read_column) if x == 'IR']
    #parsed_data_weather['ir_up']=float(current_read_column[ir_ind[0]+1])
    #parsed_data_weather['ir_down']=float(current_read_column[ir_ind[1]+1])
    
    # read from arduino
    msg_weather = ard.readline()
    current_read=msg_weather.split(',')[1:-1]
    for i,key in enumerate(current_read[::2]):
        parsed_data_weather[key.lower()]=float(current_read[2*i+1])

    upload_phant(pht_weather,parsed_data_weather,screen_display)

    # save to file
    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
    if screen_display: print time_now,delimiter,msg_weather.rstrip()
    if save_to_file: fid.write(time_now+delimiter+msg_weather)
       
    # sleep to the next loop
    #time.sleep(sleep_time_seconds)

        
      

