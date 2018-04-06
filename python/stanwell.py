#!/usr/bin/python
import serial
import time
import numpy as np
import sys
from phant import Phant
import serial_openlock
import get_ip
from upload_phant import upload_phant
# below required by gpio
import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep,gmtime, strftime             # lets us have a delay  
import subprocess
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(25, GPIO.OUT)           # set GPIO24 as an output   
GPIO.setup(26, GPIO.OUT)           # set GPIO24 as an output   
GPIO.setup(24, GPIO.OUT)           # set GPIO24 as an output   


with open('/home/pi/script/pass/public_stanwell_moisture_suction', 'r') as myfile:
    public_stanwell_moisture_suction=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_stanwell_moisture_suction', 'r') as myfile:
    private_stanwell_moisture_suction=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/public_stanwell_sali_gs3_p', 'r') as myfile:
    public_stanwell_sali_gs3_p=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_stanwell_sali_gs3_p', 'r') as myfile:
    private_stanwell_sali_gs3_p=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')



#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['mo0','mo1','mo2','mo3','mo4','mo5','mo6','mo7','mo8','mo9',
            'su0','su1','su2','su3','su4','su5','su6','su7','su8','su9',
            'tmp0','tmp1','tmp2','tmp3','tmp4','tmp5','tmp6','tmp7','tmp8','tmp9'
            ]
mo_su=dict((el,0.0) for el in field_name)
pht_sensor = Phant(publicKey=public_stanwell_moisture_suction, fields=field_name ,privateKey=private_stanwell_moisture_suction,baseUrl=nectar_address)



#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['tmp0','tmp1','tmp2','tmp3',
            'hum0','hum1','hum2','hum3',
            'dp0',
            'ec0',
            'gstmp0',
            'pre0','pre1',
            'pretmp0','pretmp1',
            'dhttmp0',
            'dhthum0',
            'volt0',
            'tmp4','tmp5','tmp6','tmp7','tmp8','tmp9','tmp10','tmp11','tmp12']
sali_gs3_p=dict((el,0.0) for el in field_name)
pht_salt_gs_p = Phant(publicKey=public_stanwell_sali_gs3_p, fields=field_name ,privateKey=private_stanwell_sali_gs3_p,baseUrl=nectar_address)


port_sensor  = 'USB VID:PID=2341:0042 SNR=9563533373035110A2B1'


# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'stanwell.csv'

sleep_time_seconds=45*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)



while True: 
    ### -------------------- below is to processing data from suction, moisture-------------------------
    if screen_display: print strftime("%Y-%m-%d %H:%M:%S", gmtime())
    if save_to_file: fid.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())  )
    
    #### below is for pressure 
    GPIO.output(25, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
    sleep(5)
    GPIO.output(26, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
    sleep(5)

    GPIO.output(24, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
    sleep(2)
    GPIO.output(24, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
    sleep(10) # change 2 to 10


    # possible update: set time out for send result
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="9548,2,type,5803,dummies,1,debug,1,points,2",initialize=True)

    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    try:
        sali_gs3_p['pre0']=float(current_read[-1])
        sali_gs3_p['pretmp0']=float(current_read[-2])
    except Exception, e:
        if screen_display: print '5803 ,2, does not get results'
        continue

    GPIO.output(24, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
    sleep(2)
    GPIO.output(24, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
    sleep(10) # change from 2 to 5
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="9548,3,type,5803,dummies,1,debug,1,points,2",initialize=True)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    try:
        sali_gs3_p['pre1']=float(current_read[-1])
        sali_gs3_p['pretmp1']=float(current_read[-2])
    except Exception, e:
        if screen_display: print '5803 ,3,does not get results'
        continue


    GPIO.output(25, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
    sleep(2)
    GPIO.output(26, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
    sleep(2)

    #sleep(10)
    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="75,3,clk,4,power,8,debug,1",initialize=True)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #sali_gs3_p['hum3']=float(current_read[-1])
    #sali_gs3_p['tmp3']=float(current_read[-2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,4,power,38,points,2,dummies,1,interval_mm,200,debug,1",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    sali_gs3_p['tmp5']=float(current_read[-1])
    sali_gs3_p['tmp6']=float(current_read[-2])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,3,power,36,points,2,dummies,1,interval_mm,200,debug,1",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    sali_gs3_p['tmp7']=float(current_read[-1])
    sali_gs3_p['tmp8']=float(current_read[-2])


    
    sleep(5)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="75,51,clk,10,power,25,debug,1",initialize=True)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    sali_gs3_p['hum0']=float(current_read[-1])
    sali_gs3_p['tmp0']=float(current_read[-2])


    sleep(5)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="75,11,clk,12,power,23,debug,1",initialize=True)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    sali_gs3_p['hum1']=float(current_read[-1])
    sali_gs3_p['tmp1']=float(current_read[-2])

    #sleep(5)
    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="75,5,clk,53,power,9,debug,1",initialize=False)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #sali_gs3_p['hum2']=float(current_read[-1])
    #sali_gs3_p['tmp2']=float(current_read[-2])
    
       


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="12,52,power,7,debug,1",initialize=True)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    sali_gs3_p['ec0']=float(current_read[9])
    sali_gs3_p['dp0']=float(current_read[7])
    sali_gs3_p['gstmp0']=float(current_read[8])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="12,52,power,7,debug,1",initialize=True)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    sali_gs3_p['tmp2']=float(current_read[9])
    sali_gs3_p['tmp3']=float(current_read[7])
    sali_gs3_p['tmp4']=float(current_read[8])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,10,power,48,points,2,dummies,1,interval_mm,200,debug,1",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    sali_gs3_p['dhthum0']=float(current_read[-1])
    sali_gs3_p['dhttmp0']=float(current_read[-2])

    # voltage measurement
    # power,43,analog,15,point,3,interval_mm,200,debug,1
    upload_phant(pht_salt_gs_p,sali_gs3_p,screen_display)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,E87C959F,dgin,50,snpw,42,htpw,22,itv,24000,otno,5",initialize=True)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp0']=float(current_read[2])
    mo_su['su0']=float(current_read[7])-float(current_read[2])



    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,F755BA01,dgin,50,snpw,42,htpw,24,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp1']=float(current_read[2])
    mo_su['su1']=float(current_read[7])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,1848BC95,dgin,50,snpw,42,htpw,33,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp2']=float(current_read[2])
    mo_su['su2']=float(current_read[7])-float(current_read[2])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,B722BBC7,dgin,50,snpw,42,htpw,31,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp3']=float(current_read[2])
    mo_su['su3']=float(current_read[7])-float(current_read[2])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,4FCAB9F7,dgin,50,snpw,42,htpw,29,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp4']=float(current_read[2])
    mo_su['su4']=float(current_read[7])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,C205BB1D,dgin,13,snpw,6,htpw,27,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp5']=float(current_read[2])
    mo_su['su5']=float(current_read[7])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,4C0F973B,dgin,13,snpw,6,htpw,41,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp6']=float(current_read[2])
    mo_su['su6']=float(current_read[7])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,C286BB98,dgin,13,snpw,6,htpw,39,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp7']=float(current_read[2])
    mo_su['su7']=float(current_read[7])-float(current_read[2])

    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="",initialize=False)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #mo_su['tmp8']=float(current_read[2])
    #mo_su['su8']=float(current_read[7])-float(current_read[2])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,EAC3B9B3,dgin,13,snpw,6,htpw,35,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp9']=float(current_read[2])
    mo_su['su9']=float(current_read[7])-float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,14,power,40,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo0']=float(current_read[2])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,13,power,26,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo1']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,12,power,28,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo2']=float(current_read[2])



    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,11,power,30,point,3,interval_mm,200,debug,0",initialize=False)
    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,11,power,30,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo3']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,10,power,32,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo4']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,9,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo5']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,8,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo6']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,7,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo7']=float(current_read[2])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,6,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo8']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,5,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo9']=float(current_read[2])

    

    upload_phant(pht_sensor,mo_su,screen_display)

    if save_to_file: fid.write("\n\r")
    # sleep to the next loop
    time.sleep(sleep_time_seconds)

        
      


