import time
import json
import serial
import paho.mqtt.client as mqtt
from time import sleep,localtime,strftime
import RPi.GPIO as GPIO
import sys, os, re, time, fcntl
from datetime import datetime   #required by is_time_between
from datetime import time as time2

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def reset():
    pin = 27
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(5)

def is_time_between(begin_time, end_time, check_time=None):
    check_time = datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

#---------------------- Define constants --------------------------------------
SCREEN_DISPLAY=True
SAVE_TO_FILE=True
DELIMITER=','
SLEEP_TIME_SECONDS=60  *20# s
SERIAL_PORT='/dev/ttyS0'
#---------------------- Create csv file to store data -------------------------
file_name= 'ewatering_sa1_sensor.csv'
fid= open(file_name,'a',0)
fid.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')
#---------------------------- Initiation --------------------------------------
with open('/home/pi/pyduino/credential/ewatering.json') as f: 
    credential = json.load(f)

print("RESET Arduino")
reset()
GPIO.cleanup()


ewatering_sa1_sensor = {}

try:
    client = mqtt.Client()
    client.username_pw_set(credential['access_token'])
    client.connect(credential['thingsboard_host'], 1883, 60)
    client.loop_start()
    print("Successfully connected to thingsboard")
except Exception:
    print("Failed to connect to thingsboard")
    time.sleep(30)

camera_switch_status=0

#----------------------Display current time and start Arduino ----------------------
    
while True:
    ewatering_sa1_sensor = {}  #ensure 

    if SCREEN_DISPLAY: print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    if SAVE_TO_FILE: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime()))

    ard = serial.Serial(SERIAL_PORT,timeout=20)
    time.sleep(5)


#--------------------------- camera switch-------------------------------
    whether_time_for_camera_on=is_time_between(time2(7,30), time2(16,40))   #brisbane time
    if whether_time_for_camera_on and camera_switch_status ==False:
        if SCREEN_DISPLAY: print("time for powering camera")
        if SAVE_TO_FILE: fid.write("time for powering camera")
        ard.write("power_switch,8,power_switch_status,1")
        ard.flushInput()
        msg=ard.readline()
        if SCREEN_DISPLAY: print (msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        camera_switch_status =1
        time.sleep(120)
    elif whether_time_for_camera_on and camera_switch_status:
        if SCREEN_DISPLAY: print("camera keeps on")
        if SAVE_TO_FILE: fid.write("camera keeps on ")
    elif whether_time_for_camera_on==False and camera_switch_status:
        if SCREEN_DISPLAY: print("time for shut down camera")
        if SAVE_TO_FILE: fid.write("time for shut down camera")
        ard.write("power_switch,8,power_switch_status,0")
        ard.flushInput()
        msg=ard.readline()
        if SCREEN_DISPLAY: print (msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        camera_switch_status =0
        time.sleep(180)
    elif whether_time_for_camera_on==False and camera_switch_status==False:
        if SCREEN_DISPLAY: print("camera keeps off")
        if SAVE_TO_FILE: fid.write("camera keeps off ")

    time.sleep(5)

#------------------------ on board humidity sensor -------------------------------
    try:
        ard.write("dht22,54,power,2,points,2,dummies,1,interval_mm,200,debug,1")
        ard.flushInput()
        msg=ard.readline()
        current_read=msg.split(',')[0:-1]
        ewatering_sa1_sensor['sa1_rh_logger']=float(current_read[-1])
        ewatering_sa1_sensor['sa1_temp_logger']=float(current_read[-2])
        if SCREEN_DISPLAY: print (msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
    except Exception as e:
        if SCREEN_DISPLAY:
            print (e)
            print ('on board humidty reading failed')
    time.sleep(5)
#-------------------------- System voltage ---------------------------------------
    try:
        ard.write("analog,15,power,9,points,5,dummies,3,interval_mm,200")
        ard.flushInput()
        msg=ard.readline()
        current_read=float(msg.split(',')[-2])
        ewatering_sa1_sensor['sa1_volt']=float(current_read)
        if SCREEN_DISPLAY: print ('raw System Voltage: ' + str(ewatering_sa1_sensor['sa1_volt']))
        if SAVE_TO_FILE:fid.write(DELIMITER + str(ewatering_sa1_sensor['sa1_volt']) + '\n')			 
    except Exception as e:
        if SCREEN_DISPLAY:
    	    print (e)
    	    print ('system voltage reading failed')
    time.sleep(5)
#--------------------------- Wind direction ----------------------------------------
    try:
        ard.write("analog,8,power,49,point,3,interval_mm,200,debug,0")
        ard.flushInput()
        msg=ard.readline()
        current_read = float(msg.split(',')[-2])
        ewatering_sa1_sensor['wind_direction']=float(current_read)
        if SCREEN_DISPLAY: print ('Wind direction: ' + str(ewatering_sa1_sensor['wind_direction']))
        if SAVE_TO_FILE:fid.write(DELIMITER + str(ewatering_sa1_sensor['wind_direction']) + '\n')
    except Exception as e:
        if SCREEN_DISPLAY:
            print (e)
            print ('wind direction reading failed')
    time.sleep(5)
#--------------Temperature, humidity and UV sensor----------------------------------
    try:
        ard.write("power_switch,30,power_switch_status,1")
        ard.flushInput()            
        time.sleep(1)
        ard.write("power_switch,31,power_switch_status,1")
        ard.flushInput()
        time.sleep(1)
        ard.write("power_switch,32,power_switch_status,1")
        ard.flushInput()
        time.sleep(3) #It is VERY IMPORTANT to set a time delay after switching on power channels for I2C because humiditity sensors would not get reading successfully if the measurement is conducted immediately.

        ard.write("9548,2,type,5803,points,3,dummies,3,debug,1,interval_mm,1000")
        ard.flushInput()
        msg_5803_channel0=ard.readline()        
        if SAVE_TO_FILE: fid.write(DELIMITER+msg_5803_channel0)
        if SCREEN_DISPLAY: print msg_5803_channel0.rstrip()
        current_read=msg_5803_channel0.split(',')
        ewatering_sa1_sensor['sa1_p_5803']=(float(current_read[-2])+float(current_read[-4])+float(current_read[-5])+float(current_read[-6]))/4.
        ewatering_sa1_sensor['sa1_t_5803']=float(current_read[-3])

#------------------------Humidity sensor SHT31-----------------------------------------------			
        ard.write("9548,0,type,sht31,debug,1")
        ard.flushInput()
        msg=ard.readline()
        time.sleep(5)
        current_read = msg.split(',')[0:-1]
        ewatering_sa1_sensor['sa1_sht31_temp_1'] = float(current_read[-2])
        ewatering_sa1_sensor['sa1_sht31_humidity_1'] = float(current_read[-1])
        if SCREEN_DISPLAY: print('Temp: ' + str(ewatering_sa1_sensor['sa1_sht31_temp_1'])  + DELIMITER + 'Rh: ' + str(ewatering_sa1_sensor['sa1_sht31_humidity_1']) + '%')  #u"\u2103" is the unicode for celsius degree
        if SAVE_TO_FILE: fid.write(DELIMITER + str(ewatering_sa1_sensor['sa1_sht31_temp_1']) + DELIMITER + str(ewatering_sa1_sensor['sa1_sht31_humidity_1']) + '\n')
#------------------------------UV sensor-----------------------------------------------
        ard.write("9548,1,type,si1145,debug,1")
        ard.flushInput()
        msg=ard.readline()
        time.sleep(12)
        current_read=msg.split(',')[0:-1]
        ewatering_sa1_sensor['sa1_uv']=float(current_read[-1])  #ultraviolet index
        ewatering_sa1_sensor['sa1_ir']=float(current_read[-3])  #Infrared light
        ewatering_sa1_sensor['sa1_vis']=float(current_read[-5]) #visible light
        if SCREEN_DISPLAY: print (msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)


   #  switch off power
        ard.write("power_switch,30,power_switch_status,0")
        time.sleep(1)
        ard.flushInput()
        ard.write("power_switch,31,power_switch_status,0")
        time.sleep(1)
        ard.flushInput()
        ard.write("power_switch,32,power_switch_status,0")
        ard.flushInput()
        time.sleep(5)

    except Exception as e :
        if SCREEN_DISPLAY: print (e)
        if SCREEN_DISPLAY: print ('9548 reading  failed')
    		
#------------------------teros-12 No.1-----------------------------
    try:
        ard.write("SDI-12,62,power,22,default_cmd,read,debug,1")
        ard.flushInput()
        msg=ard.readline()        
        current_read=msg.split('Addr')[-1]     
        ewatering_sa1_sensor['sa1_ec1']=float(current_read.split(',')[-2])
        ewatering_sa1_sensor['sa1_temp1']=float(current_read.split(',')[-3])            
        ewatering_sa1_sensor['sa1_raw1']=float(current_read.split(',')[-4])
        if SCREEN_DISPLAY: print (msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        time.sleep(5)
    except Exception as e :
        if SCREEN_DISPLAY:
    	    print (e)
            print ('MO1 reading failed')

#------------------------teros-12 No.2-----------------------------
    try:
        ard.write("SDI-12,63,power,23,default_cmd,read,debug,1")
        ard.flushInput()
        msg=ard.readline()        
        current_read=msg.split('Addr')[-1]     
        ewatering_sa1_sensor['sa1_ec2']=float(current_read.split(',')[-2])
        ewatering_sa1_sensor['sa1_temp2']=float(current_read.split(',')[-3])            
        ewatering_sa1_sensor['sa1_raw2']=float(current_read.split(',')[-4])
        if SCREEN_DISPLAY: print (msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        time.sleep(5)
    except Exception as e :
        if SCREEN_DISPLAY:
    	    print(e)
            print('MO2 reading failed')

#------------------------teros-12 No.3-----------------------------
    try:
        ard.write("SDI-12,64,power,24,default_cmd,read,debug,1")
        ard.flushInput()
        msg=ard.readline()        
        current_read=msg.split('Addr')[-1]     
        ewatering_sa1_sensor['sa1_ec3']=float(current_read.split(',')[-2])
        ewatering_sa1_sensor['sa1_temp3']=float(current_read.split(',')[-3])            
        ewatering_sa1_sensor['sa1_raw3']=float(current_read.split(',')[-4])
        if SCREEN_DISPLAY: print(msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        time.sleep(5)
    except Exception as e :
        if SCREEN_DISPLAY:
    	    print(e)
            print('MO3 reading failed')

#------------------------teros-12 No.4-----------------------------
    try:
        ard.write("SDI-12,65,power,25,default_cmd,read,debug,1")
        ard.flushInput()
        msg=ard.readline()        
        current_read=msg.split('Addr')[-1]     
        ewatering_sa1_sensor['sa1_ec4']=float(current_read.split(',')[-2])
        ewatering_sa1_sensor['sa1_temp4']=float(current_read.split(',')[-3])            
        ewatering_sa1_sensor['sa1_raw4']=float(current_read.split(',')[-4])
        if SCREEN_DISPLAY: print(msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        time.sleep(5)
    except Exception as e :
        if SCREEN_DISPLAY:
    	    print(e)
            print('MO4 reading failed')

#------------------------teros-12 No.5-----------------------------
    try:
        ard.write("SDI-12,66,power,26,default_cmd,read,debug,1")
        ard.flushInput()
        msg=ard.readline()        
        current_read=msg.split('Addr')[-1]     
        ewatering_sa1_sensor['sa1_ec5']=float(current_read.split(',')[-2])
        ewatering_sa1_sensor['sa1_temp5']=float(current_read.split(',')[-3])            
        ewatering_sa1_sensor['sa1_raw5']=float(current_read.split(',')[-4])
        if SCREEN_DISPLAY: print(msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        time.sleep(5)
    except Exception as e :
        if SCREEN_DISPLAY:
    	    print(e)
            print('MO5 reading failed')
#------------------------aqua troll 200-----------------------------
try:
    ard.write("SDI-12,50,custom_cmd,aM!,debug,1")  # do measurement
    ard.flushInput()
    msg=ard.readline()        
    if SAVE_TO_FILE: fid.write(DELIMITER+msg)
    #time.sleep(5)
    #print(msg.rstrip())
    if SCREEN_DISPLAY: print msg.rstrip()
    if SAVE_TO_FILE: fid.write(DELIMITER+msg)
    

    time.sleep(5) # this appears to be important
   
    ard.write("SDI-12,50,custom_cmd,aD0!,debug,1")
    ard.flushInput()
    msg=ard.readline()        
    if SCREEN_DISPLAY: print(msg.rstrip())
    if SAVE_TO_FILE: fid.write(DELIMITER+msg)
    current_read=msg[:-3].split('+')    
    ewatering_sa1_sensor['sa1_p_piezo']=float(current_read[1])
    ewatering_sa1_sensor['sa1_t_piezo']=float(current_read[2])
    ewatering_sa1_sensor['sa1_ec_piezo']=float(current_read[3])
    time.sleep(5)
except Exception as e:
    if SCREEN_DISPLAY:
        print(e)
        print('pressure transducer reading failed')

    ard.close()
    
    client.publish('v1/devices/me/telemetry', json.dumps(ewatering_sa1_sensor), 1)    
    print('data successfully uploaded')
    
    if SAVE_TO_FILE: fid.write("\n\r")
    if SCREEN_DISPLAY: print('sleep for ' + str(SLEEP_TIME_SECONDS) + ' seconds')
    time.sleep(SLEEP_TIME_SECONDS) # sleep to the next loop

client.loop_stop()
client.disconnect()
