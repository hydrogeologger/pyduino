import time
import json
import serial
from phant import Phant
import paho.mqtt.client as mqtt
#from upload_phant import upload_phant
from time import sleep,localtime,strftime


SCREEN_DISPLAY=True
SAVE_TO_FILE=True
DELIMITER=','
SLEEP_TIME_SECONDS=60*30# s
SERIAL_PORT='/dev/ttyS0' # datalogger version 2 uses ttyS0
#SERIAL_PORT='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2:1.0' # datalogger version 1 uses ttyACM0

#---------------------- Create csv file to store data -------------------------

file_name= 'ewatering_sensor.csv'
fid= open(file_name,'a',0)
fid.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')
          
#---------------------------- Initiation --------------------------------------

with open('/home/pi/pyduino/credential/ewatering.json') as f: 
    credential = json.load(f)

field_name=['p_piezo1','t_piezo1','temp_logger','rh_logger']

ewatering_sensor = dict((el,0.0) for el in field_name)

try:
    client = mqtt.Client()
    client.username_pw_set(credential['access_token'])
    client.connect(credential['thingsboard_host'], 1883, 60)
    client.loop_start()
    print("Successfully connected to thingsboard")
except Exception:
    print("Failed to publish to thingsboard")
    time.sleep(30)
 
try:    
    while True:

        if SCREEN_DISPLAY: print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        if SAVE_TO_FILE: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime()))

        ard = serial.Serial(SERIAL_PORT,timeout=20)
        time.sleep(5)

#----------------------------on board humidity sensor------------------------------------


        try:
            msg=ard.write("dht22,54,power,2,points,2,dummies,1,interval_mm,200,debug,1")
            msg=ard.flushInput()
            msg=ard.readline()
            if SCREEN_DISPLAY: print msg.rstrip()
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            current_read=msg.split(',')
            ewatering_sensor['rh_logger']=float(current_read[-2])
            ewatering_sensor['temp_logger']=float(current_read[-3])
        except Exception as e:
            if SCREEN_DISPLAY:
                print(e)
                print('on board humidty reading failed')



        #----------------System voltage-----------------------------
        msg2 = ard.write("analog,15,power,9,points,5,dummies,3,interval_mm,200")
        msg2 = ard.flushInput()
        msg2 = ard.readline()

        try:
            current_read = float(msg2.split(',')[-2])
            ewatering_sensor['volt'] = int(current_read)
            if SCREEN_DISPLAY:
                print ('raw System Voltage: ' + str(ewatering_sensor['volt']))
            if SAVE_TO_FILE:
                fid.write(DELIMITER + str(ewatering_sensor['volt']) + '\n')
        except Exception as e :
            if SCREEN_DISPLAY:
                print('System voltage reading failed')

        time.sleep(5)

        #-----------------Temperature, humidity and UV sensor--------------------
        try:
            msg=ard.write("power_switch,30,power_switch_status,1")
            msg=ard.flushInput()

            time.sleep(5)

            msg=ard.write("power_switch,31,power_switch_status,1")
            msg=ard.flushInput()
            #For I2C communication, all sensors have to be connected to the same power OR if they use different power, all reserved power channels have to be switched on before measuring one by one.

            time.sleep(5) #It is VERY IMPORTANT to set a time delay after switching on power channels for I2C because humiditity sensors would not get reading successfully if the measurement is conducted immediately.

            msg4 = ard.write("9548,0,type,sht31,debug,1")
            msg4 = ard.flushInput()
            msg4 = ard.readline()

            time.sleep(5)

            msg5 = ard.write("9548,1,type,si1145,debug,1")
            msg5 = ard.flushInput()
            msg5 = ard.readline()

            time.sleep(5)

            msg=ard.write("power_switch,30,power_switch_status,0")
            msg=ard.flushInput()

            msg=ard.write("power_switch,31,power_switch_status,0")
            msg=ard.flushInput()
 
            #time.sleep(5)
        
            current_read = msg4.split(',')[0:-1]
            ewatering_sensor['sht31_temp_1'] = float(current_read[-2])
            ewatering_sensor['sht31_humidity_1'] = float(current_read[-1])
            if SCREEN_DISPLAY:
                print('Temperature: ' + str(ewatering_sensor['sht31_temp_1']) + u"\u2103"  + DELIMITER + 'Relative humidity: ' + str(ewatering_sensor['sht31_humidity_1']) + '%')  #u"\u2103" is the unicode for celsius degree
            if SAVE_TO_FILE:
                fid.write(DELIMITER + str(ewatering_sensor['sht31_temp_1']) + DELIMITER + str(ewatering_sensor['sht31_humidity_1']) + '\n')
            if SCREEN_DISPLAY: print(msg5.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg5)
        except Exception as e :
            if SCREEN_DISPLAY:
                print('humidity sensor and uv reading failed')





#---------------------------aqua troll 200-----------------------------
        #try:
        #    ard.write("SDI-12,52,custom_cmd,pM!,debug,1")  # do measurement
        #    ard.flushInput()
        #    msg=ard.readline()        
        #    if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        #    #time.sleep(5)
        #    #print(msg.rstrip())
        #    if SCREEN_DISPLAY: print msg.rstrip()
        #    if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        #    

        #    time.sleep(5) # this appears to be important
        #   
        #    ard.write("SDI-12,52,custom_cmd,pD0!,debug,1")
        #    ard.flushInput()
        #    msg=ard.readline()        
        #    if SCREEN_DISPLAY: print(msg.rstrip())
        #    if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        #    current_read=msg[:-3].split('+')    
        #    ewatering_sensor['p_piezo1']=float(current_read[1])
        #    ewatering_sensor['t_piezo1']=float(current_read[2])
        #    ewatering_sensor['ec_piezo1']=float(current_read[3])
        #    time.sleep(5)
        #except Exception as e:
        #    if SCREEN_DISPLAY:
        #        print(e)
        #        print('pressure transducer reading failed')


#----------------------------pressure transducer ------------------------



        #try:
        #    ard.write("power_switch,22,power_switch_status,1")
        #    time.sleep(5)
        #    ard.write("9548,0,type,5803,power,22,points,3,dummies,3,debug,1,interval_mm,1000")
        #    ard.flushInput()
        #    msg_5803_channel0=ard.readline()        
        #    if SAVE_TO_FILE: fid.write(DELIMITER+msg_5803_channel0)
        #    if SCREEN_DISPLAY: print msg_5803_channel0.rstrip()
        #    current_read=msg_5803_channel0.split(',')
        #    ewatering_sensor['p_5802']=(float(current_read[-2])+float(current_read[-4])+float(current_read[-5])+float(current_read[-6]))/4.
        #    ewatering_sensor['t_5802']=float(current_read[3])

        #    ard.write("9548,1,type,5803,power,22,points,3,dummies,3,debug,1,interval_mm,1000")

        #    ard.flushInput()
        #    msg2=ard.readline()        
        #    if SAVE_TO_FILE: fid.write(DELIMITER+msg2)
        #    if SCREEN_DISPLAY: print msg2.rstrip()
        #    current_read=msg2.split(',')
        #    ewatering_sensor['p_5802_2']=(float(current_read[-2])+float(current_read[-4])+float(current_read[-5])+float(current_read[-6]))/4.
        #    ewatering_sensor['t_5802_2']=float(current_read[3])

        #    time.sleep(5)
        #    ard.write("power_switch,22,power_switch_status,0")
        #except Exception as e:
        #    if SCREEN_DISPLAY:
        #        print(e)
        #        print('5802 sensor at port 0 reading failed')


#SDI-12,62,power,22,default_cmd,read,debug,1
#SDI-12,62,default_cmd,read,power,22,power_off,1,no_sensors,1,Addr,0_MET,points,3,1803.49,26.4,1,
#
#SDI-12,63,power,23,default_cmd,read,debug,1
#SDI-12,63,default_cmd,read,power,23,power_off,1,no_sensors,1,Addr,0_MET,points,3,1793.23,26.6,1,
#
#
#SDI-12,64,power,25,default_cmd,read,debug,1
#
#
#SDI-12,62,power,25,default_cmd,read,debug,1
#p

# read from cambel scientific sensor cs451

        ##      campell scientific sensor
        #try:
        #    ard.write("SDI-12,62,default_cmd,read,debug,1")  # do measurement
        #    ard.flushInput()
        #    msg=ard.readline()        
        #    if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        #    if SCREEN_DISPLAY: print msg.rstrip()
        #    if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        #    

        #    current_read=msg.split(',')    
        #    ewatering_sensor['p_cs451']=float(current_read[-2])
        #    ewatering_sensor['t_cs451']=float(current_read[-3])
        #    time.sleep(5)
        #except Exception as e:
        #    if SCREEN_DISPLAY:
        #        print(e)
        #        print('pressure transducer reading failed')


#---------------------------teros-12 No.1-----------------------------
        try:
            ard.write("SDI-12,62,power,22,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            ewatering_sensor['ec1']=float(current_read.split(',')[-2])
            ewatering_sensor['temp1']=float(current_read.split(',')[-3])            
            ewatering_sensor['raw1']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception as e :
            if SCREEN_DISPLAY:
                print('MO1 reading failed')
    
#---------------------------teros-12 No.2-----------------------------
        try:
            ard.write("SDI-12,63,power,23,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            ewatering_sensor['ec2']=float(current_read.split(',')[-2])
            ewatering_sensor['temp2']=float(current_read.split(',')[-3])            
            ewatering_sensor['raw2']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception as e :
            if SCREEN_DISPLAY:
                print('MO2 reading failed')

#---------------------------teros-12 No.3-----------------------------
        try:
            ard.write("SDI-12,64,power,24,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            ewatering_sensor['ec3']=float(current_read.split(',')[-2])
            ewatering_sensor['temp3']=float(current_read.split(',')[-3])            
            ewatering_sensor['raw3']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception as e :
            if SCREEN_DISPLAY:
                print('MO3 reading failed')

#---------------------------teros-12 No.4-----------------------------
        try:
            ard.write("SDI-12,65,power,25,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            ewatering_sensor['ec4']=float(current_read.split(',')[-2])
            ewatering_sensor['temp4']=float(current_read.split(',')[-3])            
            ewatering_sensor['raw4']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception as e :
            if SCREEN_DISPLAY:
                print('MO4 reading failed')

#---------------------------teros-12 No.5-----------------------------
        try:
            ard.write("SDI-12,66,power,26,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            ewatering_sensor['ec6']=float(current_read.split(',')[-2])
            ewatering_sensor['temp6']=float(current_read.split(',')[-3])            
            ewatering_sensor['raw6']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception as e :
            if SCREEN_DISPLAY:
                print('MO5 reading failed')


        ard.close()
    
        client.publish('v1/devices/me/telemetry', json.dumps(ewatering_sensor), 1)    
        #upload_phant(pht_ewatering_sensor,salt_marsh_sensor,SCREEN_DISPLAY)
    
        if SAVE_TO_FILE: fid.write("\n\r")
        if SCREEN_DISPLAY: print('sleep for ' + str(SLEEP_TIME_SECONDS) + ' seconds')
        time.sleep(SLEEP_TIME_SECONDS) # sleep to the next loop

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()

