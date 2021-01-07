import time
import json
import serial
import subprocess
from phant import Phant
import paho.mqtt.client as mqtt
from upload_phant import upload_phant

#------------------- Constants and Ports Information---------------------------

SCREEN_DISPLAY=True
SAVE_TO_FILE=True
DELIMITER=','
HEAT_TIME=6000 # ms (reduce this when testing)
SLEEP_TIME_SECONDS=30*60 # s
SERIAL_PORT='/dev/ttyS0' # serial port terminal
PORT_SCALE_1='/dev/serial/by-path/platform-20980000.usb-usb-0:1.3:1.0-port0' 
PORT_SCALE_2='/dev/serial/by-path/platform-20980000.usb-usb-0:1.1:1.0-port0' 

#---------------------- Create csv file to store data -------------------------

file_name= 'wwl_cali.csv'
fid= open(file_name,'a',0)
fid.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')

#------------------------- Define Functions -----------------------------------

def read_suction_sensor(ard,sensor_num,sensor_id,dgin,snpw,htpw,low,high,delta):
    """Read suction sensor

    Parameters:
        ard (serial.Serial): the device (arduino) carrying out serial communication with pi
        sensor_num (int): the No. of the suction sensor
        sensor_id (str): 2nd,3rd,5th,8th digits of a ds18b20 intrinsic 8-digit id
        dgin, snpw, htpw (int): digital pin, power supply pin and heating power pin respectively
        delta (str): the key used to update the delta value in dictionary wwl_cali, same for high and low 
          
    """
    try:
        ard.write("fred,"+sensor_id+",dgin,"+str(dgin)+",snpw,"+str(snpw)+",htpw,"+str(htpw)+",itv,"+str(HEAT_TIME)+",otno,5")
        ard.flushInput()
        msg=ard.readline()      
        current_read=msg.split(',')[0:-1]
        wwl_cali[low]=float(current_read[2])
        wwl_cali[high]=float(current_read[8])  
        wwl_cali[delta]=float(current_read[8])-float(current_read[2])
        if SCREEN_DISPLAY: print(msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg.rstrip()+'\n')  
        time.sleep(5)
    except Exception:
        if SCREEN_DISPLAY:
            print('suction sensor No.'+str(sensor_num)+' reading failed')
            
def read_teros(ard,sensor_num,dgin,power,raw,ec):
    """Read teros-12/gs3 sensor (moisture, temperature and electric conductivity)

    Parameters:
        ard (serial.Serial): the device (arduino) carrying out serial communication with pi
        sensor_num (int): the No. of the teros-12 sensor
        dgin, power (int): digital pin and power supply pin respectively
        raw (str): the key used to update the raw value in dictionary wwl_cali, same for ec
  
    """
    try:
        ard.write("SDI-12,"+str(dgin)+",power,"+str(power)+",default_cmd,read,debug,1")
        ard.flushInput()
        msg=ard.readline()        
        current_read=msg.split('Addr')[-1]     
        wwl_cali[ec]=float(current_read.split(',')[-2])
        wwl_cali[raw]=float(current_read.split(',')[-4])
        if SCREEN_DISPLAY: print(msg.rstrip())
        if SAVE_TO_FILE: fid.write(DELIMITER+msg)
        time.sleep(5)
    except Exception:
        if SCREEN_DISPLAY:
            print('teros-12 sensor No.'+str(sensor_num)+' reading failed')

def read_scale(port_scale,key_scale):
    """Read scale

    Parameters:
        port_scale (str): the address of the scale
        key_scale (str): the key used to update the scale value in dictionary wwl_cali
  
    """
    scale_attempts=1
    while scale_attempts < 5:
        try:
            scale=serial.Serial(port_scale,timeout=20)
            scale.write('IP\n\r')
            time.sleep(3)
            str_scale=scale.readline()
            weight_scale=str_scale.split()[0]
            wwl_cali[key_scale]=float(weight_scale)
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

with open('/home/pi/pyduino/credential/wwl_cali.json') as f: 
    credential = json.load(f)

field_name=['scale1','scale2',
            'delta_t1','delta_t2','delta_t3','delta_t4','delta_t5',
            'delta_t6','delta_t7','delta_t8','delta_t9','delta_t10',
            'raw1','raw2','raw3','raw4','raw5','raw6',
            'ec1','ec2','ec3','ec4','ec5','ec6',
            'dp1','dp2','dp3','dp4','dp5','dp6',
            'mo1','mo2','mo3','mo4','mo5','mo6',
            'tba1','tba2','tba3','tba4','tba5','tba6',
            't1_low','t1_high','t2_low','t2_high','t3_low','t3_high','t4_low','t4_high','t5_low','t5_high',
            't6_low','t6_high','t7_low','t7_high','t8_low','t8_high','t9_low','t9_high','t10_low','t10_high']

wwl_cali = dict((el,0.0) for el in field_name)
pht_wwl_cali = Phant(publicKey=credential['public_wwl_cali'],
                     fields=field_name,
                     privateKey=credential['private_wwl_cali'],
                     baseUrl=credential['nectar_address'])

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
        su1 = read_suction_sensor(ard,1,'7F40A107',4,41,22,'t1_low','t1_high','delta_t1')
        su2 = read_suction_sensor(ard,2,'BC1BA124',4,41,23,'t2_low','t2_high','delta_t2')
        su3 = read_suction_sensor(ard,3,'80D6A0F5',4,41,24,'t3_low','t3_high','delta_t3')
        su4 = read_suction_sensor(ard,4,'2C1AA158',4,41,25,'t4_low','t4_high','delta_t4')
        su5 = read_suction_sensor(ard,5,'FDF0A043',4,41,26,'t5_low','t5_high','delta_t5')
        su6 = read_suction_sensor(ard,6,'3BF1A0A3',5,42,30,'t6_low','t6_high','delta_t6')
        su7 = read_suction_sensor(ard,7,'6640A1CA',5,42,31,'t7_low','t7_high','delta_t7')  
        su8 = read_suction_sensor(ard,8,'FAF0A0C6',5,42,32,'t8_low','t8_high','delta_t8')
        su9 = read_suction_sensor(ard,9,'F1F0A03E',5,42,33,'t9_low','t9_high','delta_t9')
        su10 = read_suction_sensor(ard,10,'381AA1DF',5,42,34,'t10_low','t10_high','delta_t10') 

#----------------------------teros-12 (GS3)------------------------------------

        teros1 = read_teros(ard,1,50,44,'raw1','ec1')
        teros2 = read_teros(ard,2,50,45,'raw2','ec2')
        teros3 = read_teros(ard,3,50,46,'raw3','ec3')
        teros4 = read_teros(ard,4,53,47,'raw4','ec4')
        teros5 = read_teros(ard,5,52,48,'raw5','ec5')
        teros6 = read_teros(ard,6,51,49,'raw6','ec6')
    
#---------------------------------scales---------------------------------------
        
        scale1 = read_scale(PORT_SCALE_1,'scale1')  
        scale2 = read_scale(PORT_SCALE_2,'scale2')
 
#------------------Switch on the light and take a photo------------------------    
# using pi@wwl_cali to control pi@pizero_camera to take photo when the light is on
    
        ard.write("power_switch,28,power_switch_status,1")
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("Taking photo ......")
        time.sleep(5)
        try: 
            process=subprocess.Popen('/home/pi/script/ssh_to_campera_take_photo.sh', stdout=subprocess.PIPE)
        except:
            pass
        time.sleep(15)
        ard.write("power_switch,28,power_switch_status,0")
        time.sleep(3)

#----------------------------Upload data now-----------------------------------    
    
        ard.close()
    
        client.publish('v1/devices/me/telemetry', json.dumps(wwl_cali), 1)    
        upload_phant(pht_wwl_cali,wwl_cali,SCREEN_DISPLAY)
    
        if SAVE_TO_FILE: fid.write("\n\r")
        time.sleep(SLEEP_TIME_SECONDS) # sleep to the next loop

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
