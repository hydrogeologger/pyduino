#!/bin/bash
sleep 33
#su pi
cd /home/pi/pyduino/python/
/usr/bin/stdbuf -i0 -o0 -e0 python  grange_type_D.py >>grange_type_D 2>&1

