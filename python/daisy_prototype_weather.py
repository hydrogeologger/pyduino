#!/usr/bin/python
# this script reads all equipment from column daisy, including sensors and weather stations, uv sensors. 
# mount specification: mega with ec5, eps2, ds18, loadcell, 
import serial
import time
import numpy as np
import sys
from phant import Phant
import serial_openlock
import get_ip
import csv_tools



with open('/home/pi/script/pass/public_daisy_weather_nectar', 'r') as myfile:
    public_daisy_weather=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_daisy_weather_nectar', 'r') as myfile:
    private_daisy_weather=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')

##------------------------ below is to initialize the si1145 at the rpi--------------------
#sensor = SI1145.SI1145() #"/dev/i2c-1")
#time.sleep(3)   # a good sleep before reading is found extremetly important
#vis = sensor.readVisible()
#si1145_number_readings=7;
#si1145_sleep_interval_seconds=10;
#while vis == 0:
#    print 'si1145 init failed'
#    time.sleep(2)
#    print str(vis)
#    SI1145.SI1145_RESET
#    time.sleep(2)
#    sensor = SI1145.SI1145() #"/dev/i2c-1")
#    time.sleep(2)
#    vis = sensor.readVisible()
##------------------------ above is to initialize the si1145 at the rpi--------------------


field_name_weather=['aet','batt','dlyrainmm','ir_down','ir_up','lt','mo_soil','p','pet','rainmm','rh','tc','temp_soil','uv_down','uv_up','vis_down','vis_up','wddir','wddiravg2m','wdgstdir','wdgstdir10m','wdgstkph','wdgstkph10m','wdspdkph','wdspdkphavg2m','tp_box_45','tp_box_47','rh_box_45','rh_box_47','ip']
parsed_data_weather=dict((el,0.0) for el in field_name_weather)
pht_weather = Phant(publicKey=public_daisy_weather, fields=field_name_weather ,privateKey=private_daisy_weather,baseUrl=nectar_address)
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
file_name= 'weather_daisy_nectar.csv'

# open up this file to get the latest uv data
column_file_name='column_daisy_nectar.csv'

fn_column=open(column_file_name,'r')

#sleep_time_seconds=55*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)

#ard = serial.Serial(port,9600,timeout=None)
[opencondition,ard]=serial_openlock.open_port(port_weather)
# the first reading is dummy readings
msg = ard.readline()

def upload_phant(pht,parsed_data,screen_display):
    log_attempts=1
    while log_attempts<6:
        try:          
            ##pht.log(iter([ parsed_data[key] for key in pht.fields]))
            # http://stackoverflow.com/questions/43414407/iterate-at-a-function-input-in-python/43414660#43414660
            pht.log(*[parsed_data[key] for key in pht.fields])
            if screen_display: print "uploaded"
            break
        except Exception, e:
            if screen_display: print "upload failed at attempt,"+str(log_attempts)+" " + str(e)
            log_attempts+=1
            time.sleep(30)
            continue

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
    
    
    #current_read=msg.split(',')[0:-1]
    ## parse tp result
    #tp_ind=[i for i,x in enumerate(current_read) if x == 'Tp']
    #for i in tp_ind:
    #    parsed_data['tp'+current_read[i+1].lower()]=float(current_read[i+2])
    ## parse moisture data
    #mo_ind=[i for i,x in enumerate(current_read) if x == 'Mo']
    #for i in mo_ind:
    #    parsed_data['mo'+current_read[i+1]]=float(current_read[i+2])
    ## parse mps2 data
    #sutp_ind=[i for i,x in enumerate(current_read) if x == 'SuTp']
    #for i in sutp_ind:
    #    parsed_data['su'+current_read[i+1][0]]=float(current_read[i+2])
    #    parsed_data['tp'+current_read[i+1][0]]=float(current_read[i+3])
    ## log the results to sparkfun
    #parsed_data['tphr45']=get_ip.get_ip_address_digit_mask('wlan0')
    #upload_phant(pht_sensor,parsed_data,screen_display)
    ### --------------------------- above is to processing data from column sensor--------------------------
    
    ## connect to new arduino
    #[port_weather_isopen, weather_fid]=serial_openlock.open_port(port_weather)
    #while port_weather_isopen == False:
    #    [port_weather_isopen, weather_fid]=serial_openlock.open_port(port_weather)
    #    time.sleep(60)
    #serial_openlock.initialize(weather_fid)
    #weather_fid.write("Weather") 
    #msg_weather = weather_fid.readline()
    #port_weather_isopen=serial_openlock.close_port(weather_fid)
    
    # the first five ones are not going to post online, but it may be needed as the rain can be better monitored
    msg_weather = ard.readline()
    # save to file
    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
    if screen_display: print time_now+delimiter+msg_weather
    if save_to_file: fid.write(time_now+delimiter+msg_weather)
    
   
    # parsing the file 
    msg_column_file=csv_tools.tail(fn_column,1)
  

    current_read_column=msg_column_file.split(',')[0:-1]

    SaltRH_ind=[i for i,x in enumerate(current_read_column) if x == 'SaltRH']
    for i in SaltRH_ind:
        parsed_data_weather['tp_box_'+current_read_column[i+1]]=float(current_read_column[i+2])
        parsed_data_weather['rh_box_'+current_read_column[i+1]]=float(current_read_column[i+3])

    vis_ind=[i for i,x in enumerate(current_read_column) if x == 'Vis']
    parsed_data_weather['vis_up']=float(current_read_column[vis_ind[0]+1])
    parsed_data_weather['vis_down']=float(current_read_column[vis_ind[1]+1])

    uv_ind=[i for i,x in enumerate(current_read_column) if x == 'UV']
    parsed_data_weather['uv_up']=float(current_read_column[uv_ind[0]+1])
    parsed_data_weather['uv_down']=float(current_read_column[uv_ind[1]+1])
    
    ir_ind=[i for i,x in enumerate(current_read_column) if x == 'IR']
    parsed_data_weather['ir_up']=float(current_read_column[ir_ind[0]+1])
    parsed_data_weather['ir_down']=float(current_read_column[ir_ind[1]+1])
    
#    str_file='tp_box_45'+str(parsed_data_weather[tp_box_45])
#        +'tp_box_47'+str(parsed_data_weather[tp_box_47])
#        +'rh_box_45'+str(parsed_data_weather[rh_box_45])
#        +'rh_box_47'+str(parsed_data_weather[rh_box_47])
#        +'vis_up'+delimiter+str(parsed_data_weather['vis_up']
#        +'vis_down'+delimiter+str(parsed_data_weather['vis_down']
#        +'uv_up'+delimiter+str(parsed_data_weather['uv_up']
#        +'uv_down'+delimiter+str(parsed_data_weather['uv_down']
#        +'ir_up'+delimiter+str(parsed_data_weather['uv_up']
#        +'ir_down'+delimiter+str(parsed_data_weather['uv_down']
    # read from arduino
    msg_weather = ard.readline()
    current_read=msg_weather.split(',')[1:-1]
    for i,key in enumerate(current_read[::2]):
        parsed_data_weather[key.lower()]=float(current_read[2*i+1])

    upload_phant(pht_weather,parsed_data_weather,screen_display)

    # save to file
    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
    if screen_display: print time_now,delimiter,msg_weather.rstrip()
    if save_to_file: fid.write(time_now+delimiter+msg_weather)
       
    # sleep to the next loop
    #time.sleep(sleep_time_seconds)

        
      

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



