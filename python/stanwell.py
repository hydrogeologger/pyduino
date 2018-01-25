#!/usr/bin/python
import serial
import time
import numpy as np
import sys
from phant import Phant
import serial_openlock
import get_ip
from upload_phant import upload_phant



with open('/home/pi/script/pass/public_stanwell_moisture_suction', 'r') as myfile:
    public_stanwell_moisture_suction=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_stanwell_moisture_suction', 'r') as myfile:
    private_stanwell_moisture_suction=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/public_stanwell_electrochem_o2', 'r') as myfile:
    public_stanwell_electrochem_o2=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_stanwell_electrochem_o2', 'r') as myfile:
    private_stanwell_electrochem_o2=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/public_stanwell_luo2', 'r') as myfile:
    public_stanwell_luo2=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_stanwell_luo2', 'r') as myfile:
    private_stanwell_luo2=myfile.read().replace('\n', '')
with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')



#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['mo0','mo1','mo2','mo3','mo4','mo5','mo6','mo7','mo8','mo9',
            'su0','su1','su2','su3','su4','su5','su6','su7','su8','su9',
            'tmp0','tmp1','tmp2','tmp3','tmp4','tmp5','tmp6','tmp7','tmp8','tmp9'
            ]
mo_su=dict((el,0.0) for el in field_name)
pht_sensor = Phant(publicKey=public_stanwell_moisture_suction, fields=field_name ,privateKey=private_stanwell_moisture_suction,baseUrl=nectar_address)



###------------------------- below are definations for the sensors in the column ---------------------------------
##field_name=['dtp0','dtp1','dtp2','dtp3','dtp6',
##            'dox0','dox1','dox2','dox3','dox6',
##            'drh0','drh1','drh2','drh3','drh6',
##            'wtp0','wtp1','wtp2','wtp3','wtp4','wtp5','wtp7',
##            'wox0','wox1','wox2','wox3','wox4','wox5','wox7']
##ele_o2=dict((el,0.0) for el in field_name)
##pht_ele_o2 = Phant(publicKey=public_stanwell_electrochem_o2, fields=field_name ,privateKey=private_stanwell_electrochem_o2,baseUrl=nectar_address)
##
##
##
###------------------------- below are definations for the sensors in the column ---------------------------------
##field_name=['dluo4' , 'dluo5', 'wluo5', 'wluo6',
##            'dlut4' , 'dlut5', 'wlut5', 'wlut6',
##            'dlup4' , 'dlup5', 'wlup5', 'wlup6',
##            'dlupe4','dlupe5','wlupe5','wlupe6',
##            'uvb','ira','lra',
##            'uvb','irb','lrb'
##            'temp','rh','flow']
##luo2=dict((el,0.0) for el in field_name)
##pht_luo2 = Phant(publicKey=public_stanwell_luo2, fields=field_name ,privateKey=private_stanwell_luo2,baseUrl=nectar_address)



port_sensor  = 'USB VID:PID=2341:0042 SNR=9563533373035110A2B1'


# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'stanwell.csv'

sleep_time_seconds=45*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)



while True: 
    ### -------------------- below is to processing data from suction, moisture-------------------------
    
# ------------------------------- below goes to electrochem_o2  --------------------------------------------
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,E87C959F,dgin,50,snpw,42,htpw,22,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp0']=float(current_read[2])
    mo_su['su0']=float(current_read[7])-float(current_read[2])



    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,F755BA01,dgin,50,snpw,42,htpw,24,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp1']=float(current_read[2])
    mo_su['su1']=float(current_read[7])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,1848BC95,dgin,50,snpw,42,htpw,33,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp2']=float(current_read[2])
    mo_su['su2']=float(current_read[7])-float(current_read[2])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,B722BBC7,dgin,50,snpw,42,htpw,31,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp3']=float(current_read[2])
    mo_su['su3']=float(current_read[7])-float(current_read[2])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,4FCAB9F7,dgin,50,snpw,42,htpw,29,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp4']=float(current_read[2])
    mo_su['su4']=float(current_read[7])-float(current_read[2])


     msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,C205BB1D,dgin,13,snpw,6,htpw,27,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp5']=float(current_read[2])
    mo_su['su5']=float(current_read[7])-float(current_read[2])


     msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,4C0F973B,dgin,13,snpw,6,htpw,41,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp6']=float(current_read[2])
    mo_su['su6']=float(current_read[7])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,C286BB98,dgin,13,snpw,6,htpw,39,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp7']=float(current_read[2])
    mo_su['su7']=float(current_read[7])-float(current_read[2])

    #msg=serial_openlock.get_result_by_input(port=port_sensor,command="",initialize=False)
    #if screen_display: print msg.rstrip()
    #if save_to_file: fid.write(delimiter+msg.rstrip())
    #current_read=msg.split(',')[0:-1]
    #mo_su['tmp8']=float(current_read[2])
    #mo_su['su8']=float(current_read[7])-float(current_read[2])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,EAC3B9B3,dgin,13,snpw,6,htpw,35,itv,1000,otno,5",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['tmp9']=float(current_read[2])
    mo_su['su9']=float(current_read[7])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,14,power,40,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo0']=float(current_read[2])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,13,power,26,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo1']=float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,12,power,28,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo2']=float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,11,power,30,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo3']=float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,10,power,32,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo4']=float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,9,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo5']=float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,8,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo6']=float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,7,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo7']=float(current_read[2])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,6,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo8']=float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,5,power,44,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    mo_su['mo9']=float(current_read[2])

    

    upload_phant(pht_sensor,mo_su,screen_display)

    ### --------------------------- above is to processing data from column sensor--------------------------
    
       
    # sleep to the next loop
    time.sleep(sleep_time_seconds)

        
      


