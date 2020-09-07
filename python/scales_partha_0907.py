#!/usr/bin/python
import serial
import time
#import paho.mqtt.client as mqtt
import json
from phant import Phant
from upload_phant import upload_phant
import serial
import os
from time import sleep,gmtime, strftime,localtime             # lets us have a delay  


#with open('/home/pi/pyduino/credential/yuan_pi2.json') as f:
#        credential = json.load(f) #,object_pairs_hook=collections.OrderedDict)

#------------------------- below are definations for the scales ---------------------------------
field_name=['scale1','scale2','humidity','temperature']

#yuan_pi2=dict((el,0.0) for el in field_name)
#port_sensor  = 'USB VID:PID=2341:0042 SNR=557363037393516030D1'
port_scale1='/dev/serial/by-path/platform-20980000.usb-usb-0:1.2:1.0-port0'
port_scale2='/dev/serial/by-path/platform-20980000.usb-usb-0:1.3:1.0-port0'
#port_tensiometer='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.5:1.0-port0'

#scale1 = serial.Serial(port_scale1,timeout=20)
#scale2 = serial.Serial(port_scale2,timeout=20)

#SERIAL_PORT='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.4:1.0' # datalogger version 1 uses ttyACM0
SERIAL_PORT='/dev/ttyS0'

screen_display=True
save_to_file=True
file_name='scales_partha_0907.csv'
sleep_time_seconds=15*60
delimiter=','

if save_to_file: fid= open(file_name,'a',0)

while True:
    try: 
        ard = serial.Serial(SERIAL_PORT,timeout=60)
        time.sleep(2)
	print('start recording sht31')
        ard.write("9548,0,type,sht31,power,22,debug,1")
        ard.flushInput()
        msg=ard.readline()
        current_read=msg.split(',')[0:-1]
        reading_temperature=float(current_read[-2])
        reading_humidity=float(current_read[-1])
	print('humidity sensor reading successful')
        if screen_display: print(msg.rstrip())
    except Exception:
        if screen_display:
            print('humidity sensor reading failed')
   
    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
    print(time_now)
    print('start recording scale readings')
    scale_attempts=1
    while scale_attempts<6:
        try:
            scale1 = serial.Serial(port_scale1,timeout=20)
            scale2 = serial.Serial(port_scale2,timeout=20)
	    time.sleep(2)
            scale1.write('IP\n\r')
            scale2.write('IP\n\r')
	    time.sleep(2)
    	    str_scale1=scale1.readline()
            str_scale2=scale2.readline()
	    time.sleep(1)
	    print('scale1 reading is '+str_scale1)
	    print('scale2 reading is '+str_scale2)
            weight_scale1=str_scale1.split()[0]
            weight_scale2=str_scale2.split()[0]      
            reading_scale1=weight_scale1
            reading_scale2=weight_scale2
            print('scale reading successful')
	   # if save_to_file: fid.write(time_now+delimiter+str(float(reading_scale1))+delimiter+str(float(reading_scale2))+delimiter+str(float(reading_scale3))+delimiter+ str(float(reading_temperature))+delimiter+str(float(reading_humidity))+delimiter+'\n\r')
            break
        except Exception, e:
            if screen_display:
                print "scale reading failed on attempt "+str(scale_attempts)+" " + str(e)
                scale_attempts+=1

#    try:
#        tensiometer=serial.Serial(port_tensiometer)
#	print('tensiometer sucessfully connected')
#        time.sleep(3)
#        tensiometer.write("OP1\r")
#        time.sleep(1)
       # tensiometer.read_until('\r')
       # time.sleep(1)
#        tensiometer.write("GN\r")
#        time.sleep(1)
       # msg_pressure=tensiometer.read_until('\r')
#	msg_pressure=tensiometer.read(10)
#        time.sleep(1)
#        tensiometer.write("OP2\r")
#        time.sleep(1)
       # tensiometer.read_until('\r')
       # time.sleep(1)
#        tensiometer.write("GN\r")
#        time.sleep(1)
       # msg_temp=tensiometer.read_until('\r')
#        msg_temp=tensiometer.read(10)
#        time.sleep(1)
#	print('tensiometer reading successful')
#        tensiometer.close()

#        if screen_display: print(msg_pressure.rstrip())
#        upload_msg_pressure=msg_pressure.rstrip()
#        current_read_pressure=upload_msg_pressure.split()[1]
      
#        if screen_display: print(msg_temp.rstrip())
#        upload_msg_temp=msg_temp.rstrip()
#        current_read_temp=upload_msg_temp.split()[1]
#        time.sleep(5)

#    except Exception:
#        if screen_display: print('Tensiometer reading failed')

    if save_to_file: fid.write(time_now+delimiter+str(float(reading_scale1))+delimiter+str(float(reading_scale2))+delimiter+ str(float(reading_temperature))+delimiter+str(float(reading_humidity))+'\n\r')


    ard.close()    
    time.sleep(3)
    print('saved to local')
    time.sleep(sleep_time_seconds)        
      


