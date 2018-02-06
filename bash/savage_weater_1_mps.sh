#!/bin/bash
sleep 13
#su pi
cd /home/pi/pyduino/python/
/usr/bin/stdbuf -i0 -o0 -e0 python  grange_weather_1_mps.py >>grange_weather_1_mps 2>&1

