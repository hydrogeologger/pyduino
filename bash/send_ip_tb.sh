#!/bin/bash
sleep 20
# ADD ACCESS_TOKEN and TB_DOMAIN variables in /pyduino/credential/tb.sh
machine_name=$(cat /etc/hostname)
ip_address=$(hostname -I|xargs)
# ip_address=$(hostname -I|xargs| tr -d '[:space:]')
date=$(date)
#volume=$(df -Hh|grep root| tr -d '[:space:]')
key=$ip_address
source /home/pi/pyduino/credential/tb.sh
#Fix the problem where CRONTAB does not get the environmental variables in .bashrc
#echo $ACCESS_TOKEN (for debug)
#echo $TB_DOMAIN (for debug)
#curl "http://144.6.225.24:8080/input/$sparkfun_public_key?private_key=$sparkfun_private_key&ip=$ip_address&name=$machine_name&volume=$volume"
#curl "http://monitoring.uqgec.org:8080/devices/ACCESS_TOKE=$ACCESS_TOKEN&key=$key&value=$ip_address"
#tb_domain=$(cat /home/pi/pyduino/credential/tb_domain)
#access_token=$(cat /home/pi/pyduino/credential/access_token)

curl -v -d "{$(cat /etc/hostname): \"$ip_address\"}" $TB_DOMAIN/api/v1/$ACCESS_TOKEN/telemetry --header "Content-Type:application/json"
#curl -v -X POST -d "{$(cat /etc/hostname): $ip_address}" $TB_DOMAIN/api/v1/$ACCESS_TOKEN/telemetry --header "Content-Type:application/json"

#curl "http://144.6.225.24:8080/input/$sparkfun_public_key?private_key=$sparkfun_private_key&ip=$ip_address&name=$machine_name&volume=$ip_address"
#curl "http://144.6.225.24:8080/input/$sparkfun_public_key?private_key=$sparkfun_private_key&ip=$ip_address&name=$machine_name"
