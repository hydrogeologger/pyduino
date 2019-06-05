#!/bin/bash
sleep 23
#su pi
cd /home/pi/pyduino/python/davis_wind
#/usr/bin/stdbuf -i0 -o0 -e0 python  UQ_davis_wind.py >>davis_weather 2>&1
python  UQ_davis_wind.py >>davis_weather 2>&1

