#!/usr/bin/python
# this script reads all equipment from column daisy, including sensors and weather stations, uv sensors. 
# mount specification: mega with ec5, eps2, ds18, loadcell, 
import serial
import time
import numpy as np
import sys
from phant import Phant
import serial_openlock


with open('/home/pi/script/pass/public_bougainvillea', 'r') as myfile:
    public_bougainvillea=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_bougainvillea', 'r') as myfile:
    private_bougainvillea=myfile.read().replace('\n', '')

#------------------------- below are definations for the sensors in the column ---------------------------------
field_name_bougainvillea=['mo0','mo1','mo2','mo3','mo4','mo5','mo6','mo7','mo8','mo9',
    'temp1','temp2','temp3','temp4','temp5','temp6','temp7','temp8','suction1',
    'suction2','suction3','suction4','suction5','suction6','suction7','suction8','evap1','ip','evap2','ip2']


#http://stackoverflow.com/questions/3869487/how-do-i-create-a-dictionary-with-keys-from-a-list-and-values-defaulting-to-say
parsed_data_bougainvillea=dict((el,0.0) for el in field_name_bougainvillea)
pht_bougainvillea = Phant(publicKey=public_bougainvillea, fields=field_name_bougainvillea ,privateKey=private_bougainvillea)
port_bougainvillea = 'USB VID:PID=2a03:0057 SNR=5563'



# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'column_bougainvillea.csv'

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
    
    msg_bougainvillea=serial_openlock.get_result_by_input(port=port_bougainvillea,command="All")

    current_read_bougainvillea=msg_bougainvillea.split(',')[1:-1]
    # parse moisture data
    mo_ind=[i for i,x in enumerate(current_read_bougainvillea) if x == 'Mo']
    for i in mo_ind:
        parsed_data_bougainvillea['mo'+current_read_bougainvillea[i+1]]=float(current_read_bougainvillea[i+2])
    # log the results to sparkfun
    upload_phant(pht_bougainvillea,parsed_data_bougainvillea,screen_display)
    ### --------------------------- above is to processing data from column sensor--------------------------
    
    ### --------------------------- bwlow is to processing data for weather station-------------------------
    ## get from previous parsing
    #vis_ind=[i for i,x in enumerate(current_read_bougainvillea) if x == 'Vis'] 
    #parsed_data_weather["vis_up"]=float(current_read_bougainvillea[vis_ind[0]+1])
    #ir_ind=[i for i,x in enumerate(current_read_bougainvillea) if x == 'IR'] 
    #parsed_data_weather["ir_up"]=float(current_read_bougainvillea[ir_ind[0]+1])
    #uv_ind=[i for i,x in enumerate(current_read_bougainvillea) if x == 'UV'] 
    #parsed_data_weather["uv_up"]=float(current_read_bougainvillea[uv_ind[0]+1])
    #
    #
    #msg_weather=serial_openlock.get_result_by_input(port=port_weather,command="Weather")
    #
    #current_read=msg_weather.split(',')[1:-1]
    #for i,key in enumerate(current_read[::2]):
    #    parsed_data_weather[key.lower()]=float(current_read[2*i+1])



    #upload_phant(pht_weather,parsed_data_weather,screen_display)

    # save to file
    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
    if screen_display: print i,delimiter,time_now,delimiter,msg_bougainvillea.rstrip()
    if save_to_file: fid.write(time_now+delimiter+msg_bougainvillea)
       
    # sleep to the next loop
    time.sleep(sleep_time_seconds)

        
