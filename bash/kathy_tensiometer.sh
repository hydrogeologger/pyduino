#!/bin/bash
sleep 23
#su pi
cd /home/pi/pyduino/python/
/usr/bin/stdbuf -i0 -o0 -e0 python  kathy_tensiometer.py >>kathy_tensiometer 2>&1

