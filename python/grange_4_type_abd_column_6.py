#!/usr/bin/python
import serial
import time
import numpy as np
import sys
# from phant import Phant
# import serial_openlock
# import get_ip
# from upload_phant import upload_phant
import paho.mqtt.client as mqtt
import json
import RPi.GPIO as GPIO            # import RPi.GPIO module
# from time import sleep, gmtime, strftime             # lets us have a delay
from time import sleep
import sys
# Append private python library to system path
sys.path.append("/home/pi/pyduino/python/lib")
import mqtthelper # MQTT helper module for publishing archive
# import subprocess
#GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD
#GPIO.setup(25, GPIO.OUT)           # set GPIO24 as an output
#GPIO.setup(26, GPIO.OUT)           # set GPIO24 as an output
#GPIO.setup(24, GPIO.OUT)           # set GPIO24 as an output


#with open('/home/pi/script/pass/public_grange_4_moisture_suction', 'r') as myfile:
#    public_grange4_moisture_suction=myfile.read().replace('\n', '')
#
#with open('/home/pi/script/pass/private_grange_4_moisture_suction', 'r') as myfile:
#    private_grange4_moisture_suction=myfile.read().replace('\n', '')
#
#with open('/home/pi/script/pass/public_grange_4_luo2_dry', 'r') as myfile:
#    public_grange_4_luo2_dry=myfile.read().replace('\n', '')
#
#with open('/home/pi/script/pass/private_grange_4_luo2_dry', 'r') as myfile:
#    private_grange_4_luo2_dry=myfile.read().replace('\n', '')
#
#with open('/home/pi/script/pass/public_grange_4_luo2_wet', 'r') as myfile:
#    public_grange_4_luo2_wet=myfile.read().replace('\n', '')
#
#with open('/home/pi/script/pass/private_grange_4_luo2_wet', 'r') as myfile:
#    private_grange_4_luo2_wet=myfile.read().replace('\n', '')
#
#
#with open('/home/pi/script/pass/nectar_address', 'r') as myfile:
#    nectar_address=myfile.read().replace('\n', '')

with open('/home/pi/pyduino/credential/grange_4.json') as f:
    credential = json.load(f) #,object_pairs_hook=collections.OrderedDict)


#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['mo0','mo1','mo2','mo3','mo4','mo5','mo6','mo7',
            'su0','su1','su2','su3','su4','su5','su6','su7',
            'tmp0','tmp1','tmp2','tmp3','tmp4','tmp5','tmp6','tmp7',
            'dluo7','dlupe7','dlup7',
            'wluo7','wlupe7','wlup7'
            ]
grange_4_mo_su=dict((el,0.0) for el in field_name)
# Following upload is deprecated
# pht_grange_4_mo_su = Phant(publicKey=credential["public_grange_4_moisture_suction"], fields=field_name ,privateKey=credential["private_grange_4_moisture_suction"],baseUrl=credential["nectar_address"])



#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['dluo0','dlupe0','dlut0','dlup0',
            'dluo1','dlupe1','dlut1','dlup1',
            'dluo2','dlupe2','dlut2','dlup2',
            'dluo3','dlupe3','dlut3','dlup3',
            'dluo4','dlupe4','dlut4','dlup4',
            'dluo5','dlupe5','dlut5','dlup5',
            'dluo6','dlupe6','dlut6','dlup6',
            'rh','temp']
grange_4_luo2_dry=dict((el,0.0) for el in field_name)
# Following upload is deprecated
# pht_grange_4_luo2_dry= Phant(publicKey=credential["public_grange_4_luo2_dry"], fields=field_name ,privateKey=credential["private_grange_4_luo2_dry"],baseUrl=credential["nectar_address"])


#------------------------- below are definations for the sensors in the column ---------------------------------
field_name=['wluo0','wlupe0','wlut0','wlup0',
            'wluo1','wlupe1','wlut1','wlup1',
            'wluo2','wlupe2','wlut2','wlup2',
            'wluo3','wlupe3','wlut3','wlup3',
            'wluo4','wlupe4','wlut4','wlup4',
            'wluo5','wlupe5','wlut5','wlup5',
            'wluo6','wlupe6','wlut6','wlup6',
            'flow','tmp']
grange_4_luo2_wet=dict((el,0.0) for el in field_name)
# pht_grange_4_luo2_wet= Phant(publicKey=credential["public_grange_4_luo2_wet"], fields=field_name ,privateKey=credential["private_grange_4_luo2_wet"],baseUrl=credential["nectar_address"])


#------------------------- below are definations for the VAISALA weather station ---------------------------------
#field_name = ['wind_direction','wind_speed','atm_temp','atm_humdity',
#            'atm_pressure','rain_gauge','rain_duration','heat_temp',
#            'heat_volt']
#grange_4_vaisala = dict((el,0.0) for el in field_name)
# pht_grange_4_vaisala = Phant(publicKey=credential["public_grange_4_vaisala"], fields=field_name ,privateKey=credential["private_grange_4_vaisala"],baseUrl=credential["nectar_address"])


#port_sensor  = 'USB VID:PID=2341:0042 SNR=5573631383735150B0E0'
#port_sensor  = 'USB VID:PID=2341:0042 SNR=55639303035351C07261'  #grange 3

#port_sensor  = 'USB VID:PID=2341:0042 SNR=5563231363835151C1B1'  #grange 4
port_sensor  = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_5563231363835151C1B1-if00'
# whether the result will be displayed on the screen
SCREEN_DISPLAY=True

# Wheter to display extra debugging information
DEBUG = False

# whether save the result as a file
SAVE_TO_FILE=True

# Wheter to publish to thingsboard, used during testing
PUBLISH_TO_THINGSBOARD = True

# wheter to enable Vaisala Weather station monitoring
ENABLE_VAISALA = False

# the Filename of the csv file for storing file
file_name= 'grange_4_type_abd_c1b1.csv'

sleep_time_seconds=10*60

# the delimiter between files, it is prefered to use ',' which is standard for csv file
delimiter=','

__author__ = 'chenming'


if SAVE_TO_FILE: fid= open(file_name,'a',0)

try:
    if PUBLISH_TO_THINGSBOARD:
        next_reading = time.time()
        client = mqtt.Client()
        client.username_pw_set(credential['access_token'])
        client.connect(credential['thingsboard_host'], 1883, 60)
        client.loop_start()
except Exception, e:
    print("Error: Initialize client connection to primary thingsboard")
    # time.sleep(60)

try:
    if PUBLISH_TO_THINGSBOARD:
        next_reading = time.time()
        client_vaisala = mqtt.Client()
        client_vaisala.username_pw_set(credential['access_token_vaisala'])
        client_vaisala.connect(credential['thingsboard_host'], 1883, 60)
        client_vaisala.loop_start()
except Exception, e:
    print("Error: Initialize client connection to vaisala thingsboard")
    # time.sleep(60)

sensor_measure_idx = 1


try:
    ard = serial.Serial(port_sensor,timeout=60)
    time.sleep(3)

    if ENABLE_VAISALA:
        # Turn on power for vaisala at start
        ard.flushInput()
        ard.write("power_switch,49,power_switch_status,1")
        sleep(1)
        msg=ard.readline()
        if SCREEN_DISPLAY:
            print(msg)
        if SAVE_TO_FILE:
            fid.write(msg)


    while True:
        time_now = time.time()
        milliseconds_since_epoch = int(round(time_now * 1000))
        utc_time = time.gmtime(time_now)
        time_now_utc_str = time.strftime("%Y-%m-%d %H:%M:%S", utc_time)

        if SCREEN_DISPLAY:
            print(time_now_utc_str)
            # print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        if SAVE_TO_FILE:
            fid.write(time_now_utc_str)
            # fid.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())  )

        grange_4_vaisala={}
        # ------------------------------- below goes to electrochem_o2  --------------------------------------------
        # ds18b20_search,50,power,44
        #CM210421
        #msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,46AB9657,dgin,50,snpw,44,htpw,32,itv,12000,otno,5",initialize=False)
        #if SCREEN_DISPLAY: print msg.rstrip()
        #if SAVE_TO_FILE: fid.write(delimiter+msg)
        #current_read=msg.split(',')[0:-1]
        #grange_4_mo_su['tmp0']=float(current_read[2])
        #grange_4_mo_su['su0']=float(current_read[7])-float(current_read[2])
        #
        #
        #
        ##msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,E703BA53,dgin,50,snpw,42,htpw,37,itv,1000,otno,5",initialize=False)
        ##msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,E703BA53,dgin,50,snpw,44,htpw,30,itv,12000,otno,5",initialize=False)
        ##if SCREEN_DISPLAY: print strftime("%Y-%m-%d %H:%M:%S", gmtime())+msg.rstrip()
        ##if SAVE_TO_FILE: fid.write(delimiter+msg)
        ##current_read=msg.split(',')[0:-1]
        ##grange_4_mo_su['tmp1']=float(current_read[2])
        ##grange_4_mo_su['su1']=float(current_read[7])-float(current_read[2])
        #
        #
        ##msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,B07E380C,dgin,50,snpw,42,htpw,39,itv,12000,otno,5",initialize=False)
        #msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred9,B07E380C,dgin,50,snpw,44,htpw,28,itv,12000,otno,5",initialize=False)
        #if SCREEN_DISPLAY: print msg.rstrip()
        #if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
        #current_read=msg.split(',')[0:-1]
        #grange_4_mo_su['tmp2']=float(current_read[2])
        #grange_4_mo_su['su2']=float(current_read[7])-float(current_read[2])

        ##msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,C859BAE9,dgin,50,snpw,42,htpw,41,itv,1000,otno,5",initialize=False)
        #msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,C859BAE9,dgin,50,snpw,44,htpw,26,itv,12000,otno,5",initialize=False)
        #if SCREEN_DISPLAY: print msg.rstrip()
        #if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
        #current_read=msg.split(',')[0:-1]
        #grange_4_mo_su['tmp3']=float(current_read[2])
        #grange_4_mo_su['su3']=float(current_read[7])-float(current_read[2])
        #
        ##msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,A05E96B8,dgin,50,snpw,42,htpw,27,itv,1000,otno,5",initialize=False)
        #msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,A05E96B8,dgin,50,snpw,44,htpw,40,itv,12000,otno,5",initialize=False)
        #if SCREEN_DISPLAY: print msg.rstrip()
        #if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
        #current_read=msg.split(',')[0:-1]
        #grange_4_mo_su['tmp4']=float(current_read[2])
        #grange_4_mo_su['su4']=float(current_read[7])-float(current_read[2])
        #
        #
        ##msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,F8BABB1F,dgin,50,snpw,42,htpw,29,itv,1000,otno,5",initialize=False)
        #msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,F8BABB1F,dgin,50,snpw,44,htpw,38,itv,12000,otno,5",initialize=False)
        #if SCREEN_DISPLAY: print msg.rstrip()
        #if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
        #current_read=msg.split(',')[0:-1]
        #grange_4_mo_su['tmp5']=float(current_read[2])
        #grange_4_mo_su['su5']=float(current_read[7])-float(current_read[2])
        #
        #
        ##msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,D936BCF2,dgin,50,snpw,42,htpw,31,itv,1000,otno,5",initialize=False)
        #msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,D936BCF2,dgin,50,snpw,44,htpw,36,itv,12000,otno,5",initialize=False)
        #if SCREEN_DISPLAY: print msg.rstrip()
        #if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
        #current_read=msg.split(',')[0:-1]
        #grange_4_mo_su['tmp6']=float(current_read[2])
        #grange_4_mo_su['su6']=float(current_read[7])-float(current_read[2])
        #
        #
        ##msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,A333B9F6,dgin,50,snpw,42,htpw,33,itv,1000,otno,5",initialize=False)
        #msg=serial_openlock.get_result_by_input(port=port_sensor,command="fred,A333B9F6,dgin,50,snpw,44,htpw,34,itv,12000,otno,5",initialize=False)
        #if SCREEN_DISPLAY: print msg.rstrip()
        #if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
        #current_read=msg.split(',')[0:-1]
        #grange_4_mo_su['tmp7']=float(current_read[2])
        #grange_4_mo_su['su7']=float(current_read[7])-float(current_read[2])

        # Only perform the following section every 4th cycle
        if np.mod(sensor_measure_idx, 3) == 0:
            sleep(2)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,0,power,42,point,3,interval_mm,200,debug,0",initialize=False)
            ard.write("analog,0,power,42,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.rstrip()
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(',')[0:-1]
            grange_4_mo_su['mo0']=float(current_read[2])

            sleep(2)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,1,power,42,point,3,interval_mm,200,debug,0",initialize=False)
            ard.write("analog,1,power,42,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()

            if SCREEN_DISPLAY: print msg.rstrip()
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(',')[0:-1]
            grange_4_mo_su['mo1']=float(current_read[2])


            sleep(2)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,2,power,42,point,3,interval_mm,200,debug,0",initialize=False)
            ard.write("analog,2,power,42,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.rstrip()
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(',')[0:-1]
            grange_4_mo_su['mo2']=float(current_read[2])


            sleep(2)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,3,power,42,point,3,interval_mm,200,debug,0",initialize=False)
            ard.write("analog,3,power,42,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.rstrip()
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(',')[0:-1]
            grange_4_mo_su['mo3']=float(current_read[2])


            sleep(2)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,4,power,42,point,3,interval_mm,200,debug,0",initialize=False)
            ard.write("analog,4,power,42,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()

            if SCREEN_DISPLAY: print msg.rstrip()
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(',')[0:-1]
            grange_4_mo_su['mo4']=float(current_read[2])


            sleep(2)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,5,power,42,point,3,interval_mm,200,debug,0",initialize=False)
            ard.write("analog,5,power,42,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.rstrip()
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(',')[0:-1]
            grange_4_mo_su['mo5']=float(current_read[2])


            sleep(2)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,6,power,42,point,3,interval_mm,200,debug,0",initialize=False)
            ard.write("analog,6,power,42,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.rstrip()
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(',')[0:-1]
            grange_4_mo_su['mo6']=float(current_read[2])


            sleep(2)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="analog,7,power,42,point,3,interval_mm,200,debug,0",initialize=False)
            ard.write("analog,7,power,42,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.rstrip()
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(',')[0:-1]
            grange_4_mo_su['mo7']=float(current_read[2])


            #sleep(5)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,33,serial,3",initialize=False)
            #if SCREEN_DISPLAY: print msg.replace('\r','')
            #if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            #current_read=msg.split(' ')[0:-1]
            # the following lines are commented as it is no longer functional on 180827
            #grange_4_mo_su['dluo7'] = float(current_read[-2])
            #grange_4_mo_su['dlupe7'] = float(current_read[-4])
            ##grange_4_luo2_dry['dlut0'] = float(current_read[-6])
            #grange_4_mo_su['dlup7'] = float(current_read[-8])

            #to 200714
            #sleep(5)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,6,serial,2",initialize=False)
            #if SCREEN_DISPLAY: print msg.replace('\r','')
            #if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            #current_read=msg.split(' ')[0:-1]
            #grange_4_mo_su['wluo7'] = float(current_read[-2])
            #grange_4_mo_su['wlupe7'] = float(current_read[-4])
            ###grange_4_luo2_dry['wlut7'] = float(current_read[-6])
            #grange_4_mo_su['wlup7'] = float(current_read[-8])

            # publish all together
            # if PUBLISH_TO_THINGSBOARD:
            #     client.publish('v1/devices/me/telemetry', json.dumps(grange_4_mo_su), 1)
            # Following upload is deprecated
            # upload_phant(pht_grange_4_mo_su,grange_4_mo_su,SCREEN_DISPLAY)


            sleep(5)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,24,serial,1",initialize=False)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,35,serial,3",initialize=False)
            ard.write("lumino2,A,power,35,serial,3")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.replace('\r','')
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(' ')[0:-1]
            try:
                grange_4_luo2_dry['dluo0'] = float(current_read[-2])
                grange_4_luo2_dry['dlupe0'] = float(current_read[-4])
                grange_4_luo2_dry['dlut0'] = float(current_read[-6])
                grange_4_luo2_dry['dlup0'] = float(current_read[-8])
            except Exception as error:
                print(error)
                print("lumino2,A,power,35,serial,3 reading failed")


            sleep(5)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,24,serial,2",initialize=False)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,37,serial,3",initialize=False)
            ard.write("lumino2,A,power,37,serial,3")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.replace('\r','')
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(' ')[0:-1]
            try:
                grange_4_luo2_dry[ 'dluo1'] = float(current_read[-2])
                grange_4_luo2_dry['dlupe1'] = float(current_read[-4])
                grange_4_luo2_dry[ 'dlut1'] = float(current_read[-6])
                grange_4_luo2_dry[ 'dlup1'] = float(current_read[-8])
            except Exception as error:
                print(error)
                print("lumino2,A,power,37,serial,3 reading failed")


            sleep(5)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,24,serial,3",initialize=False)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,39,serial,3",initialize=False)
            ard.write("lumino2,A,power,39,serial,3")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.replace('\r','')
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(' ')[0:-1]
            try:
                grange_4_luo2_dry[ 'dluo2'] = float(current_read[-2])
                grange_4_luo2_dry['dlupe2'] = float(current_read[-4])
                grange_4_luo2_dry[ 'dlut2'] = float(current_read[-6])
                grange_4_luo2_dry[ 'dlup2'] = float(current_read[-8])
            except Exception as error:
                print(error)
                print("lumino2,A,power,39,serial,3 reading failed")


            sleep(5)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,41,serial,3",initialize=False)
            ard.write("lumino2,A,power,41,serial,3")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.replace('\r','')
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(' ')[0:-1]
            try:
                grange_4_luo2_dry[ 'dluo3'] = float(current_read[-2])
                grange_4_luo2_dry['dlupe3'] = float(current_read[-4])
                grange_4_luo2_dry[ 'dlut3'] = float(current_read[-6])
                grange_4_luo2_dry[ 'dlup3'] = float(current_read[-8])
            except Exception as error:
                print(error)
                print("lumino2,A,power,41,serial,3 reading failed")



            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,22,serial,2",initialize=False)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,27,serial,3",initialize=False)
            ard.write("lumino2,A,power,27,serial,3")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.replace('\r','')
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(' ')[0:-1]
            try:
                grange_4_luo2_dry[ 'dluo4'] = float(current_read[-2])
                grange_4_luo2_dry['dlupe4'] = float(current_read[-4])
                grange_4_luo2_dry[ 'dlut4'] = float(current_read[-6])
                grange_4_luo2_dry[ 'dlup4'] = float(current_read[-8])
            except Exception as error:
                print(error)
                if SCREEN_DISPLAY: print('  lumino2,A,power,27,serial,3 ,does not get results')



            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,29,serial,3",initialize=False)
            ard.write("lumino2,A,power,29,serial,3")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.replace('\r','')
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(' ')[0:-1]
            try:
                grange_4_luo2_dry[ 'dluo5'] = float(current_read[-2])
                grange_4_luo2_dry['dlupe5'] = float(current_read[-4])
                grange_4_luo2_dry[ 'dlut5'] = float(current_read[-6])
                grange_4_luo2_dry[ 'dlup5'] = float(current_read[-8])
            except Exception as error:
                print(error)
                print("lumino2,A,power,29,serial,3 reading failed")


            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,23,serial,1",initialize=False)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,31,serial,3",initialize=False)
            ard.write("lumino2,A,power,31,serial,3")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.replace('\r','')
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(' ')[0:-1]
            try:
                grange_4_luo2_dry[ 'dluo6'] = float(current_read[-2])
                grange_4_luo2_dry['dlupe6'] = float(current_read[-4])
                grange_4_luo2_dry[ 'dlut6'] = float(current_read[-6])
                grange_4_luo2_dry[ 'dlup6'] = float(current_read[-8])
            except Exception as error:
                print(error)
                print("lumino2,A,power,31,serial,3 reading failed")

            # enclosure temperature and humidity
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="dht22,10,power,48,points,2,dummies,1,interval_mm,2000,debug,0",initialize=False)
            ard.write("dht22,10,power,48,points,2,dummies,1,interval_mm,2000,debug,0")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.rstrip()
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(',')[0:-1]
            grange_4_luo2_dry['rh']=float(current_read[-1])
            grange_4_luo2_dry['temp']=float(current_read[-2])

            # publish later all together
            # if PUBLISH_TO_THINGSBOARD:
            #     client.publish('v1/devices/me/telemetry', json.dumps(grange_4_luo2_dry), 1)
            # Following upload is deprecated
            # upload_phant(pht_grange_4_luo2_dry,grange_4_luo2_dry,SCREEN_DISPLAY)


            sleep(5)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,24,serial,2",initialize=False)
            ard.write("lumino2,A,power,24,serial,2")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.replace('\r','')
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            current_read=msg.split(' ')[0:-1]
            try:
                grange_4_luo2_wet[ 'wluo0'] = float(current_read[-2])
                grange_4_luo2_wet['wlupe0'] = float(current_read[-4])
                grange_4_luo2_wet[ 'wlut0'] = float(current_read[-6])
                grange_4_luo2_wet[ 'wlup0'] = float(current_read[-8])
            except Exception as error:
                print(error)
                print("lumino2,A,power,24,serial,2 reading failed")


            sleep(5)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,22,serial,2",initialize=False)
            ard.write("lumino2,A,power,22,serial,2")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.replace('\r','')
            if SCREEN_DISPLAY: print msg.rstrip()
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            try:
                current_read=msg.split(' ')[0:-1]
                grange_4_luo2_wet[ 'wluo1'] = float(current_read[-2])
                grange_4_luo2_wet['wlupe1'] = float(current_read[-4])
                grange_4_luo2_wet[ 'wlut1'] = float(current_read[-6])
                grange_4_luo2_wet[ 'wlup1'] = float(current_read[-8])
            except Exception as error:
                print(error)
                print("lumino2,A,power,22,serial,2 reading failed")



            sleep(5)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,23,serial,2",initialize=False)
            ard.write("lumino2,A,power,23,serial,2")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.replace('\r','')
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            try:
                current_read=msg.split(' ')[0:-1]
                grange_4_luo2_wet[ 'wluo2'] = float(current_read[-2])
                grange_4_luo2_wet['wlupe2'] = float(current_read[-4])
                grange_4_luo2_wet[ 'wlut2'] = float(current_read[-6])
                grange_4_luo2_wet[ 'wlup2'] = float(current_read[-8])
            except Exception as error:
                print(error)
                print("lumino2,A,power,23,serial,2 reading failed")


            sleep(5)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,25,serial,2",initialize=False)
            ard.write("lumino2,A,power,25,serial,2")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.replace('\r','')
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            try:
                current_read=msg.split(' ')[0:-1]
                #grange_4_luo2_wet[ 'wluo3'] = float(current_read[-2])
                #grange_4_luo2_wet['wlupe3'] = float(current_read[-4])
                #grange_4_luo2_wet[ 'wlut3'] = float(current_read[-6])
                #grange_4_luo2_wet[ 'wlup3'] = float(current_read[-8])
            except Exception as error:
                print(error)
                print("lumino2,A,power,25,serial,2 reading failed")

            sleep(5)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,9,serial,2",initialize=False)
            ard.write("lumino2,A,power,9,serial,2")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.replace('\r','')
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            try:
                current_read=msg.split(' ')[0:-1]
                grange_4_luo2_wet[ 'wluo4'] = float(current_read[-2])
                grange_4_luo2_wet['wlupe4'] = float(current_read[-4])
                grange_4_luo2_wet[ 'wlut4'] = float(current_read[-6])
                grange_4_luo2_wet[ 'wlup4'] = float(current_read[-8])
            except Exception as error:
                print(error)
                print("lumino2,A,power,9,serial,2 reading failed")


            sleep(5)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,8,serial,2",initialize=False)
            ard.write("lumino2,A,power,8,serial,2")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.replace('\r','')
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            try:
                current_read=msg.split(' ')[0:-1]
                grange_4_luo2_wet[ 'wluo5'] = float(current_read[-2])
                grange_4_luo2_wet['wlupe5'] = float(current_read[-4])
                grange_4_luo2_wet[ 'wlut5'] = float(current_read[-6])
                grange_4_luo2_wet[ 'wlup5'] = float(current_read[-8])
            except Exception as error:
                print(error)
                print("lumino2,A,power,8,serial,2 reading failed")

            sleep(5)
            #msg=serial_openlock.get_result_by_input(port=port_sensor,command="lumino2,A,power,7,serial,2",initialize=False)
            ard.write("lumino2,A,power,7,serial,2")
            ard.flushInput()
            sleep(1)
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.replace('\r','')
            if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
            try:
                current_read=msg.split(' ')[0:-1]
                grange_4_luo2_wet[ 'wluo6'] = float(current_read[-2])
                grange_4_luo2_wet['wlupe6'] = float(current_read[-4])
                grange_4_luo2_wet[ 'wlut6'] = float(current_read[-6])
                grange_4_luo2_wet[ 'wlup6'] = float(current_read[-8])
            except Exception as error:
                print(error)
                print("lumino2,A,power,7,serial,2 reading failed")

            if PUBLISH_TO_THINGSBOARD:
                # client.publish('v1/devices/me/telemetry', json.dumps(grange_4_luo2_wet), 1)
                # [grange_4_mo_su, grange_4_luo2_dry, grange_4_luo2_wet]
                data_collected = grange_4_mo_su.copy()
                data_collected.update(grange_4_luo2_dry)
                data_collected.update(grange_4_luo2_wet)
                publish_result = mqtthelper.publish_to_thingsboard(client,
                        payload=data_collected,
                        ts=milliseconds_since_epoch, timeout=1.0,
                        filename="grange_4_type_abd_column_6_mqttqueue.json", display_payload=True, debug=False)
                data_collected.clear()
                if SCREEN_DISPLAY:
                    print(publish_result) # Display the last publish result
            # Following upload is deprecated
            # upload_phant(pht_grange_4_luo2_wet,grange_4_luo2_wet,SCREEN_DISPLAY)



        #GPIO.output(25, 1)         # set GPIO24 to 1/GPIO.HIGH/True
        #sleep(5)
        #GPIO.output(26, 1)         # set GPIO24 to 1/GPIO.HIGH/True
        #sleep(5)

        #GPIO.output(24, 1)         # set GPIO24 to 1/GPIO.HIGH/True
        #sleep(1)
        #GPIO.output(24, 0)         # set GPIO24 to 1/GPIO.HIGH/True
        #sleep(2)
        #
        #
        #GPIO.output(24, 1)         # set GPIO24 to 1/GPIO.HIGH/True
        #sleep(1)
        #GPIO.output(24, 0)         # set GPIO24 to 1/GPIO.HIGH/True

        #sleep(2)

        #### below is for pressure
        #GPIO.output(25, 0)         # set GPIO24 to 1/GPIO.HIGH/True
        #sleep(5)
        #GPIO.output(26, 0)         # set GPIO24 to 1/GPIO.HIGH/True
        #sleep(5)


        #sleep(2)
        #
        #sleep(2)

        #================================================================================= #
        # VAISALA TRANSMITTER VIA SDI-12 - OK
        #================================================================================= #
        #---------------------- below are definations for the sensors in the column ---------------------------------
        # if ENABLE_VAISALA:
        #     VAISALA_ADDRESS = "V"
        #     try:
        #         ard.flushInput()
        #         ard.write("12,51,custom_cmd,VM!,debug,1")
        #         msg = ard.readline()
        #         if SCREEN_DISPLAY:
        #             print(msg.strip())

        #         current_read = msg.split(",")[-2]
        #         if DEBUG:
        #             print(current_read)
        #     except Exception as error:
        #         # print(msg.strip())
        #         print("Vaisala get measurement error")
        #         print(type(error))
        #         print(error)

        #     # Reset rain counter
        #     time.sleep(1) # Give a little break between data request
        #     ard.flushInput()
        #     ard.write("12,51,custom_cmd,VXZRU!,debug,1")
        #     msg = ard.readline()
        #     if SCREEN_DISPLAY:
        #         print(msg.rstrip())

        #     # strip sensor address prefix
        #     try:
        #         if current_read[0] == VAISALA_ADDRESS:
        #             vaisala_values = current_read[1:]
        #     except IndexError:
        #         pass
        #     # Delimit vaisala values with commas ","
        #     for delim_sign in "+-":
        #         try:
        #             # vaisala_values = vaisala_values[0] + vaisala_values[1:].replace(delim_sign, "," + delim_sign)
        #             vaisala_values = "".join([vaisala_values[0],
        #                     vaisala_values[1:].replace(delim_sign, "".join([",", delim_sign]))])
        #         except IndexError:
        #             pass
        #     if DEBUG:
        #         print(vaisala_values)
            
        #     if SAVE_TO_FILE:
        #         fid.write("\nVaisala" + delimiter + vaisala_values[1:])

        #     # Order of vaisala messages, all
        #         # Wind (M1): Dn Dm Dx Sn Sm Sx
        #         # PTU (M2): Ta Tp Ua Pa
        #         # Rain (M3): Rc Rd Ri Hc Hd Hi Rp Hp
        #         # Supv (M5): Th Vh Vs Vr Id
        #         # Comp (M): Wind PTU Rain Supv (parameters in above order)

        #     # Parsing vaisala data
        #     # Expecting: WindDir(Dm) WindSpd(Sm) AirTemp(Ta) Humidity(Ua)
        #     #            AirPress(Pa) RainAmt(Rc) RainDur(Rd) SupplyVolt(Vs)
        #     current_read = vaisala_values.split(',')
        #     if DEBUG:
        #         print(current_read)
            
        #     # Parse the data
        #     try:
        #         try:
        #             grange_4_vaisala['wind_direction'] = float(current_read[0])
        #         except ValueError:
        #             pass
        #         try:
        #             grange_4_vaisala['wind_speed'] = float(current_read[1])
        #         except ValueError:
        #             pass
        #         try:
        #             grange_4_vaisala['atm_temp'] = float(current_read[2])
        #         except ValueError:
        #             pass
        #         try:
        #             grange_4_vaisala['atm_humdity'] = float(current_read[3])
        #         except ValueError:
        #             pass
        #         try:
        #             grange_4_vaisala['atm_pressure'] = float(current_read[4])
        #         except ValueError:
        #             pass
        #         try:
        #             grange_4_vaisala['rain_gauge'] = float(current_read[5])
        #         except ValueError:
        #             pass
        #         try:
        #             grange_4_vaisala['rain_duration'] = float(current_read[6])
        #         except ValueError:
        #             pass
        #         try:
        #             grange_4_vaisala['heat_temp'] = float(current_read[7])
        #         except ValueError:
        #             pass
        #         try:
        #             grange_4_vaisala['heat_volt'] = float(current_read[8])
        #         except ValueError:
        #             pass
        #     except IndexError:
        #         print("Vaisala data parsing for thingsboard error")

        #     if SCREEN_DISPLAY:
        #         try:
        #             print("wind_direction: " + str(grange_4_vaisala['wind_direction']) + "(Deg)")
        #             print("wind_speed: " + str(grange_4_vaisala['wind_speed']) + "(m/s)")
        #             print("atm_temperature: " + str(grange_4_vaisala['atm_temp']) + "(Cels)")
        #             print("atm_humidity: " + str(grange_4_vaisala['atm_humdity']) + "(%)")
        #             print("atm_pressure: " + str(grange_4_vaisala['atm_pressure']) + "(hPa)")
        #             print("rain_gauge: " + str(grange_4_vaisala['rain_gauge']) +"(mm)")
        #             print("rain_duration: " + str(grange_4_vaisala['rain_duration']) +"(seconds)")
        #             print("heat_temp: " + str(grange_4_vaisala['heat_temp']) + "(Cels)")
        #             print("heat_volt: " + str(grange_4_vaisala['heat_volt']) + "(Volt)")
        #         except (KeyError, IndexError):
        #             pass

        #     # UV Information together with vaisala reading
        #     try:
        #         ard.write("1145,3,power,33,dummies,1,interval_mm,2000,debug,0")
        #         ard.flushInput()
        #         sleep(1)
        #         msg = ard.readline()
        #         if SCREEN_DISPLAY:
        #             print(msg.rstrip())
        #         if SAVE_TO_FILE:
        #             fid.write(delimiter + msg.rstrip())
        #         current_read=msg.split(',')[0:-1]
        #         grange_4_vaisala['uv']=float(current_read[-1])
        #         grange_4_vaisala['ir']=float(current_read[-3])
        #         grange_4_vaisala['vis']=float(current_read[-5])
        #     except Exception as error:
        #         print("1145,3,power,33,dummies,1,interval_mm,2000, Reading failed")
        #         print(type(error))
        #         print(error)

        #     # Publish results from vaisala and uv            
        #     if PUBLISH_TO_THINGSBOARD:
        #         # client_vaisala.publish('v1/devices/me/telemetry', json.dumps(grange_4_vaisala), 1)
        #         publish_result = mqtthelper.publish_to_thingsboard(client_vaisala, payload=grange_4_vaisala,
        #                 ts=milliseconds_since_epoch, timeout=1.0, filename="grange_4_vaisala_mqttqueue.json", display_payload=True, debug=False)
        #         if SCREEN_DISPLAY:
        #             print(publish_result) # Display the last publish result

        if ENABLE_VAISALA:
            try:
                # msg = serial_openlock.get_result_by_input(port=port_sensor,command="12,53,custom_cmd,VI!,debug,1",initialize=False).rstrip()
                # if SCREEN_DISPLAY:
                #     print(msg)

                #msg = serial_openlock.get_result_by_input(port=port_sensor,command="12,51,custom_cmd,VM!,debug,1",initialize=False).rstrip()
                ard.write("12,51,custom_cmd,VM!,debug,1")
                ard.flushInput()
                sleep(1)
                msg=ard.readline()
                if SCREEN_DISPLAY:
                    print(msg)

                current_read = msg.rstrip()[-6:-1]
                try:
                    wait_seconds = int(current_read[1:4])
                except (ValueError):
                    wait_seconds = 10

                try:
                    number_points = int(current_read[-1])
                except (ValueError):
                    number_points = 1

                print("Waiting " + str(wait_seconds) + " seconds for measurements, expecting " + str(number_points) + " values")
                # Critical to wait for measurement to be completed
                time.sleep(wait_seconds)        # important for next command

                count = 0
                vaisala_values = ""
                for value_index in range(0, number_points):
                    #msg = serial_openlock.get_result_by_input(port=port_sensor,command="12,51,custom_cmd,VD" + str(value_index) + "!,debug,1",initialize=False).rstrip()
                    msg="12,51,custom_cmd,VD" + str(value_index) + "!,debug,1"
                    ard.write(msg)
                    ard.flushInput()
                    sleep(10)
                    msg=ard.readline()
                    msg=msg.rstrip()
                    time.sleep(10)
                    response = msg[0:-1].split('response,V')[-1]
                    vaisala_values += response
                    count += response.count('+') + response.count('-')
                    if SCREEN_DISPLAY:
                        print(msg)
                    if (count >= number_points):
                        break


                vaisala_values_original=vaisala_values
                # modify string for concatenation
                vaisala_values = vaisala_values.replace('+', ",+")
                vaisala_values = vaisala_values.replace('-', ",-")
                current_read = vaisala_values[1:].split(',')

                if SCREEN_DISPLAY:
                    print(current_read)
                grange_4_vaisala['wind_direction'] = float(current_read[0])
                grange_4_vaisala['wind_speed'] = float(current_read[1])
                grange_4_vaisala['atm_temp'] = float(current_read[2])
                grange_4_vaisala['atm_humdity'] = float(current_read[3])
                grange_4_vaisala['atm_pressure'] = float(current_read[4])
                grange_4_vaisala['rain_gauge'] = float(current_read[5])
                grange_4_vaisala['rain_duration'] = float(current_read[6])
                grange_4_vaisala['heat_temp'] = float(current_read[7])
                grange_4_vaisala['heat_volt'] = float(current_read[8])


                # Reset vaisala rain counter and duration
                #msg = serial_openlock.get_result_by_input(port=port_sensor,command="12,51,custom_cmd,VXZRU!,debug,1",initialize=False).rstrip()
                ard.write("12,51,custom_cmd,VXZRU!,debug,1")
                ard.flushInput()
                sleep(10)
                msg=ard.readline()
                time.sleep(5)

                if SCREEN_DISPLAY:
                    print("wind_direction: " + str(grange_4_vaisala['wind_direction']) + "(Deg)")
                    print("wind_speed: " + str(grange_4_vaisala['wind_speed']) + "(m/s)")
                    print("atm_temperature: " + str(grange_4_vaisala['atm_temp']) + "(Cels)")
                    print("atm_humidity: " + str(grange_4_vaisala['atm_humdity']) + "(%)")
                    print("atm_pressure: " + str(grange_4_vaisala['atm_pressure']) + "(hPa)")
                    print("rain_gauge: " + str(grange_4_vaisala['rain_gauge']) +"(mm)")
                    print("rain_duration: " + str(grange_4_vaisala['rain_duration']) +"(seconds)")
                    print("heat_temp: " + str(grange_4_vaisala['heat_temp']) + "(Cels)")
                    print("heat_volt: " + str(grange_4_vaisala['heat_volt']) + "(Volt)")
                if SAVE_TO_FILE:
                    fid.write("\nVaisala" + delimiter + vaisala_values[1:])

                #msg=serial_openlock.get_result_by_input(port=port_sensor,command="1145,3,power,33,dummies,1,interval_mm,2000,debug,0",initialize=False)
                ard.write("1145,3,power,33,dummies,1,interval_mm,2000,debug,0")
                ard.flushInput()
                sleep(1)
                msg=ard.readline()
                if SCREEN_DISPLAY: print msg.rstrip()
                if SAVE_TO_FILE: fid.write(delimiter+msg.rstrip())
                current_read=msg.split(',')[0:-1]
                grange_4_vaisala['uv']=float(current_read[-1])
                grange_4_vaisala['ir']=float(current_read[-3])
                grange_4_vaisala['vis']=float(current_read[-5])



                # Publish data
                client_vaisala.publish('v1/devices/me/telemetry', json.dumps(grange_4_vaisala), 1)
                # Following upload is deprecated
                # upload_phant(pht_grange_4_vaisala,grange_4_vaisala,SCREEN_DISPLAY)

            except Exception as error:
                print("Vaisala reading failed")
                print(type(error))
                print(error)


        ### End of procedure loop cycle
        if SCREEN_DISPLAY:
            print('Sleep for '+str(sleep_time_seconds)+' seconds'+'\r\n')
        if SAVE_TO_FILE:
            fid.write("\r\n")

        # Cycle counter update
        if sensor_measure_idx >= 3:
            sensor_measure_idx = 1
        else:
            sensor_measure_idx += 1


        time.sleep(sleep_time_seconds)

except KeyboardInterrupt:
    pass
finally:
    # Tidy up connections and file access
    if (SAVE_TO_FILE and (fid.closed == False)):
        fid.close()
    if (ard.isOpen()):
        ard.close()
    if (PUBLISH_TO_THINGSBOARD):
        client.loop_stop()
        client.disconnect()
