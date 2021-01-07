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
    7*suction sensors
    7*ms5803 pressure sensors
"""
#------------------- Constants and Ports Information---------------------------

SCREEN_DISPLAY=True
SAVE_TO_FILE=True
DELIMITER=','
HEAT_TIME=6000 # ms 
SLEEP_TIME_SECONDS=40*60 # s
#SERIAL_PORT='/dev/ttyS0' # datalogger version 2 uses ttyS0
SERIAL_PORT='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.3:1.0' # datalogger version 1 uses ttyACM0

#---------------------- Create csv file to store data -------------------------

file_name= 'kathy_portbris_enclosure_2.csv'
fid= open(file_name,'a',0)
fid.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')
          
#---------------------------- Initiation --------------------------------------

with open('/home/pi/pyduino/credential/kathy_portbris_enclosure_2.json') as f: 
    credential = json.load(f)

field_name=['delta_t1','delta_t2','delta_t3','delta_t4','delta_t5','delta_t6','delta_t7',
            'pressure_1','pressure_2','pressure_3','pressure_4','pressure_5',
            'pressure_6','pressure_7',
            't1_low','t1_high','t2_low','t2_high','t3_low','t3_high','t4_low','t4_high',
            't5_low','t5_high','t6_low','t6_high','t7_low','t7_high']

kathy_portbris_enclosure_2 = dict((el,0.0) for el in field_name)
pht_kathy_portbris_enclosure_2 = Phant(publicKey=credential['public_kathy_portbris_enclosure_2'],
                                       fields=field_name,
                                       privateKey=credential['private_kathy_portbris_enclosure_2'],
                                       baseUrl=credential['nectar_address'])

try:
    client = mqtt.Client()
    client.username_pw_set(credential['access_token'])
    client.connect(credential['thingsboard_host'], 1883, 60)
    client.loop_start()
    print("Successfully publish to thingsboard")
except Exception:
    print("Failed to publish to thingsboard")
    time.sleep(30)
 
try:    
    while True:
        ard = serial.Serial(SERIAL_PORT,timeout=60)
        time.sleep(5)
#----------------------------suction sensors-----------------------------------
#----------------------------suction sensor 1----------------------------
        try:
            ard.write("fred,280BC7A00A000056,dgin,50,snpw,6,htpw,34,itv,"+str(HEAT_TIME)+",otno,5")
            ard.flushInput()
            msg=ard.readline()      
            current_read=msg.split(',')[1:-1]
            kathy_portbris_enclosure_2['t1_low']=float(current_read[2])
            kathy_portbris_enclosure_2['t1_high']=float(current_read[7])  
            kathy_portbris_enclosure_2['delta_t1']=float(current_read[7])-float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg.rstrip()+'\n')  
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY: print('suction sensor No.1 reading failed')
#----------------------------suction sensor 2----------------------------
        try:
            ard.write("fred,2875D6A00A00006C,dgin,50,snpw,6,htpw,36,itv,"+str(HEAT_TIME)+",otno,5")
            ard.flushInput()
            msg=ard.readline()      
            current_read=msg.split(',')[1:-1]
            kathy_portbris_enclosure_2['t2_low']=float(current_read[2])
            kathy_portbris_enclosure_2['t2_high']=float(current_read[7])  
            kathy_portbris_enclosure_2['delta_t2']=float(current_read[7])-float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg.rstrip()+'\n')  
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY: print('suction sensor No.2 reading failed')
#----------------------------suction sensor 3----------------------------
        try:
            ard.write("fred,2874D6A00A00005B,dgin,50,snpw,6,htpw,38,itv,"+str(HEAT_TIME)+",otno,5")
            ard.flushInput()
            msg=ard.readline()      
            current_read=msg.split(',')[1:-1]
            kathy_portbris_enclosure_2['t3_low']=float(current_read[2])
            kathy_portbris_enclosure_2['t3_high']=float(current_read[7])  
            kathy_portbris_enclosure_2['delta_t3']=float(current_read[7])-float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg.rstrip()+'\n')  
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY: print('suction sensor No.3 reading failed')
#----------------------------suction sensor 4----------------------------
        try:
            ard.write("fred,288A40A10A00009E,dgin,50,snpw,6,htpw,40,itv,"+str(HEAT_TIME)+",otno,5")
            ard.flushInput()
            msg=ard.readline()      
            current_read=msg.split(',')[1:-1]
            kathy_portbris_enclosure_2['t4_low']=float(current_read[2])
            kathy_portbris_enclosure_2['t4_high']=float(current_read[7])  
            kathy_portbris_enclosure_2['delta_t4']=float(current_read[7])-float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg.rstrip()+'\n')  
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY: print('suction sensor No.4 reading failed')
#----------------------------suction sensor 5----------------------------
        try:
            ard.write("fred,28FDF0A00A000043,dgin,50,snpw,6,htpw,26,itv,"+str(HEAT_TIME)+",otno,5")
            ard.flushInput()
            msg=ard.readline()      
            current_read=msg.split(',')[1:-1]
            kathy_portbris_enclosure_2['t5_low']=float(current_read[2])
            kathy_portbris_enclosure_2['t5_high']=float(current_read[7])  
            kathy_portbris_enclosure_2['delta_t5']=float(current_read[7])-float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg.rstrip()+'\n')  
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY: print('suction sensor No.5 reading failed')
#----------------------------suction sensor 6----------------------------
        try:
            ard.write("fred,28BC1BA10A000024,dgin,50,snpw,6,htpw,28,itv,"+str(HEAT_TIME)+",otno,5")
            ard.flushInput()
            msg=ard.readline()      
            current_read=msg.split(',')[1:-1]
            kathy_portbris_enclosure_2['t6_low']=float(current_read[2])
            kathy_portbris_enclosure_2['t6_high']=float(current_read[7])  
            kathy_portbris_enclosure_2['delta_t6']=float(current_read[7])-float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg.rstrip()+'\n')  
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY: print('suction sensor No.6 reading failed')
#----------------------------suction sensor 7----------------------------
        try:
            ard.write("fred,282C1AA10A000058,dgin,50,snpw,6,htpw,30,itv,"+str(HEAT_TIME)+",otno,5")
            ard.flushInput()
            msg=ard.readline()      
            current_read=msg.split(',')[1:-1]
            kathy_portbris_enclosure_2['t7_low']=float(current_read[2])
            kathy_portbris_enclosure_2['t7_high']=float(current_read[7])  
            kathy_portbris_enclosure_2['delta_t7']=float(current_read[7])-float(current_read[2])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg.rstrip()+'\n')  
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY: print('suction sensor No.7 reading failed')



#----------------------------Pressure sensor ms5803-------------------------------
#---------------------------Pressure sensor No.1-------------------------
        try:
            ard.write("9548,2,type,5803,power,42,debug,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_2['pressure_1']=float(current_read[-1])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY: print('Pressure sensor No.1 reading failed')
#---------------------------Pressure sensor No.2-------------------------
        try:
            ard.write("9548,3,type,5803,power,42,debug,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_2['pressure_2']=float(current_read[-1])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY: print('Pressure sensor No.2 reading failed')
#---------------------------Pressure sensor No.3-------------------------
        try:
            ard.write("9548,4,type,5803,power,42,debug,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_2['pressure_3']=float(current_read[-1])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY: print('Pressure sensor No.3 reading failed')
#---------------------------Pressure sensor No.4-------------------------
        try:
            ard.write("9548,5,type,5803,power,42,debug,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_2['pressure_4']=float(current_read[-1])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY: print('Pressure sensor No.4 reading failed')
#---------------------------Pressure sensor No.5-------------------------
        try:
            ard.write("9548,1,type,5803,power,42,debug,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_2['pressure_5']=float(current_read[-1])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY: print('Pressure sensor No.5 reading failed')
#---------------------------Pressure sensor No.6-------------------------
        try:
            ard.write("9548,0,type,5803,power,42,debug,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_2['pressure_6']=float(current_read[-1])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY: print('Pressure sensor No.6 reading failed')
#---------------------------Pressure sensor No.7-------------------------
        try:
            ard.write("9548,6,type,5803,power,42,debug,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            kathy_portbris_enclosure_2['pressure_7']=float(current_read[-1])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY: print('Pressure sensor No.7 reading failed')
            
#----------------------------Upload data -----------------------------------    
    
        ard.close()
    
        client.publish('v1/devices/me/telemetry', json.dumps(kathy_portbris_enclosure_2), 1)    
        upload_phant(pht_kathy_portbris_enclosure_2,kathy_portbris_enclosure_2,SCREEN_DISPLAY)
    
        if SAVE_TO_FILE: fid.write("\n\r")
        time.sleep(SLEEP_TIME_SECONDS) # sleep to the next loop

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
