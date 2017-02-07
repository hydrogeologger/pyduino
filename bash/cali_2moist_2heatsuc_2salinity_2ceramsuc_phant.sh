#!/bin/bash
# this scripts wirte the detail about what is going to be sent through email
# for example the new ip address, whether the sensors/programs is working and so on.

sleep 33
#su pi
cd /home/pi/pyduino/python/
python cali_2moist_2heatsuc_2salinity_2ceramsuc_phant.py

