#!/bin/bash
sleep 33 
#su pi
cd /home/pi/pyduino/python/
/usr/bin/stdbuf -i0 -o0 -e0 python  bacteria.py >>bacteria 2>&1

