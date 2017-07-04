import time
import datetime
from pycampbellcr1000 import CR1000

delta_t_sec=30*60
time_current=datetime.datetime.now()
time_previous=datetime.datetime.now() - datetime.timedelta(seconds=delta_t_sec)

#logger_address='serial:/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0:38400'
#device = CR1000.from_url('serial:/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0:38400')
#time.sleep(5)
#device = CR1000.from_url(logger_address)

file_name='campbell_output.csv'

fid= open(file_name,'a',0)


while True:
    log_attempt=1
    while log_attempt<10:
        try:
            device = CR1000.from_url('serial:/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0:38400')
            data = device.get_data('WPS_Tab_noarray',time_previous,time_current)
            break
        except Exception, e:
            # https://stackoverflow.com/questions/1483429/how-to-print-an-error-in-python
            print time_current.strftime("%d/%b/%Y %H:%M:%S")+" extracting failed "+str(log_attempt)+ ' '+ str(e)
            log_attempt+=1
            time.sleep(10)
            #device = CR1000.from_url('serial:/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0:38400')
            continue
    data[0]['Datetime'] =data[0]['Datetime'].strftime("%d/%b/%Y %H:%M:%S")
    #data['Datetime'] =data['Datetime'].strftime("%d/%b/%Y %H:%M:%S")
    
    str_data=''
    for key in data[0]:
       str_data+=key+','+str(data[0][key])+','
    fid.write(str_data+'\n')     
    print data[0]['Datetime']+' done'
    time.sleep(delta_t_sec)
    time_previous=time_current
    time_current=datetime.datetime.now()


    
    
    
