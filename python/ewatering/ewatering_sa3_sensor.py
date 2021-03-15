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
    #GPIO.output(pin, GPIO.HIGH)
    #time.sleep(0.32)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(5)

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

#---------------------- Define constants --------------------------------------
SCREEN_DISPLAY=True
SAVE_TO_FILE=True
DELIMITER=','
SLEEP_TIME_SECONDS=60  *30# s
SERIAL_PORT='/dev/ttyS0'
#---------------------- Create csv file to store data -------------------------
file_name= 'ewatering_sa3_sensor.csv'
fid= open(file_name,'a',0)
fid.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')
#---------------------------- Initiation --------------------------------------
with open('/home/pi/pyduino/credential/ewatering.json') as f:
    credential = json.load(f)


print("RESET Arduino")
reset()
GPIO.cleanup()

ewatering_sa3_sensor = {}

try:
    client = mqtt.Client()
    client.username_pw_set(credential['access_token'])
    client.connect(credential['thingsboard_host'], 1883, 60)
    client.loop_start()
    print("Successfully connected to thingsboard")
except Exception:
    print("Failed to connect to thingsboard")
    time.sleep(30)

camera_switch_status=False
#----------------------Display current time and start Arduino ----------------------
while True:

    if SCREEN_DISPLAY: print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    if SAVE_TO_FILE: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime()))

    ard = serial.Serial(SERIAL_PORT,timeout=20) 
    time.sleep(5)


    

#--------------------------- camera switch-------------------------------
    whether_time_for_camera_on=is_time_between(time2(7,30), time2(16,30))   #brisbane time
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
#--------------------------- on board humidity sensor -------------------------------
    try:
        ard.write("dht22,54,power,2,points,2,dummies,1,interval_mm,200,debug,1")
        ard.flushInput()
        msg=ard.readline()
        current_read=msg.split(',')[0:-1]
        ewatering_sa3_sensor['sa3_rh_logger']=float(current_read[-1])
        ewatering_sa3_sensor['sa3_temp_logger']=float(current_read[-2])
        if SCREEN_DISPLAY: print (msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
    except Exception as e:
        if SCREEN_DISPLAY:
            print (e)
            print ('sa3 on board humidty reading failed')
    time.sleep(5)
#-------------------------- System voltage ---------------------------------------
    try:
        ard.write("analog,15,power,9,points,5,dummies,3,interval_mm,200")
        ard.flushInput()
        msg=ard.readline()
        current_read=float(msg.split(',')[-2])
        ewatering_sa3_sensor['sa3_volt']=float(current_read)
        if SCREEN_DISPLAY: print ('raw System Voltage: ' + str(ewatering_sa3_sensor['sa3_volt']))
        if SAVE_TO_FILE:fid.write(DELIMITER + str(ewatering_sa3_sensor['sa3_volt']) + '\n')
    except Exception as e:
        if SCREEN_DISPLAY:
            print (e)
            print ('sa3 system voltage reading failed')
    time.sleep(5)
#------------------------ GEC MOisture sensor No.1-----------------------------
    try:
        ard.write("analog,1,power,22,points,5,dummies,3,interval_mm,10,debug,1")
        ard.flushInput()
        msg=ard.readline()
        current_read = msg.split(',')[-2]
        ewatering_sa3_sensor['sa3_mo1']=float(current_read)
        if SCREEN_DISPLAY: print (msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
    except Exception as e :
        if SCREEN_DISPLAY:
            print (e)
            print ('SA3_MO1 reading failed')

#------------------------ GEC MOisture sensor No.2-----------------------------
    try:
        ard.write("analog,2,power,23,points,5,dummies,3,interval_mm,10,debug,1")
        ard.flushInput()
        msg=ard.readline()
        current_read = msg.split(',')[-2]
        ewatering_sa3_sensor['sa3_mo2']=float(current_read)
        if SCREEN_DISPLAY: print (msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
    except Exception as e :
        if SCREEN_DISPLAY:
            print (e)
            print ('SA3_MO2 reading failed')

#------------------------ GEC MOisture sensor No.3-----------------------------
    try:
        ard.write("analog,3,power,24,points,5,dummies,3,interval_mm,10,debug,1")
        ard.flushInput()
        msg=ard.readline()
        current_read = msg.split(',')[-2]
        ewatering_sa3_sensor['sa3_mo3']=float(current_read)
        if SCREEN_DISPLAY: print (msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
    except Exception as e :
        if SCREEN_DISPLAY:
            print (e)
            print ('SA3_MO3 reading failed')

#------------------------ GEC MOisture sensor No.4-----------------------------
    try:
        ard.write("analog,4,power,25,points,5,dummies,3,interval_mm,10,debug,1")
        ard.flushInput()
        msg=ard.readline()
        current_read = msg.split(',')[-2]
        ewatering_sa3_sensor['sa3_mo4']=float(current_read)
        if SCREEN_DISPLAY: print (msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
    except Exception as e :
        if SCREEN_DISPLAY:
            print (e)
            print ('SA3_MO4 reading failed')

#------------------------ GEC MOisture sensor No.5-----------------------------
    try:
        ard.write("analog,5,power,26,points,5,dummies,3,interval_mm,10,debug,1")
        ard.flushInput()
        msg=ard.readline()
        current_read = msg.split(',')[-2]
        ewatering_sa3_sensor['sa3_mo5']=float(current_read)
        if SCREEN_DISPLAY: print (msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
    except Exception as e :
        if SCREEN_DISPLAY:
            print (e)
            print ('SA3_MO5 reading failed')

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


        time.sleep(8) # this appears to be important

        ard.write("SDI-12,50,custom_cmd,aD0!,debug,1")
        ard.flushInput()
        msg=ard.readline()
        if SCREEN_DISPLAY: print(msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        current_read=msg[:-3].split('+')
        ewatering_sa3_sensor['sa3_p_piezo']=float(current_read[1])
        ewatering_sa3_sensor['sa3_t_piezo']=float(current_read[2])
        ewatering_sa3_sensor['sa3_ec_piezo']=float(current_read[3])
        time.sleep(8)
    except Exception as e:
        if SCREEN_DISPLAY:
            print(e)
            print('sa3 pressure transducer reading failed')
#-------------------------barometer (ms5803) ------------------------
    try:
        ard.write("power_switch,30,power_switch_status,1")
        ard.flushInput()
        time.sleep(2)
        ard.write("power_switch,31,power_switch_status,1")
        ard.flushInput()
        time.sleep(2)	    

        ard.write("9548,0,type,5803,points,3,dummies,3,debug,1,interval_mm,1000")
        ard.flushInput()
        msg_5803_channel0=ard.readline()        
        if SAVE_TO_FILE: fid.write(DELIMITER+msg_5803_channel0)
        if SCREEN_DISPLAY: print msg_5803_channel0.rstrip()
        current_read=msg_5803_channel0.split(',')
        ewatering_sa3_sensor['sa3_p_5803']=(float(current_read[-2])+float(current_read[-4])+float(current_read[-5])+float(current_read[-6]))/4.
        ewatering_sa3_sensor['sa3_t_5803']=float(current_read[-3])
        time.sleep(5)
    except Exception as e:
        if SCREEN_DISPLAY:
            print(e)
            print('5803 sensor at port 0 reading failed')

#-------------- UV sensor----------------------------------
    try:
        time.sleep(2)
        ard.write("9548,1,type,si1145,debug,1")
        ard.flushInput()
        msg=ard.readline()
        time.sleep(12)
        current_read=msg.split(',')[0:-1]
        ewatering_sa3_sensor['sa3_uv']=float(current_read[-1])  #ultraviolet index
        ewatering_sa3_sensor['sa3_ir']=float(current_read[-3])  #Infrared light
        ewatering_sa3_sensor['sa3_vis']=float(current_read[-5]) #visible light
        if SCREEN_DISPLAY: print (msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)

    #  switch off power
        ard.write("power_switch,30,power_switch_status,0")
        ard.flushInput()
        ard.write("power_switch,31,power_switch_status,0")
        ard.flushInput()
        time.sleep(2)

    except Exception as e :
        if SCREEN_DISPLAY: print (e)
        if SCREEN_DISPLAY: print ('si1145 sensor at port 1 reading failed')


    ard.close()

    client.publish('v1/devices/me/telemetry', json.dumps(ewatering_sa3_sensor), 1)
    print('data successfully uploaded')

    if SAVE_TO_FILE: fid.write("\n\r")
    if SCREEN_DISPLAY: print('sleep for ' + str(SLEEP_TIME_SECONDS) + ' seconds')
    time.sleep(SLEEP_TIME_SECONDS) # sleep to the next loop


client.loop_stop()
client.disconnect()

