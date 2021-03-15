#!/bin/bash
echo -n "RESET" > /dev/ttyS0
/sbin/shutdown -h now
