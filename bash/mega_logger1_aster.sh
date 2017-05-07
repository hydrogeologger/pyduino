#!/bin/bash
# this scripts wirte the detail about what is going to be sent through email
# for example the new ip address, whether the sensors/programs is working and so on.

sleep 18 
#su pi
cd /home/pi/pyduino/python/
#python rs232_adam.py
python mega_logger1_aster.py  >>aster_log

