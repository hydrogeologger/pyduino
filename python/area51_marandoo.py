#!/usr/bin/python
import serial
import time
import numpy as np
import sys
from phant import Phant
import get_ip

import serial_openlock


with open('/home/pi/script/pass/public_marandoo', 'r') as myfile:
    public_marandoo=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_marandoo', 'r') as myfile:
    private_marandoo=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')


field_name_area51=['scale1','scale2','scale3','t_1','t_2','t_3',
    'delta_t_1','delta_t_2','delta_t_3','mosture_1','mosture_2','moisture_3']

pht_area51 = Phant(publicKey=public_marandoo, 
    fields=field_name_area51,privateKey=private_marandoo,baseUrl=nectar_address)

parsed_data_area51=dict((el,0.0) for el in field_name_area51)

#-------------------below are preparation for the sensor arduino ----------- 


port_scale1='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.5.1.1:1.0-port0'
port_scale2='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.5.4:1.0-port0'
port_scale3='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.5.1.2:1.0-port0'

scale1 = serial.Serial(port_scale1)

scale2 = serial.Serial(port_scale2)

scale3 = serial.Serial(port_scale3)



scale1.write('IP\n\r')
scale2.write('IP\n\r')
scale3.write('IP\n\r')

str_scale1=scale1.readline()
str_scale2=scale2.readline()
str_scale3=scale3.readline()

sleep(10)
scale1.write('IP\n\r')
scale2.write('IP\n\r')
scale3.write('IP\n\r')

str_scale1=scale1.readline()
str_scale2=scale2.readline()
str_scale3=scale3.readline()


weight_scale1=str_scale1.split()[0]
weight_scale2=str_scale2.split()[0]
weight_scale3=str_scale3.split()[0]



#
temp_sampling_number=20
# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'area51_mandaroo.csv'

sleep_time_seconds=10*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)


def upload_phant(pht,parsed_data,screen_display):
    log_attempts=1
    while log_attempts<10:
        try:          
            pht.log(*[parsed_data[key] for key in pht.fields])
            if screen_display: print "uploaded"
            break
        except  Exception, e: # catch all errors
            if screen_display: print "upload failed at attempt",log_attempts,' '+str(e)
            log_attempts+=1
            time.sleep(30)
            continue


while True: 

    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
    if screen_display: print time_now,delimiter,weight_scale1.rstrip(),delimiter,weight_scale2.rstrip(),delimiter,weight_scale3.rstrip()
    if save_to_file: fid.write(time_now+delimiter+weight_scale1+delimiter+weight_scale2+delimiter+weight_scale3+'\n\r')

    scale1.write('IP\n\r')
    scale2.write('IP\n\r')
    scale3.write('IP\n\r')
    
    str_scale1=scale1.readline()
    str_scale2=scale2.readline()
    str_scale3=scale3.readline()
    
    weight_scale1=str_scale1.split()[0]
    weight_scale2=str_scale2.split()[0]
    weight_scale3=str_scale3.split()[0]
    

    parsed_data_area51['scale1']=float(weight_scale1)
    parsed_data_area51['scale2']=float(weight_scale2)
    parsed_data_area51['scale3']=float(weight_scale3)


    upload_phant(pht_area51,parsed_data_area51,screen_display)

    time.sleep(sleep_time_seconds)





