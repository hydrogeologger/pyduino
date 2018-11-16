#!/bin/bash
# this scripts wirte the detail about what is going to be sent through email
# for example the new ip address, whether the sensors/programs is working and so on.

sleep 33
#su pi
cd /home/pi/pyduino/python/
/usr/bin/stdbuf -i0 -o0 -e0 python   area51_2mo_3heatsuc_2salt_2drsuc_2gs3_compacted_redmud.py >>area51_log
