import time
import json
import serial
from phant import Phant
import paho.mqtt.client as mqtt
from upload_phant import upload_phant
from time import sleep,localtime,strftime

"""
This is the code for salt marsh project.
The enclosure contains:
    9*teros-12 sensors (SDI-12)
    1*sht31 humidity sensors (I2C)
    1*UV sensor (I2C)
    1*rain gauge (incorporated in salt_marsh_weather.py)
    1*anemometer (wind direction only, wind speed is incorporated in salt_marsh_weather.py)
"""
#------------------------------ Functions--------------------------------------

def convert_to_angle(raw):
    """This function converts the output of the wind vane to angles"""
    
    if abs(raw-758)<= 5:
        angle = 0
    elif abs(raw-956)<=5:
        angle = 45
    elif abs(raw-1023)<=5:
        angle = 90
    elif abs(raw-522)<=5:
        angle = 135
    elif abs(raw-181)<=5:
        angle = 180    
    elif abs(raw-107)<=5:
        angle = 225    
    elif abs(raw-50)<=5:
        angle = 270
    elif abs(raw-330)<=5:
        angle = 315

    return angle

#------------------- Constants and Ports Information---------------------------

SCREEN_DISPLAY=True
SAVE_TO_FILE=True
DELIMITER=','
SLEEP_TIME_SECONDS=60*60 # s
SERIAL_PORT='/dev/ttyS0' # datalogger version 2 uses ttyS0
#SERIAL_PORT='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2:1.0' # datalogger version 1 uses ttyACM0

#---------------------- Create csv file to store data -------------------------

file_name= 'salt_marsh_sensor.csv'
fid= open(file_name,'a',0)
fid.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')
          
#---------------------------- Initiation --------------------------------------

with open('/home/pi/pyduino/credential/salt_marsh_sensor.json') as f: 
    credential = json.load(f)

field_name=['raw1','raw2','raw3','raw4','raw5','raw6','raw7','raw8','raw9',
            'ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9',
            'temp1','temp2','temp3','temp4','temp5','temp6','temp7','temp8','temp9',
            'sht31_temp','sht31_humidity',
            'ir','uv','vis',
            'wd']

salt_marsh_sensor = dict((el,0.0) for el in field_name)
pht_salt_marsh_sensor = Phant(publicKey=credential['public_salt_marsh_sensor'],
                                       fields=field_name,
                                       privateKey=credential['private_salt_marsh_sensor'],
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

        if SCREEN_DISPLAY: print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        if SAVE_TO_FILE: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime()))

        ard = serial.Serial(SERIAL_PORT,timeout=20)
        time.sleep(5)

#----------------------------teros-12 (GS3)------------------------------------
#---------------------------teros-12 No.1-----------------------------
        try:
            ard.write("SDI-12,53,power,22,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            salt_marsh_sensor['ec1']=float(current_read.split(',')[-2])
            salt_marsh_sensor['temp1']=float(current_read.split(',')[-3])            
            salt_marsh_sensor['raw1']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('MO1 reading failed')

#---------------------------teros-12 No.2-----------------------------
        try:
            ard.write("SDI-12,53,power,23,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            salt_marsh_sensor['ec2']=float(current_read.split(',')[-2])
            salt_marsh_sensor['temp2']=float(current_read.split(',')[-3])            
            salt_marsh_sensor['raw2']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('MO2 reading failed')

#---------------------------teros-12 No.3-----------------------------
        try:
            ard.write("SDI-12,53,power,24,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            salt_marsh_sensor['ec3']=float(current_read.split(',')[-2])
            salt_marsh_sensor['temp3']=float(current_read.split(',')[-3])            
            salt_marsh_sensor['raw3']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('MO3 reading failed')                

#---------------------------teros-12 No.4-----------------------------
        try:
            ard.write("SDI-12,53,power,25,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            salt_marsh_sensor['ec4']=float(current_read.split(',')[-2])
            salt_marsh_sensor['temp4']=float(current_read.split(',')[-3])            
            salt_marsh_sensor['raw4']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('MO4 reading failed')

#---------------------------teros-12 No.5-----------------------------
        try:
            ard.write("SDI-12,53,power,26,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            salt_marsh_sensor['ec5']=float(current_read.split(',')[-2])
            salt_marsh_sensor['temp5']=float(current_read.split(',')[-3])            
            salt_marsh_sensor['raw5']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('MO5 reading failed')
  
#---------------------------teros-12 No.6-----------------------------
        try:
            ard.write("SDI-12,53,power,27,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            salt_marsh_sensor['ec6']=float(current_read.split(',')[-2])
            salt_marsh_sensor['temp6']=float(current_read.split(',')[-3])            
            salt_marsh_sensor['raw6']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('MO6 reading failed')

#---------------------------teros-12 No.7-----------------------------
        try:
            ard.write("SDI-12,52,power,28,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            salt_marsh_sensor['ec7']=float(current_read.split(',')[-2])
            salt_marsh_sensor['temp7']=float(current_read.split(',')[-3])            
            salt_marsh_sensor['raw7']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('MO7 reading failed')

#---------------------------teros-12 No.8-----------------------------
        try:
            ard.write("SDI-12,52,power,29,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            salt_marsh_sensor['ec8']=float(current_read.split(',')[-2])
            salt_marsh_sensor['temp8']=float(current_read.split(',')[-3])            
            salt_marsh_sensor['raw8']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('MO8 reading failed')

#---------------------------teros-12 No.9-----------------------------
        try:
            ard.write("SDI-12,52,power,30,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            salt_marsh_sensor['ec9']=float(current_read.split(',')[-2])
            salt_marsh_sensor['temp9']=float(current_read.split(',')[-3])            
            salt_marsh_sensor['raw9']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception:
            if SCREEN_DISPLAY:
                print('MO9 reading failed')
            
#----------------------------Humidity sensor sht31-------------------------------
        try:
            ard.write("9548,0,type,sht31,dummies,1,power,40,debug,1,points,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            salt_marsh_sensor['sht31_temp']=float(current_read[-2])
            salt_marsh_sensor['sht31_humidity']=float(current_read[-1])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('humidity sensor reading failed')

#----------------------------UV sensor si1145-------------------------------
        try:
            ard.write("9548,1,type,si1145,dummies,1,power,40,debug,1,points,1")
            ard.flushInput()
            msg=ard.readline()
            current_read=msg.split(',')[0:-1]
            salt_marsh_sensor['uv']=float(current_read[-1]) #ultraviolet index
            salt_marsh_sensor['ir']=float(current_read[-3]) #Infrared light, unit in lm
            salt_marsh_sensor['vis']=float(current_read[-5]) #visible light, unit in lm            
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('UV sensor reading failed')

#----------------------------Wind Direction---------------------------------
#take multiple readings over a short period of time and then calculate the average value to improve the accuracy of your results

        try:
            ard.write("analog,15,power,37,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=float(msg.split(',')[-2])
            wd_1 = convert_to_angle(current_read)
            if SCREEN_DISPLAY: print('First time wind direction reading is '+str(wd_1))
        except Exception:
            if SCREEN_DISPLAY: print('First time wind direction reading failed')
            
        time.sleep(5)    
        try:
            ard.write("analog,15,power,37,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=float(msg.split(',')[-2])
            wd_2 = convert_to_angle(current_read)
            if SCREEN_DISPLAY: print('Second time wind direction reading is '+str(wd_2))
        except Exception:
            if SCREEN_DISPLAY: print('Second time wind direction reading failed')
            
        time.sleep(5)    
        try:
            ard.write("analog,15,power,37,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read=float(msg.split(',')[-2])
            wd_3 = convert_to_angle(current_read)
            if SCREEN_DISPLAY: print('Third time wind direction reading is '+str(wd_3))
        except Exception:
            if SCREEN_DISPLAY: print('Third time wind direction reading failed')
                        
        average_wd = (wd_1 + wd_2 + wd_3)/3
        salt_marsh_sensor['wd']=average_wd
        if SCREEN_DISPLAY: print('Average wind direction is '+str(average_wd)+' degree from North')
        if SAVE_TO_FILE: fid.write(DELIMITER+str(average_wd)+'\n')

#----------------------------Upload data -----------------------------------    
    
        ard.close()
    
        client.publish('v1/devices/me/telemetry', json.dumps(salt_marsh_sensor), 1)    
        upload_phant(pht_salt_marsh_sensor,salt_marsh_sensor,SCREEN_DISPLAY)
    
        if SAVE_TO_FILE: fid.write("\n\r")
        time.sleep(SLEEP_TIME_SECONDS) # sleep to the next loop

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()

