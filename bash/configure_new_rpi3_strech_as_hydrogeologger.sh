#!/bin/bash

systemctl enable ssh
systemctl start ssh
apt update
apt install vim tmux tightvncserver ipython autossh mplayer python
sed -i '${s/raspberrypi/hydrogeologger/}' /etc/hosts
sed -i '${s/raspberrypi/hydrogeologger/}' /etc/hostname


#https://raspberrypi.stackexchange.com/questions/14229/how-can-i-enable-the-camera-without-using-raspi-config



#su pi
##this is runnings as normal users
#ssh-keygen
#python phant
#send ip copy script
#disable serial 
#enable pycamera
#add cron to send ip address
