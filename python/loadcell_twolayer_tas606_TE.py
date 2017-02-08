#!/usr/bin/python
import serial
import time
import numpy as np
import sys
from phant import Phant

field_name=['tas606','te','measure_local_time'];

pht = Phant(publicKey='KJo3Nx8grJcMDpEWQOXg', 
    fields=field_name ,privateKey='vzVe5AZkyzcdvlKWG741')

parsed_data={'tas606':0.0,'te':0.0,'measure_local_time':''};


### --------------------------input section ---------------------------
# the port arduino has been connected to. in windows, it is usually 'COM4, COM5' where
#   the number is subject to change. Just try 'devmgmt.msc' after pressing ctrl+r.
# In linux it is usually /dev/ttyUSB
#  below are the ls /dev/serial/by-id result:
#lrwxrwxrwx 1 root root 13 Feb  8 11:13 usb-FTDI_FT231X_USB_UART_DN01J0QE-if00-port0 -> ../../ttyUSB1
#lrwxrwxrwx 1 root root 13 Feb  8 11:13 usb-FTDI_FT231X_USB_UART_DN01JJDJ-if00-port0 -> ../../ttyUSB0
#lrwxrwxrwx 1 root root 13 Feb  8 11:13 usb-FTDI_USB__-__Serial-if00-port0 -> ../../ttyUSB2

#port = '/dev/ttyUSB1'  # USB1 is for all the EC 5 moisture sensors
port = '/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_DN01J0QE-if00-port0'  # USB1 is for all the EC 5 moisture sensors

# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'loadcell_twolayer_tas606_TE.csv'


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

line_head_identifier='scale'
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
    if current_read[0]==line_head_identifier and len([i for i,x in enumerate(current_read) if x == line_head_identifier])==1:

        # parse "tas606"
        tas606_ind=[i for i,x in enumerate(current_read) if x == 'tas606']
        for i in tas606_ind:
            parsed_data['tas606']=float(current_read[i+1])

        # parse "te"
        te_ind=[i for i,x in enumerate(current_read) if x == 'te']
        for i in te_ind:
            parsed_data['te']=float(current_read[i+1])


        # start uploading results;
        ## notice: during debuging phase, it is suggested to run the script line-by-line to avoid bugs that can be passed by try and catch 
        time_now=time.strftime("%Y-%b-%d %H:%M:%S")
        parsed_data['measure_local_time']=time_now


        log_attempts=1
        while log_attempts<10:
            try:
                pht.log(parsed_data['tas606']  # warning: the sequence of the upload values has to follow strict from sequence in variable pased_data and field name
                    ,parsed_data['te']
                    ,parsed_data['measure_local_time'])
                break
            except: # catch all errors
                log_attempts+=1
                time.sleep(30)
                continue
        if screen_display: print i,delimiter,time_now,delimiter,msg.rstrip()
        if save_to_file: fid.write(time_now+delimiter+msg)
       
    time.sleep(sleep_time_seconds)

        
fid.close()
ser.close()




