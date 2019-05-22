import paho.mqtt.client as mqtt
import json

with open('/home/pi/pyduino/credential/humchamber.json') as f: credential = json.load(f) #,object_pairs_hook=collections.OrderedDict)

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

humchamber {'value1' : 1, 'value2' : 2}
while True:
    client.publish('v1/devices/me/telemetry', json.dumps(humchamber), 1)
    sleep(1)

client.loop_stop()
client.disconnect()


