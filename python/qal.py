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
from time import sleep             # lets us have a delay  
from time import sleep,gmtime, strftime             # lets us have a delay  
import subprocess
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(25, GPIO.OUT)           # set GPIO24 as an output 
GPIO.setup(26, GPIO.OUT)           # set GPIO24 as an output 
GPIO.setup(24, GPIO.OUT)           # set GPIO24 as an output   


with open('/home/pi/script/pass/public_qal_moisture_suction', 'r') as myfile:
    public_qal_moisture_suction=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_qal_moisture_suction', 'r') as myfile:
    private_qal_moisture_suction=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/public_qal_sali_gs3_p', 'r') as myfile:
    public_qal_sali_gs3_p=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_qal_sali_gs3_p', 'r') as myfile:
    private_qal_sali_gs3_p=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')



#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['mo0','mo1','mo2','mo3','mo4','mo5','mo6','mo7','mo8','mo9',
            'su0','su1','su2','su3','su4','su5','su6','su7','su8','su9',
            'tmp0','tmp1','tmp2','tmp3','tmp4','tmp5','tmp6','tmp7','tmp8','tmp9'
            ]
qal_mo_su=dict((el,0.0) for el in field_name)
pht_sensor = Phant(publicKey=public_qal_moisture_suction, fields=field_name ,privateKey=private_qal_moisture_suction,baseUrl=nectar_address)



#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['tmp0','tmp1','tmp2',
            'hum0','hum1','hum2',
            'dp0','dp1',
            'ec0','ec1',
            'gstmp0','gstemp1',
            'pre0','pre1',
            'pretmp0','pretmp1',
            'dhttmp0',
            'dhthum0',
            'volt0',
            'tmp4','tmp5','tmp6','tmp7','tmp8','tmp9','tmp10','tmp11','tmp12']
qal_sali_gs3_p=dict((el,0.0) for el in field_name)
pht_qal_sali_gs3_p= Phant(publicKey=public_qal_sali_gs3_p, fields=field_name ,privateKey=private_qal_sali_gs3_p,baseUrl=nectar_address)






port_sensor  = 'USB VID:PID=2341:0042 SNR=9563533373035120B2F1'


# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'qal.csv'

sleep_time_seconds=45*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)



while True: 
# ------------------------------- below goes to electrochem_o2  --------------------------------------------

    if screen_display: print strftime("%Y-%m-%d %H:%M:%S", gmtime())
    if save_to_file: fid.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())  )


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,C824B9E0,dgin,13,snpw,6,htpw,22,itv,12000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['tmp0']=float(current_read[2])
    qal_mo_su['su0']=float(current_read[7])-float(current_read[2])
    
    
    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,C1C1BCFF,dgin,13,snpw,6,htpw,24,itv,12000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['tmp1']=float(current_read[2])
    qal_mo_su['su1']=float(current_read[7])-float(current_read[2])
    
    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,DA24B9D5,dgin,13,snpw,6,htpw,33,itv,12000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['tmp2']=float(current_read[2])
    qal_mo_su['su2']=float(current_read[7])-float(current_read[2])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,2F219674,dgin,13,snpw,6,htpw,31,itv,12000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['tmp3']=float(current_read[2])
    qal_mo_su['su3']=float(current_read[7])-float(current_read[2])
    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,6D0D96B6,dgin,13,snpw,6,htpw,29,itv,12000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['tmp4']=float(current_read[2])
    qal_mo_su['su4']=float(current_read[7])-float(current_read[2])
    
            
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,952BB9EB,dgin,50,snpw,42,htpw,27,itv,12000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['tmp5']=float(current_read[2])
    qal_mo_su['su5']=float(current_read[7])-float(current_read[2])   
    
    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,A4A2BB0E,dgin,50,snpw,42,htpw,41,itv,12000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['tmp6']=float(current_read[2])
    qal_mo_su['su6']=float(current_read[7])-float(current_read[2])   
    
    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,A16BB933,dgin,50,snpw,42,htpw,39,itv,12000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['tmp7']=float(current_read[2])
    qal_mo_su['su7']=float(current_read[7])-float(current_read[2])    
    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,76E2B94A,dgin,50,snpw,42,htpw,37,itv,12000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['tmp8']=float(current_read[2])
    qal_mo_su['su8']=float(current_read[7])-float(current_read[2])
    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,F8FD964A,dgin,50,snpw,42,htpw,35,itv,12000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['tmp9']=float(current_read[2])
    qal_mo_su['su9']=float(current_read[7])-float(current_read[2])        


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,14,power,40,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['mo0']=float(current_read[2])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,13,power,26,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['mo1']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,12,power,28,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['mo2']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,11,power,30,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['mo3']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,10,power,32,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['mo4']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,9,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['mo5']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,8,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['mo6']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,7,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['mo7']=float(current_read[2])



    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,6,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['mo8']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,5,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_mo_su['mo9']=float(current_read[2])

    upload_phant(pht_sensor,qal_mo_su,screen_display)
    

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="75,10,clk,3,power,25,debug,1",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_sali_gs3_p['tmp0'] = float(current_read[-2])
    qal_sali_gs3_p['hum0'] = float(current_read[-1])
    
    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="75,52,clk,5,power,38,debug,1",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_sali_gs3_p['tmp1'] = float(current_read[-2])
    qal_sali_gs3_p['hum1'] = float(current_read[-1])
   
    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,2,power,36,points,2,dummies,1,interval_mm,2000,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_sali_gs3_p['tmp4']=float(current_read[-1])
    qal_sali_gs3_p['tmp5']=float(current_read[-2])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,2,power,34,points,2,dummies,1,interval_mm,2000,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_sali_gs3_p['tmp6']=float(current_read[-1])
    qal_sali_gs3_p['tmp7']=float(current_read[-2])

    sleep(2)
   # msg=serial_openlock.get_result_by_input(port=port_sensor,command="75,2,clk,52,power,36,debug,1",initialize=False)
   # if screen_display: print msg.rstrip()
   # if save_to_file: fid.write(delimiter+msg.rstrip())
   # current_read=msg.split(',')[0:-1]
   # qal_sali_gs3_p['temp2'] = float(current_read[-2])
   # qal_sali_gs3_p['hum2'] = float(current_read[-1])

    ### below is for pressure 
#    GPIO.output(25, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
#    sleep(5)
#    GPIO.output(26, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
#    sleep(5)

#    GPIO.output(24, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
#    sleep(1)
#    GPIO.output(24, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
#    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="power_switch,9,power_switch_status,1",initialize=False)
    sleep(5)

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="9548,2,type,5803,dummies,1,power,9,debug,1,points,1",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    try:   
       qal_sali_gs3_p['pre0'] = float(current_read[-1])
       qal_sali_gs3_p['pretmp0'] = float(current_read[-2])
    except Exception, e:
        if screen_display: print '5803 ,2,does not get results'
        continue
#    sleep(2)
#    GPIO.output(24, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
#    sleep(1)
#    GPIO.output(24, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
#    sleep(2)

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="9548,3,type,5803,dummies,1,power,9,debug,1,points,1",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    try:
       qal_sali_gs3_p['pre1'] = float(current_read[-1])
       qal_sali_gs3_p['pretmp1'] = float(current_read[-2])
    except Exception, e:
        if screen_display: print '5803 ,3,does not get results'
        continue
#    sleep(2)
    ### below is for pressure 
#    GPIO.output(25, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
#    sleep(5)
#    GPIO.output(26, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
#    sleep(5)

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="power_switch,9,power_switch_status,0",initialize=False)

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="12,51,power,8,debug,1",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_sali_gs3_p['dp0'] = float(current_read[7])
    qal_sali_gs3_p['ec0'] = float(current_read[9])
    qal_sali_gs3_p['gstmp0'] = float(current_read[8])
    
    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="12,53,power,7,debug,1",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_sali_gs3_p['dp1'] = float(current_read[7])
    qal_sali_gs3_p['ec1'] = float(current_read[9])
    qal_sali_gs3_p['gstemp1'] = float(current_read[8])
    

    # enclosure temperature and humidity
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,10,power,48,points,2,dummies,1,interval_mm,2000,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    qal_sali_gs3_p['dhthum0']=float(current_read[-1])
    qal_sali_gs3_p['dhttmp0']=float(current_read[-2])


    upload_phant(pht_qal_sali_gs3_p,qal_sali_gs3_p,screen_display)






    time.sleep(sleep_time_seconds)

        
      
