#!/bin/bash
sleep 23
#su pi
cd /home/pi/pyduino/python/
/usr/bin/stdbuf -i0 -o0 -e0 python  grange_4_type_abd_column_6.py >>grange_4_type_abd_column_6 2>&1

