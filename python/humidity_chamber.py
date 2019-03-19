#!/usr/bin/python
import serial
import time
import numpy as np
import sys
from phant import Phant
import paho.mqtt.client as mqtt
import json
import serial_openlock
import get_ip
from upload_phant import upload_phant
import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep,gmtime, strftime,localtime             # lets us have a delay  
import subprocess



with open('/home/pi/pyduino/credential/humchamber.json') as f:
        credential = json.load(f) #,object_pairs_hook=collections.OrderedDict)


field_name=['dht22_rh','dht22_t','rh0','rh1','rh2','rh3','rh4','rh5','rh6','rh7','t0','t1','t2','t3','t4','t5','t6','t7','volt0']
humchamber=dict((el,0.0) for el in field_name)
pht_humchamber = Phant(publicKey=credential['public_humchamber'],fields=field_name,privateKey=credential['private_humchamber'],baseUrl=credential['nectar_address'])


#port_sensor  = 'USB VID:PID=2341:0042 SNR=55639303035351A04171'
#port_sensor = '/dev/ttyACM0'  # remember when using device at /dev/folder rather than USB VID:PID, serial_openlock needs to have match_existing=False
port_sensor = '/dev/ttyS0' # port for serial connection 



# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'pizo.csv'

sleep_time_seconds=30*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


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


if save_to_file: fid= open(file_name,'a',0)


try:

    while True: 

        if screen_display: print strftime("%Y-%m-%d %H:%M:%S", localtime())
        if save_to_file: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime())  )
     
    
        ard=serial.Serial(port_sensor,timeout=60)
        msg=ard.write("power_switch,22,power_switch_status,1")
        msg=ard.flushInput()
        sleep(5)

        msg=ard.write("power_switch,23,power_switch_status,1")
        msg=ard.flushInput()
        sleep(5)

        msg=ard.write("power_switch,24,power_switch_status,1")
        msg=ard.flushInput()
        sleep(5)

        msg=ard.write("power_switch,25,power_switch_status,1")
        msg=ard.flushInput()
        sleep(5)

        msg1=ard.write("9548,0,type,sht31,dummies,1,power,28,debug,1,points,1,timeout,60")
        msg1=ard.flushInput()
        msg1=ard.readline()
        sleep(5)

        msg2=ard.write("9548,1,type,sht31,dummies,1,power,28,debug,1,points,1,timeout,60")
        msg2=ard.flushInput()
        msg2=ard.readline()
        sleep(5)

        msg3=ard.write("9548,2,type,sht31,dummies,1,power,28,debug,1,points,1,timeout,60")
        msg3=ard.flushInput()
        msg3=ard.readline()
        sleep(5)

        msg4=ard.write("9548,3,type,sht31,dummies,1,power,28,debug,1,points,1,timeout,60")
        msg4=ard.flushInput()
        msg4=ard.readline()
        sleep(5)

        msg5=ard.write("9548,4,type,sht31,dummies,1,power,28,debug,1,points,1,timeout,60")
        msg5=ard.flushInput()
        msg5=ard.readline()
        sleep(5)

        msg6=ard.write("9548,5,type,sht31,dummies,1,power,28,debug,1,points,1,timeout,60")
        msg6=ard.flushInput()
        msg6=ard.readline()
        sleep(5)

        msg7=ard.write("9548,6,type,sht31,dummies,1,power,28,debug,1,points,1,timeout,60")
        msg7=ard.flushInput()
        msg7=ard.readline()
        sleep(5)

        msg8=ard.write("9548,7,type,sht31,dummies,1,power,28,debug,1,points,1,timeout,60")
        msg8=ard.flushInput()
        msg8=ard.readline()
        sleep(5)

        msg=ard.write("power_switch,22,power_switch_status,0")
        msg=ard.flushInput()
        sleep(5)

        msg=ard.write("power_switch,23,power_switch_status,0")
        msg=ard.flushInput()
        sleep(5)
    
        msg=ard.write("power_switch,24,power_switch_status,0")
        msg=ard.flushInput()
        sleep(5)

        msg=ard.write("power_switch,25,power_switch_status,0")
        msg=ard.flushInput()
        sleep(5)


        if screen_display: print msg1.rstrip()
        if save_to_file: fid.write(delimiter+msg1.rstrip())
        current_read=msg1.split(',')[0:-1]
        humchamber['rh0']=float(current_read[-1])
        humchamber['t0']=float(current_read[-2])
    
    
        if screen_display: print msg2.rstrip()
        if save_to_file: fid.write(delimiter+msg2.rstrip())
        current_read=msg2.split(',')[0:-1]
        humchamber['rh1']=float(current_read[-1])
        humchamber['t1']=float(current_read[-2])
    
        if screen_display: print msg3.rstrip()
        if save_to_file: fid.write(delimiter+msg3.rstrip())
        current_read=msg3.split(',')[0:-1]
        humchamber['rh2']=float(current_read[-1])
        humchamber['t2']=float(current_read[-2])


        if screen_display: print msg4.rstrip()
        if save_to_file: fid.write(delimiter+msg4.rstrip())
        current_read=msg4.split(',')[0:-1]
        humchamber['rh3']=float(current_read[-1])
        humchamber['t3']=float(current_read[-2])


        if screen_display: print msg5.rstrip()
        if save_to_file: fid.write(delimiter+msg5.rstrip())
        current_read=msg5.split(',')[0:-1]
        humchamber['rh4']=float(current_read[-1])
        humchamber['t4']=float(current_read[-2])


        if screen_display: print msg6.rstrip()
        if save_to_file: fid.write(delimiter+msg6.rstrip())
        current_read=msg6.split(',')[0:-1]
        humchamber['rh5']=float(current_read[-1])
        humchamber['t5']=float(current_read[-2])


        if screen_display: print msg7.rstrip()
        if save_to_file: fid.write(delimiter+msg7.rstrip())
        current_read=msg7.split(',')[0:-1]
        humchamber['rh6']=float(current_read[-1])
        humchamber['t6']=float(current_read[-2])

        if screen_display: print msg8.rstrip()
        if save_to_file: fid.write(delimiter+msg8.rstrip())
        current_read=msg8.split(',')[0:-1]
        humchamber['rh7']=float(current_read[-1])
        humchamber['t7']=float(current_read[-2])


        msg=ard.write("analog,15,power,9,point,3,interval_mm,200,debug,1")
        msg=ard.flushInput()
        msg=ard.readline()
    
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        humchamber['volt0']=float(current_read[-1])
        sleep(2)
    
        msg=ard.write("dht22,54,power,2,points,2,dummies,1,interval_mm,2000,debug,1")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        humchamber['dht22_rh']=float(current_read[-1])
        humchamber['dht22_t']=float(current_read[-2])
        sleep(2)

        ard.close()
    
        client.publish('v1/devices/me/telemetry', json.dumps(humchamber), 1)    
        upload_phant(pht_humchamber,humchamber,screen_display)
    
        if save_to_file: fid.write("\n\r")
        # sleep to the next loop
        time.sleep(sleep_time_seconds)

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()

