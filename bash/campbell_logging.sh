#!/bin/bash
# this scripts wirte the detail about what is going to be sent through email
# for example the new ip address, whether the sensors/programs is working and so on.

sleep 38 
cd /home/pi/pyduino/python/
#python rs232_adam.py
python  campbell_logging.py   >>aster_log

