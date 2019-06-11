#!/usr/bin/python
import serial
import time
import paho.mqtt.client as mqtt
import json
from phant import Phant
from upload_phant import upload_phant
from time import sleep,gmtime,localtime,strftime


with open('/home/pi/pyduino/credential/wwl2.json') as f:
        credential = json.load(f) #,object_pairs_hook=collections.OrderedDict)

#SDI_total = 20
#gs = 'gs', cs = 'cs'
#temp = 'temp', ec = 'ec', dp = 'dp'
#
#field_name = {'volt', 'dht22_rh','dht22_t')
#
#for i in range(0, SDI_total):
#       fiel_nae


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

field_name=['volt','dht22_rh','dht22_t','vis_1','vis_2','uv_1','uv_2','ir_1','ir_2']

wwl2=dict((el,0.0) for el in field_name)
#pht_sensor = Phant(publicKey=credential["public_wwl1"], fields=field_name ,privateKey=credential["private_wwl1"],baseUrl=credential["nectar_address"])

port_sensor  = '/dev/ttyS0'

# whether the result will be displayed on the screen
screen_display=True

# whether save the result as a file 
save_to_file=True

# the Filename of the csv file for storing file
file_name= 'wwl2.csv'

sleep_time_seconds=10*60
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
        wwl2['volt']=float(current_read[-1])
        #sleep(2)

#------enclosure------------------
        msg=ard.write("dht22,54,power,2,points,2,dummies,1,interval_mm,200,debug,1")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        wwl2['dht22_rh']=float(current_read[-1])
        wwl2['dht22_t']=float(current_read[-2])

#------UV sensors------------------
        msg=ard.write("9548,0,type,si1145,power,8,debug,1")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        wwl2['uv_1']=float(current_read[-1])
        wwl2['ir_1']=float(current_read[-3])
        wwl2['vis_1']=float(current_read[-5])

        msg=ard.write("9548,1,type,si1145,power,8,debug,1")
        msg=ard.flushInput()
        msg=ard.readline()

        if screen_display: print msg.rstrip()
        if save_to_file: fid.write(delimiter+msg)
        current_read=msg.split(',')[0:-1]
        wwl2['uv_2']=float(current_read[-1])
        wwl2['ir_2']=float(current_read[-3])
        wwl2['vis_2']=float(current_read[-5])



	ard.close()

	client.publish('v1/devices/me/telemetry', json.dumps(wwl2), 1)
	print "uploaded"
        if save_to_file: fid.write("\n\r")
        # sleep to the next loop
        time.sleep(sleep_time_seconds)


except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()

