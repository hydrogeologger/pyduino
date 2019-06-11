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


with open('/home/pi/pyduino/credential/wwl1.json') as f:
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
heat_time            = str(6000)
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

field_name=['volt','dht22_rh','dht22_t',
	    'gstemp_0','gstemp_1','gstemp_2','gstemp_3','gstemp_4',
	    'gstemp_5','gstemp_6','gstemp_7','gstemp_8','gstemp_9',
	    'gstemp_10','gstemp_11','gstemp_12','gstemp_13','gstemp_14',
	    'gstemp_15','gstemp_16','gstemp_17','gstemp_18','gstemp_19',
	    'gsec_0','gsec_1','gsec_2','gsec_3','gsec_4',
	    'gsec_5','gsec_6','gsec_7','gsec_8','gsec_9',
	    'gsec_10','gsec_11','gsec_12','gsec_13','gsec_14',
	    'gsec_15','gsec_16','gsec_17','gsec_18','gsec_19',
            'gsdp_0','gsdp_1','gsdp_2','gsdp_3','gsdp_4',
            'gsdp_5','gsdp_6','gsdp_7','gsdp_8','gsdp_9',
            'gsdp_10','gsdp_11','gsdp_12','gsdp_13','gsdp_14',
            'gsdp_15','gsdp_16','gsdp_17','gsdp_18','gsdp_19',
            'cstemp_a','cstemp_b','cstemp_c','cstemp_d','cstemp_e',
 	    'csec_a','csec_b','csec_c','csec_d','csec_e',
	    'csdp_a','csdp_b','csdp_c','csdp_d','csdp_e',
            'su_a0','su_a1','su_a2','su_a3','su_a4',
            'su_b0','su_b1','su_b2','su_b3','su_b4',
            'su_c0','su_c1','su_c2','su_c3','su_c4',
            'su_d0','su_d1','su_d2','su_d3','su_d4',
            'su_e0','su_e1','su_e2','su_e3','su_e4',
            'su_f0','su_f1','su_f2','su_f3','su_f4',
            'su_g0','su_g1','su_g2','su_g3','su_g4',
            'su_h0','su_h1','su_h2','su_h3','su_h4',
            'su_i0','su_i1','su_i2','su_i3','su_i4',
            'su_j0','su_j1','su_j2','su_j3','su_j4',
            'su_k0','su_k1','su_k2','su_k3','su_k4',
            'su_l0','su_l1','su_l2','su_l3','su_l4',
            'su_m0','su_m1','su_m2','su_m3','su_m4',
            'su_n0','su_n1','su_n2','su_n3','su_n4',
            'su_o0','su_o1','su_o2','su_o3','su_o4',
            'su_p0','su_p1','su_p2','su_p3','su_p4',
            'temp_a','temp_b','temp_c','temp_d','temp_e','temp_f','temp_g','temp_h','temp_i','temp_j',
	    'temp_k','temp_l','temp_m','temp_n','temp_o','temp_p'
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


wwl1=dict((el,0.0) for el in field_name)
pht_sensor = Phant(publicKey=credential["public_wwl1"], fields=field_name ,privateKey=credential["private_wwl1"],baseUrl=credential["nectar_address"])

port_sensor  = '/dev/ttyS0'

# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'wwl1.csv'

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

#------system voltage------------------
        msg=ard.write("analog,15,power,9,point,3,interval_mm,200,debug,1")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg.rstrip())
        current_read=msg.split(',')[0:-1]
        wwl1['volt0']=float(current_read[-1])
        #sleep(2)

#------enclosure------------------
        msg=ard.write("dht22,54,power,2,points,2,dummies,1,interval_mm,200,debug,1")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        wwl1['dht22_rh']=float(current_read[-1])
        wwl1['dht22_t']=float(current_read[-2])
        #sleep(2)

#------sdi12 (gs3&cs)------------------
        while True:
	    msg=ard.write("SDI-12,53,power,46,default_cmd,read,debug,1")
            msg=ard.flushInput()
            msg=ard.readline()
	    if len(msg.split('Addr')) is 5:
		print "HAVE 4 sensors"
		break
	    print "FAILED TO GET 4 sensors"
	    sleep(1)

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)

#	sensor_msg = msg.split('Addr')
#	for i in range(0,4)
#		sensor = msg[i]	
#		temp_field = look_up.get(sensor)[0]
#		ec_field = look_up.get(sensor)[1]
#		dp_field = look_up.get(sensor)[2]


#-------moisture sensors on channel 1---------------------
        sensor_1=msg.split('Addr')[-1]
	print sensor_1

        upload_1=sensor_1.split(',')[0:-1]
	
#	for i in range(1,len(sensor_msg)):
#            sensor = sensor_msg[i]
#            try:
#                temp_field = SDI12_LOOK_UP.get(sensor.split(',')[1])[0]
#                ec_field = SDI12_LOOK_UP.get(sensor.split(',')[1])[1]
#                dp_field = SDI12_LOOK_UP.get(sensor.split(',')[1])[2]
#                print(sensor)
#                print(temp_field)
#                print(ec_field)
#                print(dp_field)
#            except:
#            #if failed, we should read the msg again
#                break
#	exit()
        #sensor_name = split('Addr')[-1] #strip and split to get the name
        #name_field = look_up.get("D_cam",None) #list of strings for certain sensor_name
        #temp_filed = name_field[0]
        #ec_field = name_field[1]
        #dp_filed = name_file[2]
        #wwl1['temp_filed']=float(upload_1[-1])
        #wwl1['ec_field']=float(upload_1[-2])
        #wwl1['dp_filed']=float(upload_1[-3])
	try:

            wwl1['csdp_d']=float(upload_1[-3])
            wwl1['csec_d']=float(upload_1[-2])
            wwl1['cstemp_d']=float(upload_1[-1])

        except Exception, e:
            if screen_display: print 'cs_D does not get results'
	
        sensor_2=msg.split('Addr')[-2]
	print sensor_2
        upload_2=sensor_2.split(',')[0:-1]

        try:

            wwl1['csdp_b']=float(upload_2[-3])
            wwl1['csec_b']=float(upload_2[-2])
            wwl1['cstemp_b']=float(upload_2[-1])

        except Exception, e:
            if screen_display: print 'cs_B does not get results'

        sensor_3=msg.split('Addr')[-3]
	print sensor_3
        upload_3=sensor_3.split(',')[0:-1]

        wwl1['gsdp_2']=float(upload_3[-3])
        wwl1['gsec_2']=float(upload_3[-1])
        wwl1['gstemp_2']=float(upload_3[-2])

        sensor_4=msg.split('Addr')[-4]
	print sensor_4
        upload_4=sensor_4.split(',')[0:-1]

        wwl1['gsdp_1']=float(upload_4[-3])
        wwl1['gsec_1']=float(upload_4[-1])
        wwl1['gstemp_1']=float(upload_4[-2])

        #sleep(5)

#-------moisture sensors on channel 2---------------------
        msg=ard.write("SDI-12,52,power,47,default_cmd,read,debug,1")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        sensor_1=msg.split('Addr')[-1]
	print sensor_1
        upload_1=sensor_1.split(',')[0:-1]

        try:

            wwl1['csdp_c']=float(upload_1[-3])
            wwl1['csec_c']=float(upload_1[-2])
            wwl1['cstemp_c']=float(upload_1[-1])

        except Exception, e:
            if screen_display: print 'cs_C does not get results'

        sensor_2=msg.split('Addr')[-2]
	print sensor_2
        upload_2=sensor_2.split(',')[0:-1]

        try:

            wwl1['csdp_a']=float(upload_2[-3])
            wwl1['csec_a']=float(upload_2[-2])
            wwl1['cstemp_a']=float(upload_2[-1])

        except Exception, e:
            if screen_display: print 'cs_A does not get results'

        sensor_3=msg.split('Addr')[-3]
	print sensor_3
        upload_3=sensor_3.split(',')[0:-1]

        wwl1['gsdp_4']=float(upload_3[-3])
        wwl1['gsec_4']=float(upload_3[-1])
        wwl1['gstemp_4']=float(upload_3[-2])

        #sleep(5)

#-------moisture sensors on channel 4---------------------
        #msg=ard.write("SDI-12,50,power,49,default_cmd,read,debug,1")
        #msg=ard.flushInput()
        #msg=ard.readline()

        #if screen_display: print msg.rstrip()
        #if save_to_file: fid.write(delimiter+msg)
        #sensor_1=msg.split('Addr')[-1]
	#print sensor_1
        #upload_1=sensor_1.split(',')[0:-1]
        #try:

        #    wwl1['gsdp_0']=float(upload_1[-3])
        #    wwl1['gsec_0']=float(upload_1[-1])
        #    wwl1['gstemp_0']=float(upload_1[-2])

        #except Exception, e:
        #    if screen_display: print 'gs_0 does not get results'

        #sleep(5)

#-------moisture sensors on channel 3---------------------
        msg=ard.write("SDI-12,51,power,48,default_cmd,read,debug,1")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        sensor_1=msg.split('Addr')[-1]
	print sensor_1
        upload_1=sensor_1.split(',')[0:-1]

	try:

            wwl1['csdp_e']=float(upload_1[-3])
            wwl1['csec_e']=float(upload_1[-2])
            wwl1['cstemp_e']=float(upload_1[-1])

        except Exception, e:
            if screen_display: print 'cs_A does not get results'

        #sleep(5)

#------suction------------------
        msg=ard.write("fred,2D927F8E,dgin,18,snpw,27,htpw,22,itv," + heat_time + ",otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        wwl1['temp_a']=float(current_read[2])
        wwl1['su_a0']=float(current_read[4])-float(current_read[2])
        wwl1['su_a1']=float(current_read[6])-float(current_read[2])
        wwl1['su_a2']=float(current_read[8])-float(current_read[2])
        wwl1['su_a3']=float(current_read[10])-float(current_read[2])
        wwl1['su_a4']=float(current_read[12])-float(current_read[2])
        #sleep(2)

        msg=ard.write("fred,A19C7FBB,dgin,18,snpw,27,htpw,23,itv," + heat_time + ",otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        wwl1['temp_b']=float(current_read[2])
        wwl1['su_b0']=float(current_read[4])-float(current_read[2])
        wwl1['su_b1']=float(current_read[6])-float(current_read[2])
        wwl1['su_b2']=float(current_read[8])-float(current_read[2])
        wwl1['su_b3']=float(current_read[10])-float(current_read[2])
        wwl1['su_b4']=float(current_read[12])-float(current_read[2])
        #sleep(2)

        msg=ard.write("fred,069D7FAF,dgin,18,snpw,27,htpw,24,itv," + heat_time + ",otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        wwl1['temp_c']=float(current_read[2])
        wwl1['su_c0']=float(current_read[4])-float(current_read[2])
        wwl1['su_c1']=float(current_read[6])-float(current_read[2])
        wwl1['su_c2']=float(current_read[8])-float(current_read[2])
        wwl1['su_c3']=float(current_read[10])-float(current_read[2])
        wwl1['su_c4']=float(current_read[12])-float(current_read[2])

        #sleep(2)

        msg=ard.write("fred,936A7F02,dgin,18,snpw,27,htpw,25,itv," + heat_time + ",otno,5")
        msg=ard.flushInput()
        msg=ard.readline()
        
        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        wwl1['temp_d']=float(current_read[2])
        wwl1['su_d0']=float(current_read[4])-float(current_read[2])
        wwl1['su_d1']=float(current_read[6])-float(current_read[2])
        wwl1['su_d2']=float(current_read[8])-float(current_read[2])
        wwl1['su_d3']=float(current_read[10])-float(current_read[2])
        wwl1['su_d4']=float(current_read[12])-float(current_read[2])

        #sleep(2)

        msg=ard.write("fred,1F7F7F3B,dgin,18,snpw,27,htpw,26,itv," + heat_time + ",otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        wwl1['temp_e']=float(current_read[2])
        wwl1['su_e0']=float(current_read[4])-float(current_read[2])
        wwl1['su_e1']=float(current_read[6])-float(current_read[2])
        wwl1['su_e2']=float(current_read[8])-float(current_read[2])
        wwl1['su_e3']=float(current_read[10])-float(current_read[2])
        wwl1['su_e4']=float(current_read[12])-float(current_read[2])
        sleep(2)

        msg=ard.write("fred,AB6A7F4E,dgin,17,snpw,33,htpw,28,itv," + heat_time + ",otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        wwl1['temp_f']=float(current_read[2])
        wwl1['su_f0']=float(current_read[4])-float(current_read[2])
        wwl1['su_f1']=float(current_read[6])-float(current_read[2])
        wwl1['su_f2']=float(current_read[8])-float(current_read[2])
        wwl1['su_f3']=float(current_read[10])-float(current_read[2])
        wwl1['su_f4']=float(current_read[12])-float(current_read[2])
	#sleep(2)

        msg=ard.write("fred,2B7F7F0A,dgin,17,snpw,33,htpw,29,itv," + heat_time + ",otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        wwl1['temp_g']=float(current_read[2])
        wwl1['su_g0']=float(current_read[4])-float(current_read[2])
        wwl1['su_g1']=float(current_read[6])-float(current_read[2])
        wwl1['su_g2']=float(current_read[8])-float(current_read[2])
        wwl1['su_g3']=float(current_read[10])-float(current_read[2])
        wwl1['su_g4']=float(current_read[12])-float(current_read[2])
        #sleep(2)

        msg=ard.write("fred,AE9C7F9F,dgin,17,snpw,33,htpw,30,itv," + heat_time + ",otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        wwl1['temp_h']=float(current_read[2])
        wwl1['su_h0']=float(current_read[4])-float(current_read[2])
        wwl1['su_h1']=float(current_read[6])-float(current_read[2])
        wwl1['su_h2']=float(current_read[8])-float(current_read[2])
        wwl1['su_h3']=float(current_read[10])-float(current_read[2])
        wwl1['su_h4']=float(current_read[12])-float(current_read[2])

        #sleep(2)

        msg=ard.write("fred,9F6A7F7F,dgin,17,snpw,33,htpw,31,itv," + heat_time + ",otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        wwl1['temp_i']=float(current_read[2])
        wwl1['su_i0']=float(current_read[4])-float(current_read[2])
        wwl1['su_i1']=float(current_read[6])-float(current_read[2])
        wwl1['su_i2']=float(current_read[8])-float(current_read[2])
        wwl1['su_i3']=float(current_read[10])-float(current_read[2])
        wwl1['su_i4']=float(current_read[12])-float(current_read[2])
        #sleep(2)

        msg=ard.write("fred,2E927FD7,dgin,17,snpw,33,htpw,32,itv," + heat_time + ",otno,5")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        wwl1['temp_j']=float(current_read[2])
        wwl1['su_j0']=float(current_read[4])-float(current_read[2])
        wwl1['su_j1']=float(current_read[6])-float(current_read[2])
        wwl1['su_j2']=float(current_read[8])-float(current_read[2])
        wwl1['su_j3']=float(current_read[10])-float(current_read[2])
        wwl1['su_j4']=float(current_read[12])-float(current_read[2])

        #sleep(2)

	ard.close()

        client.publish('v1/devices/me/telemetry', json.dumps(wwl1), 1)
        #upload_phant(pht_sensor,wwl1,screen_display)
	print "uploaded"	

        if save_to_file: fid.write("\n\r")
        # sleep to the next loop
        time.sleep(sleep_time_seconds)


except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()

