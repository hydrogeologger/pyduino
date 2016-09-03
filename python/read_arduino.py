#!/usr/bin/python
import serial
import syslog
import time
# this script reads off from arduino on the go.


port = '/dev/ttyUSB0'
ard = serial.Serial(port,9600,timeout=5)
msg = ard.readline()
for i in range(1000): msg = ard.readline();print i,msg

