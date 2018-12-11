#!/usr/bin/python
import serial
import time
import numpy as np
import sys
from phant import Phant
import serial_openlock
import get_ip
from upload_phant import upload_phant
# below required by gpio
#import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep,gmtime, strftime,localtime             # lets us have a delay  

with open('/home/pi/script/pass/public_scales_kathy', 'r') as myfile:
    public_scales_kathy=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_scales_kathy', 'r') as myfile:
    private_scales_kathy=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')

#------------------------- below are definations for the scales ---------------------------------
field_name=['scale1','scale2','scale3']

scales_kathy=dict((el,0.0) for el in field_name)
pht_scales_kathy= Phant(publicKey=public_scales_kathy, fields=field_name ,privateKey=private_scales_kathy,baseUrl=nectar_address)

#port_sensor  = 'USB VID:PID=2341:0042 SNR=557363037393516030D1'
port_scale1='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2:1.0-port0'
port_scale2='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.4:1.0-port0'

scale1 = serial.Serial(port_scale1,timeout=20)
scale2 = serial.Serial(port_scale2,timeout=20)
#scale3 = serial.Serial(port_scale3,timeout=20)

scale1.write('IP\n\r')
scale2.write('IP\n\r')
#scale3.write('IP\n\r')

time.sleep(2)
str_scale1=scale1.readline()
str_scale2=scale2.readline()
#str_scale3=scale3.readline()

screen_display=True

scale_attempts=1
while scale_attempts<6:
    try:
        scale1.write('IP\n\r')
        scale2.write('IP\n\r')
        #scale3.write('IP\n\r')
        time.sleep(2)#wait for two seconds before leaving   
        str_scale1=scale1.readline()
        str_scale2=scale2.readline()
        #str_scale3=scale3.readline()
        weight_scale1=str_scale1.split()[0]
        weight_scale2=str_scale2.split()[0]
        #weight_scale3=str_scale3.split()[0]
        break
    except Exception, e:
        if screen_display: print "scale reading failed,"+str(scale_attempts)+" " + str(e)
        scale_attempts+=1
        time.sleep(3)
        scale1.close()
        scale2.close()
        #scale3.close()
        time.sleep(5)
        scale1 = serial.Serial(port_scale1,timeout=20)
        scale2 = serial.Serial(port_scale2,timeout=20)
        #scale3 = serial.Serial(port_scale3,timeout=20)
        pass

#time.sleep(10)
#scale1.write('IP\n\r')
#scale2.write('IP\n\r')
#
#time.sleep(2)
#str_scale1=scale1.readline()
#str_scale2=scale2.readline()

#weight_scale1=str_scale1.split()[0]
#weight_scale2=str_scale2.split()[0]
temp_sampling_number=20
#whether the result will be displayed on the screen
#screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'scales_kathy.csv'
sleep_time_seconds=30*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)



while True: 
    ### -------------------- below is to processing data from suction, moisture-------------------------
    #if screen_display: print strftime("%Y-%m-%d %H:%M:%S", localtime())
    #if save_to_file: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime())  )
    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
#    if screen_display: print time_now,delimiter,weight_scale1.rstrip(),delimiter,weight_scale2.rstrip(),delimiter,weight_scale3.rstrip(),delimiter,weight_scale4.rstrip(),delimiter,weight_scale5.rstrip(),delimiter,weight_scale6.rstrip()
#    if save_to_file: fid.write(time_now+delimiter+weight_scale1+delimiter+weight_scale2+delimiter+weight_scale3+delimiter+weight_scale4+delimiter+weight_scale5+delimiter+weight_scale6+'\n\r')

   # if screen_display: print time_now,delimiter,weight_scale1.rstrip(),delimiter,weight_scale2.rstrip(),delimiter,weight_scale3.rstrip()
   # if save_to_file: fid.write(time_now+delimiter+weight_scale1+delimiter+weight_scale2+delimiter+weight_scale3+'\n\r')   
    if screen_display: print time_now,delimiter,weight_scale1.rstrip(),delimiter,weight_scale2.rstrip()
    if save_to_file: fid.write(time_now+delimiter+weight_scale1+delimiter+weight_scale2+'\n\r')    
    
    #if screen_display: print time_now,delimiter,weight_scale1.rstrip()
    #if save_to_file: fid.write(time_now+delimiter+weight_scale1+'\n\r')

    scale_attempts=1
    while scale_attempts<6:
        try:
            scale1.write('IP\n\r')
            scale2.write('IP\n\r')
            #scale3.write('IP\n\r')
            time.sleep(2)#wait for two seconds before leaving   
            str_scale1=scale1.readline()
            str_scale2=scale2.readline()
            #str_scale2=scale3.readline()
            weight_scale1=str_scale1.split()[0]
            weight_scale2=str_scale2.split()[0]
            #weight_scale3=str_scale3.split()[0]
            scales_kathy['scale1']=float(weight_scale1)
            scales_kathy['scale2']=float(weight_scale2)
            #scales_kathy['scale3']=float(weight_scale3)
            break
        except Exception, e:
            if screen_display: print "scale reading failed,"+str(scale_attempts)+" " + str(e)
            scale_attempts+=1
            time.sleep(20)
            scale1.close()
            scale2.close()
            #scale3.close()
            time.sleep(20)
            scale1 = serial.Serial(port_scale1,timeout=20)
            scale2 = serial.Serial(port_scale2,timeout=20)
            #scale3 = serial.Serial(port_scale3,timeout=20)
            pass           
             
             
 


    upload_phant(pht_scales_kathy,scales_kathy,screen_display)
    # sleep to the next loop
    time.sleep(sleep_time_seconds)

        
      


