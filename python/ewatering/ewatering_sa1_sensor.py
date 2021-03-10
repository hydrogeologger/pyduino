import time
import json
import serial
import paho.mqtt.client as mqtt
from time import sleep,localtime,strftime
#---------------------- Define constants --------------------------------------
SCREEN_DISPLAY=True
SAVE_TO_FILE=True
DELIMITER=','
SLEEP_TIME_SECONDS=60  *30# s
SERIAL_PORT='/dev/ttyS0'
#---------------------- Create csv file to store data -------------------------
file_name= 'ewatering_sa1_sensor.csv'
fid= open(file_name,'a',0)
fid.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')
#---------------------------- Initiation --------------------------------------
with open('/home/pi/pyduino/credential/ewatering.json') as f: 
    credential = json.load(f)

field_name = ['sa1_rh_logger','sa1_temp_logger','sa1_volt','wind_direction','sa1_p_5803','sa1_t_5803','sa1_sht31_temp_1','sa1_sht31_humidity_1','sa1_uv','sa1_ir','sa1_vis','sa1_ec1','sa1_temp1','sa1_raw1','sa1_ec2','sa1_temp2','sa1_raw2','sa1_ec3','sa1_temp3','sa1_raw3','sa1_ec4','sa1_temp4','sa1_raw4','sa1_ec5','sa1_temp5','sa1_raw5','sa1_p_piezo','sa1_t_piezo','sa1_ec_piezo',]

ewatering_sa1_sensor = {}

try:
    client = mqtt.Client()
    client.username_pw_set(credential['access_token'])
    client.connect(credential['thingsboard_host'], 1883, 60)
    client.loop_start()
    print("Successfully connected to thingsboard")
except Exception:
    print("Failed to connect to thingsboard")
    time.sleep(30)

#----------------------Display current time and start Arduino ----------------------
try:    
    while True:

        if SCREEN_DISPLAY: print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        if SAVE_TO_FILE: fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime()))

        ard = serial.Serial(SERIAL_PORT,timeout=20)
        time.sleep(5)

#--------------------------- on board humidity sensor -------------------------------
        try:
            ard.write("dht22,54,power,2,points,2,dummies,1,interval_mm,200,debug,1")
            ard.flushInput()
            msg=ard.readline()
	    current_read=msg.split(',')[0:-1]
            ewatering_sa1_sensor['sa1_rh_logger']=float(current_read[-1])
            ewatering_sa1_sensor['sa1_temp_logger']=float(current_read[-2])
            if SCREEN_DISPLAY: print (msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        except Exception as e:
            if SCREEN_DISPLAY:
                print (e)
                print ('on board humidty reading failed')
	time.sleep(5)
#----------------------------- System voltage ---------------------------------------
        try:
	    ard.write("analog,15,power,9,points,5,dummies,3,interval_mm,200")
	    ard.flushInput()
            msg=ard.readline()
	    current_read=float(msg.split(',')[-2])
	    ewatering_sa1_sensor['sa1_volt']=float(current_read)
	    if SCREEN_DISPLAY: print ('raw System Voltage: ' + str(ewatering_sa1_sensor['sa1_volt']))
            if SAVE_TO_FILE:fid.write(DELIMITER + str(ewatering_sa1_sensor['sa1_volt']) + '\n')			 
	except Exception as e:
	    if SCREEN_DISPLAY:
		print (e)
		print ('system voltage reading failed')
        time.sleep(5)
#------------------------------ Wind direction ----------------------------------------
        try:
            ard.write("analog,8,power,49,point,3,interval_mm,200,debug,0")
            ard.flushInput()
            msg=ard.readline()
            current_read = float(msg.split(',')[-2])
            ewatering_sa1_sensor['wind_direction']=float(current_read)
            if SCREEN_DISPLAY: print ('Wind direction: ' + str(ewatering_sa1_sensor['wind_direction']))
            if SAVE_TO_FILE:fid.write(DELIMITER + str(ewatering_sa1_sensor['wind_direction']) + '\n')
        except Exception as e:
            if SCREEN_DISPLAY:
                print (e)
                print ('wind direction reading failed')
        time.sleep(5)
#-----------------Temperature, humidity and UV sensor----------------------------------
        try:
            ard.write("power_switch,30,power_switch_status,1")
            ard.flushInput()            
	    time.sleep(1)
	    ard.write("power_switch,31,power_switch_status,1")
            ard.flushInput()
	    time.sleep(1)
            ard.write("power_switch,32,power_switch_status,1")
            ard.flushInput()
            time.sleep(3) #It is VERY IMPORTANT to set a time delay after switching on power channels for I2C because humiditity sensors would not get reading successfully if the measurement is conducted immediately.

            ard.write("9548,2,type,5803,points,3,dummies,3,debug,1,interval_mm,1000")
            ard.flushInput()
            msg_5803_channel0=ard.readline()        
            if SAVE_TO_FILE: fid.write(DELIMITER+msg_5803_channel0)
            if SCREEN_DISPLAY: print msg_5803_channel0.rstrip()
            current_read=msg_5803_channel0.split(',')
            ewatering_sa1_sensor['sa1_p_5803']=(float(current_read[-2])+float(current_read[-4])+float(current_read[-5])+float(current_read[-6]))/4.
            ewatering_sa1_sensor['sa1_t_5803']=float(current_read[-3])

         #------------------------Humidity sensor SHT31-----------------------------------------------			
            ard.write("9548,0,type,sht31,debug,1")
            ard.flushInput()
            msg=ard.readline()
            time.sleep(5)
            current_read = msg.split(',')[0:-1]
            ewatering_sa1_sensor['sa1_sht31_temp_1'] = float(current_read[-2])
            ewatering_sa1_sensor['sa1_sht31_humidity_1'] = float(current_read[-1])
            if SCREEN_DISPLAY: print('Temp: ' + str(ewatering_sa1_sensor['sa1_sht31_temp_1'])  + DELIMITER + 'Rh: ' + str(ewatering_sa1_sensor['sa1_sht31_humidity_1']) + '%')  #u"\u2103" is the unicode for celsius degree
            if SAVE_TO_FILE: fid.write(DELIMITER + str(ewatering_sa1_sensor['sa1_sht31_temp_1']) + DELIMITER + str(ewatering_sa1_sensor['sa1_sht31_humidity_1']) + '\n')
         #------------------------------UV sensor-----------------------------------------------
            ard.write("9548,1,type,si1145,debug,1")
            ard.flushInput()
            msg=ard.readline()
            time.sleep(12)
	    current_read=msg.split(',')[0:-1]
            ewatering_sa1_sensor['sa1_uv']=float(current_read[-1])  #ultraviolet index
            ewatering_sa1_sensor['sa1_ir']=float(current_read[-3])  #Infrared light
            ewatering_sa1_sensor['sa1_vis']=float(current_read[-5]) #visible light
	    if SCREEN_DISPLAY: print (msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)


        #  switch off power
            ard.write("power_switch,30,power_switch_status,0")
            time.sleep(1)
            ard.flushInput()
            ard.write("power_switch,31,power_switch_status,0")
            time.sleep(1)
            ard.flushInput()
            ard.write("power_switch,32,power_switch_status,0")
            ard.flushInput()
            time.sleep(5)
    
        except Exception as e :
            if SCREEN_DISPLAY: print (e)
            if SCREEN_DISPLAY: print ('9548 reading  failed')
			
#---------------------------teros-12 No.1-----------------------------
        try:
            ard.write("SDI-12,62,power,22,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            ewatering_sa1_sensor['sa1_ec1']=float(current_read.split(',')[-2])
            ewatering_sa1_sensor['sa1_temp1']=float(current_read.split(',')[-3])            
            ewatering_sa1_sensor['sa1_raw1']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print (msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception as e :
            if SCREEN_DISPLAY:
		print (e)
                print ('MO1 reading failed')
    
#---------------------------teros-12 No.2-----------------------------
        try:
            ard.write("SDI-12,63,power,23,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            ewatering_sa1_sensor['sa1_ec2']=float(current_read.split(',')[-2])
            ewatering_sa1_sensor['sa1_temp2']=float(current_read.split(',')[-3])            
            ewatering_sa1_sensor['sa1_raw2']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print (msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception as e :
            if SCREEN_DISPLAY:
		print(e)
                print('MO2 reading failed')

#---------------------------teros-12 No.3-----------------------------
        try:
            ard.write("SDI-12,64,power,24,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            ewatering_sa1_sensor['sa1_ec3']=float(current_read.split(',')[-2])
            ewatering_sa1_sensor['sa1_temp3']=float(current_read.split(',')[-3])            
            ewatering_sa1_sensor['sa1_raw3']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception as e :
            if SCREEN_DISPLAY:
		print(e)
                print('MO3 reading failed')

#---------------------------teros-12 No.4-----------------------------
        try:
            ard.write("SDI-12,65,power,25,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            ewatering_sa1_sensor['sa1_ec4']=float(current_read.split(',')[-2])
            ewatering_sa1_sensor['sa1_temp4']=float(current_read.split(',')[-3])            
            ewatering_sa1_sensor['sa1_raw4']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception as e :
            if SCREEN_DISPLAY:
		print(e)
                print('MO4 reading failed')

#---------------------------teros-12 No.5-----------------------------
        try:
            ard.write("SDI-12,66,power,26,default_cmd,read,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            current_read=msg.split('Addr')[-1]     
            ewatering_sa1_sensor['sa1_ec5']=float(current_read.split(',')[-2])
            ewatering_sa1_sensor['sa1_temp5']=float(current_read.split(',')[-3])            
            ewatering_sa1_sensor['sa1_raw5']=float(current_read.split(',')[-4])
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            time.sleep(5)
        except Exception as e :
            if SCREEN_DISPLAY:
		print(e)
                print('MO5 reading failed')
#---------------------------aqua troll 200-----------------------------
        try:
            ard.write("SDI-12,50,custom_cmd,aM!,debug,1")  # do measurement
            ard.flushInput()
            msg=ard.readline()        
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            #time.sleep(5)
            #print(msg.rstrip())
            if SCREEN_DISPLAY: print msg.rstrip()
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            

            time.sleep(5) # this appears to be important
           
            ard.write("SDI-12,50,custom_cmd,aD0!,debug,1")
            ard.flushInput()
            msg=ard.readline()        
            if SCREEN_DISPLAY: print(msg.rstrip())
            if SAVE_TO_FILE: fid.write(DELIMITER+msg)
            current_read=msg[:-3].split('+')    
            ewatering_sa1_sensor['sa1_p_piezo']=float(current_read[1])
            ewatering_sa1_sensor['sa1_t_piezo']=float(current_read[2])
            ewatering_sa1_sensor['sa1_ec_piezo']=float(current_read[3])
            time.sleep(5)
        except Exception as e:
            if SCREEN_DISPLAY:
                print(e)
                print('pressure transducer reading failed')


#----------------------------barometer (ms5803) ------------------------
        #try:
        #    ard.write("power_switch,22,power_switch_status,1")
        #    time.sleep(5)
        #    ard.write("9548,0,type,5803,power,22,points,3,dummies,3,debug,1,interval_mm,1000")
        #    ard.flushInput()
        #    msg_5803_channel0=ard.readline()        
        #    if SAVE_TO_FILE: fid.write(DELIMITER+msg_5803_channel0)
        #    if SCREEN_DISPLAY: print msg_5803_channel0.rstrip()
        #    current_read=msg_5803_channel0.split(',')
        #    ewatering_sa1_sensor['p_5803']=(float(current_read[-2])+float(current_read[-4])+float(current_read[-5])+float(current_read[-6]))/4.
        #    ewatering_sa1_sensor['t_5803']=float(current_read[3])

        #    ard.write("9548,1,type,5803,power,22,points,3,dummies,3,debug,1,interval_mm,1000")

        #    ard.flushInput()
        #    msg2=ard.readline()        
        #    if SAVE_TO_FILE: fid.write(DELIMITER+msg2)
        #    if SCREEN_DISPLAY: print msg2.rstrip()
        #    current_read=msg2.split(',')
        #    ewatering_sa1_sensor['p_5803_2']=(float(current_read[-2])+float(current_read[-4])+float(current_read[-5])+float(current_read[-6]))/4.
        #    ewatering_sa1_sensor['t_5803_2']=float(current_read[3])

        #    time.sleep(5)
        #    ard.write("power_switch,22,power_switch_status,0")
        #except Exception as e:
        #    if SCREEN_DISPLAY:
        #        print(e)
        #        print('5803 sensor at port 0 reading failed')


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



        ard.close()

        client.publish('v1/devices/me/telemetry', json.dumps(ewatering_sa1_sensor), 1)    
        print('data successfully uploaded')
    
        if SAVE_TO_FILE: fid.write("\n\r")
        if SCREEN_DISPLAY: print('sleep for ' + str(SLEEP_TIME_SECONDS) + ' seconds')
        time.sleep(SLEEP_TIME_SECONDS) # sleep to the next loop

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
