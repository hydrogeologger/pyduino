#!/usr/bin/python
import serial
import syslog
import time
# this script reads off from arduino on the go.
# it is currently confirmed that arduino behaves similarly as all the scale sensors
# 1. having internal buffers
# 2. Being able to use simple serial interface to communicate with
# currently it is decided to use the time in raspberry pi/PC to record the time that
#    data collected by arduino for two reasons
# 1. it is not known how much arduino time will be derivated over time.
# 2. raspberry pi has internet connected and so has time weel syncronized. 
# However, it is always important that the reading intervals in arduino has to be 
#    the same as the current script reading interval. because the existing buffer in 
#    arduino may cause the time deviation between the time arduino has been read and 
#    the time raspberry has recorded the data
# It is found so far that arduino will store 500 undisplayed data, if these data has
#    yet retrived, arduino will stop running as indicated by RX stopped flashing.
#http://stackoverflow.com/questions/15184932/how-to-upload-source-code-to-arduino-from-bash



port = '/dev/ttyUSB0'
ard = serial.Serial(port,9600,timeout=5)
msg = ard.readline()
for i in range(1000): msg = ard.readline();print i,msg

ard.close()
