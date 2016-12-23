#!/bin/bash
# this scripts wirte the detail about what is going to be sent through email
# for example the new ip address, whether the sensors/programs is working and so on.

sleep 5 
cd /home/pi/pyduino/python/
python read_moist_DS18x20_sht11_bp_phant.py
