import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
import subprocess
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(23, GPIO.OUT)           # set GPIO24 as an output   
GPIO.output(23, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
sleep(2)                 # wait half a second  
subprocess.call("/home/pi/script/raspstill_snapshot_marandoo.sh", shell=True)
sleep(2)                 # wait half a second  
GPIO.output(23, 0)         # set GPIO24 to 0/GPIO.LOW/False  

