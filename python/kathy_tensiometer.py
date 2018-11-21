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
from time import sleep,gmtime, strftime,localtime             # lets us have a delay  
import subprocess

with open('/home/pi/script/pass/public_kathy_tensiometer', 'r') as myfile:
    public_kathy_tensiometer=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_kathy_tensiometer', 'r') as myfile:
    private_kathy_tensiometer=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/access_token', 'r') as myfile:
    access_token=myfile.read().replace('\n', '')
#
with open('/home/pi/script/pass/thingsboard_host', 'r') as myfile:
    thingsboard_host=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')



field_name=['pressure1','pressure2','temp1_tensiometer','temp2_tensiometer','temp1_humsensor','temp2_humsensor','temp3_humsensor','temp4_humsensor','temp5_humsensor','temp6_humsensor','humidity1','humidity2','humidity3','humidity4','humidity5','humidity6','dhthum','dhttemp','scale1','scale2','scale3']
kathy_tensiometer=dict((el,0.0) for el in field_name)
pht_sensor = Phant(publicKey=public_kathy_tensiometer, fields=field_name ,privateKey=private_kathy_tensiometer,baseUrl=nectar_address)


#port_sensor  = 'USB VID:PID=2341:0042 SNR=55639303035351A04171'
#port_sensor = '/dev/ttyACM0'  # remember when using device at /dev/folder rather than USB VID:PID, serial_openlock needs to have match_existing=False
#port_sensor0 = '/dev/ttyUSB0' # port for serial connection 
#port_sensor1 = '/dev/ttyUSB4'
port_sensor0 = '/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2:1.0-port0'
port_sensor1 = '/dev/serial/by-path/platform-3f980000.usb-usb-0:1.3:1.0-port0'
port_sensor2  = '/dev/ttyACM0'
port_scale1='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.5.2:1.0-port0'
port_scale2='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.5.3:1.0-port0'
port_scale3='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.5.4:1.0-port0'

scale1 = serial.Serial(port_scale1,timeout=20)
scale2 = serial.Serial(port_scale2,timeout=20)
scale3 = serial.Serial(port_scale3,timeout=20) 
    
scale1.write('IP\n\r')
scale2.write('IP\n\r')
scale3.write('IP\n\r')

time.sleep(2)
str_scale1=scale1.readline()
str_scale2=scale2.readline()
str_scale3=scale3.readline()

screen_display=True

scale_attempts=1
while scale_attempts<6:
    try:
        scale1.write('IP\n\r')
        scale2.write('IP\n\r')
        scale3.write('IP\n\r')
        time.sleep(2)#wait for two seconds before leaving   
        str_scale1=scale1.readline()
        str_scale2=scale2.readline()
        str_scale3=scale3.readline()
        weight_scale1=str_scale1.split()[0]
        weight_scale2=str_scale2.split()[0]
        weight_scale3=str_scale3.split()[0]
        break
    except Exception, e:
        if screen_display: print "scale reading failed,"+str(scale_attempts)+" " + str(e)
        scale_attempts+=1
        time.sleep(3)
        scale1.close()
        scale2.close()
        scale3.close()
        time.sleep(5)
        scale1 = serial.Serial(port_scale1,timeout=20)
        scale2 = serial.Serial(port_scale2,timeout=20)
        scale3 = serial.Serial(port_scale3,timeout=20)
        pass


#


# whether the result will be displayed on the screen
#screen_display=True
temp_sampling_number=20
# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'kathy_tensiometer.csv'

sleep_time_seconds=30*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

next_reading = time.time()

client = mqtt.Client()

client.username_pw_set(access_token)

client.connect(thingsboard_host, 1883, 60)

client.loop_start()

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)

try:

    while True: 
        ### -------------------- below is to processing data from suction, moisture-------------------------
        if screen_display: print strftime("%Y-%m-%d %H:%M:%S", localtime())
        if save_to_file: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime())  )
     
        
    #    try:
            # possible update: set time out for send result
        ard=serial.Serial(port_sensor0)
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
        kathy_tensiometer['pressure1']=float(current_read)
    
    
        if screen_display: print msg2.rstrip()
        if save_to_file: fid.write(delimiter+msg2.rstrip())
        upload_msg=msg2.rstrip()
        #current_read=msg2.split(',')[0:-1]
        current_read=upload_msg.split()[0]
        kathy_tensiometer['temp1_tensiometer']=float(current_read)
    
        sleep(5)        
 
        ard=serial.Serial(port_sensor1) 
        msg=ard.write("OP3\r")
        msg=ard.read_until('\r')
        sleep(1)
        msg=ard.write("GN\r")
        msg1=ard.read_until('\r')
        sleep(1)
        msg=ard.write("OP4\r")
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
        kathy_tensiometer['pressure2']=float(current_read) 
        
    
        if screen_display: print msg2.rstrip()
        if save_to_file: fid.write(delimiter+msg2.rstrip())
        upload_msg=msg2.rstrip()
        #current_read=msg2.split(',')[0:-1]
        current_read=upload_msg.split()[0]
        kathy_tensiometer['temp2_tensiometer']=float(current_read)
    
        sleep(5)   
        msg=serial_openlock.get_result_by_input(port=port_sensor2,command="dht22,10,power,48,points,1,dummies,1,interval_mm,200,debug,0",initialize=False,match_existing_ports=False)         
        #ard=serial.Serial(port_sensor2,timeout=20)
        #msg=ard.write("dht22,10,power,48,points,1,dummies,1,interval_mm,200,debug,0")            
        #sleep(10)
        #        
        #msg=ard.readline()
        #    
        #sleep(5)
        #ard.close()
        #    
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        kathy_tensiometer['dhthum']=float(current_read[-1])
        kathy_tensiometer['dhttemp']=float(current_read[-2])

        #try:
        #   kathy_tensiometer['dhthum']=float(current_read[-1])
        #   kathy_tensiometer['dhttemp']=float(current_read[-2])
        #except Exception, e:
        #    if screen_display: print 'dht does not get results'
        #    pass
    
        time_now=time.strftime("%d/%b/%Y %H:%M:%S")
        if screen_display: print time_now,delimiter,weight_scale1.rstrip(),delimiter,weight_scale2.rstrip(),weight_scale3.rstrip()
        #if save_to_file: fid.write(time_now+delimiter+weight_scale1+delimiter+weight_scale2+delimiter+weight_scale3+'\n\r')
    
        #if save_to_file: fid.write(time_now+delimiter+weight_scale1+delimiter+weight_scale2+'\n\r')
        if save_to_file: fid.write(time_now+delimiter+weight_scale1+delimiter+weight_scale2+delimiter+weight_scale3+'\n\r')
    
        scale_attempts=1
        while scale_attempts<6:
            try:
                scale1.write('IP\n\r')
                scale2.write('IP\n\r')
                scale3.write('IP\n\r')
                time.sleep(2)#wait for two seconds before leaving   
                str_scale1=scale1.readline()
                str_scale2=scale2.readline()
                str_scale3=scale3.readline()
                weight_scale1=str_scale1.split()[0]
                weight_scale2=str_scale2.split()[0]
                weight_scale3=str_scale3.split()[0]
                kathy_tensiometer['scale1']=float(weight_scale1)
                kathy_tensiometer['scale2']=float(weight_scale2)
                kathy_tensiometer['scale3']=float(weight_scale3)
                break
            except Exception, e:
                if screen_display: print "scale reading failed,"+str(scale_attempts)+" " + str(e)
                scale_attempts+=1
                time.sleep(20)
                scale1.close()
                scale2.close()
                scale3.close()
                time.sleep(20)
                scale1 = serial.Serial(port_scale1,timeout=20)
                scale2 = serial.Serial(port_scale2,timeout=20)
                scale3 = serial.Serial(port_scale3,timeout=20)
                pass
    
    
        client.publish('v1/devices/me/telemetry', json.dumps(kathy_tensiometer), 1)   
        upload_phant(pht_sensor,kathy_tensiometer,screen_display)

        if save_to_file: fid.write("\n\r")
        # sleep to the next loop
        time.sleep(sleep_time_seconds)

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
