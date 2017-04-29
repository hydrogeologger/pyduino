#!/usr/bin/python
# this script reads all equipment from column daisy, including sensors and weather stations, uv sensors. 
# mount specification: mega with ec5, eps2, ds18, loadcell, 
import serial
import time
import numpy as np
import sys
from phant import Phant
import serial_openlock


import SI1145.SI1145 as SI1145

##------------------------ below is to initialize the si1145 at the rpi--------------------
sensor = SI1145.SI1145() #"/dev/i2c-1")
time.sleep(3)   # a good sleep before reading is found extremetly important
vis = sensor.readVisible()
while vis == 0:
    print 'si1145 init failed'
    time.sleep(2)
    print str(vis)
    sensor=SI1145.SI1145_RESET
    time.sleep(2)
    sensor = SI1145.SI1145() #"/dev/i2c-1")
    time.sleep(2)
    vis = sensor.readVisible()
##------------------------ above is to initialize the si1145 at the rpi--------------------


#------------------------- below are definations for the sensors in the column ---------------------------------
field_name_sensor=['mo23','mo25','mo27','mo29','mo31','mo33','mo35','mo37','mo39','mo41',
    't26_begin','t26_peak','t26_end','te2_begin','te2_peak','te2_end','t45_begin','t45_peak','t45_end',
    't57_begin','t57_peak','t57_end','tfb_begin','tfb_peak','tfb_end','t7b_begin','t7b_peak','t7b_end','evap1','evap2']

#http://stackoverflow.com/questions/3869487/how-do-i-create-a-dictionary-with-keys-from-a-list-and-values-defaulting-to-say
parsed_data_sensor=dict((el,0.0) for el in field_name_sensor)
pht_sensor = Phant(publicKey='q5YnK9A9qMCqoNqv78XD', fields=field_name_sensor ,privateKey='BV4RMyryYdtyYEyrbeMK')
port_sensor  = 'USB VID:PID=2341:0042 SNR=55639303035351A0B171'

#------------------------- above are definations for the sensors in the column ---------------------------------
field_name_weather=['aet','batt','dlyrainmm','ir_down','ir_up','lt','mo_soil','p','pet','rainmm','rh','tc','temp_soil',
    'uv_down','uv_up','vis_down','vis_up','wddir','wddiravg2m','wdgstdir','wdgstdir10m','wdgstkph','wdgstkph10m','wdspdkph','wdspdkphavg2m']
parsed_data_weather=dict((el,0.0) for el in field_name_weather)
pht_weather = Phant(publicKey='v0NOoW7RLRU3gYpAGdKW', fields=field_name_weather ,privateKey='aP9dMkmbzbiP2RkmJXNw')
port_weather = 'USB VID:PID=0403:6015 SNR=DN01J0PU'
#------------------------- below are definations for the weather station ---------------------------------


# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'column_camellias.csv'

#sleep_time_seconds=20*60  # this ends up with 49 min interval
sleep_time_seconds=30*60  # this ends up with 49 min interval

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','


# temp sampling number 
temp_sampling_number=20
__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)


def upload_phant(pht,parsed_data,screen_display):
    log_attempts=1
    while log_attempts<3:
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

def read_si1145(number_readings,sleep_time_s):
    # make sure it gives useful data by repeating the reset
    sensor = SI1145.SI1145() #"/dev/i2c-1")
    time.sleep(3)   # a good sleep before reading is found extremetly important
    vis = sensor.readVisible()
    while vis == 0:
        print 'si1145 init failed'
        time.sleep(2)
        print str(vis)
        sensor=SI1145.SI1145_RESET
        time.sleep(2)
        sensor = SI1145.SI1145() #"/dev/i2c-1")
        time.sleep(2)
        vis = sensor.readVisible()
    vis=0
    ir=0
    uv=0
    for i in range(number_readings):
        vis+=sensor.readVisible()
        time.sleep(1)
        ir+=sensor.readIR()
        time.sleep(1)
        uv+=sensor.readUV()
        time.sleep(sleep_time_s)
    vis/=float(number_readings)
    ir/=float(number_readings)
    uv/=float(number_readings)
    sensor=SI1145.SI1145_RESET
    return vis,ir,uv

# initialize the weather station data
# it is found that all the first readings from weather station would give 0 atmosphere reading. call this 
# function is to discard the first reading
msg_weather=serial_openlock.get_result_by_input(port=port_weather,command="Weather")
time.sleep(3)
msg_weather=serial_openlock.get_result_by_input(port=port_weather,command="Weather")

while True: 
    
    msg_sensor=serial_openlock.get_result_by_input(port=port_sensor,command="All")

    current_read_sensor=msg_sensor.split(',')[1:-1]
    # parse moisture data
    mo_ind=[i for i,x in enumerate(current_read_sensor) if x == 'Mo']
    for i in mo_ind:
        parsed_data_sensor['mo'+current_read_sensor[i+1]]=float(current_read_sensor[i+2])
    # parse "SucHeat"
    sucheat_ind=[i for i,x in enumerate(current_read_sensor) if x == 'SucHeat']
    for i in sucheat_ind:
        parsed_data_sensor['t'+current_read_sensor[i+1][2:].lower()+'_begin']=float(current_read_sensor[i+3])
        parsed_data_sensor['t'+current_read_sensor[i+1][2:].lower()+'_peak']=float(current_read_sensor[i+temp_sampling_number+3])
        parsed_data_sensor['t'+current_read_sensor[i+1][2:].lower()+'_end']=float(current_read_sensor[i+2*temp_sampling_number+5])
    # log the results to sparkfun
    upload_phant(pht_sensor,parsed_data_sensor,screen_display)
    ### --------------------------- above is to processing data from column sensor--------------------------
    
    ## --------------------------- bwlow is to processing data for weather station-------------------------
    # get from previous parsing
    vis_ind=[i for i,x in enumerate(current_read) if x == 'Vis'] 
    parsed_data_weather["vis_up"]=float(current_read[vis_ind[0]+1])
    ir_ind=[i for i,x in enumerate(current_read) if x == 'IR'] 
    parsed_data_weather["ir_up"]=float(current_read[ir_ind[0]+1])
    uv_ind=[i for i,x in enumerate(current_read) if x == 'UV'] 
    parsed_data_weather["uv_up"]=float(current_read[uv_ind[0]+1])
    
    
    msg_weather=serial_openlock.get_result_by_input(port=port_weather,command="Weather")
    
    current_read=msg_weather.split(',')[1:-1]
    for i,key in enumerate(current_read[::2]):
        parsed_data_weather[key.lower()]=float(current_read[2*i+1])
    ## get solar from rpi
    msg_solar=''
    [vis,ir,uv]=read_si1145(si1145_number_readings,si1145_sleep_interval_seconds)
    parsed_data_weather["vis_down"]=vis
    parsed_data_weather["ir_down"]=ir
    parsed_data_weather["uv_down"]=uv
    msg_solar='vis_down'+delimiter+str(vis)+delimiter+'ir_down'+delimiter+str(ir)+delimiter+'uv_down'+delimiter+str(uv)+delimiter



    upload_phant(pht_weather,parsed_data_weather,screen_display)

    # save to file
    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
    if screen_display: print i,delimiter,time_now,delimiter,msg_sensor.rstrip(),msg_solar,msg_weather.rstrip()
    if save_to_file: fid.write(time_now+delimiter+msg_sensor.rstrip()+msg_solar+msg_weather)
       
    # sleep to the next loop
    time.sleep(sleep_time_seconds)

        
