from gpiozero import Button
from phant import Phant
from upload_phant import upload_phant
import time
from time import sleep,localtime,strftime
import paho.mqtt.client as mqtt
import json

with open('/home/pi/pyduino/credential/salt_marsh_weather.json') as f:
        credential = json.load(f)

field_name=["salt_marsh_rain","salt_marsh_wind","tmp1","tmp2"]
salt_marsh_weather=dict((el,0.0) for el in field_name)

pht_salt_marsh_weather = Phant(publicKey=credential['public_salt_marsh_weather'],
                                       fields=field_name,
                                       privateKey=credential['private_salt_marsh_weather'],
                                       baseUrl=credential['nectar_address'])

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

delimiter=','
screen_display=True
save_to_file=True
file_name= 'salt_marsh_weather.csv'
if save_to_file: fid= open(file_name,'a',0)

#==================================================#
'''
This is for testing
Adjust the value debounce for best performance. Note 0.01 is
the minimum value.
'''
#print("Testing")

test1 = UQ_RainFall(pin = 18, debounce = 0.01, name = "Bucket 1", debug=False)
test2 = UQ_RainFall(pin = 8, debounce = 0.01, name = "Wind", debug=False)

#Once config, the tipping is count automatically as an hardware event
#and immune to sleep in the main thread
test1.config()
test2.config()
#print("Start observing")

try:

    while True:

        if screen_display: print strftime("%Y-%m-%d %H:%M:%S", localtime())
        if save_to_file: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime())  )

        #print("rainfall_1:")
        if screen_display: print "salt_marsh_rain:"+str(test1.get_count())
        if screen_display: print "salt_marsh_wind:"+str(test2.get_count())        
        if save_to_file: fid.write("salt_marsh_rain"+delimiter+str(test1.get_count())+delimiter+
                                   "salt_marsh_wind"+delimiter+str(test2.get_count())+"\n")
        #current_read=int(test1.get_count())
        salt_marsh_weather['salt_marsh_rain']=int(test1.get_count())
        salt_marsh_weather['salt_marsh_wind']=int(test2.get_count())

        test1.reset()
        test2.reset()

        client.publish('v1/devices/me/telemetry', json.dumps(salt_marsh_weather), 1)
        upload_phant(pht_salt_marsh_weather,salt_marsh_weather,screen_display)
        sleep(600)
        continue

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
        
#==================================================#
"""Notes
test1.get_count() is the tip number of the tipping bucket in 10 minutes (600 seconds)
test2.get_count() is the number of signals the reed switch generates during rotation in 
10 minutes (Note a whole rotation generates two signals)
"""

"""To calculate the wind speed, use the following:"""
#import math
#radius_cm = 9.0
#wind_interval = 600
#circumference_cm = (2 * math.pi) * radius_cm
#rotations = test2.get_count() / 2.0
#dist_cm = circumference_cm * rotations
#speed = 3600*(dist_cm/100000) / wind_interval #km/h
#print(speed)

