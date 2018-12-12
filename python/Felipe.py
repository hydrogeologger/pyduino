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
#import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep,gmtime, strftime,localtime             # lets us have a delay  
#GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
#GPIO.setup(25, GPIO.OUT)           # set GPIO24 as an output   
#GPIO.setup(26, GPIO.OUT)           # set GPIO24 as an output   
#GPIO.setup(24, GPIO.OUT)           # set GPIO24 as an output   

# make pycamera working
import subprocess
import picamera

#command_taking_picture_basin_1='ssh uqxlei@    '


with open('/home/pi/script/pass/public_amphiroll_tank1', 'r') as myfile:
    public_amphiroll_tank1=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_amphiroll_tank1', 'r') as myfile:
    private_amphiroll_tank1=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/public_amphiroll_tank2', 'r') as myfile:
    public_amphiroll_tank2=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_amphiroll_tank2', 'r') as myfile:
    private_amphiroll_tank2=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/public_amphiroll_tank3', 'r') as myfile:
    public_amphiroll_tank3=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_amphiroll_tank3', 'r') as myfile:
    private_amphiroll_tank3=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')

#with open('/home/pi/script/pass/cmd_area51_taking_photo', 'r') as myfile:
 #   cmd_area51_taking_photo=myfile.read().replace('\n', '')



#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['mo0','mo1','mo2','mo3', 
            'tempa0','tempa1','tempa2','tempa3',
            'tempb0','tempb1','tempb2','tempb3',
            'su0','su1','su2','su3', 
            'scale1','tmp0','tmp1','tmp2','tmp3'] 
amphiroll_tank1=dict((el,0.0) for el in field_name)
pht_amphiroll_tank1 = Phant(publicKey=public_amphiroll_tank1, fields=field_name ,privateKey=private_amphiroll_tank1,baseUrl=nectar_address)

#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['mo4','mo5','mo6','mo7',
            'tempa4','tempa5','tempa6','tempa7',
            'tempb4','tempb5','tempb6','tempb7',
            'su4','su5','su6','su7',
            'scale2','tmp4','tmp5','tmp6','tmp7']
amphiroll_tank2=dict((el,0.0) for el in field_name)
pht_amphiroll_tank2 = Phant(publicKey=public_amphiroll_tank2, fields=field_name ,privateKey=private_amphiroll_tank2,baseUrl=nectar_address)


#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['mo8','mo9','mo10','mo11',
            'tempa8','tempa9','tempa10','tempa11',
            'tempb8','tempb9','tempb10','tempb11',
            'su8','su9','su10','su11',
            'scale3','tmp8','tmp9','tmp10','tmp11']
amphiroll_tank3=dict((el,0.0) for el in field_name)
pht_amphiroll_tank3 = Phant(publicKey=public_amphiroll_tank3, fields=field_name ,privateKey=private_amphiroll_tank3,baseUrl=nectar_address)



port_sensor  = 'USB VID:PID=2341:0042 SNR=557363037393516021A1'


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
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'amphiroll_tank.csv'
sleep_time_seconds=30*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)



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

    

    # voltage measurement
    # power,43,analog,15,point,3,interval_mm,200,debug,1

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,26E39767,dgin,50,snpw,42,htpw,35,itv,24000,otno,5",initialize=True)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank1['tempa0']=float(current_read[2])
    amphiroll_tank1['tempb0']=float(current_read[7])
    amphiroll_tank1['su0']=float(current_read[7])-float(current_read[2])



    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,3041992B,dgin,50,snpw,42,htpw,37,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank1['tempa1']=float(current_read[2])
    amphiroll_tank1['tempb1']=float(current_read[7])
    amphiroll_tank1['su1']=float(current_read[7])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,CEF1988A,dgin,50,snpw,42,htpw,39,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank1['tempa2']=float(current_read[2])
    amphiroll_tank1['tempb2']=float(current_read[7])
    amphiroll_tank1['su2']=float(current_read[7])-float(current_read[2])
    

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,2C6796F3,dgin,50,snpw,42,htpw,41,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank1['tempa3']=float(current_read[2])
    amphiroll_tank1['tempb3']=float(current_read[7])
    amphiroll_tank1['su3']=float(current_read[7])-float(current_read[2])

   
    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,12,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank1['mo0']=float(current_read[2])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,13,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank1['mo1']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,14,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank1['mo2']=float(current_read[2])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,15,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank1['mo3']=float(current_read[2])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,0,power,25,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank1['scale1']=float(current_read[2])


    upload_phant(pht_amphiroll_tank1,amphiroll_tank1,screen_display)


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,1AED37FC,dgin,50,snpw,42,htpw,31,itv,24000,otno,5",initialize=True)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank2['tempa4']=float(current_read[2])
    amphiroll_tank2['tempb4']=float(current_read[7])
    amphiroll_tank2['su4']=float(current_read[7])-float(current_read[2])



    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,9DFD96C9,dgin,13,snpw,6,htpw,22,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank2['tempa5']=float(current_read[2])
    amphiroll_tank2['tempb5']=float(current_read[7])
    amphiroll_tank2['su5']=float(current_read[7])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,94EA9867,dgin,50,snpw,42,htpw,38,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank2['tempa6']=float(current_read[2])
    amphiroll_tank2['tempb6']=float(current_read[7])
    amphiroll_tank2['su6']=float(current_read[7])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,9A6B97E8,dgin,13,snpw,6,htpw,29,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank2['tempa7']=float(current_read[2])
    amphiroll_tank2['tempb7']=float(current_read[7])
    amphiroll_tank2['su7']=float(current_read[7])-float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,8,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank2['mo4']=float(current_read[2])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,9,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank2['mo5']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,10,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank2['mo6']=float(current_read[2])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,11,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank2['mo7']=float(current_read[2])



    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,1,power,9,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank2['scale2']=float(current_read[2])

    upload_phant(pht_amphiroll_tank2,amphiroll_tank2,screen_display)


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,5EBC99B1,dgin,13,snpw,6,htpw,40,itv,24000,otno,5",initialize=True)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank3['tempa8']=float(current_read[2])
    amphiroll_tank3['tempb8']=float(current_read[7])
    amphiroll_tank3['su8']=float(current_read[7])-float(current_read[2])



    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,9EB99666,dgin,13,snpw,6,htpw,7,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank3['tempa9']=float(current_read[2])
    amphiroll_tank3['tempb9']=float(current_read[7])
    amphiroll_tank3['su9']=float(current_read[7])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,1FFE9603,dgin,13,snpw,6,htpw,8,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank3['tempa10']=float(current_read[2])
    amphiroll_tank3['tempb10']=float(current_read[7])
    amphiroll_tank3['su10']=float(current_read[7])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,127696BC,dgin,50,snpw,42,htpw,33,itv,24000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank3['tempa11']=float(current_read[2])
    amphiroll_tank3['tempb11']=float(current_read[7])
    amphiroll_tank3['su11']=float(current_read[7])-float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,6,power,26,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank3['mo8']=float(current_read[2])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,5,power,28,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank3['mo9']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,3,power,32,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank3['mo10']=float(current_read[2])

    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,4,power,30,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank3['mo11']=float(current_read[2])


    sleep(2)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,2,power,24,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    amphiroll_tank3['scale3']=float(current_read[2])


    upload_phant(pht_amphiroll_tank3,amphiroll_tank3,screen_display)



    #camera = picamera.PiCamera()
    #camera.resolution = (3280,2464)
    #time_now=time.strftime("%Y_%b_%d_%H_%M_%S")
    #file_name_basin_2=time_now+'_bct_basin_2.jpg'
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="power_switch,43,power_switch_status,1",initialize=False)
    time.sleep(2)
    #camera.capture('/home/pi/photo/'+file_name_basin_2)
    process=subprocess.Popen('/home/pi/script/raspistill_snapshot.sh', stdout=subprocess.PIPE)

    time.sleep(10)
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="power_switch,43,power_switch_status,0",initialize=False)
    #camera.close()




    if save_to_file: fid.write("\n\r")
    # sleep to the next loop
    time.sleep(sleep_time_seconds)

        
      


