import time
import serial
SCREEN_DISPLAY=True
SAVE_TO_FILE=True
DELIMITER=','

#SERIAL_PORT='/dev/ttyACM0' # serial port terminal
SERIAL_PORT='COM6'

file_name= 'output.csv'
fid= open(file_name,'r+',0)
#fid.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')

scale=serial.Serial(SERIAL_PORT,timeout=20,baudrate=4800)

while True:
    str_scale=scale.readline()
    time_now=time.strftime("%Y-%m-%d %H:%M:%S")

    if SCREEN_DISPLAY: print(str_scale)
    time.sleep(1)  #seconds
    if SAVE_TO_FILE: fid.write(time_now+DELIMITER+weight_scale+DELIMITER+'\n\r')
