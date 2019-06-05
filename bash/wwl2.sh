#!/bin/bash
sleep 23
#su pi
cd /home/pi/pyduino/python/
# debug code
#/usr/bin/stdbuf -i0 -o0 -e0 python  wwl2.py >>wwl2 2>&1
#normal code
python  wwl2.py >>wwl2 2>&1

