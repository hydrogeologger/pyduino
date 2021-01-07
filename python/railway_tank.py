#!/usr/bin/python
import serial
import os
import time
#import numpy as np
import sys
import paho.mqtt.client as mqtt
import json
from phant import Phant
import serial_openlock
#import get_ip
from upload_phant import upload_phant
# below required by gpio
import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep,gmtime,localtime,strftime


with open('/home/pi/pyduino/credential/railway_tank.json') as f:
        credential = json.load(f) #,object_pairs_hook=collections.OrderedDict)

#SDI_total = 20
#gs = 'gs', cs = 'cs'
#temp = 'temp', ec = 'ec', dp = 'dp'
#
#field_name = {'volt', 'dht22_rh','dht22_t')
#
#for i in range(0, SDI_total):
#	fiel_nae


##change values here
#heat_time            = str(6000)
#SDI12_TOTAL         = [20, 5] #total sensors for each type
#SDI12_SENSOR_TYPE   = ['gs', 'cs'] #types
#SDI12_SENSOR_NAME   = ['DEC', 'Cam']
#SDI12_TYPE_COUNT    = len(SDI12_SENSOR_TYPE)
#SDI12_FIELD_TYPE    = ['temp', 'ec', 'dp']
#SU_SENSOR           = 'su'
#SU_COUNT            = 16
#SU_CHANNEL          = 5
#TEMP_SENSOR         = 'temp'
#TEMP_COUNT           = 16
#
##construct field name
#field_name = ['volt', 'dht22_rh', 'dht22_t']
#
#for t in SDI12_SENSOR_TYPE:
#    for field in SDI12_FIELD_TYPE:
#        for c in SDI12_TOTAL:
#            for i in range (0, c):
#                if t is SDI12_SENSOR_TYPE[1] and c is SDI12_TOTAL[1]:
#                    name = t + field + '_' + chr(ord('a') + i)
#                elif t is SDI12_SENSOR_TYPE[0] and c is SDI12_TOTAL[0]:
#                    name = t + field + str(i)
#                else:
#                    break
#                field_name.append(name)
#
#
#for s in range(0, SU_COUNT):
#    for c in range(0, SU_CHANNEL):
#        name = SU_SENSOR + '_' + chr(ord('a') + s) + str(c) 
#        field_name.append(name)
#
#for s in range(0, TEMP_COUNT):
#    name = TEMP_SENSOR + '_' + chr(ord('a') + s)
#    field_name.append(name)
#
##construct look up table
#SDI12_LOOK_UP = {}
#for c in SDI12_TOTAL:
#    for t in SDI12_SENSOR_NAME:
#        for i in range(0, c):
#            key = ''
#            if t is SDI12_SENSOR_NAME[0] and c is SDI12_TOTAL[0]:
#                key = str(i) + '_' + t
#            elif t is SDI12_SENSOR_NAME[1] and c is SDI12_TOTAL[1]:
#                key = chr(ord('A') + i) + '_' + t
#            else:
#                break
#            values =[]
#            for field in SDI12_FIELD_TYPE:
#                if t is SDI12_SENSOR_NAME[0]:
#                    name = SDI12_SENSOR_TYPE[0] + field + str(i)
#                else:
#                    name = SDI12_SENSOR_TYPE[1] + field + str(i)
#                values.append(name)
#            SDI12_LOOK_UP.update({key : values})

field_name=['dht22_rh','dht22_t',
	    'mo0','mo1','mo2','mo3','mo4','mo5','mo6','mo7',
            'su_a0','su_a1','su_a2','su_a3','su_a4',
            'su_b0','su_b1','su_b2','su_b3','su_b4',
            'su_c0','su_c1','su_c2','su_c3','su_c4',
            'su_d0','su_d1','su_d2','su_d3','su_d4',
            'su_e0','su_e1','su_e2','su_e3','su_e4',
            'su_f0','su_f1','su_f2','su_f3','su_f4',
            'su_g0','su_g1','su_g2','su_g3','su_g4',
            'su_h0','su_h1','su_h2','su_h3','su_h4',
            'temp_a','temp_b','temp_c','temp_d','temp_e','temp_f','temp_g','temp_h'
            ]

#look_up = {
#	'0_DEC' : ['gstemp0', 'gsec0', 'gsdp0'],
#	'1_DEC' : ['gstemp1', 'gsec1', 'gsdp1'],
#	'2_DEC' : ['gstemp2', 'gsec2', 'gsdp2'],
#	'3_DEC' : ['gstemp3', 'gsec3', 'gsdp3'],
#	'A_Cam' : ['cstemp0', 'csec0', 'csdp0'],
#	'B_Cam' : ['cstemp1', 'csec1', 'csdp1'],
#	'C_Cam' : ['cstemp2', 'csec2', 'csdp2'],
#	'D_Cam' : ['cstemp3', 'csec3', 'csdp3'],
#	'E_Cam' : ['cstemp4', 'csec4', 'csdp4'],
#
#}
#
#sensor_name = #strip and split to get the name
#name_field = look_up.get(sensor_name) #list of strings for certain sensor_name
#temp_filed = name_field[0]
#ec_field = name_field[1]
#dp_filed = name_file[2]


railway_tank=dict((el,0.0) for el in field_name)
pht_sensor = Phant(publicKey=credential["public_railway_tank"], fields=field_name ,privateKey=credential["private_railway_tank"],baseUrl=credential["nectar_address"])

port_sensor  = '/dev/ttyS0'

# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'railway_tank.csv'

sleep_time_seconds=60*60
#sleep_time_seconds=1*10

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

while True:
    try:
        next_reading = time.time()
        client = mqtt.Client()
        client.username_pw_set(credential['access_token'])
        client.connect(credential['thingsboard_host'], 1883, 60)
        client.loop_start()
        break
    except Exception, e:
        time.sleep(60)
        break

if save_to_file: fid= open(file_name,'a',0)

try:

    while True:

        if screen_display: print strftime("%Y-%m-%d %H:%M:%S", localtime())
        if save_to_file: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime())  )


        ard=serial.Serial(port_sensor,timeout=60)

#------enclosure------------------
        msg=ard.write("dht22,54,power,2,points,2,dummies,1,interval_mm,200,debug,1")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        railway_tank['dht22_rh']=float(current_read[-1])
        railway_tank['dht22_t']=float(current_read[-2])
        #sleep(2)

#------moisture 1------------------
        msg=ard.write("analog,1,power,34,point,3,interval_mm,200,debug,0")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
	current_read=msg.split(',')[0:-1]
        railway_tank['mo0']=float(current_read[2])


#------moisture 2------------------
        msg=ard.write("analog,2,power,35,point,3,interval_mm,200,debug,0")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
	current_read=msg.split(',')[0:-1]
        railway_tank['mo1']=float(current_read[2])

#------moisture 3------------------
        msg=ard.write("analog,3,power,36,point,3,interval_mm,200,debug,0")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
	current_read=msg.split(',')[0:-1]
        railway_tank['mo2']=float(current_read[2])

#------moisture 4------------------
        msg=ard.write("analog,4,power,37,point,3,interval_mm,200,debug,0")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
	current_read=msg.split(',')[0:-1]
        railway_tank['mo3']=float(current_read[2])

#------moisture 5------------------
        msg=ard.write("analog,5,power,38,point,3,interval_mm,200,debug,0")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
	current_read=msg.split(',')[0:-1]
        railway_tank['mo4']=float(current_read[2])

#------moisture 6------------------
        msg=ard.write("analog,6,power,39,point,3,interval_mm,200,debug,0")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
	current_read=msg.split(',')[0:-1]
        railway_tank['mo5']=float(current_read[2])

#------moisture 7------------------
        msg=ard.write("analog,7,power,40,point,3,interval_mm,200,debug,0")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
	current_read=msg.split(',')[0:-1]
        railway_tank['mo6']=float(current_read[2])

#------moisture 8------------------
        msg=ard.write("analog,8,power,41,point,3,interval_mm,200,debug,0")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
	current_read=msg.split(',')[0:-1]
        railway_tank['mo7']=float(current_read[2])

#------suction group 1--------------
#----4 sensors in power 22, digital 5-------------
        msg=ard.write("fred9,3BF1A0A3,dgin,5,snpw,22,htpw,24,itv,6000,otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        railway_tank['temp_a']=float(current_read[2])
        railway_tank['su_a0']=float(current_read[4])-float(current_read[2])
        railway_tank['su_a1']=float(current_read[6])-float(current_read[2])
        railway_tank['su_a2']=float(current_read[8])-float(current_read[2])
        railway_tank['su_a3']=float(current_read[10])-float(current_read[2])
        railway_tank['su_a4']=float(current_read[12])-float(current_read[2])

        #sleep(2)

        msg=ard.write("fred9,FAF0A0C6,dgin,5,snpw,22,htpw,25,itv,6000,otno,5")
        msg=ard.flushInput()
        msg=ard.readline()
        
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        railway_tank['temp_b']=float(current_read[2])
        railway_tank['su_b0']=float(current_read[4])-float(current_read[2])
        railway_tank['su_b1']=float(current_read[6])-float(current_read[2])
        railway_tank['su_b2']=float(current_read[8])-float(current_read[2])
        railway_tank['su_b3']=float(current_read[10])-float(current_read[2])
        railway_tank['su_b4']=float(current_read[12])-float(current_read[2])

#        msg=ard.write("fred9,381AA1DF,dgin,5,snpw,22,htpw,26,itv,6000,otno,5")
        msg=ard.write("fred9,0141A0CE,dgin,5,snpw,22,htpw,26,itv,6000,otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        railway_tank['temp_c']=float(current_read[2])
        railway_tank['su_c0']=float(current_read[4])-float(current_read[2])
        railway_tank['su_c1']=float(current_read[6])-float(current_read[2])
        railway_tank['su_c2']=float(current_read[8])-float(current_read[2])
        railway_tank['su_c3']=float(current_read[10])-float(current_read[2])
        railway_tank['su_c4']=float(current_read[12])-float(current_read[2])

        msg=ard.write("fred9,80D6A0F5,dgin,5,snpw,22,htpw,27,itv,6000,otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        railway_tank['temp_d']=float(current_read[2])
        railway_tank['su_d0']=float(current_read[4])-float(current_read[2])
        railway_tank['su_d1']=float(current_read[6])-float(current_read[2])
        railway_tank['su_d2']=float(current_read[8])-float(current_read[2])
        railway_tank['su_d3']=float(current_read[10])-float(current_read[2])
        railway_tank['su_d4']=float(current_read[12])-float(current_read[2])
	#sleep(2)

#------------------suction group 2---------------------------------------------
#--------4 sensors in power 23, digital 4-------------------------------------
        msg=ard.write("fred9,F1F0A03E,dgin,4,snpw,23,htpw,28,itv,6000,otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        railway_tank['temp_e']=float(current_read[2])
        railway_tank['su_e0']=float(current_read[4])-float(current_read[2])
        railway_tank['su_e1']=float(current_read[6])-float(current_read[2])
        railway_tank['su_e2']=float(current_read[8])-float(current_read[2])
        railway_tank['su_e3']=float(current_read[10])-float(current_read[2])
        railway_tank['su_e4']=float(current_read[12])-float(current_read[2])
        #sleep(2)

        msg=ard.write("fred9,F540A0AD,dgin,4,snpw,23,htpw,30,itv,6000,otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        railway_tank['temp_f']=float(current_read[2])
        railway_tank['su_f0']=float(current_read[4])-float(current_read[2])
        railway_tank['su_f1']=float(current_read[6])-float(current_read[2])
        railway_tank['su_f2']=float(current_read[8])-float(current_read[2])
        railway_tank['su_f3']=float(current_read[10])-float(current_read[2])
        railway_tank['su_f4']=float(current_read[12])-float(current_read[2])


        msg=ard.write("fred9,F208A0FF,dgin,4,snpw,23,htpw,31,itv,6000,otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        railway_tank['temp_g']=float(current_read[2])
        railway_tank['su_g0']=float(current_read[4])-float(current_read[2])
        railway_tank['su_g1']=float(current_read[6])-float(current_read[2])
        railway_tank['su_g2']=float(current_read[8])-float(current_read[2])
        railway_tank['su_g3']=float(current_read[10])-float(current_read[2])
        railway_tank['su_g4']=float(current_read[12])-float(current_read[2])

        msg=ard.write("fred9,4B09A0A3,dgin,4,snpw,23,htpw,32,itv,6000,otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        railway_tank['temp_h']=float(current_read[2])
        railway_tank['su_h0']=float(current_read[4])-float(current_read[2])
        railway_tank['su_h1']=float(current_read[6])-float(current_read[2])
        railway_tank['su_h2']=float(current_read[8])-float(current_read[2])
        railway_tank['su_h3']=float(current_read[10])-float(current_read[2])
        railway_tank['su_h4']=float(current_read[12])-float(current_read[2])




	ard.close()

        client.publish('v1/devices/me/telemetry', json.dumps(railway_tank), 1)
        upload_phant(pht_sensor,railway_tank,screen_display)
	print "uploaded"	

        if save_to_file: fid.write("\n\r")
        # sleep to the next loop
        time.sleep(sleep_time_seconds)


except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()

