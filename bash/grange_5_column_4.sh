#!/bin/bash
sleep 23
#su pi
cd /home/pi/pyduino/python/
/usr/bin/stdbuf -i0 -o0 -e0 python  grange_5.py >>grange_5 2>&1

