#!/usr/bin/python
import serial
import time
import numpy as np
import sys
from phant import Phant
import serial_openlock
import get_ip
from upload_phant import upload_phant



with open('/home/pi/script/pass/public_grange_a_moisture_suction', 'r') as myfile:
    public_grange_a_moisture_suction=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_grange_a_moisture_suction', 'r') as myfile:
    private_grange_a_moisture_suction=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/public_grange_a_electrochem_o2', 'r') as myfile:
    public_grange_a_electrochem_o2=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_grange_a_electrochem_o2', 'r') as myfile:
    private_grange_a_electrochem_o2=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/public_grange_a_luo2', 'r') as myfile:
    public_grange_a_luo2=myfile.read().replace('\n', '')

with open('/home/pi/script/pass/private_grange_a_luo2', 'r') as myfile:
    private_grange_a_luo2=myfile.read().replace('\n', '')
with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
    nectar_address=myfile.read().replace('\n', '')



#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['mo0','mo1','mo2','mo3','mo4','mo5','mo6','mo7',
            'su0','su1','su2','su3','su4','su5','su6','su7',
            'tmp0','tmp1','tmp2','tmp3','tmp4','tmp5','tmp6','tmp7',
            's2','s3','s4','s5','s6','s7']
parsed_data=dict((el,0.0) for el in field_name)
pht_sensor = Phant(publicKey=public_grange_a_moisture_suction, fields=field_name ,privateKey=private_grange_a_moisture_suction,baseUrl=nectar_address)



#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['dtp0','dtp1','dtp2','dtp3','dtp6',
            'dox0','dox1','dox2','dox3','dox6',
            'drh0','drh1','drh2','drh3','drh6',
            'wtp0','wtp1','wtp2','wtp3','wtp4','wtp5','wtp7',
            'wox0','wox1','wox2','wox3','wox4','wox5','wox7']
ele_o2=dict((el,0.0) for el in field_name)
pht_ele_o2 = Phant(publicKey=public_grange_a_electrochem_o2, fields=field_name ,privateKey=private_grange_a_electrochem_o2,baseUrl=nectar_address)



#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['dluo4' , 'dluo5', 'wluo5', 'wluo6',
            'dlut4' , 'dlut5', 'wlut5', 'wlut6',
            'dlup4' , 'dlup5', 'wlup5', 'wlup6',
            'dlupe4','dlupe5','wlupe5','wlupe6',
            'uvb','ira','lra',
            'irb','lrbtemp','rh','flow']
luo2=dict((el,0.0) for el in field_name)


pht_luo2 = Phant(publicKey=public_grange_a_luo2, fields=field_name ,privateKey=private_grange_a_luo2,baseUrl=nectar_address)



port_sensor  = 'USB VID:PID=2341:0042 SNR=9563533373035110B1D1'


# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'Grange_a.csv'

sleep_time_seconds=45*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if save_to_file: fid= open(file_name,'a',0)



while True: 
# ------------------------------- below goes to electrochem_o2  --------------------------------------------
    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="o2_ana_ay,1,power,6,point,3,interval_mm,2000,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    ele_o2['wtp0']=float(current_read[2])
    ele_o2['wtp1']=float(current_read[5])
    ele_o2['wtp2']=float(current_read[8])
    ele_o2['wtp3']=float(current_read[11])
    ele_o2['wtp4']=float(current_read[14])
    ele_o2['wtp5']=float(current_read[17])

    ele_o2['wox0']=float(current_read[4])
    ele_o2['wox1']=float(current_read[7])
    ele_o2['wox2']=float(current_read[10])
    ele_o2['wox3']=float(current_read[13])
    ele_o2['wox4']=float(current_read[16])
    ele_o2['wox5']=float(current_read[19])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dhto2,4,power,23,points,2,anain,7,dummies,1,interval_mm,2000,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    ele_o2['wtp7']=float(current_read[2])
    ele_o2['wrh7']=float(current_read[3])
    ele_o2['wox7']=float(current_read[4])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dhto2,12,power,41,points,2,anain,0,dummies,1,interval_mm,2000,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    ele_o2['dtp0']=float(current_read[2])
    ele_o2['drh0']=float(current_read[3])
    ele_o2['dox0']=float(current_read[4])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dhto2,11,power,27,points,2,anain,1,dummies,1,interval_mm,2000,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    ele_o2['dtp1']=float(current_read[2])
    ele_o2['drh1']=float(current_read[3])
    ele_o2['dox1']=float(current_read[4])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dhto2,10,power,29,points,2,anain,2,dummies,1,interval_mm,2000,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    ele_o2['dtp2']=float(current_read[2])
    ele_o2['drh2']=float(current_read[3])
    ele_o2['dox2']=float(current_read[4])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dhto2,51,power,31,points,2,anain,3,dummies,1,interval_mm,2000,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    ele_o2['dtp3']=float(current_read[2])
    ele_o2['drh3']=float(current_read[3])
    ele_o2['dox3']=float(current_read[4])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dhto2,5,power,24,points,2,anain,6,dummies,1,interval_mm,2000,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    ele_o2['dtp6']=float(current_read[2])
    ele_o2['drh6']=float(current_read[3])
    ele_o2['dox6']=float(current_read[4])

    upload_phant(pht_ele_o2,ele_o2,screen_display)
    

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,22,serial,3",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    luo2['wluo5'] = float(current_read[7])
    luo2['wlupe5']= float(current_read[5])
    luo2['wlut5'] = float(current_read[3])
    luo2['wlup5'] = float(current_read[1])

    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,33,serial,2",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(' ')[0:-1]
    luo2['wluo6'] = float(current_read[7])
    luo2['wlupe6']= float(current_read[5])
    luo2['wlut6'] = float(current_read[3])
    luo2['wlup6'] = float(current_read[1])


    # enclosure temperature and humidity
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,10,power,48,points,2,dummies,1,interval_mm,2000,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    luo2['temp']=float(current_read[2])
    luo2['rh']=float(current_read[3])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="1145,3,power,8,dummies,1,interval_mm,2000,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    luo2['uvb']=float(current_read[-1])
    luo2['irb']=float(current_read[-3])
    luo2['lrbtemp']=float(current_read[-5])


    upload_phant(pht_luo2,luo2,screen_display)





    ### -------------------- bwlow is to processing data from suction, moisture-------------------------
    
    msg=serial_openlock.get_result_by_input(port=port_sensor,command="anaay,1,power,42,point,3,interval_mm,200",initialize=False)
    # save to file it needs to be done immediately after read so that bugs could be found during parsing
    time_now=time.strftime("%d/%b/%Y %H:%M:%S")
    if screen_display: print time_now,delimiter,msg.rstrip()
    if save_to_file: fid.write(time_now+delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    parsed_data['mo0']=float(current_read[2])
    parsed_data['mo1']=float(current_read[3])
    parsed_data['mo2']=float(current_read[4])
    parsed_data['mo3']=float(current_read[5])
    parsed_data['mo4']=float(current_read[6])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,13,power,35,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    parsed_data['mo5']=float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,14,power,37,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    parsed_data['mo6']=float(current_read[2])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,15,power,39,point,3,interval_mm,200,debug,0",initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    parsed_data['mo7']=float(current_read[2])

    

    msg=serial_openlock.get_result_by_input(port=port_sensor,command='fred,6C51BC5E,dgin,50,snpw,44,htpw,32,itv,3000,otno,10',initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    parsed_data['tmp0']=float(current_read[2])
    parsed_data['su0']=float(current_read[12])-float(current_read[2])

    msg=serial_openlock.get_result_by_input(port=port_sensor,command='fred,523EBCDE,dgin,50,snpw,44,htpw,30,itv,3000,otno,10',initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    parsed_data['tmp1']=float(current_read[2])
    parsed_data['su1']=float(current_read[12])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command='fred,F655BA36,dgin,50,snpw,44,htpw,28,itv,3000,otno,10',initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    parsed_data['tmp2']=float(current_read[2])
    parsed_data['su2']=float(current_read[12])-float(current_read[2])
    parsed_data['s2']=float(current_read[5])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command='fred,5EFCB983,dgin,50,snpw,44,htpw,26,itv,3000,otno,10',initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    parsed_data['tmp3']=float(current_read[2])
    parsed_data['su3']=float(current_read[12])-float(current_read[2])
    parsed_data['s3']=float(current_read[5])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command='fred,CA4DBCED,dgin,50,snpw,44,htpw,40,itv,3000,otno,10',initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    parsed_data['tmp4']=float(current_read[2])
    parsed_data['su4']=float(current_read[12])-float(current_read[2])
    parsed_data['s4']=float(current_read[5])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command='fred,2E42BC77,dgin,50,snpw,44,htpw,38,itv,3000,otno,10',initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    parsed_data['tmp5']=float(current_read[2])
    parsed_data['su5']=float(current_read[12])-float(current_read[2])
    parsed_data['s5']=float(current_read[5])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command='fred,DD33BCFC,dgin,50,snpw,44,htpw,36,itv,3000,otno,10',initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    parsed_data['tmp6']=float(current_read[2])
    parsed_data['su6']=float(current_read[12])-float(current_read[2])
    parsed_data['s6']=float(current_read[5])-float(current_read[2])


    msg=serial_openlock.get_result_by_input(port=port_sensor,command='fred,E0CFB95D,dgin,50,snpw,44,htpw,34,itv,3000,otno,10',initialize=False)
    if screen_display: print msg.rstrip()
    if save_to_file: fid.write(delimiter+msg.rstrip())
    current_read=msg.split(',')[0:-1]
    parsed_data['tmp7']=float(current_read[2])
    parsed_data['su7']=float(current_read[12])-float(current_read[2])
    parsed_data['s7']=float(current_read[5])-float(current_read[2])

    upload_phant(pht_sensor,parsed_data,screen_display)
    ### --------------------------- above is to processing data from column sensor--------------------------
       
    # sleep to the next loop
    time.sleep(sleep_time_seconds)

        
      


