#!/usr/bin/python
import serial
import time
import numpy as np
import sys
from phant import Phant
import serial_openlock
import get_ip
from upload_phant import upload_phant
from time import sleep,gmtime, strftime,localtime

with open('/home/pi/script/pass/public_scales_partha', 'r') as myfile:
    public_scales_partha=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_scales_partha', 'r') as myfile:
    private_scales_partha=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')


field_name_scales_partha=['scale1','scale2','scale3','scale4','scale5','scale6','temperature_1','humidity_1','temperature_1','humidity_1',
                         'temperature_2','humidity_2','temperature_3','humidity_3','temperature_4','humidity_4','temperature_5','humidity_5',
                         'temperature_6','humidity_6','temperature_7','humidity_7']

pht_scales_partha = Phant(publicKey=public_scales_partha,fields=field_name_scales_partha,privateKey=private_scales_partha,baseUrl=nectar_address)

scales_partha=dict((el,0.0) for el in field_name_scales_partha)

#-------------------below are preparation for the sensor arduino ----------- 

port_sensor  = 'USB VID:PID=2341:0042 SNR=557363037393516030D1'
#port_sensor  = '/dev/ttyACM0'
port_scale1='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2.1:1.0-port0'
port_scale2='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2.2:1.0-port0'
#port_scale3='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.3.3:1.0-port0'
port_scale4='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2.4.1:1.0-port0'
port_scale5='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2.4.2:1.0-port0'
port_scale6='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2.4.3:1.0-port0'

scale1 = serial.Serial(port_scale1,timeout=20)

scale2 = serial.Serial(port_scale2,timeout=20)

#scale3 = serial.Serial(port_scale3,timeout=20)

scale4 = serial.Serial(port_scale4,timeout=20)

scale5 = serial.Serial(port_scale5,timeout=20)

scale6 = serial.Serial(port_scale6,timeout=20)

scale1.write('IP\n\r')
scale2.write('IP\n\r')
#scale3.write('IP\n\r')
scale4.write('IP\n\r')
scale5.write('IP\n\r')
scale6.write('IP\n\r')

time.sleep(2)

str_scale1=scale1.readline()
str_scale2=scale2.readline()
#str_scale3=scale3.readline()
str_scale4=scale4.readline()
str_scale5=scale5.readline()
str_scale6=scale6.readline()

screen_display=True

scale_attempts=1
while scale_attempts<6:
    try:
        scale1.write('IP\n\r')
        scale2.write('IP\n\r')
        #scale3.write('IP\n\r')
        scale4.write('IP\n\r')
        scale5.write('IP\n\r')
        scale6.write('IP\n\r')
        time.sleep(2)#wait for two seconds before leaving   
        str_scale1=scale1.readline()
        str_scale2=scale2.readline()
        #time.sleep(3)
        #str_scale3=scale3.readline()
        #time.sleep(3)
        str_scale4=scale4.readline()
        str_scale5=scale5.readline()
        str_scale6=scale6.readline()
        weight_scale1=str_scale1.split()[0]
        weight_scale2=str_scale2.split()[0]
        #weight_scale3=str_scale3.split()[0]
        #time.sleep(3)
        weight_scale4=str_scale4.split()[0]
        weight_scale5=str_scale5.split()[0]
        weight_scale6=str_scale6.split()[0]     
        break
    except Exception, e:
        if screen_display: print "scale reading failed,"+str(scale_attempts)+" " + str(e)
        scale_attempts+=1
        time.sleep(3)
        scale1.close()
        scale2.close()
        #scale3.close()
        scale4.close()
        scale5.close()
        scale6.close()
        time.sleep(10)
        scale1 = serial.Serial(port_scale1,timeout=20)
        scale2 = serial.Serial(port_scale2,timeout=20)
        #scale3 = serial.Serial(port_scale3,timeout=20)
        scale4 = serial.Serial(port_scale4,timeout=20)
        scale5 = serial.Serial(port_scale5,timeout=20)
        scale6 = serial.Serial(port_scale6,timeout=20)
        #continue
        pass


#sleep(10)
#
#scale1.write('IP\n\r')
#scale2.write('IP\n\r')
#scale3.write('IP\n\r')
#scale4.write('IP\n\r')
#scale5.write('IP\n\r')
#scale6.write('IP\n\r')
#
#str_scale1=scale1.readline()
#str_scale2=scale2.readline()
#str_scale3=scale3.readline()
#str_scale4=scale4.readline()
#str_scale5=scale5.readline()
#str_scale6=scale6.readline()


#weight_scale1=str_scale1.split()[0]
#weight_scale2=str_scale2.split()[0]
##weight_scale3=str_scale3.split()[0]
#weight_scale4=str_scale4.split()[0]
#weight_scale5=str_scale5.split()[0]
#weight_scale6=str_scale6.split()[0]



#
temp_sampling_number=20
# whether the result will be displayed on the screen
#screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'scales_partha.csv'

sleep_time_seconds=30*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)


#def upload_phant(pht,parsed_data,screen_display):
#    log_attempts=1
#    while log_attempts<10:
#        try:          
#            pht.log(*[parsed_data[key] for key in pht.fields])
#            if screen_display: print "uploaded"
#            break
#        except  Exception, e: # catch all errors
#            if screen_display: print "upload failed at attempt",log_attempts,' '+str(e)
#            log_attempts+=1
#            time.sleep(30)
#            continue


while True: 

#    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
#    if screen_display: print time_now,delimiter,weight_scale1.rstrip(),delimiter,weight_scale2.rstrip(),delimiter,weight_scale3.rstrip(),delimiter,weight_scale4.rstrip(),delimiter,weight_scale5.rstrip(),delimiter,weight_scale6.rstrip()
#    if save_to_file: fid.write(time_now+delimiter+weight_scale1+delimiter+weight_scale2+delimiter+weight_scale3+delimiter+weight_scale4+delimiter+weight_scale5+delimiter+weight_scale6+'\n\r')
    if screen_display: print strftime("%Y-%m-%d %H:%M:%S", localtime())
    if save_to_file: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime())  )
    

#-----------------Setup1--------------------------

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,5,power,35,points,2,dummies,1,interval_mm,2000,debug,1,timeout,60",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    scales_partha['temperature_1']=float(current_read[-2])
    scales_partha['humidity_1']=float(current_read[-1])
    sleep(5)

    #ard=serial.Serial(port_sensor)
    #msg=ard.write("dht22,5,power,35,points,2,dummies,1,interval_mm,2000,debug,1,timeout,60")
    #sleep(1)
    #msg=ard.readline()
    #sleep(2)
    #ard.close()
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #scales_partha['temperature_1']=float(current_read[-2])
    #scales_partha['humidity_1']=float(current_read[-1])
    #sleep(5)    
    
    #msg2=ard.write("dht22,11,power,37,points,2,dummies,1,interval_mm,2000,debug,1")
    #sleep(1)
    #msg2=ard.readline()
    #sleep(2)

    #msg3=ard.write("dht22,13,power,39,points,2,dummies,1,interval_mm,2000,debug,1")
    #sleep(1)
    #msg3=ard.readline()
    #sleep(2)

    #msg4=ard.write("dht22,51,power,41,points,2,dummies,1,interval_mm,2000,debug,1")
    #sleep(1)
    #msg4=ard.readline()
    #sleep(2)
    #
    #msg5=ard.write("dht22,52,power,27,points,2,dummies,1,interval_mm,2000,debug,1")
    #sleep(1)
    #msg5=ard.readline()
    #sleep(2)

    #msg6=ard.write("dht22,53,power,29,points,2,dummies,1,interval_mm,2000,debug,1")
    #sleep(1)
    #msg6=ard.readline()
    #sleep(2)

    #msg7=ard.write("dht22,4,power,31,points,2,dummies,1,interval_mm,2000,debug,1")
    #sleep(1)
    #msg7=ard.readline()
    #sleep(2)
    #
    #ard.close()

    #if screen_display: print msg1.rstrip()
    #if save_to_file: fid.write(delimiter+msg1.rstrip())
    #upload_msg1=msg1.rstrip()
    #current_read=msg1.split(',')[0:-1]
    #scales_partha['humidity_1']=float(current_read[-1])
    #scales_partha['temperature_1']=float(current_read[-2]) 
    #sleep(5)

    #if screen_display: print msg2.rstrip()
    #if save_to_file: fid.write(delimiter+msg2.rstrip())
    #upload_msg2=msg2.rstrip()
    #current_read=msg2.split(',')[0:-1]
    #scales_partha['humidity_2']=float(current_read[-1])
    #scales_partha['temperature_2']=float(current_read[-2])
    #sleep(5)

    #if screen_display: print msg3.rstrip()
    #if save_to_file: fid.write(delimiter+msg3.rstrip())
    #upload_msg3=msg3.rstrip()
    #current_read=msg3.split(',')[0:-1]
    #scales_partha['humidity_3']=float(current_read[-1])
    #scales_partha['temperature_3']=float(current_read[-2])
    #sleep(5)

    #if screen_display: print msg4.rstrip()
    #if save_to_file: fid.write(delimiter+msg4.rstrip())
    #upload_msg4=msg4.rstrip()
    #current_read=msg4.split(',')[0:-1]
    #scales_partha['humidity_4']=float(current_read[-1])
    #scales_partha['temperature_4']=float(current_read[-2])
    #sleep(5)

    #if screen_display: print msg5.rstrip()
    #if save_to_file: fid.write(delimiter+msg5.rstrip())
    #upload_msg5=msg5.rstrip()
    #current_read=msg5.split(',')[0:-1]
    #scales_partha['humidity_5']=float(current_read[-1])
    #scales_partha['temperature_5']=float(current_read[-2])
    #sleep(5)

    #if screen_display: print msg6.rstrip()
    #if save_to_file: fid.write(delimiter+msg6.rstrip())
    #upload_msg6=msg6.rstrip()
    #current_read=msg6.split(',')[0:-1]
    #scales_partha['humidity_6']=float(current_read[-1])
    #scales_partha['temperature_6']=float(current_read[-2])
    #sleep(5)

    #if screen_display: print msg7.rstrip()
    #if save_to_file: fid.write(delimiter+msg7.rstrip())
    #upload_msg7=msg7.rstrip()
    #current_read=msg7.split(',')[0:-1]
    #scales_partha['humidity_7']=float(current_read[-1])
    #scales_partha['temperature_7']=float(current_read[-2])
    #sleep(5)

#-----------------Setup2--------------------------

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,11,power,37,points,2,dummies,1,interval_mm,2000,debug,1,timeout,60",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    scales_partha['temperature_2']=float(current_read[-2])
    scales_partha['humidity_2']=float(current_read[-1])
    sleep(5)

    #ard=serial.Serial(port_sensor)
    #msg=ard.write("dht22,11,power,37,points,2,dummies,1,interval_mm,2000,debug,1,timeout,60")
    #sleep(1)
    #msg=ard.readline()
    #sleep(2)
    #ard.close()
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #upload_msg=msg.rstrip()
    #current_read=msg.split(',')[0:-1]
    #scales_partha['temperature_2']=float(current_read[-2])
    #scales_partha['humidity_2']=float(current_read[-1])
    #sleep(5)

#-----------------Setup3--------------------------

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,13,power,39,points,2,dummies,1,interval_mm,2000,debug,1,timeout,60",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    scales_partha['temperature_3']=float(current_read[-2])
    scales_partha['humidity_3']=float(current_read[-1])
    sleep(5)

    #ard=serial.Serial(port_sensor)
    #msg=ard.write("dht22,13,power,39,points,2,dummies,1,interval_mm,2000,debug,1,timeout,60")
    #sleep(1)
    #msg=ard.readline()
    #sleep(2)
    #ard.close()
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #upload_msg=msg.rstrip()
    #current_read=msg.split(',')[0:-1]
    #scales_partha['temperature_3']=float(current_read[-2])
    #scales_partha['humidity_3']=float(current_read[-1])
    #sleep(5)

#-----------------Setup4--------------------------

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,51,power,41,points,2,dummies,1,interval_mm,2000,debug,1,timeout,60",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    scales_partha['temperature_4']=float(current_read[-2])
    scales_partha['humidity_4']=float(current_read[-1])
    sleep(5)

    #ard=serial.Serial(port_sensor)
    #msg=ard.write("dht22,51,power,41,points,2,dummies,1,interval_mm,2000,debug,1,timeout,60")
    #sleep(1)
    #msg=ard.readline()
    #sleep(2)
    #ard.close()
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #upload_msg=msg.rstrip()
    #current_read=msg.split(',')[0:-1]
    #scales_partha['temperature_4']=float(current_read[-2])
    #scales_partha['humidity_4']=float(current_read[-1])
    #sleep(5)

#-----------------Setup5--------------------------

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,52,power,27,points,2,dummies,1,interval_mm,2000,debug,1,timeout,60",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    scales_partha['temperature_5']=float(current_read[-2])
    scales_partha['humidity_5']=float(current_read[-1])
    sleep(5)

    #ard=serial.Serial(port_sensor)
    #msg=ard.write("dht22,52,power,27,points,2,dummies,1,interval_mm,2000,debug,1,timeout,60")
    #sleep(1)
    #msg=ard.readline()
    #sleep(2)
    #ard.close()
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #upload_msg=msg.rstrip()
    #current_read=msg.split(',')[0:-1]
    #scales_partha['temperature_5']=float(current_read[-2])
    #scales_partha['humidity_5']=float(current_read[-1])
    #sleep(5)

#-----------------Setup6--------------------------

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,53,power,29,points,2,dummies,1,interval_mm,2000,debug,1,timeout,60",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    scales_partha['temperature_6']=float(current_read[-2])
    scales_partha['humidity_6']=float(current_read[-1])
    sleep(5)

    #ard=serial.Serial(port_sensor)
    #msg=ard.write("dht22,53,power,29,points,2,dummies,1,interval_mm,2000,debug,1,timeout,60")
    #sleep(1)
    #msg=ard.readline()
    #sleep(2)
    #ard.close()
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #upload_msg=msg.rstrip()
    #current_read=msg.split(',')[0:-1]
    #scales_partha['temperature_6']=float(current_read[-2])
    #scales_partha['humidity_6']=float(current_read[-1])
    #sleep(5)

#-----------------Ambient--------------------------

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,4,power,31,points,2,dummies,1,interval_mm,2000,debug,1,timeout,60",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    scales_partha['temperature_7']=float(current_read[-2])
    scales_partha['humidity_7']=float(current_read[-1])
    sleep(5)

    #ard=serial.Serial(port_sensor)
    #msg=ard.write("dht22,4,power,31,points,2,dummies,1,interval_mm,2000,debug,1,timeout,60")
    #sleep(1)
    #msg=ard.readline()
    #sleep(2)
    #ard.close()
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #upload_msg=msg.rstrip()
    #current_read=msg.split(',')[0:-1]
    #scales_partha['temperature_7']=float(current_read[-2])
    #scales_partha['humidity_7']=float(current_read[-1])
    #sleep(5)
   
    #ard.close()
    #sleep(2)

    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
#    if screen_display: print time_now,delimiter,weight_scale1.rstrip(),delimiter,weight_scale2.rstrip(),delimiter,weight_scale3.rstrip(),delimiter,weight_scale4.rstrip(),delimiter,weight_scale5.rstrip(),delimiter,weight_scale6.rstrip()
#    if save_to_file: fid.write(time_now+delimiter+weight_scale1+delimiter+weight_scale2+delimiter+weight_scale3+delimiter+weight_scale4+delimiter+weight_scale5+delimiter+weight_scale6+'\n\r')

    if screen_display: print time_now,delimiter,weight_scale1.rstrip(),delimiter,weight_scale2.rstrip(),delimiter,weight_scale4.rstrip(),delimiter,weight_scale5.rstrip(),delimiter,weight_scale6.rstrip()
    if save_to_file: fid.write(time_now+delimiter+weight_scale1+delimiter+weight_scale2+delimiter+weight_scale4+delimiter+weight_scale5+delimiter+weight_scale6+'\n\r')

    scale_attempts=1
    while scale_attempts<6:
        try:
            scale1.write('IP\n\r')
            scale2.write('IP\n\r')
            #scale3.write('IP\n\r')
            scale4.write('IP\n\r')
            scale5.write('IP\n\r')
            scale6.write('IP\n\r')
            time.sleep(2)#wait for two seconds before leaving   
            str_scale1=scale1.readline()
            str_scale2=scale2.readline()
            #time.sleep(3)
            #str_scale3=scale3.readline()
            #time.sleep(3)
            str_scale4=scale4.readline()
            str_scale5=scale5.readline()
            str_scale6=scale6.readline()
            weight_scale1=str_scale1.split()[0]
            weight_scale2=str_scale2.split()[0]
            #weight_scale3=str_scale3.split()[0]
            #time.sleep(3)
            weight_scale4=str_scale4.split()[0]
            weight_scale5=str_scale5.split()[0]
            weight_scale6=str_scale6.split()[0]
            scales_partha['scale1']=float(weight_scale1)
            scales_partha['scale2']=float(weight_scale2)
            #scales_partha['scale3']=float(weight_scale3)
            scales_partha['scale4']=float(weight_scale4)
            scales_partha['scale5']=float(weight_scale5)
            scales_partha['scale6']=float(weight_scale6)
            break
        except Exception, e:
            if screen_display: print "scale reading failed,"+str(scale_attempts)+" " + str(e)
            scale_attempts+=1
            time.sleep(30)
            scale1.close()
            scale2.close()
            #scale3.close()
            scale4.close()
            scale5.close()
            scale6.close()
            time.sleep(10)
            scale1 = serial.Serial(port_scale1,timeout=20)
            scale2 = serial.Serial(port_scale2,timeout=20)
            #scale3 = serial.Serial(port_scale3,timeout=20)
            scale4 = serial.Serial(port_scale4,timeout=20)
            scale5 = serial.Serial(port_scale5,timeout=20)
            scale6 = serial.Serial(port_scale6,timeout=20)
            #continue
            pass


    #scale1.write('IP\n\r')
    #scale2.write('IP\n\r')
    ##scale3.write('IP\n\r')
    #scale4.write('IP\n\r')
    #scale5.write('IP\n\r')
    #scale6.write('IP\n\r')

    #str_scale1=scale1.readline()
    #str_scale2=scale2.readline()
    ##str_scale3=scale3.readline()
    #str_scale4=scale4.readline()
    #str_scale5=scale5.readline()
    #str_scale6=scale6.readline()

    #weight_scale1=str_scale1.split()[0]
    #weight_scale2=str_scale2.split()[0]
    ##weight_scale3=str_scale3.split()[0]
    #weight_scale4=str_scale4.split()[0]
    #weight_scale5=str_scale5.split()[0]
    #weight_scale6=str_scale6.split()[0]

    #scales_partha['scale1']=float(weight_scale1)
    #scales_partha['scale2']=float(weight_scale2)
    ##parsed_data_scales_partha['scale3']=float(weight_scale3)
    #scales_partha['scale4']=float(weight_scale4)
    #scales_partha['scale5']=float(weight_scale5)
    #scales_partha['scale6']=float(weight_scale6)
    

    upload_phant(pht_scales_partha,scales_partha,screen_display)

    time.sleep(sleep_time_seconds)





