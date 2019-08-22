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
    3*scales
    6*teros-12 sensors
    7*sht31 humidity sensors
"""
#------------------- Constants and Ports Information---------------------------

SCREEN_DISPLAY=True
SAVE_TO_FILE=True
DELIMITER=','
SLEEP_TIME_SECONDS=47*60 # s
#SERIAL_PORT='/dev/ttyS0' # datalogger version 2 uses ttyS0
SERIAL_PORT='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2:1.0' # datalogger version 1 uses ttyACM0

#---------------------- Create csv file to store data -------------------------

file_name= 'kathy_portbris_enclosure_1.csv'
fid= open(file_name,'a',0)
fid.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')
          
#---------------------------- Initiation --------------------------------------

with open('/home/pi/pyduino/credential/kathy_portbris_enclosure_1.json') as f: 
    credential = json.load(f)

field_name=['scale1','scale2','scale3',
            'raw1','raw2','raw3','raw4','raw5','raw6',
            'ec1','ec2','ec3','ec4','ec5','ec6',
            'dp1','dp2','dp3','dp4','dp5','dp6',
            'mo1','mo2','mo3','mo4','mo5','mo6',
            'sht33_temp_1','sht33_temp_2','sht33_temp_3','sht33_temp_4',
            'sht33_temp_5','sht33_temp_6','sht33_temp_7',
            'sht33_humidity_1','sht33_humidity_2','sht33_humidity_3','sht33_humidity_4',
            'sht33_humidity_5','sht33_humidity_6','sht33_humidity_7']

kathy_portbris_enclosure_1 = dict((el,0.0) for el in field_name)
pht_kathy_portbris_enclosure_1 = Phant(publicKey=credential['public_kathy_portbris_enclosure_1'],
                                       fields=field_name,
                                       privateKey=credential['private_kathy_portbris_enclosure_1'],
                                       baseUrl=credential['nectar_address'])
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
            kathy_portbris_enclosure_1['ec1']=float(current_read.split(',')[-2])
            kathy_portbris_enclosure_1['raw1']=float(current_read.split(',')[-4])
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
            kathy_portbris_enclosure_1['ec2']=float(current_read.split(',')[-2])
            kathy_portbris_enclosure_1['raw2']=float(current_read.split(',')[-4])
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
            kathy_portbris_enclosure_1['ec3']=float(current_read.split(',')[-2])
            kathy_portbris_enclosure_1['raw3']=float(current_read.split(',')[-4])
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
            kathy_portbris_enclosure_1['ec4']=float(current_read.split(',')[-2])
            kathy_portbris_enclosure_1['raw4']=float(current_read.split(',')[-4])
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
            kathy_portbris_enclosure_1['ec5']=float(current_read.split(',')[-2])
            kathy_portbris_enclosure_1['raw5']=float(current_read.split(',')[-4])
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
            kathy_portbris_enclosure_1['ec6']=float(current_read.split(',')[-2])
            kathy_portbris_enclosure_1['raw6']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('teros-12 sensor No.6 reading failed')

#----------------------------Humidity sensor sht31-------------------------------
#---------------------------Hunmidity sensor No.1-------------------------
        try:
            ard.write("9548,2,type,sht31,power,6,debug,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_1['sht33_temp_1']=float(current_read[-2])
            kathy_portbris_enclosure_1['sht33_humidity_1']=float(current_read[-1])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('humidity sensor No.1 reading failed')
#---------------------------Hunmidity sensor No.2-------------------------
        try:
            ard.write("9548,3,type,sht31,power,6,debug,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_1['sht33_temp_2']=float(current_read[-2])
            kathy_portbris_enclosure_1['sht33_humidity_2']=float(current_read[-1])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('humidity sensor No.2 reading failed')
#---------------------------Hunmidity sensor No.3-------------------------
        try:
            ard.write("9548,4,type,sht31,power,6,debug,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_1['sht33_temp_3']=float(current_read[-2])
            kathy_portbris_enclosure_1['sht33_humidity_3']=float(current_read[-1])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('humidity sensor No.3 reading failed')
#---------------------------Hunmidity sensor No.4-------------------------
        try:
            ard.write("9548,5,type,sht31,power,6,debug,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_1['sht33_temp_4']=float(current_read[-2])
            kathy_portbris_enclosure_1['sht33_humidity_4']=float(current_read[-1])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('humidity sensor No.4 reading failed')
#---------------------------Hunmidity sensor No.5-------------------------
        try:
            ard.write("9548,1,type,sht31,power,6,debug,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_1['sht33_temp_5']=float(current_read[-2])
            kathy_portbris_enclosure_1['sht33_humidity_5']=float(current_read[-1])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('humidity sensor No.5 reading failed')
#---------------------------Hunmidity sensor No.6-------------------------
        try:
            ard.write("9548,0,type,sht31,power,6,debug,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_1['sht33_temp_6']=float(current_read[-2])
            kathy_portbris_enclosure_1['sht33_humidity_6']=float(current_read[-1])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('humidity sensor No.6 reading failed')
#---------------------------Hunmidity sensor No.7-------------------------
        try:
            ard.write("9548,6,type,sht31,power,6,debug,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_1['sht33_temp_7']=float(current_read[-2])
            kathy_portbris_enclosure_1['sht33_humidity_7']=float(current_read[-1])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('humidity sensor No.7 reading failed')


#---------------------------------scales---------------------------------------
#---------------------------------scale 1---------------------------
        try:
            ard.write("analog,8,power,32,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_1['scale1']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('scale 1 reading failed')
#---------------------------------scale 2---------------------------
        try:
            ard.write("analog,9,power,30,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_1['scale2']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('scale 2 reading failed')
#---------------------------------scale 3---------------------------
        try:
            ard.write("analog,10,power,28,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_1['scale3']=float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('scale 3 reading failed')            
 

#----------------------------Upload data -----------------------------------    
    
        ard.close()
    
        client.publish('v1/devices/me/telemetry', json.dumps(kathy_portbris_enclosure_1), 1)    
        upload_phant(pht_kathy_portbris_enclosure_1,kathy_portbris_enclosure_1,SCREEN_DISPLAY)
    
        if SAVE_TO_FILE: fid.write("\n\r")
        time.sleep(SLEEP_TIME_SECONDS) # sleep to the next loop

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
