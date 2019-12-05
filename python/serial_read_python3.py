# -*- coding: utf-8 -*-
import time
import serial
SCREEN_DISPLAY=True
SAVE_TO_FILE=True
DELIMITER=','

#SERIAL_PORT='/dev/ttyACM0' # serial port terminal
SERIAL_PORT='COM5'

file_name= 'output.csv'
fid= open(file_name,'ab')

scale=serial.Serial(SERIAL_PORT,timeout=20,baudrate=4800)

while True:
    str_scale=scale.readline()
    time_now=time.strftime("%Y-%m-%d %H:%M:%S")

    if SCREEN_DISPLAY: print(str.encode(time_now+DELIMITER)+str_scale)
    time.sleep(0.01)  # in seconds
    if SAVE_TO_FILE: fid.write(str.encode(time_now)+str_scale)

scale.close()
fid.close()
