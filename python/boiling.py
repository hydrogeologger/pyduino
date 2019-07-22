import time
import json
import serial
import subprocess
from phant import Phant
import paho.mqtt.client as mqtt
from upload_phant import upload_phant
import pdb
#import logger

#------------------- Constants and Ports Information---------------------------

SCREEN_DISPLAY=True
SAVE_TO_FILE=True
DELIMITER=','
HEAT_TIME=2000 # ms (reduce this when testing)
SLEEP_TIME_SECONDS=60*10 # s
SERIAL_PORT='/dev/ttyACM0' # serial port terminal
PORT_SCALE_1='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2:1.0-port0' 
PORT_SCALE_2='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.3:1.0-port0'
#PORT_SCALE_2='/dev/serial/by-path/platform-3f980000.usb-usb-0:1.3:1.0-port0' 
#PORT_SCALE_2='/dev/ttyUSB1' 

#---------------------- Create csv file to store data -------------------------

file_name= 'boiling.csv'
fid= open(file_name,'a',0)
fid.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')

#------------------------- Define Functions -----------------------------------

#def read_suction_sensor(ard,sensor_num,sensor_id,dgin,snpw,htpw,low,high,delta):
def read_suction_sensor(ard,**kwargs):
    """Read suction sensor
    Parameters:
    name_address -- a dictionary that stores the key and index number of string received from device.
                    For example:
                    ard provides a string of "aaa,bbb,123,dd"
                    the goal is to store 123 into object data['value']
                    the name_address will be written as {'value':2}
    debug        -- print parsed details
    delimiter    -- the delimiter to separate the string, NOTICE, if wish to use multiple space as delimiter, just put in None
    """
    arg_defaults = {
                'input_command' :'abc',
                'names_address':{},
                'delimiter':',',
                'debug':False
                   }
    arg=arg_defaults
    for d in kwargs:
        arg[d]= kwargs.get(d)
    try:
        ard.flushInput()
        ard.write(arg['input_command'])
        msg=ard.readline()      
        current_read=msg.split(arg['delimiter'])[0:-1]
        #pdb.set_trace()
        if SCREEN_DISPLAY: print(msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg.rstrip()+'\n')  
        if arg['debug']:
            for i in current_read:
                print i+'\n'
        for i in arg['names_address']:
            #pdb.set_trace()
            #print i,arg['names_address'][i]
            boiling[i]=float(current_read[ arg['names_address'][i]  ])
        #if SCREEN_DISPLAY: print(msg.rstrip())
        #if SAVE_TO_FILE: fid.write(DELIMITER+msg.rstrip()+'\n')  
        time.sleep(5)
    except Exception, e:
        if SCREEN_DISPLAY:
            print ('Failed to do something: ' + str(e))
            print('input command'+arg['input_command']+' reading failed')
            
def read_scale(port_scale,key_scale):
    """Read scale

    Parameters:
        port_scale (str): the address of the scale
        key_scale (str): the key used to update the scale value in dictionary boiling
  
    """
    scale_attempts=1
    while scale_attempts < 5:
        try:
            scale=serial.Serial(port_scale,timeout=20)
            scale.write('IP\n\r')
            time.sleep(3)
            str_scale=scale.readline()
            weight_scale=str_scale.split()[0]
            boiling[key_scale]=float(weight_scale)
            time_now=time.strftime("%Y-%m-%d %H:%M:%S")
            if SCREEN_DISPLAY: print(key_scale+" reading sucessfully, weight is "+weight_scale)
            if SAVE_TO_FILE: fid.write(time_now+DELIMITER+weight_scale+DELIMITER+'\n\r')
            break
        except Exception:
            if SCREEN_DISPLAY: print(key_scale+" reading failed on trial No."+str(scale_attempts))
            scale_attempts+=1
            scale.close()
            time.sleep(3)
            
#---------------------------- Initiation --------------------------------------

with open('/home/pi/pyduino/credential/boiling.json') as f: 
    credential = json.load(f)

field_name=['scale1','scale2','scale3',
            'temp_1','temp_2','temp_3','temp_4','temp_5',
            'temp_6','temp_air','humidity']

boiling = dict((el,0.0) for el in field_name)

try:
    client = mqtt.Client()
    client.username_pw_set(credential['access_token'])
    client.connect(credential['thingsboard_host'], 1883, 60)
    client.loop_start()
    print("Successfully publish to thingsboard")
except Exception:
    print("Failed to publish to thingsboard")
    time.sleep(30)
 
#----------------------------suction sensors-----------------------------------

try:    
    while True:
        ard = serial.Serial(SERIAL_PORT,timeout=60)             
        time.sleep(1)
        read_suction_sensor(ard,input_command="fred,288C6A7F0A00007D,dgin,50,snpw,44,htpw,-1,itv,1000,otno,1",names_address={'temp_1':4})
        #ard.write("fred,288C6A7F0A00007D,dgin,50,snpw,44,htpw,-1,itv,1000,otno,1")
        #time.sleep(3)
        #msg=ard.readline()       
        #current_read=msg.split(',')[0:-1]
        #boiling['temp_1']=float( current_read[4])


        read_suction_sensor(ard,input_command="fred,28FE697F0A0000C5,dgin,50,snpw,44,htpw,-1,itv,1000,otno,1",names_address={'temp_2':4})
        #ard.write("fred,28FE697F0A0000C5,dgin,50,snpw,44,htpw,-1,itv,1000,otno,1")
        #time.sleep(3)
        #msg=ard.readline()       
        #current_read=msg.split(',')[0:-1]
        #boiling['temp_2']=float( current_read[4])

        read_suction_sensor(ard,input_command="fred,28056A7F0A000001,dgin,50,snpw,44,htpw,-1,itv,1000,otno,1",names_address={'temp_3':4})
        #ard.write("fred,28056A7F0A000001,dgin,50,snpw,44,htpw,-1,itv,1000,otno,1")
        #time.sleep(3)
        #msg=ard.readline()       
        #current_read=msg.split(',')[0:-1]
        #boiling['temp_3']=float( current_read[4])
        

        read_suction_sensor(ard,input_command="fred,28377F7F0A00002C,dgin,50,snpw,44,htpw,-1,itv,1000,otno,1",names_address={'temp_4':4})
        #ard.write("fred,28377F7F0A00002C,dgin,50,snpw,44,htpw,-1,itv,1000,otno,1")
        #time.sleep(3)
        #msg=ard.readline()       
        #current_read=msg.split(',')[0:-1]
        #boiling['temp_4']=float( current_read[4])

        read_suction_sensor(ard,input_command="fred,281C7F7F0A000062,dgin,13,snpw,42,htpw,-1,itv,1000,otno,1",names_address={'temp_5':4})
        #ard.write("fred,281C7F7F0A000062,dgin,13,snpw,42,htpw,-1,itv,1000,otno,1")
        #time.sleep(3)
        #msg=ard.readline()       
        #current_read=msg.split(',')[0:-1]
        #boiling['temp_5']=float( current_read[4])

        read_suction_sensor(ard,input_command="fred,28779C7F0A0000CD,dgin,13,snpw,42,htpw,-1,itv,1000,otno,1",names_address={'temp_6':4})
        #ard.write("fred,28779C7F0A0000CD,dgin,13,snpw,42,htpw,-1,itv,1000,otno,1")
        #time.sleep(3)
        #msg=ard.readline()       
        #current_read=msg.split(',')[0:-1]
        #boiling['temp_6']=float( current_read[4])
        
        #read_suction_sensor(ard,input_command="fred,28779C7F0A0000CD,dgin,13,snpw,42,htpw,-1,itv,1000,otno,1",names_address={'temp_6':4})
    
#---------------------------------scales---------------------------------------
        
        read_suction_sensor(ard,input_command="dht22,10,power,48,points,2,dummies,1,interval_mm,200,debug,1",names_address={'humidity':11,'temp_air':10},delimiter=',')
        #"dht22,10,power,48,points,2,dummies,1,interval_mm,200,debug,1"

        # ard.write("dht22,10,power,48,points,2,dummies,1,interval_mm,200,debug,1")



        scale_1=serial.Serial(PORT_SCALE_1,timeout=20)
        read_suction_sensor(scale_1,input_command="IP\n\r",names_address={'scale1':5},delimiter=None,debug=False)
        #scale_1.write('IP\n\r')
        #time.sleep(3)
        #str_scale=scale_1.readline()
        #weight_scale=str_scale.split()[5]
        #boiling['scale_1']=float(weight_scale)

        scale_2=serial.Serial(PORT_SCALE_2,timeout=20)
        read_suction_sensor(scale_2,input_command="P\n\r",names_address={'scale2':0},delimiter=None,debug=True)
        #scale_2.write('P\n\r')
        #time.sleep(3)
        #str_scale=scale_2.readline()
        #weight_scale=str_scale.split()[5]
        #boiling['scale_1']=float(weight_scale)
#----------------------------Upload data now-----------------------------------    
    
        ard.close()
    
        client.publish('v1/devices/me/telemetry', json.dumps(boiling), 1)    
        #upload_phant(pht_wwl_cali,wwl_cali,SCREEN_DISPLAY)
    
        if SAVE_TO_FILE: fid.write("\n\r")
        time.sleep(SLEEP_TIME_SECONDS) # sleep to the next loop

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
