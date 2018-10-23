#!/usr/bin/python 
import sys
import time
from time import sleep
import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep
import picamera  
import subprocess
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
#GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)           # set GPIO24 as an output   
#subprocess.call("/home/pi/script/raspstill_snapshot_marandoo.sh", shell=True)  
GPIO.output(23, 1)         # set GPIO24 to 1/GPIO.HIGH/True    

with open('/home/pi/script/pass/cmd_area51_taking_photo', 'r') as myfile:
    cmd_area51_taking_photo=myfile.read().replace('\n', '')

sleep(5)

#camera.capture('/home/pi/photo/'+file_name_basin_2)
#camera = picamera.PiCamera()
process=subprocess.Popen('/home/pi/script/raspistill_snapshot_bacteria_basin_2.sh', stdout=subprocess.PIPE)
process=subprocess.Popen(cmd_area51_taking_photo.split(), stdout=subprocess.PIPE)
process.wait()
#time.sleep(5)
#time.sleep(10)
GPIO.output(23,0)

sleep(5)
#camera.close()



