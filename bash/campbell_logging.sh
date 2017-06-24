#!/bin/bash
# this scripts wirte the detail about what is going to be sent through email
# for example the new ip address, whether the sensors/programs is working and so on.

sleep 38 
cd /home/pi/pyduino/python/
p/usr/bin/stdbuf -i0 -o0 -e0 ython  campbell_logging.py   >> campbell_log

