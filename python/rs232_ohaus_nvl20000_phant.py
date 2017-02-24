# this script records scale readings from adam gfk 600
import serial
import time
import numpy as np
import sys
from phant import Phant
ser = serial.Serial('/dev/serial/by-id/usb-FTDI_USB__-__Serial-if00-port0')

no_of_readings=60000  # totally how many readings will be done
sleep_time_seconds=300 # the interval of neighbouring reading


field_name=['commercial','nvl','ohaus','measure_local_time'];

pht = Phant(publicKey='7Jlzv3bb9vhZ4LLd9Waj', 
    fields=field_name ,privateKey='mz4rqWGGoqHjeYYaB9Nn')

parsed_data={'commercial':0.0,'nvl':0.0,'ohaus':0.0,'measure_local_time':''};


# the Filename of the csv file for storing file
file_name= 'rs232_ohaus_nvl20000_phant.csv'

save_to_file=True
screen_display=True
#temp=["" for x in range(no_of_readings)]
#reading_scale=["" for x in range(no_of_readings)]
#reading_time =["" for x in range(no_of_readings)]

__author__ = 'chenming'


#if __name__ == "__main__":
#    while True:
#        fid= open('scale_record.dat','a',0)
#        #ser.write('P\n\r')
#        ser.write('IP\n\r')
#        ser.readline()
#
#
#
#        for n in range(0, no_of_readings-1):
#            #ser.write('P\n\r')  # output STABLE results. warning, not good for roof test or test under a fan
#            ser.write('IP\n\r')  # output constant result, if it is a unsable one, the result ends up with a question mark.
#            temp[n]=ser.readline()
#            current_scale_read=temp[n].split()[0]
#            thermometer(current_scale_read)
#            fid.write(time.strftime("%d/%b/%Y %H:%M:%S")+temp[n])
#            time.sleep(sleep_time_seconds)
#
#        fid.close()
#        ser.close()


ser.write('IP\n\r')
# throw away the first reading as it is always formated poorly
msg = ser.readline()
if save_to_file: fid= open(file_name,'a',0)
for i in xrange(no_of_readings): 
    ser.write('IP\n\r')
    msg = ser.readline()
    current_read=msg.split()[0]
    parsed_data['commercial']=float(current_read)
    parsed_data['nvl']=0.0
    parsed_data['ohaus']=0.0
    time_now=time.strftime("%Y-%b-%d %H:%M:%S")
    parsed_data['measure_local_time']=time_now


    log_attempts=1
    while log_attempts<10:
        try:
            pht.log(parsed_data['commercial']  # warning: the sequence of the upload values has to follow strict from sequence in variable pased_data and field name
                ,parsed_data['nvl']
                ,parsed_data['ohaus']
                ,parsed_data['measure_local_time'])
            break
        except: # catch all errors
            log_attempts+=1
            time.sleep(30)
            continue
        if screen_display: print i,delimiter,time_now,delimiter,msg.rstrip()
        if save_to_file: fid.write(time_now+delimiter+msg)
       
    time.sleep(sleep_time_seconds)

        
fid.close()
ser.close()





