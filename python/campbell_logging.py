import time
import datetime
from pycampbellcr1000 import CR1000

delta_t_sec=30*60
time_current=datetime.datetime.now()
time_previous=datetime.datetime.now() - datetime.timedelta(seconds=delta_t_sec)

device = CR1000.from_url('serial:/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0:38400')
file_name='campbell_output.csv'

fid= open(file_name,'a',0)


while True:
    log_attempt=1
    while log_attempt<5:
        try:
            data = device.get_data('WPS_Tab_noarray',time_previous,time_current)
            break
        except:
            log_attempts+=1
            time.sleep(30)
            continue
    data[0]['Datetime'] =data[0]['Datetime'].strftime("%d/%b/%Y %H:%M:%S")
    
    str_data=''
    for key in data[0]:
       str_data+=key+','+str(data[0][key])+','
    fid.write(str_data+'\n')     
    time.sleep(delta_t_sec)

    
    
    
