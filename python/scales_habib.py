#!/usr/bin/python
import serial
import os
import time
import numpy as np
import sys
import paho.mqtt.client as mqtt
import json
from phant import Phant
import serial_openlock
import get_ip
from upload_phant import upload_phant
# below required by gpio
#import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep,gmtime, strftime,localtime             # lets us have a delay  

#with open('/home/pi/script/pass/public_scales_habib', 'r') as myfile:
#    public_scales_habib=myfile.read().replace('\n', '')
#
#with open('/home/pi/script/pass/private_scales_habib', 'r') as myfile:
#    private_scales_habib=myfile.read().replace('\n', '')
#
#with open('/home/pi/script/pass/access_token', 'r') as myfile:
#    access_token=myfile.read().replace('\n', '')
#
#with open('/home/pi/script/pass/thingsboard_host', 'r') as myfile:
#    thingsboard_host=myfile.read().replace('\n', '')
#
#with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
#    nectar_address=myfile.read().replace('\n', '')

with open('/home/pi/pyduino/credential/scale_habib.json') as f:
        credential = json.load(f) #,object_pairs_hook=collections.OrderedDict)

#------------------------- below are definations for the scales ---------------------------------
field_name=['scale1','scale2','scale3','scale4','scale5','scale6','pressure1','pressure2','temperature1','temperature2']

scales_habib=dict((el,0.0) for el in field_name)
pht_scales_habib= Phant(publicKey=credential['public_scales_habib'], fields=field_name ,privateKey=credential['private_scales_habib'],baseUrl=credential['nectar_address'])

#port_sensor  = 'USB VID:PID=2341:0042 SNR=557363037393516030D1'
port_scale1='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.4.1.4:1.0-port0'
port_scale2='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.4.1.3:1.0-port0'
port_scale3='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.4.1.2:1.0-port0'
port_scale4='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.4.4:1.0-port0'
port_scale5='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.4.3:1.0-port0'
port_scale6='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.4.2:1.0-port0'
port_sensor1 ='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2:1.0-port0'
port_sensor2 ='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.3:1.0-port0'


scale1 = serial.Serial(port_scale1,baudrate=2400,bytesize=7,parity='E',timeout=20)
scale2 = serial.Serial(port_scale2,baudrate=2400,bytesize=7,parity='E',timeout=20)
scale3 = serial.Serial(port_scale3,baudrate=2400,bytesize=7,parity='E',timeout=20)
scale4 = serial.Serial(port_scale4,baudrate=2400,bytesize=7,parity='E',timeout=20)
scale5 = serial.Serial(port_scale5,baudrate=2400,bytesize=7,parity='E',timeout=20)
scale6 = serial.Serial(port_scale6,baudrate=2400,bytesize=7,parity='E',timeout=20)

time.sleep(2)
scale1.write('Q\r\n')
scale2.write('Q\r\n')
scale3.write('Q\r\n')
scale4.write('Q\r\n')
scale5.write('Q\r\n')
scale6.write('Q\r\n')

time.sleep(2)
str_scale1=scale1.readline()
str_scale2=scale2.readline()
str_scale3=scale3.readline()
str_scale4=scale4.readline()
str_scale5=scale5.readline()
str_scale6=scale6.readline()

screen_display=True

scale_attempts=1
while scale_attempts<6:
    try:
        scale1.write('Q\r\n')
        scale2.write('Q\r\n')
        scale3.write('Q\r\n')
        scale4.write('Q\r\n')
        scale5.write('Q\r\n')
        scale6.write('Q\r\n')
        time.sleep(2)#wait for two seconds before leaving   
        str_scale1=scale1.readline()
        str_scale2=scale2.readline()
        str_scale3=scale3.readline()
        str_scale4=scale4.readline()
        str_scale5=scale5.readline()
        str_scale6=scale6.readline()
        weight_scale1=str_scale1.split()[0]
        weight_scale2=str_scale2.split()[0]
        weight_scale3=str_scale3.split()[0]
        weight_scale4=str_scale4.split()[0]
        weight_scale5=str_scale5.split()[0]
        weight_scale6=str_scale6.split()[0]
        reading_scale1=weight_scale1.split(',')[1]
        reading_scale2=weight_scale2.split(',')[1]
        reading_scale3=weight_scale3.split(',')[1]
        reading_scale4=weight_scale4.split(',')[1]
        reading_scale5=weight_scale5.split(',')[1]
        reading_scale6=weight_scale6.split(',')[1]
        break
    except Exception, e:
        if screen_display: print "scale reading failed,"+str(scale_attempts)+" " + str(e)
        scale_attempts+=1
        time.sleep(3)
        scale1.close()
        scale2.close()
        scale3.close()
        scale4.close()
        scale5.close()
        scale6.close()
        time.sleep(5)
        scale1 = serial.Serial(port_scale1,baudrate=2400,bytesize=7,parity='E',timeout=20)
        scale2 = serial.Serial(port_scale2,baudrate=2400,bytesize=7,parity='E',timeout=20)
        scale3 = serial.Serial(port_scale3,baudrate=2400,bytesize=7,parity='E',timeout=20)
        scale4 = serial.Serial(port_scale4,baudrate=2400,bytesize=7,parity='E',timeout=20)
        scale5 = serial.Serial(port_scale5,baudrate=2400,bytesize=7,parity='E',timeout=20)
        scale6 = serial.Serial(port_scale6,baudrate=2400,bytesize=7,parity='E',timeout=20)
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
file_name= 'scales_habib.csv'
sleep_time_seconds=15*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

while True:
    try:
        next_reading = time.time()
        client = mqtt.Client()
        client.username_pw_set(credential['access_token'])
        client.connect(credential['thingsboard_host'], 1883, 60)
        client.loop_start()
        break
    except Exception, e:
        time.sleep(60)

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)


try:

    while True: 
        ### -------------------- below is to processing data from suction, moisture-------------------------
        if screen_display: print strftime("%Y-%m-%d %H:%M:%S", localtime())
        if save_to_file: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime())  )

        ard=serial.Serial(port_sensor1)
        msg=ard.write("OP1\r")
        msg=ard.read_until('\r')
        sleep(1)
        msg=ard.write("GN\r")
        msg1=ard.read_until('\r')
        sleep(1)
        msg=ard.write("OP2\r")
        msg=ard.read_until('\r')
        sleep(1)
        msg=ard.write("GN\r")
        msg2=ard.read_until('\r')
        sleep(2)
        ard.close()
        
        if screen_display: print msg1.rstrip()
        if save_to_file: fid.write(delimiter+msg1.rstrip())
        upload_msg=msg1.rstrip()
        #current_read=msg1.split(',')[0:-1]
        current_read=upload_msg.split()[0]
        scales_habib['pressure1']=float(current_read)


        if screen_display: print msg2.rstrip()
        if save_to_file: fid.write(delimiter+msg2.rstrip())
        upload_msg=msg2.rstrip()
        #current_read=msg2.split(',')[0:-1]
        current_read=upload_msg.split()[0]
        scales_habib['tensiometer1']=float(current_read)

        sleep(5)




        time_now=time.strftime("%d/%b/%Y %H:%M:%S")
    #    if screen_display: print time_now,delimiter,weight_scale1.rstrip(),delimiter,weight_scale2.rstrip(),delimiter,weight_scale3.rstrip(),delimiter,weight_scale4.rstrip(),delimiter,weight_scale5.rstrip(),delimiter,weight_scale6.rstrip()
    #    if save_to_file: fid.write(time_now+delimiter+weight_scale1+delimiter+weight_scale2+delimiter+weight_scale3+delimiter+weight_scale4+delimiter+weight_scale5+delimiter+weight_scale6+'\n\r')
    
       # if screen_display: print time_now,delimiter,weight_scale1.rstrip(),delimiter,weight_scale2.rstrip(),delimiter,weight_scale3.rstrip()
       # if save_to_file: fid.write(time_now+delimiter+weight_scale1+delimiter+weight_scale2+delimiter+weight_scale3+'\n\r')   
        if screen_display: print time_now,delimiter,reading_scale1.rstrip(),delimiter,reading_scale2.rstrip(),delimiter,reading_scale3.rstrip(),delimiter,reading_scale4.rstrip(),delimiter,reading_scale5.rstrip(),delimiter,reading_scale6.rstrip()
        if save_to_file: fid.write(time_now+delimiter+reading_scale1+delimiter+reading_scale2+reading_scale3+delimiter+reading_scale4+reading_scale5+delimiter+reading_scale6+'\n\r')    
        
        #if screen_display: print time_now,delimiter,weight_scale1.rstrip()
        #if save_to_file: fid.write(time_now+delimiter+weight_scale1+'\n\r')
    
        scale_attempts=1
        while scale_attempts<6:
            try:
                scale1.write('Q\r\n')
                scale2.write('Q\r\n')
                scale3.write('Q\r\n')
                scale4.write('Q\r\n')
                scale5.write('Q\r\n')
                scale6.write('Q\r\n')
                time.sleep(2)#wait for two seconds before leaving   
                str_scale1=scale1.readline()
                str_scale2=scale2.readline()
                str_scale3=scale3.readline()
                str_scale4=scale4.readline()
                str_scale5=scale5.readline()
                str_scale6=scale6.readline()
                weight_scale1=str_scale1.split()[0]
                weight_scale2=str_scale2.split()[0]
                weight_scale3=str_scale3.split()[0]
                weight_scale4=str_scale4.split()[0]
                weight_scale5=str_scale5.split()[0]
                weight_scale6=str_scale6.split()[0]
                reading_scale1=weight_scale1.split(',')[1]
                reading_scale2=weight_scale2.split(',')[1]
                reading_scale3=weight_scale3.split(',')[1]
                reading_scale4=weight_scale4.split(',')[1]
                reading_scale5=weight_scale5.split(',')[1]
                reading_scale6=weight_scale6.split(',')[1]
                scales_habib['scale1']=float(reading_scale1)
                scales_habib['scale2']=float(reading_scale2)
                scales_habib['scale3']=float(reading_scale3)
                scales_habib['scale4']=float(reading_scale4)
                scales_habib['scale5']=float(reading_scale5)
                scales_habib['scale6']=float(reading_scale6)
                break
            except Exception, e:
                if screen_display: print "scale reading failed,"+str(scale_attempts)+" " + str(e)
                scale_attempts+=1
                time.sleep(3)
                scale1.close()
                scale2.close()
                scale3.close()
                scale4.close()
                scale5.close()
                scale6.close()
                time.sleep(5)
                scale1 = serial.Serial(port_scale1,baudrate=2400,bytesize=7,parity='E',timeout=20)
                scale2 = serial.Serial(port_scale2,baudrate=2400,bytesize=7,parity='E',timeout=20)
                scale3 = serial.Serial(port_scale3,baudrate=2400,bytesize=7,parity='E',timeout=20)
                scale4 = serial.Serial(port_scale4,baudrate=2400,bytesize=7,parity='E',timeout=20)
                scale5 = serial.Serial(port_scale5,baudrate=2400,bytesize=7,parity='E',timeout=20)
                scale6 = serial.Serial(port_scale6,baudrate=2400,bytesize=7,parity='E',timeout=20)
                pass
    
        client.publish('v1/devices/me/telemetry', json.dumps(scales_habib), 1)
        upload_phant(pht_scales_habib,scales_habib,screen_display)
        # sleep to the next loop
        time.sleep(sleep_time_seconds)

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
        
      


