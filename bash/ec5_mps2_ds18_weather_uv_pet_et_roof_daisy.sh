#!/bin/bash
# this scripts wirte the detail about what is going to be sent through email
# for example the new ip address, whether the sensors/programs is working and so on.

sleep 18 
#su pi
cd /home/pi/pyduino/python/
#python rs232_adam.py
#python ec5_mps2_ds18_weather_uv_pet_et_roof_daisy.py >>daisy_log
# https://stackoverflow.com/questions/3465619/how-to-make-output-of-any-shell-command-unbuffered
#/usr/bin/stdbuf -i0 -o0 -e0 python ec5_mps2_ds18_weather_uv_pet_et_roof_daisy.py >>daisy_log 2>&1
/usr/bin/stdbuf -i0 -o0 -e0 python daisy_prototype_logger.py >>daisy_log 2>&1

