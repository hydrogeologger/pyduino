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

file_name= 'weather_station_roof2_winddir.csv'
fid= open(file_name,'a',0)
#---------------------------- Initiation --------------------------------------

with open('/home/pi/pyduino/credential/weather_station_roof2.json') as f:
    credential = json.load(f)

field_name=['volt','wind_direction','sht31_temp_1','sht31_humidity_1','sht31_temp_2','sht31_humidity_2','uv','ir','vis','tmp1','tmp2','dht22_rh','dht22_t']
weather_roof2=dict((el,0.0) for el in field_name)

try:
    client = mqtt.Client()
    client.username_pw_set(credential['access_token'])
    client.connect(credential['thingsboard_host'], 1883, 60)
    client.loop_start()
except Exception:
    print("Failed to connect to thingsboard")
    time.sleep(2)

davisWindPowerSwitch = 45 #Arduino Switch Power
#davisWindSpeedPin = 8 #RPI GPIO
davisWindDirPin = 8 #Arduino Analog Pin
systemVoltPin = 15 #Aruino Analog Pin
ststemVoltPowerSwitch = 9 #Arduino Switch Power
#davisRainPin = 11 #RPI GPIO

#ard = serial.Serial(SERIAL_PORT, timeout = 20)


#mph_2_kmh= 1.609



#------------------------------ Functions--------------------------------------
#class UQ_RainFall:
#    '''
#    UQ_RainFall class, set up a bucket pin with approprisate debouncing time (time required for
#    a tipping duration to be register), name, volume of each tip and debug flag
#    Requires to run config after initialisation to allow automatic counting
#    '''
#    def __init__(self, pin = 2, debounce = 0.05, name = "Bucket 1" , volume = 0.2794, debug = True):
#        #base on the Button class of gpiozero, pull_up = True means the reading pin default state is
#        #high, so connect one pin to GND and one pin to the reading pin
#        self.sensor_pin = Button(pin, pull_up = True, bounce_time = debounce)
#        self.name = name
#        self.debug = debug
#        self.count = 0
#        self.volume = volume
#
#    def update(self):
#        self.count = self.count + 1
#        if self.debug is True:
#            print(self.name + " tipped, new count = " + str(self.count))
#
#    def config(self):
#        #assign the event when_pressed to function update
#        self.sensor_pin.when_pressed = self.update
#
#    def reset(self):
#        self.count = 0
#
#    def get_count(self):
#        return self.count
#
#
#
#def convert_to_angle(raw):
#    """This function converts the output of the wind vane to angles"""
#    
#    if abs(raw-758)<= 5:
#        angle = 0
#    elif abs(raw-956)<=5:
#        angle = 45
#    elif abs(raw-1023)<=5:
#        angle = 90
#    elif abs(raw-522)<=5:
#        angle = 135
#    elif abs(raw-181)<=5:
#        angle = 180    
#    elif abs(raw-107)<=5:
#        angle = 225    
#    elif abs(raw-50)<=5:
#        angle = 270
#    elif abs(raw-330)<=5:
#        angle = 315
#
#    return angle

#test1 = UQ_RainFall(pin = davisRainPin, debounce = 0.001, name = "Bucket", debug=False)
#test2 = UQ_RainFall(pin = davisWindSpeedPin, debounce = None, name = "Wind Speed", debug=False)
#Once config, the tipping is count automatically as an hardware event
#and immune to sleep in the main thread
#test1.config()
#test2.config()
#print("Start observing")

#t0 = time.time()
#ard = serial.Serial(SERIAL_PORT, timeout = 20)

try:
    while True:
        #ard = serial.Serial(SERIAL_PORT, timeout = 20)
        #time.sleep(5)
        if SCREEN_DISPLAY:
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if SAVE_TO_FILE:
            fid.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  )
        ard = serial.Serial(SERIAL_PORT, timeout = 20)

        #try:  
        #    cum_count_rain = int(test1.get_count())
        #    weather_roof['rain_roof'] = cum_count_rain*0.2 #Each tip indicates 0.2 mm or 0.01" of rain 
        #    if SCREEN_DISPLAY:
        #        print ('Rain: ' + str(weather_roof['rain_roof']) + ' mm')
        #    if SAVE_TO_FILE:
        #        fid.write(DELIMITER+str(weather_roof['rain_roof'])+'\n')
        #except Exception:
        #    if SCREEN_DISPLAY:
        #        print('Rainfall reading failed')

        #try:
        #    elapsedTime = time.time() - t0
        #    cum_count_wind = int(test2.get_count())
        #    weather_roof['wind_speed'] = cum_count_wind * (2.25 / elapsedTime) * mph_2_kmh
        #    #based on Davis tech document
        #    # V = P*(2.25/T) the speed is in MPh
        #    # P = no. of pulses per sample period
        #    # T = sample period in seconds
        #    if SCREEN_DISPLAY:
        #        print ('Time elapsed: ' + str(elapsedTime) + ' s')
        #        print ('Wind:' + str(weather_roof['wind_speed']) + ' km/h')
        #    if SAVE_TO_FILE:
        #        fid.write(DELIMITER+str(elapsedTime)+'\n') 
        #        fid.write(DELIMITER+str(weather_roof['wind_speed'])+'\n')
        #except Exception:
        #    if SCREEN_DISPLAY: 
        #        print('Wind speed reading failed')
        
        #-----------------Wind direction---------------------------
        msg1 = ard.write("analog," + str(davisWindDirPin) + ",power," + str(davisWindPowerSwitch) + ",point,3,interval_mm,200,debug,0")
        msg1 = ard.flushInput()
        msg1 = ard.readline()

        try:
            current_read = float(msg1.split(',')[-2])
            weather_roof2['wind_direction'] = int(current_read)
            if SCREEN_DISPLAY:
                print ('Wind direction: ' + str(weather_roof2['wind_direction']))
            if SAVE_TO_FILE:
                fid.write(DELIMITER + str(weather_roof2['wind_direction']) + '\n')
        except Exception:
            if SCREEN_DISPLAY: 
                print('Wind direction reading failed')

        #----------------System voltage-----------------------------
        msg2 = ard.write("analog," + str(systemVoltPin) + ",power," + str(ststemVoltPowerSwitch) + ",point,3,interval_mm,200,debug,0")
        msg2 = ard.flushInput()
        msg2 = ard.readline()

        try:
            current_read = float(msg2.split(',')[-2])
            weather_roof2['volt'] = int(current_read)
            if SCREEN_DISPLAY:
                print ('raw System Voltage: ' + str(weather_roof2['volt']))
            if SAVE_TO_FILE:
                fid.write(DELIMITER + str(weather_roof2['volt']) + '\n')
        except Exception:
            if SCREEN_DISPLAY:
                print('System voltage reading failed')

        #----------------Temperature & humidity on the datalogger (DHT22)-----------------------------
             
        try:
            ard.write("dht22,54,power,2,points,2,dummies,1,interval_mm,2000,debug,1")
            ard.flushInput()
            msg = ard.readline()
            current_read=msg.split(',')[0:-1]
            weather_roof2['dht22_rh']=float(current_read[-1])
            weather_roof2['dht22_t']=float(current_read[-2])
            if SCREEN_DISPLAY:
                print ('Temperature on board: ' + str(weather_roof2['dht22_t']) + DELIMITER + 'Relative humidity: ' + str(weather_roof2['dht22_rh']) + '%')
            if SAVE_TO_FILE:
                fid.write(DELIMITER + str(weather_roof2['dht22_t']) + DELIMITER + str(weather_roof2['dht22_rh']) + '\n')
        except Exception:
            if SCREEN_DISPLAY:
                print('DHT22 sensor reading failed')

        time.sleep(2)
        #-----------------Temperature, humidity and UV sensor--------------------
        msg=ard.write("power_switch,23,power_switch_status,1")
        msg=ard.flushInput()

        #msg=ard.write("power_switch,23,power_switch_status,1")
        #msg=ard.flushInput()
        time.sleep(5)

        msg=ard.write("power_switch,25,power_switch_status,1")
        msg=ard.flushInput()
        #For I2C communication, all sensors have to be connected to the same power OR if they use different power, all reserved power channels have to be switched on before measuring one by one.

        time.sleep(5) #It is VERY IMPORTANT to set a time delay after switching on power channels for I2C because humiditity sensors would not get reading successfully if the measurement is conducted immediately.

        ard.write("9548,0,type,sht31,power,28,debug,1")
        ard.flushInput()
        msg4 = ard.readline()

        #msg4 = ard.write("9548,1,type,sht31,power,28,debug,1")
        #msg4 = ard.flushInput()
        #msg4 = ard.readline()
        time.sleep(5)

        ard.write("9548,3,type,si1145,power,28,debug,1")
        #msg5 = ard.write("9548,3,type,si1145,dummies,1,power,28,debug,1,points,1,timeout,5")
        ard.flushInput()
        msg5 = ard.readline()

        time.sleep(5)

        
        try:
            current_read = msg4.split(',')[0:-1]
            weather_roof2['sht31_temp_1'] = float(current_read[-2])
            weather_roof2['sht31_humidity_1'] = float(current_read[-1])
            if SCREEN_DISPLAY:
                print('Temperature: ' + str(weather_roof2['sht31_temp_1']) + u"\u2103"  + DELIMITER + 'Relative humidity: ' + str(weather_roof2['sht31_humidity_1']) + '%')  #u"\u2103" is the unicode for celsius degree
            if SAVE_TO_FILE:
                fid.write(DELIMITER + str(weather_roof2['sht31_temp_1']) + DELIMITER + str(weather_roof2['sht31_humidity_1']) + '\n')
            #if SCREEN_DISPLAY: print(msg.rstrip())
            #if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception:
            if SCREEN_DISPLAY:
                print('humidity sensor No.1 reading failed')

        #try:
        #    current_read=msg4.split(',')[0:-1]
        #    weather_roof2['sht31_temp_2']=float(current_read[-2])
        #    weather_roof2['sht31_humidity_2']=float(current_read[-1])
        #    if SCREEN_DISPLAY:
        #       #print (msg1)
        #        print('Temperature: ' + str(weather_roof2['sht31_temp_2']) + u"\u2103"  + DELIMITER + 'Relative humidity: ' + str(weather_roof2['sht31_humidity_2']) + '%')  #u"\u2103" is the unicode for celsius degree
        #    if SAVE_TO_FILE:
        #        fid.write(DELIMITER+str(weather_roof2['sht31_temp_2'])+DELIMITER+str(weather_roof2['sht31_humidity_2'])+'\n')
        #    #if SCREEN_DISPLAY: print(msg.rstrip())
        #    #if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        #except Exception:
        #    if SCREEN_DISPLAY:
        #        print('humidity sensor No.2 reading failed')

        try:
            current_read=msg5.split(',')[0:-1]
            weather_roof2['uv']=float(current_read[-1])  #This is the raw UV (ultraviolet index) data,and it should be divided by 100 to get real UV index based on the si1145 adafruit reading.
            weather_roof2['ir']=float(current_read[-3]) #Infrared light, unit in lm
            weather_roof2['vis']=float(current_read[-5]) #visible light, unit in lm            
            if SCREEN_DISPLAY:
                print('uv: ' + str(weather_roof2['uv']) + DELIMITER + 'ir: ' + str(weather_roof2['ir']) + DELIMITER + 'vis: ' + str(weather_roof2['vis']))  #u"\u2103" is the unicode for celsius degree
            if SAVE_TO_FILE:
                fid.write(DELIMITER+str(weather_roof2['uv']) + DELIMITER + str(weather_roof2['ir']) + DELIMITER + str(weather_roof2['vis']) + '\n')
        except Exception:
            if SCREEN_DISPLAY:
                print('UV sensor reading failed')


        msg=ard.write("power_switch,23,power_switch_status,0")
        msg=ard.flushInput()

        #msg=ard.write("power_switch,23,power_switch_status,0")
        #msg=ard.flushInput()

        msg=ard.write("power_switch,25,power_switch_status,0")
        msg=ard.flushInput()
 
        time.sleep(2)


#----------------------------Upload data -----------------------------------
        ard.close()

        client.publish('v1/devices/me/telemetry', json.dumps(weather_roof2), 1)
        print('data successfully uploaded')
        if SAVE_TO_FILE: fid.write("\n\r")
        time.sleep(500)#SLEEP_TIME_SECONDS) # sleep to the next loop
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
