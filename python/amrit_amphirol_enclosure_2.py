#!/usr/bin/python
import time
import json
import serial
import subprocess
from phant import Phant
import paho.mqtt.client as mqtt
from upload_phant import upload_phant

"""
This is the code for enclosure 2.
Enclosure 2 contains:
    24*capacitive moisture sensors
    1*webcam
"""
#------------------- Constants and Ports Information---------------------------

SCREEN_DISPLAY=True
SAVE_TO_FILE=True
DELIMITER=','
SLEEP_TIME_SECONDS=30*60 # s
#SERIAL_PORT='/dev/ttyS0' # datalogger version 2 uses ttyS0
SERIAL_PORT='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.3:1.0' # datalogger version 1 uses ttyACM0

#---------------------- Create csv file to store data -------------------------

file_name= 'amrit_amphirol_enclosure_2.csv'
fid= open(file_name,'a',0)
fid.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')
          
#---------------------------- Initiation --------------------------------------

with open('/home/pi/pyduino/credential/amrit_amphirol_enclosure_2.json') as f: 
    credential = json.load(f)

#-------------------------------Sensor Layout----------------------------------
#                        ----- -----
#                        |   | |   |
#                        |E2 | |E1 |
#		         |   | |   |
#                        ----- -----
#           Back                             Back
#      --------------                   -------------- 
#      |            |                   |            |
#      |            |                   |            |
#      |            | 	         	|	     |	
#      |            |			| 	     |
# Left |   Tank B   | Right	   Left	|   Tank A   | Right
#      |            |			|	     |
#      |            |			|	     |
#      |            |			|	     |
#      |            |            	|     	     |
#      --------------                   --------------
#          Front                             Front
#
#    -------------------------------------
#    | Tank A  |  TOP  | MIDDLE | BOTTOM |
#    -------------------------------------
#    |  Front  | mo_a1 | mo_a5  | mo_a9  |
#    -------------------------------------
#    |	Right  | mo_a2 | mo_a6  | mo_a10 |
#    -------------------------------------
#    |  Left   | mo_a3 | mo_a7  | mo_a11 |
#    -------------------------------------
#    |  Back   | mo_a4 | mo_a8  | mo_a12 |
#    -------------------------------------
#    -------------------------------------
#    | Tank B  |  TOP  | MIDDLE | BOTTOM |
#    -------------------------------------
#    |  Front  | mo_b1 | mo_b5  | mo_b9  |
#    -------------------------------------
#    |  Right  | mo_b2 | mo_b6  | mo_b10 |
#    -------------------------------------
#    |  Left   | mo_b3 | mo_b7  | mo_b11 |
#    -------------------------------------
#    |  Back   | mo_b4 | mo_b8  | mo_b12 |
#    -------------------------------------
#---------------------------------------------------------------------------------
field_name=['mo_a1','mo_a2','mo_a3','mo_a4','mo_a5','mo_a6','mo_a7','mo_a8','mo_a9','mo_a10','mo_a11','mo_a12',
            'mo_b1','mo_b2','mo_b3','mo_b4','mo_b5','mo_b6','mo_b7','mo_b8','mo_b9','mo_b10','mo_b11','mo_b12']

amrit_amphirol_enclosure_2 = dict((el,0.0) for el in field_name)

try:
    client = mqtt.Client()
    client.username_pw_set(credential['access_token'])
    client.connect(credential['thingsboard_host'], 1883, 60)
    client.loop_start()
except Exception:
    print("Failed to connect to thingsboard")
    time.sleep(30)
 
try:    
    while True:
        ard = serial.Serial(SERIAL_PORT,timeout=60)
	time.sleep(5)

#---------------------------------Moisture Sensors---------------------------------------
#---------------------------------mo_a1---------------------------
        try:
            ard.write("analog,5,power,25,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_a1']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_a1 reading failed')
#---------------------------------mo_a2---------------------------
        try:
            ard.write("analog,5,power,24,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_a2']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_a2 reading failed')
#---------------------------------mo_a3---------------------------
        try:
            ard.write("analog,4,power,41,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_a3']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_a3 reading failed')
#---------------------------------mo_a4---------------------------
        try:
            ard.write("analog,4,power,35,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_a4']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_a4 reading failed')
#---------------------------------mo_a5---------------------------
        try:
            ard.write("analog,5,power,9,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_a5']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_a5 reading failed')
#---------------------------------mo_a6---------------------------
        try:
            ard.write("analog,5,power,22,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_a6']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_a6 reading failed')
#---------------------------------mo_a7---------------------------
        try:
            ard.write("analog,4,power,27,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_a7']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_a7 reading failed')
#---------------------------------mo_a8---------------------------
        try:
            ard.write("analog,4,power,37,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_a8']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_a8 reading failed')
#---------------------------------mo_a9---------------------------
        try:
            ard.write("analog,5,power,8,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_a9']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_a9 reading failed')
#---------------------------------mo_a10---------------------------
        try:
            ard.write("analog,5,power,23,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_a10']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_a10 reading failed')
#---------------------------------mo_a11---------------------------
        try:
            ard.write("analog,4,power,29,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_a11']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_a11 reading failed')
#---------------------------------mo_a12---------------------------
        try:
            ard.write("analog,4,power,39,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_a12']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_a12 reading failed')
#---------------------------------mo_b1---------------------------
        try:
            ard.write("analog,10,power,44,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_b1']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_b1 reading failed')
#---------------------------------mo_b2---------------------------
        try:
            ard.write("analog,13,power,44,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_b2']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_b2 reading failed')
#---------------------------------mo_b3---------------------------
        try:
            ard.write("analog,1,power,42,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_b3']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_b3 reading failed')
#---------------------------------mo_b4---------------------------
        try:
            ard.write("analog,0,power,42,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_b4']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_b4 reading failed')
#---------------------------------mo_b5---------------------------
        try:
            ard.write("analog,9,power,44,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_b5']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_b5 reading failed')
#---------------------------------mo_b6---------------------------
        try:
            ard.write("analog,2,power,42,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_b6']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_b6 reading failed')
#---------------------------------mo_b7---------------------------
        try:
            ard.write("analog,4,power,31,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_b7']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_b7 reading failed')
#---------------------------------mo_b8---------------------------
        try:
            ard.write("analog,15,power,44,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_b8']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_b8 reading failed')
#---------------------------------mo_b9---------------------------
        try:
            ard.write("analog,8,power,44,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_b9']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_b9 reading failed')
#---------------------------------mo_b10---------------------------
        try:
            ard.write("analog,11,power,44,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_b10']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_b10 reading failed')
#---------------------------------mo_b11---------------------------
        try:
            ard.write("analog,3,power,42,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_b11']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_b11 reading failed')
#---------------------------------mo_b12---------------------------
        try:
            ard.write("analog,14,power,44,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_2['mo_b12']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('mo_b12 reading failed')
 

#----------------------------Upload data -----------------------------------    
    
        ard.close()
    
        client.publish('v1/devices/me/telemetry', json.dumps(amrit_amphirol_enclosure_2), 1)    
        print('data successfully uploaded')      
        if SAVE_TO_FILE: fid.write("\n\r")
        time.sleep(SLEEP_TIME_SECONDS) # sleep to the next loop

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
