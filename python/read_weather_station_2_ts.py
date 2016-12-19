#!/usr/bin/python
import serial
import time
import numpy as np
import class_thingspeak as ts
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
port = '/dev/ttyUSB2'  # USB1 is for all the EC 5 moisture sensors
#port = '/dev/ttyACM0'
#port = 'COM3'

# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# whether plot the result on the go
#plot=True
plot=False
#number_of_columns=4;

# the Filename of the csv file for storing file
file_name= 'arduino_weather_station_2.csv'

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
# This program logs a Raspberry Pi's CPU temperature to a Thingspeak Channel
# To use, get a Thingspeak.com account, set up a channel, and capture the Channel Key at https://thingspeak.com/docs/tutorials/
# Then paste your channel ID in the code for the value of "key" below.
# Then run as sudo python pitemp.py (access to the CPU temp requires sudo access)
# You can see my channel at https://thingspeak.com/channels/41518

import httplib, urllib
#key = 'UR338L6I57M3PO39'  # Thingspeak channel to update
#key1 = '0AJ9RH5MI2180ZRP'  # the key for weather on the roof
#key1 = 'I1TJ4V3DGNVQE3MV' # load cell calibration
#key1  = '45LM6BV9GT0ARZAN'    # weather_station_1

key1  =  'N6MMMYT7CHR5ZS8I'   # weather_station_2

key2  =  'RJWQWYHOR88HD3TY'   #weather_station_2_wind


### --------------------------- Processing data --------------------
# open up the arduino port
ard = serial.Serial(port,9600,timeout=None)

# the '0' at the end of the script helps save instantly.
# http://stackoverflow.com/questions/18984092/python-2-7-wr
if save_to_file: fid= open(file_name,'a',0)


# the first reading is dummy readings
msg = ard.readline()

for i in xrange(no_reading): 
    msg = ard.readline()
    current_read=msg.split(',')[1:-1]
    # '$,WdDir,135,WdSpdkph,3.3,WdGstkph,4.2,WdGstDir,135,WdSpdKphAvg2m,0.1,WdDirAvg2m,3,WdGstKph10m,4.2,WdGstDir10m,135,rh,87.6,TC,25.3,RainMM,0.00,DlyRainMM,0.00,P,100415.75,batt,4.10,lt,0.00,#\r\n'
    read_float=np.array([float(current_read[_]) for _ in range(1,31,2)])
    upload_array=read_float[[0,1,8,9,10,11,12,14] ]
    ts.ts_upload(upload_array,key1) # in total there are 8 channels


    upload_array=read_float[[2,3,4,5,6,7,13]]
    ts.ts_upload(upload_array,key2) # in total there are 8 channels

    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
    if screen_display: print i,seperator,time_now,seperator,msg.rstrip()
    if save_to_file: fid.write(time_now+seperator+msg)

    time.sleep(sleep_time_seconds)

    if plot:
        colors = iter(cm.rainbow(np.linspace(0, 1, len(ys))))
        for j in xrange(number_of_column):
            data[j][i]=float(msg_parse[j])
            plt.scatter(range(i),data[j][0:i],color=next(colors))
            plt.axis([0, i+100, 0, 800])
            plt.pause(0.0001)
        
      

fid.close()
ser.close()

