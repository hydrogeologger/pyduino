#!/bin/bash
#   Exports pin to userspace
echo "27" > /sys/class/gpio/export                  

# Sets pin 18 as an output
echo "out" > /sys/class/gpio/gpio18/direction

# Sets pin 18 to high
echo "1" > /sys/class/gpio/gpio18/value

sleep 5

# Sets pin 18 to low
echo "0" > /sys/class/gpio/gpio18/value 

sleep 5

echo -n "RESET" > /dev/ttyS0
/sbin/shutdown -h now
