#!/usr/bin/python
import serial
import time
import numpy as np
import sys
from phant import Phant

import serial_openlock


field_name_area51=['t_2896_begin','t_2896_peak','t_2896_end','t_14_begin','t_14_peak','t_14_end',
    't_19_begin','t_19_peak','t_19_end',
    'saltrh_2_t','saltrh_2_rh','saltrh_11_t','saltrh_11_rh','mo_7','mo_8','mo_9','mo_10',
    'te','tas606','commercial','evap']

pht_area51 = Phant(publicKey='21mmonra90TYXlx9KL4J', 
    fields=field_name_area51,privateKey='GZGGko8KJWtKaoAYNe5b')

parsed_data_area51=dict((el,0.0) for el in field_name_area51)

#-------------------below are preparation for the sensor arduino ----------- 
port_sensors='USB VID:PID=0403:6015 SNR=DN01JJDJ'
#'All,SucHeat,2896,Heating,21.81,21.81,21.94,22.00,22.12,22.25,22.31,22.44,22.50,22.62,22.69,22.75,22.81,22.94,22.94,23.00,23.06,23.12,23.19,23.25,23.31,Dsping,23.31,23.31,23.25,23.19,23.12,23.00,22.94,22.87,22.75,22.75,22.69,22.62,22.56,22.50,22.50,22.44,22.44,22.37,22.37,22.31,22.31,SucHeat,14,Heating,25.68,41.80,42.77,43.26,43.75,44.24,44.73,45.70,45.70,46.19,50.10,46.68,47.17,47.66,47.66,48.14,48.14,48.14,48.63,48.63,48.63,Dsping,32.03,31.05,30.57,30.08,30.08,29.59,29.10,29.10,28.61,28.61,28.12,28.12,27.64,27.64,27.64,27.64,27.64,27.15,27.15,27.15,27.15,SucHeat,19,Heating,26.17,38.38,38.38,38.87,38.87,39.36,40.33,40.33,40.82,41.31,41.31,41.80,41.80,42.29,42.29,42.77,43.26,43.26,43.75,43.75,44.24,Dsping,30.57,30.08,29.59,29.59,29.10,29.10,28.61,28.61,28.12,28.12,28.12,28.12,27.64,27.15,27.15,27.15,27.15,26.66,26.66,26.66,26.66,SaltRH,11,21.50,99.90,SaltRH,2,22.30,96.20,Mo,7,341.86,Mo,8,402.00,Mo,9,319.29,Mo,10,344.00,AllDone\r\n'
#'All,SucHeat,2896,Heating,21.81,21.87,21.94,22.06,22.19,22.31,22.37,22.50,22.56,22.69,22.75,22.81,22.87,22.94,23.06,23.06,23.12,23.19,23.25,23.25,23.31,Dsping,23.37,23.31,23.31,23.19,23.12,23.06,23.00,22.87,22.81,22.75,22.75,22.62,22.62,22.56,22.50,22.44,22.44,22.37,22.37,22.31,22.31,SucHeat,14,Heating,25.68,42.29,42.77,43.26,43.75,44.24,45.21,45.70,45.70,46.19,46.68,46.68,47.66,47.66,47.66,48.14,48.14,48.63,48.63,49.12,49.12,Dsping,31.54,31.05,30.57,30.57,30.08,29.59,29.59,29.10,28.61,28.61,28.12,28.12,28.12,27.64,27.64,27.64,27.15,27.15,27.64,27.15,27.15,SucHeat,19,Heating,25.20,38.38,38.38,38.38,39.36,39.36,39.84,40.33,40.82,40.82,41.31,41.80,41.80,42.29,42.77,42.77,43.26,43.26,43.75,43.75,44.24,Dsping,30.08,29.59,29.59,29.59,29.10,29.10,28.61,28.61,28.12,28.12,27.64,27.64,27.64,27.64,27.15,27.15,27.15,26.66,26.66,26.66,26.66,SaltRH,11,21.50,99.90,SaltRH,2,22.30,96.50,Mo,7,338.71,Mo,8,404.00,Mo,9,318.43,Mo,10,344.43,AllDone\r\n'

# makesure the salinity sensor are well initialized
serial_openlock.get_result_by_input(port=port_sensors,command="SoilSalinity")
time.delay(3)
serial_openlock.get_result_by_input(port=port_sensors,command="SoilSalinity")
time.delay(3)


#-------------------below are preparation for the scale arduino ----------- 
port_loadcell='USB VID:PID=0403:6015 SNR=DN01J0QE'

#-------------------below are preparation for the commercial balance ----------- 
port_balance='USB VID:PID=0403:6001'

 # make a good initialization
b=serial_openlock.get_result_by_input(port=port_balance,command='IP\n\r',initialize=False)
time.sleep(2)
b=serial_openlock.get_result_by_input(port=port_balance,command='IP\n\r',initialize=False)


#
temp_sampling_number=20
# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'area51_redmud.csv'

sleep_time_seconds=1 #25*60

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


while True: 

    # below is to get results from sensor arduino
    msg_sensors=serial_openlock.get_result_by_input(port=port_sensors,command="All")
    current_read_sensors=msg_sensors.split(',')[1:-1]
    # parse "SucHeat"
    sucheat_ind=[i for i,x in enumerate(current_read_sensors) if x == 'SucHeat']
    for i in sucheat_ind:
        parsed_data_area51['t_'+current_read_sensors[i+1].lower()+'_begin']=float(current_read_sensors[i+3])
        parsed_data_area51['t_'+current_read_sensors[i+1].lower()+'_peak'] =float(current_read_sensors[i+temp_sampling_number+3])
        parsed_data_area51['t_'+current_read_sensors[i+1].lower()+'_end']  =float(current_read_sensors[i+2*temp_sampling_number+5])

    # parse salinity sensor using relative humidty data
    saltrh_ind=[i for i,x in enumerate(current_read_sensors) if x == 'SaltRH']
    for i in saltrh_ind:
        if float(current_read_sensors[i+2])<0 :
            parsed_data_area51['saltrh_'+current_read_sensors[i+1]+'_t']=np.nan
            parsed_data_area51['saltrh_'+current_read_sensors[i+1]+'_rh']=np.nan
        else:
            parsed_data_area51['saltrh_'+current_read_sensors[i+1]+'_t']=float(current_read_sensors[i+2])
            parsed_data_area51['saltrh_'+current_read_sensors[i+1]+'_rh']=float(current_read_sensors[i+3])

    # parse moisture_sensor data
    mo_ind=[i for i,x in enumerate(current_read_sensors) if x == 'Mo']
    for i in mo_ind:
        parsed_data_area51['mo_'+current_read_sensors[i+1]]=float(current_read_sensors[i+2])
    # -------------- below is to get result from loadcell arduino
    msg_loadcell=serial_openlock.get_result_by_input(port=port_loadcell,command="All")
    current_read_loadcell=msg_loadcell.split(',')[1:-1]
    
    for i,key in enumerate(current_read_loadcell[::2]):
        parsed_data_area51[key.lower()]=float(current_read_loadcell[2*i+1])

    # below are for balance readings
    msg_balance=serial_openlock.get_result_by_input(port=port_balance,command='IP\n\r',initialize=False)
    current_read_balance=msg_balance.split()[0]
    parsed_data_area51['commercial']=float(current_read_balance)


    upload_phant(pht_weather,parsed_data_weather,screen_display)
    # save to file
    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
    if screen_display: print i,delimiter,time_now,delimiter,msg_sensors.rstrip(),msg_loadcell.rstrip(),delimiter,msg_balance.rstrip()
    if save_to_file: fid.write(time_now+delimiter+msg_sensors.rstrip()+msg_loadcell.rstrip()+msg_balance)
    time.sleep(sleep_time_seconds)





