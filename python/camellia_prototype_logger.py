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

with open('/home/pi/script/pass/public_camellia_sensors_nectar', 'r') as myfile:
    public_camellia_sensors=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_camellia_sensors_nectar', 'r') as myfile:
    private_camellia_sensors=myfile.read().replace('\n', '')

#with open('/home/pi/script/pass/public_camellia_weather_nectar', 'r') as myfile:
#    public_camellia_weather=myfile.read().replace('\n', '')
#
#with open('/home/pi/script/pass/private_camellia_weather_nectar', 'r') as myfile:
#    private_camellia_weather=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')

#import SI1145.SI1145 as SI1145

###------------------------ below is to initialize the si1145 at the rpi--------------------
#sensor = SI1145.SI1145()
#si1145_number_readings=5
#si1145_sleep_interval_seconds=20
#time.sleep(3)   # a good sleep before reading is found extremetly important
#vis = sensor.readVisible()
#while vis == 0:
#    print 'si1145 init failed'
#    time.sleep(2)
#    #print str(vis)
#    sensor=SI1145.SI1145_RESET
#    time.sleep(2)
#    sensor = SI1145.SI1145() #"/dev/i2c-1")
#    time.sleep(2)
#    vis = sensor.readVisible()
###------------------------ above is to initialize the si1145 at the rpi--------------------


#------------------------- below are definations for the sensors in the column ---------------------------------
field_name_sensor=['mo0','mo1','mo2','mo3','mo4','mo5','mo6','mo7','mo8','mo9',
    'mo10','mo11','mo12','mo13','mo14','mo15',
    't26_begin','t26_peak','te2_begin','te2_peak','t45_begin','t45_peak',
    't57_begin','t57_peak','tfb_begin','tfb_peak','t7b_begin','t7b_peak','ip','evap']


#'All,Mo,0,482.00,Mo,1,330.00,Mo,2,305.86,Mo,3,617.29,Mo,4,327.57,Mo,5,859.86,Mo,6,650.71,Mo,7,341.00,Mo,8,368.00,Mo,9,322.86,Mo,10,484.14,Mo,11,380.43,Mo,12,701.43,Mo,13,578.86,Mo,14,695.86,Mo,15,13.00,Vis,260.43,IR,252.71,UV,2.14,Vis,260.57,IR,253.00,UV,2.00,SucHeat,E2,Heating,15.94,15.94,15.88,15.94,16.00,16.12,16.25,16.37,16.56,16.62,16.81,16.94,17.06,17.25,17.25,Dsping,17.31,17.31,17.31,17.25,17.19,17.12,17.06,17.00,16.94,16.94,16.87,SucHeat,26,Heating,13.94,13.94,13.81,13.88,13.94,14.06,14.19,14.31,14.44,14.56,14.69,14.81,14.94,15.13,15.19,Dsping,15.25,15.25,15.25,15.25,15.19,15.13,15.06,15.00,14.94,14.94,14.88,SucHeat,7B,Heating,19.25,19.25,19.19,19.25,19.31,19.37,19.50,19.62,19.75,19.81,19.94,20.06,20.19,20.31,20.31,Dsping,20.37,20.44,20.37,20.37,20.31,20.25,20.25,20.19,20.12,20.12,20.06,SucHeat,FB,Heating,18.06,18.06,18.00,18.06,18.12,18.31,18.50,18.69,18.81,19.00,19.19,19.31,19.44,19.62,19.75,Dsping,19.75,19.75,19.69,19.62,19.56,19.50,19.37,19.31,19.25,19.19,19.12,SucHeat,45,Heating,16.25,16.25,-0.25,-0.25,-0.25,-0.25,-0.06,-0.25,-0.25,-0.25,-0.25,-0.06,-0.25,17.75,17.81,Dsping,17.87,17.87,17.87,17.81,17.75,17.69,17.62,17.50,17.44,17.37,17.31,SucHeat,57,Heating,17.37,17.37,-0.25,-0.25,-0.25,-0.25,-0.25,-0.25,-0.25,-0.25,-0.25,-0.25,-0.25,18.62,18.69,Dsping,18.75,18.81,18.75,18.69,18.69,18.62,18.50,18.44,18.44,18.37,18.31,SaltRH,6,16.00,38.10,16.00,39.10,SaltRH,7,16.70,34.10,16.70,35.10,AllDone\r\n'

#http://stackoverflow.com/questions/3869487/how-do-i-create-a-dictionary-with-keys-from-a-list-and-values-defaulting-to-say
parsed_data_sensor=dict((el,0.0) for el in field_name_sensor)
pht_sensor = Phant(publicKey=public_camellia_sensors, fields=field_name_sensor ,privateKey=private_camellia_sensors,baseUrl=nectar_address)
port_sensor  = 'USB VID:PID=2341:0010 SNR=55639313533351318031'


# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'column_camellias_sensor_nectar.csv'

#sleep_time_seconds=20*60  # this ends up with 49 min interval
sleep_time_seconds=10*60  # this ends up with 49 min interval

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','


# temp sampling number 
temp_sampling_number=10

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)



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
    
    msg_sensor=serial_openlock.get_result_by_input(port=port_sensor,command="All")

    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
    if screen_display: print time_now,delimiter,msg_sensor.rstrip()
    if save_to_file: fid.write(time_now+delimiter+msg_sensor)

    current_read_sensor=msg_sensor.split(',')[1:-1]
    # parse moisture data
    mo_ind=[i for i,x in enumerate(current_read_sensor) if x == 'Mo']
    for i in mo_ind:
        parsed_data_sensor['mo'+current_read_sensor[i+1]]=float(current_read_sensor[i+2])
    # parse "SucHeat"
    sucheat_ind=[i for i,x in enumerate(current_read_sensor) if x == 'SucHeat']
    for i in sucheat_ind:
        parsed_data_sensor['t'+current_read_sensor[i+1].lower()+'_begin']=float(current_read_sensor[i+4])
        parsed_data_sensor['t'+current_read_sensor[i+1].lower()+'_peak']=float(current_read_sensor[i+temp_sampling_number+3+4])
    # log the results to sparkfun
    upload_phant(pht_sensor,parsed_data_sensor,screen_display)
    ### --------------------------- above is to processing data from column sensor--------------------------
    
       
    # sleep to the next loop
    time.sleep(sleep_time_seconds)

        
