#!/usr/bin/python

### run this on python to reset arduin
import RPi.GPIO as GPIO
import sys, os, re, time, fcntl

#fd = sys.stdin.fileno()
#fl = fcntl.fcntl(fd, fcntl.F_GETFL)
#fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def reset():
  pin = 27
  GPIO.setup(pin, GPIO.OUT)
  #GPIO.output(pin, GPIO.HIGH)
  #time.sleep(0.32)
  GPIO.output(pin, GPIO.LOW)
  time.sleep(5)


print("RESET")
reset()
GPIO.cleanup()
#print "done with autoreset - ignore Broken pipe errors if Done uploading"
exit
