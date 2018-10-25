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

with open('/home/pi/script/pass/public_pizo_pre', 'r') as myfile:
    public_pizo_pre=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_pizo_pre', 'r') as myfile:
    private_pizo_pre=myfile.read().replace('\n', '')

#with open('/home/pi/script/pass/zero_pressure_public', 'r') as myfile:
#    zero_pressure_public=myfile.read().replace('\n', '')
#
#with open('/home/pi/script/pass/zero_pressure_private', 'r') as myfile:
#    zero_pressure_private=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')

#with open('/home/pi/script/pass/gelita_borehole', 'r') as myfile:
#    gelita_borehole=myfile.read().replace('\n', '')
#
#with open('/home/pi/script/pass/remote_mango', 'r') as myfile:
#    remote_mango=myfile.read().replace('\n', '')


field_name=['dp0','hum0','pre0','pre1','pre2','pre3','pre4','pretmp0','pretmp1','pretmp2','pretmp3','pretmp4','timestamp','tmp0','tmp1','tmp10','tmp11','tmp12','tmp2','tmp3','tmp4','tmp5','tmp6','tmp7','tmp8','tmp9','volt0']
pizo_pre=dict((el,0.0) for el in field_name)
pht_pizo_pre = Phant(publicKey=public_pizo_pre, fields=field_name ,privateKey=private_pizo_pre,baseUrl=nectar_address)


#port_sensor  = 'USB VID:PID=2341:0042 SNR=55639303035351A04171'
#port_sensor = '/dev/ttyACM0'  # remember when using device at /dev/folder rather than USB VID:PID, serial_openlock needs to have match_existing=False
port_sensor = '/dev/ttyS0' # port for serial connection 

#ard=serial.Serial(port_sensor)
#msg=

#below is working
#msg=ard.write("power_switch,30,power_switch_status,1")
#sleep(1)
#msg=ard.readline()
#msg=ard.write("power_switch,32,power_switch_status,1")
#sleep(1)
#msg=ard.readline()
#msg=ard.write("power_switch,35,power_switch_status,1")
#sleep(1)
#msg=ard.readline()
#msg=ard.write("power_switch,35,power_switch_status,0")
#sleep(1)
#msg=ard.readline()
#msg=ard.write("9548,4,type,5803,dummies,1,power,28,debug,1,points,1,timeout,60")
#sleep(1)
#msg=ard.readline()
#print msg
#msg=ard.write("9548,3,type,5803,dummies,1,power,28,debug,1,points,1,timeout,60")
#sleep(1)
#msg=ard.readline()
#print msg
#msg=ard.write("power_switch,30,power_switch_status,0")
#sleep(1)
#msg=ard.readline()
#msg=ard.write("power_switch,32,power_switch_status,0")
#sleep(1)
#msg=ard.readline()
#
#ard.close()



#msg=serial_openlock.get_result_by_input(port=port_sensor,command="power_switch,30,power_switch_status,1",initialize=True,match_existing_ports=False)
#sleep(1)
#msg=serial_openlock.get_result_by_input(port=port_sensor,command="power_switch,32,power_switch_status,1",initialize=False,match_existing_ports=False)
#sleep(1)
#print msg
#msg=serial_openlock.get_result_by_input(port=port_sensor,command="power_switch,35,power_switch_status,1",initialize=False,match_existing_ports=False)
#sleep(1)
#print msg
#msg=serial_openlock.get_result_by_input(port=port_sensor,command="power_switch,35,power_switch_status,0",initialize=False,match_existing_ports=False)
#sleep(1)
#print msg
#msg=serial_openlock.get_result_by_input(port=port_sensor,command="9548,4,type,5803,dummies,1,power,28,debug,1,points,1,timeout,60",initialize=False,match_existing_ports=False)
#sleep(1)
#print msg
#msg=serial_openlock.get_result_by_input(port=port_sensor,command="9548,3,type,5803,dummies,1,power,28,debug,1,points,1,timeout,60",initialize=False,match_existing_ports=False)
#sleep(1)
#print msg
#msg=serial_openlock.get_result_by_input(port=port_sensor,command="power_switch,30,power_switch_status,0",initialize=False,match_existing_ports=False)
#sleep(1)
#print msg
#msg=serial_openlock.get_result_by_input(port=port_sensor,command="power_switch,32,power_switch_status,0",initialize=False,match_existing_ports=False)
#sleep(1)
#print msg
#


# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'pizo.csv'

sleep_time_seconds=30*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)


while True: 
    ### -------------------- below is to processing data from suction, moisture-------------------------
    if screen_display: print strftime("%Y-%m-%d %H:%M:%S", localtime())
    if save_to_file: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime())  )
 
    
#    try:
        # possible update: set time out for send result
    ard=serial.Serial(port_sensor)
    msg=ard.write("power_switch,30,power_switch_status,1")
    sleep(1)
    msg=ard.readline()
    msg=ard.write("power_switch,32,power_switch_status,1")
    sleep(1)
    msg=ard.readline()
    msg=ard.write("power_switch,35,power_switch_status,1")
    sleep(1)
    msg=ard.readline()
    msg=ard.write("power_switch,35,power_switch_status,0")
    sleep(1)
    msg=ard.readline()
        #msg=ard.write("9548,4,type,5803,dummies,1,power,28,debug,1,points,1,timeout,60")
    sleep(1)
        #msg=ard.readline()
        #print msg
    msg2=ard.write("9548,3,type,5803,dummies,1,power,28,debug,1,points,1,timeout,60")
    sleep(15)
    msg2=ard.readline()
#    except Exception, e:
#        if screen_display: print '5803 ,3, does not get results'
#        continue
    sleep(5)

    msg=ard.write("power_switch,30,power_switch_status,0")
    sleep(1)
    msg=ard.readline()
    msg=ard.write("power_switch,32,power_switch_status,0")
    sleep(1)
    msg=ard.readline()   
    sleep(5)
    if screen_display: print msg2.rstrip()
    if save_to_file: fid.write(delimiter+msg2.rstrip())
    upload_msg=msg2.rstrip()
    current_read=msg2.split(',')[0:-1]
    pizo_pre['pre0']=float(current_read[-1])
    pizo_pre['pretmp0']=float(current_read[-2])


    ard=serial.Serial(port_sensor)
    msg=ard.write("power_switch,30,power_switch_status,1")
    sleep(1)
    msg=ard.readline()
    msg=ard.write("power_switch,32,power_switch_status,1")
    sleep(1)
    msg=ard.readline()
    msg=ard.write("power_switch,35,power_switch_status,1")
    sleep(1)
    msg=ard.readline()
    msg=ard.write("power_switch,35,power_switch_status,0")
    sleep(1)
    msg=ard.readline()
    sleep(1)
    msg2=ard.write("9548,4,type,5803,dummies,1,power,28,debug,1,points,1,timeout,60")
    sleep(15)
    msg2=ard.readline()
    sleep(5)
    msg=ard.write("power_switch,30,power_switch_status,0")
    sleep(1)
    msg=ard.readline()
    msg=ard.write("power_switch,32,power_switch_status,0")
    sleep(1)
    msg=ard.readline()


    if screen_display: print msg2.rstrip()
    if save_to_file: fid.write(delimiter+msg2.rstrip())
    upload_msg+=msg2.rstrip()
    current_read=msg2.split(',')[0:-1]
    pizo_pre['pre1']=float(current_read[-1])
    pizo_pre['pretmp1']=float(current_read[-2])

    #try:
    #   msg=serial_openlock.get_result_by_input(port=port_sensor,command="9548,1,type,5803l,dummies,1,power,8,debug,1,points,1,timeout,60",initialize=True)
    #   if screen_display: print msg.rstrip()
    #   if save_to_file: fid.write(delimiter+msg.rstrip())
    #   upload_msg+=msg.rstrip()
    #   current_read=msg.split(',')[0:-1]
    #   pizo_pre['pre2']=float(current_read[-1])
    #   pizo_pre['pretmp2']=float(current_read[-2])
    #except Exception, e:
    #    if screen_display: print '5803 ,1l,does not get results'
    #    continue

    sleep(2) 

    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,15,power,43,point,3,interval_mm,200,debug,0",initialize=False)
    msg=ard.write("analog,15,power,43,point,3,interval_mm,200,debug,0")
    sleep(2)
    msg=ard.readline()
    sleep(2)

    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    upload_msg+=msg.rstrip()
    current_read=msg.split(',')[0:-1]
    pizo_pre['volt0']=float(current_read[2])

    sleep(2)

    msg=ard.write("dht22,10,power,48,points,2,dummies,1,interval_mm,2000,debug,0")
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg)
    current_read=msg.split(',')[0:-1]
    pizo_pre['tmp8']=float(current_read[-1])
    pizo_pre['tmp9']=float(current_read[-2])


    ard.close()

    #bashCommand = "ssh " + remote_mango + " echo "+ strftime("%Y-%m-%d %H:%M:%S", localtime())+','+ upload_msg.rstrip() +" >> " + gelita_borehol

    #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)

    upload_phant(pht_pizo_pre,pizo_pre,screen_display)

    if save_to_file: fid.write("\n\r")
    # sleep to the next loop
    time.sleep(sleep_time_seconds)



                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
