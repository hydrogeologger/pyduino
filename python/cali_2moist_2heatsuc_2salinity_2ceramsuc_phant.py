#!/usr/bin/python
import serial
import time
import numpy as np
import sys
from phant import Phant

# 

field_name=['suht_28e5_begin','suht_28e5_peak','suht_28e5_end','suht_2847_begin','suht_2847_peak','suht_2847_end',
    'saltrh_2_tp','saltrh_2_rh','saltrh_3_tp','saltrh_3_rh','mo_7','mo_8','mo_9','mo_10']

pht = Phant(publicKey='9J2rX3QZ94s5RJ9LjrbN', 
    fields=field_name ,privateKey='xz6exl8ypjCAvaK6W4PB')

parsed_data={'suht_28e5_begin':0.0,
    'suht_28e5_peak':0.0,
    'suht_28e5_end':0.0,
    'suht_2847_begin':0.0,
    'suht_2847_peak':0.0,
    'suht_2847_end':0.0,
    'saltrh_2_tp':0.0,
    'saltrh_2_rh':0.0,
    'saltrh_3_tp':0.0,
    'saltrh_3_rh':0.0,
    'mo_7':0.0,
    'mo_8':0.0,
    'mo_9':0.0,
    'mo_10':0.0};


### --------------------------input section ---------------------------
# the port arduino has been connected to. in windows, it is usually 'COM4, COM5' where
#   the number is subject to change. Just try 'devmgmt.msc' after pressing ctrl+r.
# In linux it is usually /dev/ttyUSB
port = '/dev/ttyUSB0'  # USB1 is for all the EC 5 moisture sensors

# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'cali_2moist_2heatsuc_2salinity_2ceramsuc_phant.csv'


temp_sampling_number=20;

# the time interval between each reading from arduino in seconds
# be careful about the data collection interval in arduino, it is always good 
# to make the sleep_time_seconds to be the same as the time interval in arduino
# to minimize the data loss.
# e.g., if arduino time interval is 1, python interval is 10, arduino will produce
# more data than python can actually retrive, as a result, arduino may replace the 
# existing data, cause the inconsistency between the data collection in arduino and 
# data save in python
# similar situation applies for commercial scales.
sleep_time_seconds=0.001

# number of readings, give a large value if you want to read the data in months
#   but it should not be too big,
no_reading=100000

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'

### --------------------------- Processing data --------------------
ard = serial.Serial(port,9600,timeout=None)

# throw away the first reading as it is always formated poorly
msg = ard.readline()
#msg = ard.readline()
# the '0' at the end of the script helps save instantly.
# http://stackoverflow.com/questions/18984092/python-2-7-wr
if save_to_file: fid= open(file_name,'a',0)


for i in xrange(no_reading): 
    msg = ard.readline()
    current_read=msg.split(delimiter)[0:-1]
    if current_read[0]=='Soil1' and len([i for i,x in enumerate(current_read) if x == 'Soil1'])==1:

        # parse "SucHeat"
        sucheat_ind=[i for i,x in enumerate(current_read) if x == 'SucHeat']
        for i in sucheat_ind:
            parsed_data['suht_'+current_read[i+1].lower()+'_begin']=float(current_read[i+3])
            parsed_data['suht_'+current_read[i+1].lower()+'_peak']=float(current_read[i+temp_sampling_number+3])
            parsed_data['suht_'+current_read[i+1].lower()+'_end']=float(current_read[i+temp_sampling_number+3])

        # parse salinity sensor using relative humidty data
        saltrh_ind=[i for i,x in enumerate(current_read) if x == 'SaltRH']
        for i in saltrh_ind:
            if float(current_read[i+2])<0 :
                parsed_data['saltrh_'+current_read[i+1]+'_tp']=np.nan
                parsed_data['saltrh_'+current_read[i+1]+'_rh']=np.nan
            else:
                parsed_data['saltrh_'+current_read[i+1]+'_tp']=float(current_read[i+2])
                parsed_data['saltrh_'+current_read[i+1]+'_rh']=float(current_read[i+3])

        # parse moisture_sensor data
        mo_ind=[i for i,x in enumerate(current_read) if x == 'Mo']
        for i in mo_ind:
            parsed_data['mo_'+current_read[i+1]]=float(current_read[i+2])
        


        # start uploading results;
        ## notice: during debuging phase, it is suggested to run the script line-by-line to avoid bugs that can be passed by try and catch 
        log_attempts=1
        while log_attempts<10:
            try:
                pht.log(parsed_data['suht_28e5_begin']
                    ,parsed_data['suht_28e5_peak']
                    ,parsed_data['suht_28e5_end']
                    ,parsed_data['suht_2847_begin']
                    ,parsed_data['suht_2847_peak']
                    ,parsed_data['suht_2847_end']
                    ,parsed_data['saltrh_2_tp']
                    ,parsed_data['saltrh_2_rh']
                    ,parsed_data['saltrh_3_tp']
                    ,parsed_data['saltrh_3_rh']
                    ,parsed_data['mo_7']
                    ,parsed_data['mo_8']
                    ,parsed_data['mo_9']
                    ,parsed_data['mo_10'])
                break
            except: # catch all errors
                log_attempts+=1
                time.sleep(30)
                continue
        time_now=time.strftime("%d/%b/%Y %H:%M:%S")
        if screen_display: print i,delimiter,time_now,delimiter,msg.rstrip()
        if save_to_file: fid.write(time_now+delimiter+msg)
       
    time.sleep(sleep_time_seconds)

        
fid.close()
ser.close()




