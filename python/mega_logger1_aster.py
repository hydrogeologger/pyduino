#!/usr/bin/python
# this script reads all equipment from column daisy, including sensors and weather stations, uv sensors. 
# mount specification: mega with ec5, eps2, ds18, loadcell, 
import serial
import time
import numpy as np
import sys
from phant import Phant
import serial_openlock
import csv_tools
import get_ip



file_name_campbell='campbell_output.csv'
fn_camp=open(file_name_campbell,'r')


with open('/home/pi/script/pass/public_aster', 'r') as myfile:
    public_aster=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_aster', 'r') as myfile:
    private_aster=myfile.read().replace('\n', '')

#------------------------- below are definations for the sensors in the column ---------------------------------
field_name_aster=['mo22','mo23','mo24','mo25','mo26','mo27','mo28','mo29','mo30','mo31',
    'temp1','temp2','temp3','temp4','temp5','temp6','temp7','temp8','suction1',
    'suction2','suction3','suction4','suction5','suction6','suction7','suction8','evap1','ip','evap2','ip2']


#http://stackoverflow.com/questions/3869487/how-do-i-create-a-dictionary-with-keys-from-a-list-and-values-defaulting-to-say
parsed_data_aster=dict((el,0.0) for el in field_name_aster)
pht_aster = Phant(publicKey=public_aster, fields=field_name_aster ,privateKey=private_aster)
port_aster = 'USB VID:PID=2341:0042 SNR=5533'

#------------------------- above are definations for the sensors in the column ---------------------------------
#field_name_weather=['aet','batt','dlyrainmm','ir_down','ir_up','lt','mo_soil','p','pet','rainmm','rh','tc','temp_soil',
#    'uv_down','uv_up','vis_down','vis_up','wddir','wddiravg2m','wdgstdir','wdgstdir10m','wdgstkph','wdgstkph10m','wdspdkph','wdspdkphavg2m']
#parsed_data_weather=dict((el,0.0) for el in field_name_weather)
#pht_weather = Phant(publicKey='v0NOoW7RLRU3gYpAGdKW', fields=field_name_weather ,privateKey='aP9dMkmbzbiP2RkmJXNw')
#port_weather = 'USB VID:PID=2341:0042'
##------------------------- below are definations for the weather station ---------------------------------


# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'column_aster.csv'

#sleep_time_seconds=20*60  # this ends up with 49 min interval
sleep_time_seconds=30*60  # this ends up with 49 min interval

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','


__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)


def upload_phant(pht,parsed_data,screen_display):
    log_attempts=1
    while log_attempts<5:
        try:          
            ##pht.log(iter([ parsed_data[key] for key in pht.fields]))
            # http://stackoverflow.com/questions/43414407/iterate-at-a-function-input-in-python/43414660#43414660
            pht.log(*[parsed_data[key] for key in pht.fields])
            if screen_display: print "uploaded"
            break
        except: # catch all errors
            if screen_display: print "upload failed at attempt",log_attempts
            log_attempts+=1
            time.sleep(30)
            continue



while True: 
    
    msg_aster=serial_openlock.get_result_by_input(port=port_aster,command="All")

    current_read_aster=msg_aster.split(',')[1:-1]
    # parse moisture data
    mo_ind=[i for i,x in enumerate(current_read_aster) if x == 'Mo']
    for i in mo_ind:
        parsed_data_aster['mo'+current_read_aster[i+1]]=float(current_read_aster[i+2])
    ### --------------------------- above is to processing data from column sensor--------------------------
    
    ### --------------------------- bwlow is to processing data for campbell scientific-------------------------
    
    msg_campbell=csv_tools.tail(fn_camp,1)
    current_read_campbell=msg_campbell.split(',')[0:-1]
    parsed_data_campbell={}
    for i,key in enumerate(current_read_campbell[::2]):
        if key.lower()=='datetime':
            parsed_data_campbell[key.lower()]=current_read_campbell[2*i+1]
        else:
            parsed_data_campbell[key.lower()]=float(current_read_campbell[2*i+1])

    parsed_data_aster['temp1']     =parsed_data_campbell['starttemp_c_1']
    parsed_data_aster['temp2']     =parsed_data_campbell['starttemp_c_2']
    parsed_data_aster['temp3']     =parsed_data_campbell['starttemp_c_3']
    parsed_data_aster['temp4']     =parsed_data_campbell['starttemp_c_4']
    parsed_data_aster['temp5']     =parsed_data_campbell['starttemp_c_5']
    parsed_data_aster['temp6']     =parsed_data_campbell['starttemp_c_6']
    parsed_data_aster['temp7']     =parsed_data_campbell['starttemp_c_7']
    parsed_data_aster['temp8']     =parsed_data_campbell['starttemp_c_8']
    parsed_data_aster['suction1']  =parsed_data_campbell['kpa_1']
    parsed_data_aster['suction2']  =parsed_data_campbell['kpa_2']
    parsed_data_aster['suction3']  =parsed_data_campbell['kpa_3']
    parsed_data_aster['suction4']  =parsed_data_campbell['kpa_4']
    parsed_data_aster['suction5']  =parsed_data_campbell['kpa_5']
    parsed_data_aster['suction6']  =parsed_data_campbell['kpa_6']
    parsed_data_aster['suction7']  =parsed_data_campbell['kpa_7']
    parsed_data_aster['suction8']  =parsed_data_campbell['kpa_8']

    str_campbell_output=''
    for key in parsed_data_aster:
         str_campbell_output+= key+delimiter+ str(parsed_data_aster[key])+delimiter

    # log the results to sparkfun
    parsed_data_aster['ip']=get_ip.get_ip_address_digit_mask('wlan0')

    # log the results to sparkfun
    upload_phant(pht_aster,parsed_data_aster,screen_display)

    # save to file
    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
    if screen_display: print i,delimiter,time_now,delimiter,str_campbell_output,msg_aster.rstrip()
    if save_to_file: fid.write(time_now+delimiter+str_campbell_output+msg_aster)
       
    # sleep to the next loop
    time.sleep(sleep_time_seconds)

        
