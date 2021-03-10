#!/usr/bin/python
import time
import json
import subprocess
import paho.mqtt.client as mqtt
from gpiozero import Button
from signal import pause
import RPi.GPIO as GPIO #for rpi gpio
import serial # For arduino comms

#------------------- Constants and Ports Information---------------------------

SCREEN_DISPLAY=True
SAVE_TO_FILE=True
DELIMITER=','
SLEEP_TIME_SECONDS=30*60 # second
SERIAL_PORT='/dev/ttyS0' # datalogger version 2 uses ttyS0
#---------------------- Create csv file to store data -------------------------
file_name= 'weather_SA1.csv'
fid= open(file_name,'a',0)
#---------------------------- Initiation --------------------------------------

with open('/home/pi/pyduino/credential/ewatering.json') as f:
    credential = json.load(f)

field_name=['rainfall','wind_speed']
weather_SA1=dict((el,0.0) for el in field_name)

try:
    client = mqtt.Client()
    client.username_pw_set(credential['access_token'])
    client.connect(credential['thingsboard_host'], 1883, 60)
    client.loop_start()
except Exception:
    print("Failed to connect to thingsboard")
    time.sleep(2)


mph_2_kmh= 1.609


#------------------------------ Functions--------------------------------------
class UQ_RainFall:
    '''
    UQ_RainFall class, set up a bucket pin with approprisate debouncing time (time required for
    a tipping duration to be register), name, volume of each tip and debug flag
    Requires to run config after initialisation to allow automatic counting
    '''
    def __init__(self, pin = 2, debounce = 0.05, name = "Bucket 1" , volume = 0.2794, debug = True):
        #base on the Button class of gpiozero, pull_up = True means the reading pin default state is
        #high, so connect one pin to GND and one pin to the reading pin
        self.sensor_pin = Button(pin, pull_up = True, bounce_time = debounce)
        self.name = name
        self.debug = debug
        self.count = 0
        self.volume = volume

    def update(self):
        self.count = self.count + 1
        if self.debug is True:
            print(self.name + " tipped, new count = " + str(self.count))

    def config(self):
        #assign the event when_pressed to function update
        self.sensor_pin.when_pressed = self.update

    def reset(self):
        self.count = 0

    def get_count(self):
        return self.count



test1 = UQ_RainFall(pin = 17, debounce = 0.001, name = "Bucket", debug=False)
test2 = UQ_RainFall(pin = 18, debounce = None, name = "Wind Speed", debug=False)
#Once config, the tipping is count automatically as an hardware event
#and immune to sleep in the main thread
test1.config()
test2.config()
#print("Start observing")

t0 = time.time()

#----------------------------------- Rainfall(mm) and wind speed (km/h) ---------------------------------
try:
    while True:
        #ard = serial.Serial(SERIAL_PORT, timeout = 20)
        #time.sleep(5)
        if SCREEN_DISPLAY:
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if SAVE_TO_FILE:
            fid.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  )
        ard = serial.Serial(SERIAL_PORT, timeout = 20)

        try:
            cum_count_rain = int(test1.get_count())
            weather_SA1['rainfall'] = cum_count_rain*0.2 #Each tip indicates 0.2 mm or 0.01" of rain 
            if SCREEN_DISPLAY:
                print ('Rain: ' + str(weather_SA1['rainfall']) + ' mm')
            if SAVE_TO_FILE:
                fid.write(DELIMITER+str(weather_SA1['rainfall'])+'\n')
        except Exception:
            if SCREEN_DISPLAY:
                print('Rainfall reading failed')

        try:
            elapsedTime = time.time() - t0
            cum_count_wind = int(test2.get_count())
            weather_SA1['wind_speed'] = cum_count_wind * (2.25 / elapsedTime) * mph_2_kmh
            #based on Davis tech document
            # V = P*(2.25/T) the speed is in MPh
            # P = no. of pulses per sample period
            # T = sample period in seconds
            if SCREEN_DISPLAY:
                print ('Time elapsed: ' + str(elapsedTime) + ' s')
                print ('Wind:' + str(weather_SA1['wind_speed']) + ' km/h')
            if SAVE_TO_FILE:
                fid.write(DELIMITER+str(elapsedTime)+'\n')
                fid.write(DELIMITER+str(weather_SA1['wind_speed'])+'\n')
        except Exception:
            if SCREEN_DISPLAY:
                print('Wind speed reading failed')

        test1.reset()
        test2.reset()
        t0 = time.time()

#----------------------------Upload data -----------------------------------
        ard.close()

        client.publish('v1/devices/me/telemetry', json.dumps(weather_SA1), 1)
        print('data successfully uploaded')
        if SAVE_TO_FILE: fid.write("\n\r")
        time.sleep(600)#SLEEP_TIME_SECONDS) # sleep to the next loop
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()

