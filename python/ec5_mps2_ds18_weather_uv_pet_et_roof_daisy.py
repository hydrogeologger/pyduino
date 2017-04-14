#!/usr/bin/python
# this script reads all equipment from column daisy, including sensors and weather stations, uv sensors. 
# mount specification: mega with ec5, eps2, ds18, loadcell, 
import serial
import time
import numpy as np
import sys
from phant import Phant
import serial_openlock

#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['tpf0','tp11','tp8d','tpa3','mo0','mo1','mo2','mo3','mo4','mo5','mo6','mo7',
    'mo8','mo9','mo10','mo11','su1','tp1','su2','tp2','su3','tp3','su4','tp4','evap1','evap2']
#http://stackoverflow.com/questions/3869487/how-do-i-create-a-dictionary-with-keys-from-a-list-and-values-defaulting-to-say
parsed_data=dict((el,0.0) for el in field_name)
#https://data.sparkfun.com/streams/RMxqjA6nRXfbm01raooM/update/lzEpXb5dxRhYAbG6177V
pht = Phant(publicKey='RMxqjA6nRXfbm01raooM', fields=field_name ,privateKey='lzEpXb5dxRhYAbG6177V')

# 'All,Tp,F0,20.44,Tp,11,20.06,Tp,8D,20.25,Tp,A3,20.62,Mo,0,247.00,Mo,1,70.15,Mo,2,69.20,Mo,3,65.90,Mo,4,69.95,Mo,5,75.00,Mo,6,66.00,Mo,7,60.80,Mo,8,69.60,Mo,9,40.35,Mo,10,190.90,Mo,11,86.60,SuTp,113DECAGON MPS-2 124,-3661.3,20.0,SuTp,213DECAGON MPS-2 124,-2251.4,20.0,SuTp,313DECAGON MPS-2 350,-6885.3,19.9,SuTp,413DECAGON MPS-2 136,-3487.4,20.3,Vis,260,IR,253,UV,0.02,AllDone\r\n'

#port_weather = '/dev/ttyACM0'
port_sensor  = 'USB VID:PID=2341:0042 '
#------------------------- above are definations for the sensors in the column ---------------------------------


#------------------------- below are definations for the weather station ---------------------------------



# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True


# the Filename of the csv file for storing file
file_name= 'column_daisy.csv'

sleep_time_seconds=10

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)
port_sensor_isopen=False


def upload_phant(pht,parsed_data,screen_display):
    log_attempts=1
    while log_attempts<10:
        try:          
            ##pht.log(iter([ parsed_data[key] for key in pht.fields]))
            # http://stackoverflow.com/questions/43414407/iterate-at-a-function-input-in-python/43414660#43414660
            pht.log(*[parsed_data[key] for key in pht.fields])
            if screen_display: print "uploaded"
            break
        except: # catch all errors
            if screen_display: print "upload failed at attempt",log_attempts
            log_attempts+=1
            time.sleep(30)
            continue

while True: 
    ### --------------------------- bwlow is to processing data from column sensor--------------------------
    while port_sensor_isopen == False:
        [port_sensor_isopen, sensor_fid]=serial_openlock.open_port(port_sensor)
        time.sleep(10)
    serial_openlock.initialize(sensor_fid)
    sensor_fid.write("All") # either "Solar", "Soil" or "All"
    msg = sensor_fid.readline()
    port_sensor_isopen=serial_openlock.close_port(sensor_fid)
    
    current_read=msg.split(',')[0:-1]
    # parse tp result
    tp_ind=[i for i,x in enumerate(current_read) if x == 'Tp']
    for i in tp_ind:
        parsed_data['tp'+current_read[i+1].lower()]=float(current_read[i+2])
    # parse moisture data
    mo_ind=[i for i,x in enumerate(current_read) if x == 'Mo']
    for i in mo_ind:
        parsed_data['mo'+current_read[i+1]]=float(current_read[i+2])
    # parse mps2 data
    sutp_ind=[i for i,x in enumerate(current_read) if x == 'SuTp']
    for i in sutp_ind:
        parsed_data['su'+current_read[i+1][0]]=float(current_read[i+2])
        parsed_data['tp'+current_read[i+1][0]]=float(current_read[i+3])
    # log the results to sparkfun
    upload_phant(pht,parsed_data,screen_display)
    
    # save to file
    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
    if screen_display: print i,delimiter,time_now,delimiter,msg.rstrip()
    if save_to_file: fid.write(time_now+delimiter+msg)
       
    # sleep to the next loop
    time.sleep(sleep_time_seconds)

        
      

#for text in current_read:
#    if 'Soil' in text:
#        print(text)
#
#for text in current_read:
#    if 'So' in text:
#        print(text)
#
#for text in current_read:
#    if 'So' == text:
#        print(text)
#
#for text in current_read:
#    if 'So' == text:
#        print(text)
#ndexes = [i for i,x in enumerate(current_read) if x == 'a']



