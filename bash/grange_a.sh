#!/bin/bash
sleep 23
#su pi
cd /home/pi/pyduino/python/
/usr/bin/stdbuf -i0 -o0 -e0 python  grange_type_a.py >>grange_type_a 2>&1

