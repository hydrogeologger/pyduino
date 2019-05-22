import paho.mqtt.client as mqtt
import json
import time
import serial



port_sensor = '/dev/ttyS0' # port for serial connection
ard=serial.Serial(port_sensor,timeout=60)



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/devices/me/rpc/request/+')


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    data = json.loads(msg.payload)
    if data['method'] == 'getData':
	ard.write("dht22,54,power,2,points,2,dummies,1,interval_mm,2000,debug,1")
	ard.flushInput()
	msg=ard.readline()
	print(msg)
        current_read=msg.split(',')[0:-1]
	rh = float(current_read[-1])
	t = float(current_read[-2])
	d = {'dht22_rh' : rh, 'dht22_t' : t}
	client.publish('v1/devices/me/telemetry', json.dumps(d), 1)    
    if data['method'] == 'getTermInfo':
	print("term requested")
	d = {
            'ok': True,
            'platform': os.platform(),
            'type': os.type(),
            'release': os.release()
        }
	print(d)
	client.publish('v1/devices/me/telemetry', json.dumps(d), 1)
    if data['method'] == 'setValue':
	print(data['params'])
        if data['params'] is True:
	    print("SWITCH ON")
            ard.write("power_switch,10,power_switch_status,0,debug,1")
            ard.flushInput()
            #print(ard.readline())
        if data['params'] is False:
	    print("SWITCH OFF")
            ard.write("power_switch,10,power_switch_status,255,debug,1")
            ard.flushInput()
            #print(ard.readline())


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set('TUdndmZQO0Ob3sTmM64y')
client.connect('www.uqtailingsmonitoringengine.cloud.edu.au', 1883, 60)

time.sleep(2)


try:
    client.loop_forever()
except KeyboardInterrupt:
    exit()


