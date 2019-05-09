import RPi.GPIO as GPIO            # import RPi.GPIO module  
def reset(bb):
   import RPi.GPIO as GPIO            # import RPi.GPIO module  

   from time import sleep
   import time

   GPIO.setmode(GPIO.BCM)
   pin=17
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.HIGH)
   time.sleep(bb)
   GPIO.output(pin, GPIO.LOW)

