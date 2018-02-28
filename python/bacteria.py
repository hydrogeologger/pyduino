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


with open('/home/pi/script/pass/public_bacteria_mo_su_sali', 'r') as myfile:
    public_bacteria_mo_su_sali=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_bacteria_mo_su_sali', 'r') as myfile:
    private_bacteria_mo_su_sali=myfile.read().replace('\n', '')

#with open('/home/pi/script/pass/public_stanwell_sali_gs3_p', 'r') as myfile:
    #public_stanwell_sali_gs3_p=myfile.read().replace('\n', '')

#with open('/home/pi/script/pass/private_stanwell_sali_gs3_p', 'r') as myfile:
    #private_stanwell_sali_gs3_p=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')



#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['mo0','mo1','mo2','mo3','mo4','mo5',
            'su0','su1','su2','su3','su4','su5',
            'tempa0','tempb0','tempa1','tempb1',
            'tempa2','tempb2','tempa3','tempb3',
            'tempa4','tempb4','tempa5','tempb5',
            'hum0','hum1','hum2','tmp0','tmp1','tmp2'
            ]
bacteria_mo_su_sali=dict((el,0.0) for el in field_name)
pht_sensor = Phant(publicKey=public_bacteria_mo_su_sali, fields=field_name ,privateKey=private_bacteria_mo_su_sali,baseUrl=nectar_address)



#------------------------- below are definations for the sensors in the column ---------------------------------
#field_name=['tmp0','tmp1','tmp2','tmp3',
#            'hum0','hum1','hum2','hum3',
#           'dp0',
#            'ec0',
#            'gstmp0',
#            'pre0','pre1',
#            'pretmp0','pretmp1',
#            'dhttmp0',
#            'dhthum0',
#            'volt0',
#            'tmp4','tmp5','tmp6','tmp7','tmp8','tmp9','tmp10','tmp11','tmp12']
#sali_gs3_p=dict((el,0.0) for el in field_name)
#pht_salt_gs_p = Phant(publicKey=public_stanwell_sali_gs3_p, fields=field_name ,privateKey=private_stanwell_sali_gs3_p,baseUrl=nectar_address)


port_sensor  = 'USB VID:PID=2341:0042 SNR=557363037393516030D1'

#whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'bacteria.csv'

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
    #GPIO.output(25, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
    #sleep(5)
    #GPIO.output(26, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
    #sleep(5)

    #GPIO.output(24, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
    #sleep(2)
    #GPIO.output(24, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
    #sleep(10) # change 2 to 10


    # possible update: set time out for send result

    #sleep(10)
    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="75,3,clk,4,power,8,debug,1",initialize=True)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #sali_gs3_p['hum3']=float(current_read[-1])
    #sali_gs3_p['tmp3']=float(current_read[-2])


    sleep(10)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,4,power,25,points,2,dummies,1,interval_mm,200,debug,1",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    bacteria_mo_su_sali['tmp0']=float(current_read[-1])
    bacteria_mo_su_sali['hum0']=float(current_read[-2])

    sleep(5)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="75,5,clk,11,power,9,debug,1",initialize=True)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    bacteria_mo_su_sali['tmp1']=float(current_read[-1])
    bacteria_mo_su_sali['hum1']=float(current_read[-2])
    
    
    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,3,power,8,points,2,dummies,1,interval_mm,200,debug,1",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    bacteria_mo_su_sali['tmp2']=float(current_read[-1])
    bacteria_mo_su_sali['hum2']=float(current_read[-2])



    #sleep(5)
    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="75,11,clk,12,power,23,debug,1",initialize=True)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #sali_gs3_p['hum1']=float(current_read[-1])
    #sali_gs3_p['tmp1']=float(current_read[-2])

    #sleep(5)
    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="75,5,clk,53,power,9,debug,1",initialize=False)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #sali_gs3_p['hum2']=float(current_read[-1])
    #sali_gs3_p['tmp2']=float(current_read[-2])
    
       

    #sleep(2)
    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,10,power,48,points,2,dummies,1,interval_mm,200,debug,1",initialize=False)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #sali_gs3_p['dhthum0']=float(current_read[-1])
    #sali_gs3_p['dhttmp0']=float(current_read[-2])

    # voltage measurement
    # power,43,analog,15,point,3,interval_mm,200,debug,1
    #upload_phant(pht_salt_gs_p,sali_gs3_p,screen_display)
    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,BB22BBBA,dgin,50,snpw,42,htpw,35,itv,1000,otno,5",initialize=True)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    bacteria_mo_su_sali['tempa0']=float(current_read[2])
    bacteria_mo_su_sali['tempb0']=float(current_read[7])
    bacteria_mo_su_sali['su0']=float(current_read[7])-float(current_read[2])



    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,2032BC09,dgin,50,snpw,42,htpw,37,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    bacteria_mo_su_sali['tempa1']=float(current_read[2])
    bacteria_mo_su_sali['tempb1']=float(current_read[7])
    bacteria_mo_su_sali['su1']=float(current_read[7])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,172B99B4,dgin,50,snpw,42,htpw,39,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    bacteria_mo_su_sali['tempa2']=float(current_read[2])
    bacteria_mo_su_sali['tempb2']=float(current_read[7])
    bacteria_mo_su_sali['su2']=float(current_read[7])-float(current_read[2])
    

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,EC20CEBB,dgin,50,snpw,42,htpw,41,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    bacteria_mo_su_sali['tempa3']=float(current_read[2])
    bacteria_mo_su_sali['tempb3']=float(current_read[7])
    bacteria_mo_su_sali['su3']=float(current_read[7])-float(current_read[2])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,94EA9867,dgin,50,snpw,42,htpw,27,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    bacteria_mo_su_sali['tempa4']=float(current_read[2])
    bacteria_mo_su_sali['tempb4']=float(current_read[7])
    bacteria_mo_su_sali['su4']=float(current_read[7])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,03DF979F,dgin,50,snpw,42,htpw,29,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    bacteria_mo_su_sali['tempa5']=float(current_read[2])
    bacteria_mo_su_sali['tempb5']=float(current_read[7])
    bacteria_mo_su_sali['su5']=float(current_read[7])-float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,8,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    bacteria_mo_su_sali['mo0']=float(current_read[2])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,9,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    bacteria_mo_su_sali['mo1']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,10,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    bacteria_mo_su_sali['mo2']=float(current_read[2])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,11,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    bacteria_mo_su_sali['mo3']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,13,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    bacteria_mo_su_sali['mo4']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,14,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    bacteria_mo_su_sali['mo5']=float(current_read[2])


    upload_phant(pht_sensor,bacteria_mo_su_sali,screen_display)

    if save_to_file: fid.write("\n\r")
    # sleep to the next loop
    time.sleep(sleep_time_seconds)

        
      


