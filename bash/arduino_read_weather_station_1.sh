#!/bin/bash
# this scripts wirte the detail about what is going to be sent through email
# for example the new ip address, whether the sensors/programs is working and so on.

sleep 3 
#su pi
cd /home/pi/pyduino/python/
#python rs232_adam.py
python read_weather_station_1_ts.py

