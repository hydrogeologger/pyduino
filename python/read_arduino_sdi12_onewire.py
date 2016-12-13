#!/usr/bin/python
import serial
#import syslog
import time
import numpy as np
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
port = '/dev/ttyUSB0'   # usb 0 is used to do sdi12 and onewire adding
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
file_name= 'arduino_data_digi_sdi12_onewire.csv'

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

### --------------------------- Processing data --------------------
# open up the arduino port
ard = serial.Serial(port,9600,timeout=None)

# the '0' at the end of the script helps save instantly.
# http://stackoverflow.com/questions/18984092/python-2-7-wr
if save_to_file: fid= open(file_name,'a',0)


if plot:
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    msg = ard.readline()
    msg = ard.readline()
    number_of_column=len(msg.split(seperator))-1
    data = [[0. for _ in range(no_reading)] for _ in range(number_of_column)]
    #http://stackoverflow.com/questions/11874767/real-time-plotting-in-while-loop-with-matplotlib
    plt.axis([0, 100, 0, 900])
    plt.ion()
    msg_parse=msg.split(',')
    x = np.arange(10)
    ys = [_+x+(_*x)**2 for _ in range(number_of_column)]


for i in xrange(no_reading): 
    msg = ard.readline()
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

