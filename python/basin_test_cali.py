#!/usr/bin/python
import serial
import os
import time
import numpy as np
import sys
import paho.mqtt.client as mqtt
import json
from phant import Phant
import serial_openlock
import get_ip
from upload_phant import upload_phant
# below required by gpio
#import RPi.GPIO as  GPIO           # import RPi.GPIO module  
from time import sleep,gmtime, strftime,localtime             # lets us have a delay  
#GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
#GPIO.setup(25, GPIO.OUT)           # set GPIO24 as an output   
#GPIO.setup(26, GPIO.OUT)           # set GPIO24 as an output   
#GPIO.setup(24, GPIO.OUT)           # set GPIO24 as an output   

# make pycamera working
import subprocess
import picamera

#command_taking_picture_basin_1='ssh uqxlei@    '


with open('/home/pi/pyduino/credential/basin_test.json') as f:
        credential = json.load(f)


#with open('/home/pi/script/pass/public_basin_test_wenqiang_mo_su', 'r') as myfile:
#    public_basin_test_wenqiang_mo_su=myfile.read().replace('\n', '')

#with open('/home/pi/script/pass/private_basin_test_wenqiang_mo_su', 'r') as myfile:
#    private_basin_test_wenqiang_mo_su=myfile.read().replace('\n', '')

#with open('/home/pi/script/pass/public_basin_test_wenqiang_mo_su_scale', 'r') as myfile:
#    public_basin_test_wenqiang_mo_su_scale=myfile.read().replace('\n', '')
#
#with open('/home/pi/script/pass/private_basin_test_wenqiang_mo_su_scale', 'r') as myfile:
#    private_basin_test_wenqiang_mo_su_scale=myfile.read().replace('\n', '')

#with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
#    nectar_address=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/cmd_area51_taking_photo_basin', 'r') as myfile:
    cmd_area51_taking_photo_basin=myfile.read().replace('\n', '')



#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['moa1','moa2','moa3','mob1','mob2','mob3','moc1','moc2','moc3',
            'sua1','sua2','sua3','sub1','sub2','sub3','suc1','suc2','suc3',
            'tempa1_a','tempa2_a','tempa3_a','tempb1_a','tempb2_a','tempb3_a',
            'tempa1_b','tempa2_b','tempa3_b','tempb1_b','tempb2_b','tempb3_b',
            'tempc1_a','tempc2_a','tempc3_a',
            'tempc1_b','tempc2_b','tempc3_b', 
            'temp_dht22','tmp1','tmp2','tmp3','tmp4','tmp5','tmp6','tmp7','tmp8',
            'hum_dht22','scale1','scale2','scale3'] 
basin_test_wenqiang_mo_su=dict((el,0.0) for el in field_name)
pht_basin_test_wenqiang_mo_su= Phant(publicKey=credential['public_basin_test_wenqiang_mo_su'], fields=field_name ,privateKey=credential['private_basin_test_wenqiang_mo_su'],baseUrl=credential['nectar_address'])
#pht_basin_test_wenqiang_mo_su= Phant(publicKey=public_basin_test_wenqiang_mo_su, fields=field_name ,privateKey=private_basin_test_wenqiang_mo_su,baseUrl=nectar_address)


#------------------------- below are definations for the sensors in the column ---------------------------------
#field_name=['tmp3','tmp4','tmp5','tmp6','tmp7','tmp8','tmp9','tmp10',
#            'hum3','hum4','hum5','hum6','hum7','hum8','hum9','hum10',
#            'scale1','scale2']
#basin_test_wenqiang_scale=dict((el,0.0) for el in field_name)
#pht_basin_test_wenqiang_scale = Phant(publicKey=public_basin_test_wenqiang_mo_su_scale, fields=field_name ,privateKey=private_basin_test_wenqiang_mo_su_scale,baseUrl=nectar_address)

port_sensor = 'USB VID:PID=2341:0042 SNR=8573531303335131F052'
port_scale1='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2.1.1:1.0-port0'
port_scale2='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2.1.2:1.0-port0'
port_scale3='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2.2:1.0-port0'

scale1 = serial.Serial(port_scale1,timeout=20)
scale2 = serial.Serial(port_scale2,timeout=20)
scale3 = serial.Serial(port_scale3,timeout=20)

scale1.write('IP\n\r')
scale2.write('IP\n\r')
scale3.write('IP\n\r')

time.sleep(2)
str_scale1=scale1.readline()
str_scale2=scale2.readline()
str_scale3=scale3.readline()

screen_display=True

scale_attempts=1
while scale_attempts<8:
    try:
        scale1.write('IP\n\r')
        scale2.write('IP\n\r')
        scale3.write('IP\n\r')
        time.sleep(2)#wait for two seconds before leaving   
        str_scale1=scale1.readline()
        str_scale2=scale2.readline()
        str_scale3=scale3.readline()
        weight_scale1=str_scale1.split()[0]
        weight_scale2=str_scale2.split()[0]
        weight_scale3=str_scale3.split()[0]
        break
    except Exception, e:
        if screen_display: print "scale reading failed,"+str(scale_attempts)+" " + str(e)
        scale_attempts+=1
        time.sleep(3)
        scale1.close()
        scale2.close()
        scale3.close()
        time.sleep(2)
        scale1 = serial.Serial(port_scale1,timeout=20)
        scale2 = serial.Serial(port_scale2,timeout=20)
        scale3 = serial.Serial(port_scale3,timeout=20)
       

#time.sleep(10)
#scale1.write('IP\n\r')
#scale2.write('IP\n\r')
#
#time.sleep(2)
#str_scale1=scale1.readline()
#str_scale2=scale2.readline()

#weight_scale1=str_scale1.split()[0]
#weight_scale2=str_scale2.split()[0]

#whether the result will be displayed on the screen
#screen_display=True
temp_sampling_number=20

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'basin_test_wenqiang.csv'
sleep_time_seconds=30*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'

while True:
    try:
        next_reading = time.time()
        client = mqtt.Client()
        client.username_pw_set(credential['access_token'])
        client.connect(credential['thingsboard_host'], 1883, 60)
        client.loop_start()
        break
    except Exception, e:
        time.sleep(60)


if save_to_file: fid= open(file_name,'a',0)


try:
    while True: 
        ### -------------------- below is to processing data from suction, moisture-------------------------
        if screen_display: print strftime("%Y-%m-%d %H:%M:%S", localtime())
        if save_to_file: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime())  )
       
        # time_now=time.strftime("%d/%b/%Y %H:%M:%S")
        #if screen_display: print time_now,delimiter,weight_scale1.rstrip(),delimiter,weight_scale2.rstrip().rstrip()
        #if save_to_file: fid.write(time_now+delimiter+weight_scale1+delimiter+weight_scale2+'\n\r')
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
    
    
        # sleep(10)
        # msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,4,power,25,points,2,dummies,1,interval_mm,200,debug,1",initialize=False)
        # if screen_display: print msg.rstrip()
        # if save_to_file: fid.write(delimiter+msg.rstrip())
        # current_read=msg.split(',')[0:-1]
        # bacteria_mo_su_sali['tmp0']=float(current_read[-1])
        # bacteria_mo_su_sali['hum0']=float(current_read[-2])
     
        # sleep(5)
        # msg=serial_openlock.get_result_by_input(port=port_sensor,command="75,5,clk,11,power,9,debug,1",initialize=True)
        # if screen_display: print msg.rstrip()
        # if save_to_file: fid.write(delimiter+msg.rstrip())
        # current_read=msg.split(',')[0:-1]
        # bacteria_mo_su_sali['tmp1']=float(current_read[-1])
        # bacteria_mo_su_sali['hum1']=float(current_read[-2])
        # 
        # 
        # sleep(2)
        # msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,3,power,8,points,2,dummies,1,interval_mm,200,debug,1",initialize=False)
        # if screen_display: print msg.rstrip()
        # if save_to_file: fid.write(delimiter+msg.rstrip())
        # current_read=msg.split(',')[0:-1]
        # bacteria_mo_su_sali['tmp2']=float(current_read[-1])
        # bacteria_mo_su_sali['hum2']=float(current_read[-2])
        
    
        # voltage measurement
        # power,43,analog,15,point,3,interval_mm,200,debug,1
    #--------------for suction sensors---------------------
        sleep(2)
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,9FEA989F,dgin,50,snpw,42,htpw,35,itv,24000,otno,5",initialize=True)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['tempa1_a']=float(current_read[2])
        basin_test_wenqiang_mo_su['tempa1_b']=float(current_read[7])
        basin_test_wenqiang_mo_su['sua1']=float(current_read[7])-float(current_read[2])
    
    
    
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,927098DF,dgin,50,snpw,42,htpw,37,itv,24000,otno,5",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['tempb1_a']=float(current_read[2])
        basin_test_wenqiang_mo_su['tempb1_b']=float(current_read[7])
        basin_test_wenqiang_mo_su['sub1']=float(current_read[7])-float(current_read[2])
    
    
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,8FE29975,dgin,50,snpw,42,htpw,39,itv,24000,otno,5",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['tempc1_a']=float(current_read[2])
        basin_test_wenqiang_mo_su['tempc1_b']=float(current_read[7])
        basin_test_wenqiang_mo_su['suc1']=float(current_read[7])-float(current_read[2])
        
    
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,2032BC09,dgin,50,snpw,42,htpw,41,itv,24000,otno,5",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['tempa2_a']=float(current_read[2])
        basin_test_wenqiang_mo_su['tempa2_b']=float(current_read[7])
        basin_test_wenqiang_mo_su['sua2']=float(current_read[7])-float(current_read[2])
    
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,EC20CEBB,dgin,50,snpw,42,htpw,27,itv,24000,otno,5",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['tempb2_a']=float(current_read[2])
        basin_test_wenqiang_mo_su['tempb2_b']=float(current_read[7])
        basin_test_wenqiang_mo_su['sub2']=float(current_read[7])-float(current_read[2])
    
    
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,172B99B4,dgin,50,snpw,42,htpw,29,itv,24000,otno,5",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['tempc2_a']=float(current_read[2])
        basin_test_wenqiang_mo_su['tempc2_b']=float(current_read[7])
        basin_test_wenqiang_mo_su['suc2']=float(current_read[7])-float(current_read[2])
    
    
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,B5779932,dgin,13,snpw,24,htpw,22,itv,24000,otno,5",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['tempa3_a']=float(current_read[2])
        basin_test_wenqiang_mo_su['tempa3_b']=float(current_read[7])
        basin_test_wenqiang_mo_su['sua3']=float(current_read[7])-float(current_read[2])
     
     
     
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,4BA697D5,dgin,13,snpw,24,htpw,23,itv,24000,otno,5",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['tempb3_a']=float(current_read[2])
        basin_test_wenqiang_mo_su['tempb3_b']=float(current_read[7])
        basin_test_wenqiang_mo_su['sub3']=float(current_read[7])-float(current_read[2])
     
     
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,C9B499BB,dgin,13,snpw,24,htpw,25,itv,24000,otno,5",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['tempc3_a']=float(current_read[2])
        basin_test_wenqiang_mo_su['tempc3_b']=float(current_read[7])
        basin_test_wenqiang_mo_su['suc3']=float(current_read[7])-float(current_read[2])
    
    #----------for moisture sensors---------------
        sleep(2)
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,8,power,44,point,3,interval_mm,200,debug,0",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['moa1']=float(current_read[2])
    
        sleep(2)
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,9,power,44,point,3,interval_mm,200,debug,0",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['mob1']=float(current_read[2])
    
    
        sleep(2)
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,10,power,44,point,3,interval_mm,200,debug,0",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['moc1']=float(current_read[2])
    
        sleep(2)
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,11,power,44,point,3,interval_mm,200,debug,0",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['moa2']=float(current_read[2])
    
    
        sleep(2)
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,13,power,44,point,3,interval_mm,200,debug,0",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['mob2']=float(current_read[2])
    
    
        sleep(2)
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,14,power,44,point,3,interval_mm,200,debug,0",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['moc2']=float(current_read[2])
    
        sleep(2)
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,0,power,32,point,3,interval_mm,200,debug,0",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['moa3']=float(current_read[2])
    
    
        sleep(2)
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,1,power,30,point,3,interval_mm,200,debug,0",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['mob3']=float(current_read[2])
    
    
        sleep(2)
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,2,power,28,point,3,interval_mm,200,debug,0",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['moc3']=float(current_read[2])
    
    
    
    #----------for moisture and humidity sensors on board---------------
        sleep(2)
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,10,power,48,points,1,dummies,1,interval_mm,200,debug,0",initialize=False)
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        basin_test_wenqiang_mo_su['temp_dht22']=float(current_read[-1])
        basin_test_wenqiang_mo_su['hum_dht22']=float(current_read[-2])
    
        
        #sleep(5)
        #msg=serial_openlock.get_result_by_input(port=port_sensor,command="75,10,clk,51,power,24,debug,1",initialize=True)
        #if screen_display: print msg.rstrip()
        #if save_to_file: fid.write(delimiter+msg.rstrip())
        #current_read=msg.split(',')[0:-1]
        #bacteria_sali_scale['tmp4']=float(current_read[-1])
        #bacteria_sali_scale['hum4']=float(current_read[-2])
    
        #sleep(5)
        #msg=serial_openlock.get_result_by_input(port=port_sensor,command="75,52,clk,53,power,22,debug,1",initialize=True)
        #if screen_display: print msg.rstrip()
        #if save_to_file: fid.write(delimiter+msg.rstrip())
        #current_read=msg.split(',')[0:-1]
        #bacteria_sali_scale['tmp5']=float(current_read[-1])
        #bacteria_sali_scale['hum5']=float(current_read[-2])
    
        #sleep(2)
        #msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,12,power,22,points,2,dummies,1,interval_mm,200,debug,1",initialize=False)
        #if screen_display: print msg.rstrip()
        #if save_to_file: fid.write(delimiter+msg.rstrip())
        #current_read=msg.split(',')[0:-1]
        #bacteria_sali_scale['tmp6']=float(current_read[-1])
        #bacteria_sali_scale['hum6']=float(current_read[-2])
        
        # sleep(2)
        # time_now=time.strftime("%d/%b/%Y %H:%M:%S")
        # if screen_display: print time_now,delimiter,weight_scale1.rstrip(),delimiter,weight_scale2.rstrip()
        # if save_to_file: fid.write(time_now+delimiter+weight_scale1+delimiter+weight_scale2+'\n\r')  
        
        
        #----------for scale reading display---------------
        time_now=time.strftime("%d/%b/%Y %H:%M:%S")
        if screen_display: print time_now,delimiter,weight_scale1.rstrip(),delimiter,weight_scale2.rstrip(),delimiter,weight_scale3.rstrip()
        if save_to_file: fid.write(time_now+delimiter+weight_scale1+delimiter+weight_scale2+delimiter+weight_scale3+'\n\r')  
        #if screen_display: print time_now,delimiter,weight_scale1.rstrip()
        #if save_to_file: fid.write(time_now+delimiter+weight_scale1+'\n\r') 
     
        scale_attempts=1
        while scale_attempts<8:
            try:
                scale1.write('IP\n\r')
                scale2.write('IP\n\r')
                scale3.write('IP\n\r')
                time.sleep(2)#wait for two seconds before leaving   
                str_scale1=scale1.readline()
                str_scale2=scale2.readline()
                str_scale3=scale3.readline()
                weight_scale1=str_scale1.split()[0]
                weight_scale2=str_scale2.split()[0]
                weight_scale3=str_scale3.split()[0]
                basin_test_wenqiang_mo_su['scale1']=float(weight_scale1)
                basin_test_wenqiang_mo_su['scale2']=float(weight_scale2)
                basin_test_wenqiang_mo_su['scale3']=float(weight_scale3)
                break
            except Exception, e:
                if screen_display: print "scale reading failed,"+str(scale_attempts)+" " + str(e)
                scale_attempts+=1
                time.sleep(30)
                scale1.close()
                scale2.close()
                scale3.close()
                time.sleep(20)
                scale1 = serial.Serial(port_scale1,timeout=20)
                scale2 = serial.Serial(port_scale2,timeout=20)
                scale3 = serial.Serial(port_scale3,timeout=20)
                
        
    
        client.publish('v1/devices/me/telemetry', json.dumps(basin_test_wenqiang_mo_su), 1)    
        upload_phant(pht_basin_test_wenqiang_mo_su,basin_test_wenqiang_mo_su,screen_display)
    
        #camera = picamera.PiCamera()
        #camera.resolution = (3280,2464)
        #time_now=time.strftime("%Y_%b_%d_%H_%M_%S")
        #file_name_basin_2=time_now+'_bct_basin_2.jpg'
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="power_switch,49,power_switch_status,1",initialize=False)
        time.sleep(2)
        #camera.capture('/home/pi/photo/'+file_name_basin_2)
        process=subprocess.Popen('/home/pi/script/raspistill_snapshot_basin_test_cali.sh', stdout=subprocess.PIPE)
    
        process=subprocess.Popen(cmd_area51_taking_photo_basin.split(), stdout=subprocess.PIPE)
        time.sleep(9)
        msg=serial_openlock.get_result_by_input(port=port_sensor,command="power_switch,49,power_switch_status,0",initialize=False)
        #camera.close()
    
    
    
    
        if save_to_file: fid.write("\n\r")
        # sleep to the next loop
        time.sleep(sleep_time_seconds)

        
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()

     
