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
from time import sleep,gmtime, strftime 
import subprocess
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(25, GPIO.OUT)           # set GPIO24 as an output 
GPIO.setup(26, GPIO.OUT)           # set GPIO24 as an output 
GPIO.setup(24, GPIO.OUT)           # set GPIO24 as an output   


with open('/home/pi/script/pass/public_grange_5_mo_su', 'r') as myfile:
    public_grange_5_mo_su=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_grange_5_mo_su', 'r') as myfile:
    private_grange_5_mo_su=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/public_grange_5_luo2_dry', 'r') as myfile:
    public_grange_5_luo2_dry=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_grange_5_luo2_dry', 'r') as myfile:
    private_grange_5_luo2_dry=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/public_grange_5_luo2_wet', 'r') as myfile:
    public_grange_5_luo2_wet=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_grange_5_luo2_wet', 'r') as myfile:
    private_grange_5_luo2_wet=myfile.read().replace('\n', '')


with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')



#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['mo0','mo1','mo2','mo3','mo4','mo5','mo6','mo7',
            'su0','su1','su2','su3','su4','su5','su6','su7',
            'tmp0','tmp1','tmp2','tmp3','tmp4','tmp5','tmp6','tmp7',
            'dluo7','dlupe7','dlup7',
            'wluo7','wlupe7','wlup7'
            ]
grange_5_mo_su=dict((el,0.0) for el in field_name)
pht_grange_5_mo_su = Phant(publicKey=public_grange_5_mo_su, fields=field_name ,privateKey=private_grange_5_mo_su,baseUrl=nectar_address)



#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['dluo0','dlupe0','dlut0','dlup0',
            'dluo1','dlupe1','dlut1','dlup1',
            'dluo2','dlupe2','dlut2','dlup2',
            'dluo3','dlupe3','dlut3','dlup3',
            'dluo4','dlupe4','dlut4','dlup4',
            'dluo5','dlupe5','dlut5','dlup5',
            'dluo6','dlupe6','dlut6','dlup6',
            'rh','temp']
grange_5_luo2_dry=dict((el,0.0) for el in field_name)
pht_grange_5_luo2_dry= Phant(publicKey=public_grange_5_luo2_dry, fields=field_name ,privateKey=private_grange_5_luo2_dry,baseUrl=nectar_address)


#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['wluo0','wlupe0','wlut0','wlup0',
            'wluo1','wlupe1','wlut1','wlup1',
            'wluo2','wlupe2','wlut2','wlup2',
            'wluo3','wlupe3','wlut3','wlup3',
            'wluo4','wlupe4','wlut4','wlup4',
            'wluo5','wlupe5','wlut5','wlup5',
            'wluo6','wlupe6','wlut6','wlup6',
            'flow','tmp']
grange_5_luo2_wet=dict((el,0.0) for el in field_name)
pht_grange_5_luo2_wet= Phant(publicKey=public_grange_5_luo2_wet, fields=field_name ,privateKey=private_grange_5_luo2_wet,baseUrl=nectar_address)




port_sensor  = 'USB VID:PID=2341:0042 SNR=5573631383735150B0E0'   #grange 5
#port_sensor  = 'USB VID:PID=2341:0042 SNR=55639303035351C07261'  #grange 3

# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'grange5.csv'

sleep_time_seconds=45*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)



while True: 
    if screen_display: print strftime("%Y-%m-%d %H:%M:%S", gmtime())
    if save_to_file: fid.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())  )
# ------------------------------- below goes to electrochem_o2  --------------------------------------------
    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,166F9644,dgin,50,snpw,44,htpw,32,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    grange_5_mo_su['tmp0']=float(current_read[2])
    grange_5_mo_su['su0']=float(current_read[7])-float(current_read[2])
    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,BCF79459,dgin,50,snpw,44,htpw,30,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    grange_5_mo_su['tmp1']=float(current_read[2])
    grange_5_mo_su['su1']=float(current_read[7])-float(current_read[2])
        
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,A21BBB00,dgin,50,snpw,44,htpw,28,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    grange_5_mo_su['tmp2']=float(current_read[2])
    grange_5_mo_su['su2']=float(current_read[7])-float(current_read[2])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,E144BA59,dgin,50,snpw,44,htpw,26,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    grange_5_mo_su['tmp3']=float(current_read[2])
    grange_5_mo_su['su3']=float(current_read[7])-float(current_read[2])
    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,0AE6B9B0,dgin,50,snpw,44,htpw,40,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    grange_5_mo_su['tmp4']=float(current_read[2])
    grange_5_mo_su['su4']=float(current_read[7])-float(current_read[2])
    
            
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,5F4ABCE6,dgin,50,snpw,44,htpw,38,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    grange_5_mo_su['tmp5']=float(current_read[2])
    grange_5_mo_su['su5']=float(current_read[7])-float(current_read[2])   
    
    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,0014B95A,dgin,50,snpw,44,htpw,36,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    grange_5_mo_su['tmp6']=float(current_read[2])
    grange_5_mo_su['su6']=float(current_read[7])-float(current_read[2])   
    
    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,1D02BA23,dgin,50,snpw,44,htpw,34,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    grange_5_mo_su['tmp7']=float(current_read[2])
    grange_5_mo_su['su7']=float(current_read[7])-float(current_read[2])    
    

    #sleep(2)
    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,8,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #grange_5_mo_su['mo0']=float(current_read[2])

    #sleep(2)
    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,9,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #grange_5_mo_su['mo1']=float(current_read[2])


    #sleep(2)
    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,10,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #grange_5_mo_su['mo2']=float(current_read[2])


    #sleep(2)
    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,11,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #grange_5_mo_su['mo3']=float(current_read[2])


    #sleep(2)
    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,12,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #grange_5_mo_su['mo4']=float(current_read[2])


    #sleep(2)
    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,13,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #grange_5_mo_su['mo5']=float(current_read[2])


    #sleep(2)
    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,14,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #grange_5_mo_su['mo6']=float(current_read[2])


    #sleep(2)
    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,15,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #grange_5_mo_su['mo7']=float(current_read[2])


    sleep(5)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,6,serial,2",initialize=False)
    if screen_display: print msg.replace('\r','') 
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    grange_5_mo_su['dluo7'] = float(current_read[-2])
    grange_5_mo_su['dlupe7'] = float(current_read[-4])
    #grange_3_luo2_dry['dlut0'] = float(current_read[-6])
    grange_5_mo_su['dlup7'] = float(current_read[-8])

    #sleep(5)
    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,6,serial,3",initialize=False)
    #if screen_display: print msg.replace('\r','') 
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(' ')[0:-1]
    #grange_5_mo_su['wluo7'] = float(current_read[-2])
    #grange_5_mo_su['wlupe7'] = float(current_read[-4])
    ##grange_3_luo2_dry['wlut7'] = float(current_read[-6])
    #grange_5_mo_su['wlup7'] = float(current_read[-8])

    upload_phant(pht_grange_5_mo_su,grange_5_mo_su,screen_display)
    

    sleep(5)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,24,serial,2",initialize=False)
    if screen_display: print msg.replace('\r','') 
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    grange_5_luo2_dry['dluo0'] = float(current_read[-2])
    grange_5_luo2_dry['dlupe0'] = float(current_read[-4])
    grange_5_luo2_dry['dlut0'] = float(current_read[-6])
    grange_5_luo2_dry['dlup0'] = float(current_read[-8])

    sleep(5)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,22,serial,2",initialize=False)
    if screen_display: print msg.replace('\r','') 
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    grange_5_luo2_dry[ 'dluo1'] = float(current_read[-2])
    grange_5_luo2_dry['dlupe1'] = float(current_read[-4])
    grange_5_luo2_dry[ 'dlut1'] = float(current_read[-6])
    grange_5_luo2_dry[ 'dlup1'] = float(current_read[-8])
    

    sleep(5)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,23,serial,2",initialize=False)
    if screen_display: print msg.replace('\r','') 
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    grange_5_luo2_dry[ 'dluo2'] = float(current_read[-2])
    grange_5_luo2_dry['dlupe2'] = float(current_read[-4])
    grange_5_luo2_dry[ 'dlut2'] = float(current_read[-6])
    grange_5_luo2_dry[ 'dlup2'] = float(current_read[-8])


    sleep(5)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,25,serial,2",initialize=False)
    if screen_display: print msg.replace('\r','') 
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    grange_5_luo2_dry[ 'dluo3'] = float(current_read[-2])
    grange_5_luo2_dry['dlupe3'] = float(current_read[-4])
    grange_5_luo2_dry[ 'dlut3'] = float(current_read[-6])
    grange_5_luo2_dry[ 'dlup3'] = float(current_read[-8])



    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,9,serial,2",initialize=False)
    if screen_display: print msg.replace('\r','') 
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    grange_5_luo2_dry[ 'dluo4'] = float(current_read[-2])
    grange_5_luo2_dry['dlupe4'] = float(current_read[-4])
    grange_5_luo2_dry[ 'dlut4'] = float(current_read[-6])
    grange_5_luo2_dry[ 'dlup4'] = float(current_read[-8])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,8,serial,2",initialize=False)
    if screen_display: print msg.replace('\r','') 
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    grange_5_luo2_dry[ 'dluo5'] = float(current_read[-2])
    grange_5_luo2_dry['dlupe5'] = float(current_read[-4])
    grange_5_luo2_dry[ 'dlut5'] = float(current_read[-6])
    grange_5_luo2_dry[ 'dlup5'] = float(current_read[-8])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,7,serial,2",initialize=False)
    if screen_display: print msg.replace('\r','') 
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    grange_5_luo2_dry[ 'dluo6'] = float(current_read[-2])
    grange_5_luo2_dry['dlupe6'] = float(current_read[-4])
    grange_5_luo2_dry[ 'dlut6'] = float(current_read[-6])
    grange_5_luo2_dry[ 'dlup6'] = float(current_read[-8])

    # enclosure temperature and humidity    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,10,power,48,points,2,dummies,1,interval_mm,2000,debug,0",initialize=False)
    if screen_display: print msg.replace('\r','') 
    #if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    grange_5_luo2_dry['rh']=float(current_read[-1])
    grange_5_luo2_dry['temp']=float(current_read[-2])

    upload_phant(pht_grange_5_luo2_dry,grange_5_luo2_dry,screen_display)


    sleep(5)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,35,serial,3",initialize=False)
    if screen_display: print msg.replace('\r','') 
    #if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    grange_5_luo2_wet[ 'wluo0'] = float(current_read[-2])
    grange_5_luo2_wet['wlupe0'] = float(current_read[-4])
    grange_5_luo2_wet[ 'wlut0'] = float(current_read[-6])
    grange_5_luo2_wet[ 'wlup0'] = float(current_read[-8])


    sleep(5)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,37,serial,3",initialize=False)
    if screen_display: print msg.replace('\r','') 
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    grange_5_luo2_wet[ 'wluo1'] = float(current_read[-2])
    grange_5_luo2_wet['wlupe1'] = float(current_read[-4])
    grange_5_luo2_wet[ 'wlut1'] = float(current_read[-6])
    grange_5_luo2_wet[ 'wlup1'] = float(current_read[-8])



    sleep(5)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,39,serial,3",initialize=False)
    if screen_display: print msg.replace('\r','') 
    #if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    grange_5_luo2_wet[ 'wluo2'] = float(current_read[-2])
    grange_5_luo2_wet['wlupe2'] = float(current_read[-4])
    grange_5_luo2_wet[ 'wlut2'] = float(current_read[-6])
    grange_5_luo2_wet[ 'wlup2'] = float(current_read[-8])


    sleep(5)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,41,serial,3",initialize=False)
    if screen_display: print msg.replace('\r','') 
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    grange_5_luo2_wet[ 'wluo3'] = float(current_read[-2])
    grange_5_luo2_wet['wlupe3'] = float(current_read[-4])
    grange_5_luo2_wet[ 'wlut3'] = float(current_read[-6])
    grange_5_luo2_wet[ 'wlup3'] = float(current_read[-8])

    sleep(5)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,27,serial,3",initialize=False)
    if screen_display: print msg.replace('\r','') 
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    grange_5_luo2_wet[ 'wluo4'] = float(current_read[-2])
    grange_5_luo2_wet['wlupe4'] = float(current_read[-4])
    grange_5_luo2_wet[ 'wlut4'] = float(current_read[-6])
    grange_5_luo2_wet[ 'wlup4'] = float(current_read[-8])


    sleep(5)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,29,serial,3",initialize=False)
    if screen_display: print msg.replace('\r','') 
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    grange_5_luo2_wet[ 'wluo5'] = float(current_read[-2])
    grange_5_luo2_wet['wlupe5'] = float(current_read[-4])
    grange_5_luo2_wet[ 'wlut5'] = float(current_read[-6])
    grange_5_luo2_wet[ 'wlup5'] = float(current_read[-8])

    sleep(5)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,31,serial,3",initialize=False)
    if screen_display: print msg.replace('\r','') 
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    grange_5_luo2_wet[ 'wluo6'] = float(current_read[-2])
    grange_5_luo2_wet['wlupe6'] = float(current_read[-4])
    grange_5_luo2_wet[ 'wlut6'] = float(current_read[-6])
    grange_5_luo2_wet[ 'wlup6'] = float(current_read[-8])


    upload_phant(pht_grange_5_luo2_wet,grange_5_luo2_wet,screen_display)


    #GPIO.output(25, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
    #sleep(5)
    #GPIO.output(26, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
    #sleep(5)

    #GPIO.output(24, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
    #sleep(1)
    #GPIO.output(24, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
    #sleep(2)
    #
    #
    #GPIO.output(24, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
    #sleep(1)
    #GPIO.output(24, 0)         # set GPIO24 to 1/GPIO.HIGH/True  

    #sleep(2)

    #### below is for pressure 
    #GPIO.output(25, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
    #sleep(5)
    #GPIO.output(26, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
    #sleep(5)


    #sleep(2)
    #
    #sleep(2)







    if save_to_file: fid.write('\n\r')
    time.sleep(sleep_time_seconds)

        
      
