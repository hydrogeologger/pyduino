#!/usr/bin/python
import serial
import time
import numpy as np
import sys
from phant import Phant


field_name=['tpf0','tp11','tp8d','tpa3','mo0','mo1','mo2','mo3','mo4','mo5','mo6','mo7',
    'mo8','mo9','mo10','mo11','su1','tp1','su2','tp2','su3','tp3','su4','tp4']
parsed_data={'tpf0':0.0,
    'tp11':0.0,
    'tp8d':0.0,
    'tpa3':0.0,
    'mo0':0.0,
    'mo1':0.0,
    'mo2':0.0,
    'mo3':0.0,
    'mo4':0.0,
    'mo5':0.0,
    'mo6':0.0,
    'mo7':0.0,
    'mo8':0.0,
    'mo9':0.0,
    'mo10':0.0,
    'mo11':0.0,
    'su1':0.0,
    'tp1':0.0,
    'su2':0.0,
    'tp2':0.0,
    'su3':0.0,
    'tp3':0.0,
    'su4':0.0,
    'tp4':0.0}
pht = Phant(publicKey='RMxqjA6nRXfbm01raooM', 
    fields=field_name ,privateKey='lzEpXb5dxRhYAbG6177V')
#    fields=['TpF0','Tp11','Tp8D','TpA3','Mo0','Mo1','Mo2','Mo3','Mo4','Mo5','Mo6','Mo7',
#    'Mo8','Mo9','Mo10','Mo11','Su1','Tp1','Su2','Tp2','Su3','Tp3','Su4','Tp4']

#TpF0,Tp11,Tp8D,TpA3,Mo0,Mo1,Mo2,Mo3,Mo4,Mo5,Mo6,Mo7,Mo8,Mo9,Mo10,Mo11,Su1,Tp1,Su2,Tp2,Su3,Tp3,Su4,Tp4,

#Soil,Tp,F0,25.62,Tp,11,25.81,Tp,8D,25.75,Tp,A3,26.56,Mo,0,423.45,Mo,1,220.70,Mo,2,224.00,Mo,3,224.70,Mo,4,227.00,Mo,5,226.10,Mo,6,204.35,Mo,7,200.00,Mo,8,213.00,Mo,9,207.00,Mo,10,240.05,Mo,11,325.55,SuTp,113DECAGON MPS-2 124,-4.6,26.5,SuTp,213DECAGON MPS-2 124,-4.7,26.6,SuTp,313DECAGON MPS-2 350,-9.7,26.4,SuTp,413DECAGON MPS-2 136,-10.0,26.8,
# this script reads off from arduino on the go.
# it is currently confirmed that arduino behaves similarly as all the scale sensors
# 1. having internal buffers
# 2. Being able to use simple serial interface to communicate with
# currently it is decided to use the time in raspberry pi/PC to record the time that
#    data collected by arduino for two reasons:
# 1. it is not known how much arduino time will be derivated over time.
# 2. raspberry pi has internet connected and so has time well syncronized. 
#
# However, it is always important that the reading intervals in arduino has to be 
#    the same as the current script reading interval. because the existing buffer in 
#    arduino may cause the time deviation between the time arduino has been read and 
#    the time raspberry has recorded the data
# Also, user needs to close the monitoring interfce in arduino GUID, as each USB port
#    can only be occupied by one process. 
# It is found so far that arduino will store 500 undisplayed data, if these data has
#    yet retrived, arduino will stop running as indicated by RX stopped flashing.
# basic usage:
#    moving the working directory to the folder where the python file exists:
# In [1]: cd /home/chenming/pydrino/python
#    execute the file
# In [2]: execfile('read_arduino.py')
# In [3]: pwd
#    pwd shows the current directory

### --------------------------input section ---------------------------
# the port arduino has been connected to. in windows, it is usually 'COM4, COM5' where
#   the number is subject to change. Just try 'devmgmt.msc' after pressing ctrl+r.
# In linux it is usually /dev/ttyUSB
#port = '/dev/ttyUSB1'  # USB1 is for all the EC 5 moisture sensors
port = '/dev/ttyACM0'

# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# whether plot the result on the go
#plot=True
#number_of_columns=4;

# the Filename of the csv file for storing file
file_name= 'arduino_data_ec5_mps2_DS18.csv'

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
seperator=','

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
    current_read=msg.split(',')[0:-1]
    if current_read[0]=='Soil' and len([i for i,x in enumerate(current_read) if x == 'Soil'])==1:
        # parse tp result
        #parsed_data['tp'+current_read[i+1]]=float(current_read[i+2]) for i in tp_ind
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
        log_attempts=1
        while log_attempts<10:
            try:          
                pht.log(parsed_data['tpf0']
                    ,parsed_data['tp11']
                    ,parsed_data['tp8d']
                    ,parsed_data['tpa3']
                    ,parsed_data['mo0']
                    ,parsed_data['mo1']
                    ,parsed_data['mo2']
                    ,parsed_data['mo3']
                    ,parsed_data['mo4']
                    ,parsed_data['mo5']
                    ,parsed_data['mo6']
                    ,parsed_data['mo7']
                    ,parsed_data['mo8']
                    ,parsed_data['mo9']
                    ,parsed_data['mo10']
                    ,parsed_data['mo11']
                    ,parsed_data['su1']
                    ,parsed_data['tp1']
                    ,parsed_data['su2']
                    ,parsed_data['tp2']
                    ,parsed_data['su3']
                    ,parsed_data['tp3']
                    ,parsed_data['su4']
                    ,parsed_data['tp4'])
                break
            except: # catch all errors
                log_attempts+=1
                time.sleep(30)
                continue
        time_now=time.strftime("%d/%b/%Y %H:%M:%S")
        if screen_display: print i,seperator,time_now,seperator,msg.rstrip()
        if save_to_file: fid.write(time_now+seperator+msg)
       


            #field_name=['tpf0','tp11','tp8d','tpa3','mo0','mo1','mo2','mo3','mo4','mo5','mo6','mo7',
            #    'mo8','mo9','mo10','mo11','su1','tp1','su2','tp2','su3','tp3','su4','tp4']

    #read_float=[float(i) for i in current_read]
    #ts_upload(read_float[0:9],key1) # in total there are 8 channels


    time.sleep(sleep_time_seconds)

        
      

fid.close()
ser.close()

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



