#!/usr/bin/python
import serial
import time
import numpy as np
import sys
from phant import Phant
import serial_openlock
import get_ip
from upload_phant import upload_phant
import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep,gmtime, strftime,localtime             # lets us have a delay  
import subprocess
import os 

pyduino_path=os.environ['pyduino']


with open('/home/pi/script/pass/public_pizo_pre', 'r') as myfile:
    public_pizo_pre=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_pizo_pre', 'r') as myfile:
    private_pizo_pre=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/gelita_borehole', 'r') as myfile:
    gelita_borehole=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/remote_mango', 'r') as myfile:
    remote_mango=myfile.read().replace('\n', '')


field_name=['dp0','hum0','pre0','pre1','pre2','pre3','pre4','pretmp0','pretmp1','pretmp2','pretmp3','pretmp4','timestamp','tmp0','tmp1','tmp10','tmp11','tmp12','tmp2','tmp3','tmp4','tmp5','tmp6','tmp7','tmp8','tmp9','volt0']
pizo_pre=dict((el,0.0) for el in field_name)
pht_pizo_pre = Phant(publicKey=public_pizo_pre, fields=field_name ,privateKey=private_pizo_pre,baseUrl=nectar_address)


port_sensor  = 'USB VID:PID=2341:0042 SNR=55639303035351A04171'

# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'pizo.csv'

sleep_time_seconds=60*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)


while True:
    ### -------------------- below is to processing data from suction, moisture-------------------------
    if screen_display: print strftime("%Y-%m-%d %H:%M:%S", localtime())
    if save_to_file: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime())  )

    try:
        # possible update: set time out for send result
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="9548,3,type,5803,dummies,1,power,8,debug,1,points,1",initialize=True)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        upload_msg=msg.rstrip()
        current_read=msg.split(',')[0:-1]
        pizo_pre['pre0']=float(current_read[-1])
        pizo_pre['pretmp0']=float(current_read[-2])
    except Exception, e:
        if screen_display: print '5803 ,3, does not get results'
        continue
    sleep(15)

    try:
       msg=serial_openlock.get_result_by_input(port=port_sensor,command="9548,1,type,5803,dummies,1,power,8,debug,1,points,1,timeout,60",initialize=True)
       if screen_display: print msg.rstrip()
       if save_to_file: fid.write(delimiter+msg.rstrip())
       upload_msg+=msg.rstrip()
       current_read=msg.split(',')[0:-1]
       pizo_pre['pre1']=float(current_read[-1])
       pizo_pre['pretmp1']=float(current_read[-2])
    except Exception, e:
        if screen_display: print '5803 ,1,does not get results'
        continue

    sleep(15)

    try:
       msg=serial_openlock.get_result_by_input(port=port_sensor,command="9548,1,type,5803l,dummies,1,power,8,debug,1,points,1,timeout,60",initialize=True)
       if screen_display: print msg.rstrip()
       if save_to_file: fid.write(delimiter+msg.rstrip())
       upload_msg+=msg.rstrip()
       current_read=msg.split(',')[0:-1]
       pizo_pre['pre2']=float(current_read[-1])
       pizo_pre['pretmp2']=float(current_read[-2])
    except Exception, e:
        if screen_display: print '5803 ,1l,does not get results'
        continue

    sleep(2)

    bashCommand = "ssh " + remote_mango + " echo "+ strftime("%Y-%m-%d %H:%M:%S", localtime())+','+ upload_msg.rstrip() +" >> " + gelita_borehole

    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,7,power,6,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    upload_msg+=msg.rstrip()
    current_read=msg.split(',')[0:-1]
    pizo_pre['volt0']=float(current_read[2])

    if save_to_file: fid.write("\n\r")
    # sleep to the next loop
    time.sleep(sleep_time_seconds)




