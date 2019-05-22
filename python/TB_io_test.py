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
    if data['method'] is 'setValue':
        if data['params'] is True:
            ard.write("power_switch,10,power_switch_status,0")
            ard.flushInput()
            ard.readline()
        if data['params'] is False:
            ard.write("power_switch,10,power_switch_status,255")
            ard.flushInput()
            ard.readline()


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


