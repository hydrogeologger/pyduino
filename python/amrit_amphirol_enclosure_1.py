#!/usr/bin/python
import time
import json
import serial
import subprocess
from phant import Phant
import paho.mqtt.client as mqtt
from upload_phant import upload_phant

"""
This is the code for enclosure 1.
Enclosure 1 contains:
    20*load cells
    6*teros-12 sensors(1,2,3 in Tank A; 4,5,6 in Tank B)
"""
#------------------- Constants and Ports Information---------------------------

SCREEN_DISPLAY=True
SAVE_TO_FILE=True
DELIMITER=','
SLEEP_TIME_SECONDS=30*60 # s
#SERIAL_PORT='/dev/ttyS0' # datalogger version 2 uses ttyS0
SERIAL_PORT='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2:1.0' # datalogger version 1 uses ttyACM0

#---------------------- Create csv file to store data -------------------------

file_name= 'amrit_amphirol_enclosure_1.csv'
fid= open(file_name,'a',0)
fid.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')
          
#---------------------------- Initiation --------------------------------------

with open('/home/pi/pyduino/credential/amrit_amphirol_enclosure_1.json') as f: 
    credential = json.load(f)

field_name=['lc_a1','lc_a2','lc_a3','lc_a4','lc_a5','lc_a6','lc_a7','lc_a8','lc_a9','lc_a10',
	    'lc_b1','lc_b2','lc_b3','lc_b4','lc_b5','lc_b6','lc_b7','lc_b8','lc_b9','lc_b10',
	    'ec1','ec2','ec3','ec4','ec5','ec6',
            'raw1','raw2','raw3','raw4','raw5','raw6']

amrit_amphirol_enclosure_1 = dict((el,0.0) for el in field_name)

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

#----------------------------teros-12 (GS3)------------------------------------
#---------------------------teros-12 No.1-----------------------------
        try:
            ard.write("SDI-12,50,power,35,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            amrit_amphirol_enclosure_1['ec1']=float(current_read.split(',')[-2])
            amrit_amphirol_enclosure_1['raw1']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('teros-12 sensor No.1 reading failed')
#---------------------------teros-12 No.2-----------------------------
        try:
            ard.write("SDI-12,50,power,37,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            amrit_amphirol_enclosure_1['ec2']=float(current_read.split(',')[-2])
            amrit_amphirol_enclosure_1['raw2']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('teros-12 sensor No.2 reading failed')
#---------------------------teros-12 No.3-----------------------------
        try:
            ard.write("SDI-12,50,power,39,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            amrit_amphirol_enclosure_1['ec3']=float(current_read.split(',')[-2])
            amrit_amphirol_enclosure_1['raw3']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('teros-12 sensor No.3 reading failed')
#---------------------------teros-12 No.4-----------------------------
        try:
            ard.write("SDI-12,50,power,41,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            amrit_amphirol_enclosure_1['ec4']=float(current_read.split(',')[-2])
            amrit_amphirol_enclosure_1['raw4']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('teros-12 sensor No.4 reading failed')
#---------------------------teros-12 No.5-----------------------------
        try:
            ard.write("SDI-12,50,power,27,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            amrit_amphirol_enclosure_1['ec5']=float(current_read.split(',')[-2])
            amrit_amphirol_enclosure_1['raw5']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('teros-12 sensor No.5 reading failed')
#---------------------------teros-12 No.6-----------------------------
        try:
            ard.write("SDI-12,50,power,29,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            amrit_amphirol_enclosure_1['ec6']=float(current_read.split(',')[-2])
            amrit_amphirol_enclosure_1['raw6']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('teros-12 sensor No.6 reading failed')

#---------------------------------load cells---------------------------------------
#---------------------------------load cell a1---------------------------
        try:
            ard.write("analog,8,power,44,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_a1']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell a1 reading failed')
#---------------------------------load cell a2---------------------------
        try:
            ard.write("analog,9,power,44,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_a2']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell a2 reading failed')
#---------------------------------load cell a3---------------------------
        try:
            ard.write("analog,10,power,44,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_a3']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell a3 reading failed')
#---------------------------------load cell a4---------------------------
        try:
            ard.write("analog,11,power,44,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_a4']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell a4 reading failed')
#---------------------------------load cell a5---------------------------
        try:
            ard.write("analog,12,power,44,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_a5']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell a5 reading failed')
#---------------------------------load cell a6---------------------------
        try:
            ard.write("analog,13,power,44,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_a6']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell a6 reading failed')
#---------------------------------load cell a7---------------------------
        try:
            ard.write("analog,14,power,32,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_a7']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell a7 reading failed')
#---------------------------------load cell a8---------------------------
        try:
            ard.write("analog,14,power,30,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_a8']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell a8 reading failed')
#---------------------------------load cell a9---------------------------
        try:
            ard.write("analog,14,power,28,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_a9']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell a9 reading failed')
#---------------------------------load cell a10---------------------------
        try:
            ard.write("analog,14,power,26,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_a10']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell a10 reading failed')
#---------------------------------load cell b1---------------------------
        try:
            ard.write("analog,14,power,40,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_b1']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell b1 reading failed')
#---------------------------------load cell b2---------------------------
        try:
            ard.write("analog,14,power,38,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_b2']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell b2 reading failed')
#---------------------------------load cell b3---------------------------
        try:
            ard.write("analog,14,power,36,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_b3']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell b3 reading failed')
#---------------------------------load cell b4---------------------------
        try:
            ard.write("analog,15,power,24,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_b4']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell b4 reading failed')
#---------------------------------load cell b5---------------------------
        try:
            ard.write("analog,15,power,22,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_b5']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell b5 reading failed')
#---------------------------------load cell b6---------------------------
        try:
            ard.write("analog,15,power,23,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_b6']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell b6 reading failed')
#---------------------------------load cell b7---------------------------
        try:
            ard.write("analog,15,power,25,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_b7']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell b7 reading failed')
#---------------------------------load cell b8---------------------------
        try:
            ard.write("analog,15,power,9,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_b8']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell b8 reading failed')
#---------------------------------load cell b9---------------------------
        try:
            ard.write("analog,15,power,8,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_b9']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell b9 reading failed')
#---------------------------------load cell b10---------------------------
        try:
            ard.write("analog,15,power,7,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            amrit_amphirol_enclosure_1['lc_b10']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('load cell b10 reading failed') 
#----------------------------Upload data -----------------------------------    
    
        ard.close()
    
        client.publish('v1/devices/me/telemetry', json.dumps(amrit_amphirol_enclosure_1), 1)    
        print('data successfully uploaded')
        if SAVE_TO_FILE: fid.write("\n\r")
        time.sleep(SLEEP_TIME_SECONDS) # sleep to the next loop

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
