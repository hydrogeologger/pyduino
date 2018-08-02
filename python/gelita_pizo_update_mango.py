#!/usr/bin/python
import os 
import sys
pyduino_path=os.environ['pyduino']
pyduino_data_path=pyduino_path+'/data/'
pyduino_credential_path=pyduino_path+'/credential/'
pyduino_python_path=pyduino_path+'/python/'
sys.path.append(pyduino_python_path)

import serial
import time
import numpy as np
import sys
import csv_tools
from phant import Phant
import serial_openlock
import get_ip
from upload_phant import upload_phant
from time import sleep, strftime,localtime             # lets us have a delay  
import subprocess

public_pizo_pre=csv_tools.get_one_line(pyduino_credential_path+'public_pizo_pre')
private_pizo_pre=csv_tools.get_one_line(pyduino_credential_path+'private_pizo_pre')
nectar_address=csv_tools.get_one_line(pyduino_credential_path+'nectar_address')


field_name=['dp0','hum0','pre0','pre1','pre2','pre3','pre4','pretmp0','pretmp1','pretmp2','pretmp3','pretmp4','timestamp','tmp0','tmp1','tmp10','tmp11','tmp12','tmp2','tmp3','tmp4','tmp5','tmp6','tmp7','tmp8','tmp9','volt0']
pizo_pre=dict((el,0.0) for el in field_name)
pht_pizo_pre = Phant(publicKey=public_pizo_pre, fields=field_name ,privateKey=private_pizo_pre,baseUrl=nectar_address)



# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'

file_name_gelita_1=pyduino_data_path+'gelita_borehole'
fn_gelita=open(file_name_gelita_1,'r')
msg_gelita=csv_tools.tail(fn_gelita,1)
if screen_display: print msg_gelita.rstrip()
current_read=msg_gelita.split(',')[0:-1]


pre_ind=[i for i,x in enumerate(current_read) if x == '9548']
pizo_pre["pre0"]=float(current_read[pre_ind[0]+17])
pizo_pre["tmp0"]=float(current_read[pre_ind[0]+16])
pizo_pre["pre1"]=float(current_read[pre_ind[1]+17])
pizo_pre["tmp1"]=float(current_read[pre_ind[1]+16])
pizo_pre["pre2"]=float(current_read[pre_ind[2]+17])
pizo_pre["tmp2"]=float(current_read[pre_ind[2]+16])


pizo_pre["pretmp1"]=pizo_pre["pre1"]-pizo_pre["pre0"]
pizo_pre["pretmp2"]=pizo_pre["pre2"]-pizo_pre["pre0"]


pre_ind=[i for i,x in enumerate(current_read) if x == 'analog']
pizo_pre["volt0"]=float(current_read[pre_ind[0]+2])


upload_phant(pht_pizo_pre,pizo_pre,screen_display)



