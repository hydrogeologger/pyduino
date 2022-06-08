#!/usr/bin/env python
# import os
import sys
# sys.path.insert(0, '/home/pi/pyduino/python/lib')
import time
import json
# Append private python library to system path
# import hydrogeolog
import paho.mqtt.client as mqtt
sys.path.append("/home/pi/pyduino/python/lib")
import mqtthelper

try:
    client = mqtt.Client()
    client.username_pw_set("UPZrVPyU2j5siBCD1IyZ")
    client.connect("www.uqtailingsmonitoringengine.cloud.edu.au", 1883, 60)
    # client.username_pw_set("UPZrVPyU2j5siBCD1IyZ")
    client.connect("www.uqtailingsmonitoringengine.dcloud.edu.au", 1883, 60)
    client.loop_start()

    # clientB = mqtt.Client()
    # clientB.username_pw_set("UPZrVPyU2j5siBCD1IyZ")
    # clientB.connect("www.uqtailingsmonitoringengine.cloud.edu.au", 1883, 60)
    # clientB.loop_start()
except Exception:
    print("Failed to connect to thingsboard")

t = {"gg": 1.1}
t2 = "{\"gg\": 1.1}"
t3 = [1,2,3]
t4 = "[1,2,3]"
t5 = "a:1"

try:
    # time_now = time.time()
    # time_now_local = time.localtime(time_now)
    ms_since_epoch = int(round(time.time() * 1000))
    print(str(ms_since_epoch))
    t0 = {"ts":ms_since_epoch, "values": t}
    # result = client.publish(topic='v1/devices/me/telemetry', payload=json.dumps(""), qos=1)
    # result = hydrogeolog.publish_mqtt_queue(client, "v1/devices/me/telemetry", t, debug=False)
    result = mqtthelper.publish_to_thingsboard(client, t2, ts=ms_since_epoch, filename=None, debug=True)
    print(result._published)
    print(result)
    # result = mqtthelper.publish_to_thingsboard(clientB, t, ts=ms_since_epoch, debug=False)
    # result = hydrogeolog.publish_to_thingsboard(client, t, debug=False)
    # print(client._state)
    # print(result._condition)
    # print(result.is_published())
    # print(result._published)
    # print(result)
    # time.sleep(1.2)
    # print(client._state)
    # print(result.is_published())
    # print(result._published)
    # print(result)
finally:
    client.loop_stop()
    client.disconnect()
    # clientB.loop_stop()
    # clientB.disconnect()
