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

#------------------------ below is to initialize the si1145 at the rpi--------------------
sensor = SI1145.SI1145() #"/dev/i2c-1")
time.sleep(3)   # a good sleep before reading is found extremetly important
vis = sensor.readVisible()
si1145_number_readings=7;
si1145_sleep_interval_seconds=10;
while vis == 0:
    print 'si1145 init failed'
    time.sleep(2)
    print str(vis)
    SI1145.SI1145_RESET
    time.sleep(2)
    sensor = SI1145.SI1145() #"/dev/i2c-1")
    time.sleep(2)
    vis = sensor.readVisible()
#------------------------ above is to initialize the si1145 at the rpi--------------------


#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['tpf0','tp11','tp8d','tpa3','mo0','mo1','mo2','mo3','mo4','mo5','mo6','mo7',
    'mo8','mo9','mo10','mo11','su1','tp1','su2','tp2','su3','tp3','su4','tp4','evap1','evap2']
#http://stackoverflow.com/questions/3869487/how-do-i-create-a-dictionary-with-keys-from-a-list-and-values-defaulting-to-say
parsed_data=dict((el,0.0) for el in field_name)
#https://data.sparkfun.com/streams/RMxqjA6nRXfbm01raooM/update/lzEpXb5dxRhYAbG6177V
pht_sensor = Phant(publicKey='RMxqjA6nRXfbm01raooM', fields=field_name ,privateKey='lzEpXb5dxRhYAbG6177V')

# 'All,Tp,F0,20.44,Tp,11,20.06,Tp,8D,20.25,Tp,A3,20.62,Mo,0,247.00,Mo,1,70.15,Mo,2,69.20,Mo,3,65.90,Mo,4,69.95,Mo,5,75.00,Mo,6,66.00,Mo,7,60.80,Mo,8,69.60,Mo,9,40.35,Mo,10,190.90,Mo,11,86.60,SuTp,113DECAGON MPS-2 124,-3661.3,20.0,SuTp,213DECAGON MPS-2 124,-2251.4,20.0,SuTp,313DECAGON MPS-2 350,-6885.3,19.9,SuTp,413DECAGON MPS-2 136,-3487.4,20.3,Vis,260,IR,253,UV,0.02,AllDone\r\n'

#port_weather = '/dev/ttyACM0'
port_sensor  = 'USB VID:PID=2341:0042 '
#------------------------- above are definations for the sensors in the column ---------------------------------
field_name_weather=['aet','batt','dlyrainmm','ir_down','ir_up','lt','mo_soil','p','pet','rainmm','rh','tc','temp_soil','uv_down','uv_up','vis_down','vis_up','wddir','wddiravg2m','wdgstdir','wdgstdir10m','wdgstkph','wdgstkph10m','wdspdkph','wdspdkphavg2m']
parsed_data_weather=dict((el,0.0) for el in field_name_weather)
pht_weather = Phant(publicKey='JxO9ydlRjnuXARaZX5od', fields=field_name_weather ,privateKey='gzregldRnxClRy8El76G')
port_weather = 'USB VID:PID=0403:6015'
#------------------------- below are definations for the weather station ---------------------------------

##------------------------- below is to initialize sensor result connect to new arduino
#[port_weather_isopen, weather_fid]=serial_openlock.open_port(port_weather)
#while port_weather_isopen == False:
#    [port_weather_isopen, weather_fid]=serial_openlock.open_port(port_weather)
#    time.sleep(60)
#serial_openlock.initialize(weather_fid)
#weather_fid.write("Weather") 
#msg_weather = weather_fid.readline()
#port_weather_isopen=serial_openlock.close_port(weather_fid)



# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'column_daisy.csv'

sleep_time_seconds=55*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)


def upload_phant(pht,parsed_data,screen_display):
    log_attempts=1
    while log_attempts<10:
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

def read_arduino(port_sensor,command):
    [port_sensor_isopen, sensor_fid]=serial_openlock.open_port(port_sensor)
    while port_sensor_isopen == False:
        [port_sensor_isopen, sensor_fid]=serial_openlock.open_port(port_sensor)
        time.sleep(10)
    serial_openlock.initialize(sensor_fid)
    sensor_fid.write(command) # either "Solar", "Soil" or "All"
    msg = sensor_fid.readline()
    port_sensor_isopen=serial_openlock.close_port(sensor_fid)
    return msg

def read_si1145(number_readings,sleep_time_s):
    # make sure it gives useful data by repeating the reset
    sensor = SI1145.SI1145() #"/dev/i2c-1")
    time.sleep(3)   # a good sleep before reading is found extremetly important
    vis = sensor.readVisible()
    while vis == 0:
        print 'si1145 init failed'
        time.sleep(2)
        print str(vis)
        SI1145.SI1145_RESET
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
    SI1145.SI1145_RESET
    return vis,ir,uv
# initialize the weather station data
# it is found that all the first readings from weather station would give 0 atmosphere reading. call this 
# function is to discard the first reading
msg_weather=read_arduino(port_weather,"Weather")
time.sleep(5)
msg_weather=read_arduino(port_weather,"Weather")
while True: 
    ### --------------------------- bwlow is to processing data from column sensor--------------------------
    #[port_sensor_isopen, sensor_fid]=serial_openlock.open_port(port_sensor)
    #while port_sensor_isopen == False:
    #    [port_sensor_isopen, sensor_fid]=serial_openlock.open_port(port_sensor)
    #    time.sleep(10)
    #serial_openlock.initialize(sensor_fid)
    #sensor_fid.write("All") # either "Solar", "Soil" or "All"
    #msg = sensor_fid.readline()
    #port_sensor_isopen=serial_openlock.close_port(sensor_fid)
    
    msg=read_arduino(port_sensor,"All")

    current_read=msg.split(',')[0:-1]
    # parse tp result
    tp_ind=[i for i,x in enumerate(current_read) if x == 'Tp']
    for i in tp_ind:
        parsed_data['tp'+current_read[i+1].lower()]=float(current_read[i+2])
    # parse moisture data
    mo_ind=[i for i,x in enumerate(current_read) if x == 'Mo']
    for i in mo_ind:
        parsed_data['mo'+current_read[i+1]]=float(current_read[i+2])
    # parse mps2 data
    sutp_ind=[i for i,x in enumerate(current_read) if x == 'SuTp']
    for i in sutp_ind:
        parsed_data['su'+current_read[i+1][0]]=float(current_read[i+2])
        parsed_data['tp'+current_read[i+1][0]]=float(current_read[i+3])
    # log the results to sparkfun
    upload_phant(pht_sensor,parsed_data,screen_display)
    ### --------------------------- above is to processing data from column sensor--------------------------
    
    ### --------------------------- bwlow is to processing data for weather station-------------------------
    # get from previous parsing
    vis_ind=[i for i,x in enumerate(current_read) if x == 'Vis'] 
    parsed_data_weather["vis_up"]=float(current_read[vis_ind[0]+1])
    ir_ind=[i for i,x in enumerate(current_read) if x == 'IR'] 
    parsed_data_weather["ir_up"]=float(current_read[ir_ind[0]+1])
    uv_ind=[i for i,x in enumerate(current_read) if x == 'UV'] 
    parsed_data_weather["uv_up"]=float(current_read[uv_ind[0]+1])
    
    ## connect to new arduino
    #[port_weather_isopen, weather_fid]=serial_openlock.open_port(port_weather)
    #while port_weather_isopen == False:
    #    [port_weather_isopen, weather_fid]=serial_openlock.open_port(port_weather)
    #    time.sleep(60)
    #serial_openlock.initialize(weather_fid)
    #weather_fid.write("Weather") 
    #msg_weather = weather_fid.readline()
    #port_weather_isopen=serial_openlock.close_port(weather_fid)
    
    msg_weather=read_arduino(port_weather,"Weather")

    
    current_read=msg_weather.split(',')[1:-1]
    for i,key in enumerate(current_read[::2]):
        parsed_data_weather[key.lower()]=float(current_read[2*i+1])
    # get solar from rpi
    #vis=sensor.readVisible()
    #ir=sensor.readIR()
    #uv=sensor.readUV()
    [vis,ir,uv]=read_si1145(si1145_number_readings,si1145_sleep_interval_seconds)
    parsed_data_weather["vis_down"]=vis
    parsed_data_weather["ir_down"]=ir
    parsed_data_weather["uv_down"]=uv
    msg_solar='vis_down'+delimiter+str(vis)+delimiter+'ir_down'+delimiter+str(ir)+delimiter+'uv_down'+delimiter+str(uv)+delimiter

    upload_phant(pht_weather,parsed_data_weather,screen_display)

    # save to file
    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
    if screen_display: print i,delimiter,time_now,delimiter,msg.rstrip(),msg_solar,msg_weather.rstrip()
    if save_to_file: fid.write(time_now+delimiter+msg.rstrip()+msg_solar+msg_weather)
       
    # sleep to the next loop
    time.sleep(sleep_time_seconds)

        
      

#for text in current_read:
#    if 'Soil' in text:
#        print(text)
#
#for text in current_read:
#    if 'So' in text:
#        print(text)
#
#for text in current_read:
#    if 'So' == text:
#        print(text)
#
#for text in current_read:
#    if 'So' == text:
#        print(text)
#ndexes = [i for i,x in enumerate(current_read) if x == 'a']



