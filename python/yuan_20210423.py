#!/usr/bin/python
import time
import json
import serial
import subprocess
#import paho.mqtt.client as mqtt

#------------------- Constants and Ports Information---------------------------
SCREEN_DISPLAY=True
SAVE_TO_FILE=True
DELIMITER=','
SLEEP_TIME_SECONDS=60*60 # s

port_scale1='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2:1.0-port0'
port_scale2='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.3:1.0-port0'
port_scale3='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.4:1.0-port0'
port_scale4='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.5:1.0-port0'

#---------------------- Create csv file to store data -------------------------
file_name= 'yuan_20210423.csv'
fid= open(file_name,'a',0)
#fid.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')
#---------------------------- Initiation --------------------------------------
#with open('/home/pi/pyduino/credential/yuan_20210423.json') as f: 
#    credential = json.load(f)
	
field_name=['scale_1','scale_2','scale_3','scale_4']

yuan_20210423 = dict((el,0.0) for el in field_name)

#try:
#    client = mqtt.Client()
#    client.username_pw_set(credential['access_token'])
#    client.connect(credential['thingsboard_host'], 1883, 60)
#    client.loop_start()
#    print("Successfully connected to thingsboard")
#except Exception:
#    print("Failed to connect to thingsboard")
#    time.sleep(30)
 
try:
    while True:
        scale_attempts=1
        while scale_attempts<6:		
            try:
                time_now = time.strftime("%d/%b/%Y %H:%M:%S")                    
                print(time_now)
                scale1 = serial.Serial(port_scale1,baudrate=2400,bytesize=7,parity='E',timeout=20)
                scale2 = serial.Serial(port_scale2,baudrate=2400,bytesize=7,parity='E',timeout=20)
    	        scale3 = serial.Serial(port_scale3,baudrate=2400,bytesize=7,parity='E',timeout=20)
	        scale4 = serial.Serial(port_scale4,baudrate=2400,bytesize=7,parity='E',timeout=20)
	        time.sleep(2)
		print('begin reading')
                scale1.write('Q\r\n')
                scale2.write('Q\r\n')
                scale3.write('Q\r\n')
                scale4.write('Q\r\n')						
	        time.sleep(2)
    	        str_scale1=scale1.readline()
                str_scale2=scale2.readline()
    	        str_scale3=scale3.readline()
    	        str_scale4=scale4.readline()			
	        time.sleep(2)
	        print('scale1 raw reading is '+str_scale1)
	        print('scale2 raw reading is '+str_scale2)
	        print('scale3 raw reading is '+str_scale3)
	        print('scale4 raw reading is '+str_scale4)	
		
	        reading_scale1=str(float(str_scale1.split()[0].split(',')[1]))
                reading_scale2=str(float(str_scale2.split()[0].split(',')[1])) 
	        reading_scale3=str(float(str_scale3.split()[0].split(',')[1]))
                reading_scale4=str(float(str_scale4.split()[0].split(',')[1]))	

                yuan_20210423['scale_1'] = reading_scale1
                yuan_20210423['scale_2'] = reading_scale2
                yuan_20210423['scale_3'] = reading_scale3
                yuan_20210423['scale_4'] = reading_scale4

                if SAVE_TO_FILE: fid.write(time_now+DELIMITER+reading_scale1+DELIMITER+reading_scale2+DELIMITER+reading_scale3+DELIMITER+reading_scale4+'\n\r')
#                if SAVE_TO_FILE: fid.write(time_now+DELIMITER+reading_scale3+DELIMITER+reading_scale4+'\n\r')



	        scale1.close()
	        scale2.close()
	        scale3.close()
	        scale4.close()

                print('scale reading successful')
            
        
	    except Exception, e:
                if SCREEN_DISPLAY:
                    print "scale reading failed on attempt "+str(scale_attempts)+" " + str(e)
                    scale_attempts+=1

            print('saved to local')
            time.sleep(SLEEP_TIME_SECONDS) # sleep to the next loop
#---------------------------Upload data -----------------------------------       
#        try:
#            client.publish('v1/devices/me/telemetry', json.dumps(yuan_20210423), 1)
#            print('uploaded to TB')
#            time.sleep(SLEEP_TIME_SECONDS) # sleep to the next loop
#        except:
#            print('uploading failed due to nasty balance reading')

except KeyboardInterrupt:
    pass

#client.loop_stop()
#client.disconnect()
