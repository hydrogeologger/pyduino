from gpiozero import Button
import time
from time import sleep,localtime,strftime
#import paho.mqtt.client as mqtt
#import json

#with open('/home/pi/pyduino/credential/rain_gauge.json') as f:
#        credential = json.load(f)

#field_name=["rain_gauge4","rain_gauge5","rain_gauge6"]
#rain_gauge=dict((el,0.0) for el in field_name)

class UQ_RainFall:
    '''
    UQ_RainFall class, set up a bucket pin with approprisate debouncing time (time required for
    a tipping duration to be register), name, volume of each tip and debug flag
    Requires to run config after initialisation to allow automatic counting
    '''
    def __init__(self, pin = 8, debounce = 0.05, name = "Bucket 1" , volume = 0.2794, debug = True):
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
        #next_reading = time.time()
        #client = mqtt.Client()
        #client.username_pw_set(credential['access_token'])
        #client.connect(credential['thingsboard_host'], 1883, 60)
        #client.loop_start()
        break
    except Exception, e:
        time.sleep(60)

delimiter=','
#screen_display=True
#save_to_file=True
#file_name= 'rain_gauge_456'
#if save_to_file: fid= open(file_name,'a',0)

#==================================================#
'''
This is for testing
Adjust the value debounce for best performance. Note 0.01 is
the minimum value.
'''
#print("Testing")

test1 = UQ_RainFall(pin = 8, debounce = 0.001, name = "Bucket", debug=True, volume = 0.2)
test2 = UQ_RainFall(pin = 18, debounce = 0.001, name = "Wind", debug=True)
#test3 = UQ_RainFall(pin = 21, debounce = 0.01, name = "Bucket 3", debug=False)
#Once config, the tipping is count automatically as an hardware event
#and immune to sleep in the main thread
test1.config()
test2.config()
#test3.config()
print("Start observing")

try:

    while True:

        #if screen_display: print strftime("%Y-%m-%d %H:%M:%S", localtime())
        #if save_to_file: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime())  )

        #print("rainfall_1:")
        #if screen_display: print "raingauge_4:"+str(test1.get_count())
        #if save_to_file: fid.write("raingauge_4"+delimiter+str(test1.get_count()))
        #current_read=int(test1.get_count())
        #rain_gauge['rain_gauge4']=int(test1.get_count())

        #print("rainfall_2:")
        #if screen_display: print "raingauge_5:"+str(test2.get_count())
        #if save_to_file: fid.write("raingauge_5"+delimiter+str(test2.get_count()))
        #current_read=int(test2.get_count())
        #rain_gauge['rain_gauge5']=int(test2.get_count())

        #print("rainfall_3:")
        #if screen_display: print "raingauge_6:"+str(test3.get_count())
        #if save_to_file: fid.write("raingauge_6"+delimiter+str(test3.get_count()))
        #current_read=test3.get_count()
        #rain_gauge['rain_gauge6']=int(test3.get_count())

        test1.reset()
        test2.reset()
        #test3.reset()

        #client.publish('v1/devices/me/telemetry', json.dumps(rain_gauge), 1)
        sleep(600)
        continue

except KeyboardInterrupt:
    pass

#client.loop_stop()
#client.disconnect()
        
#==================================================#


