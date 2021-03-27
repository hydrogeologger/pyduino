#!/bin/bash
# ADD ACCESS_TOKEN and TB_DOMAIN variables in /pyduino/credential/tb.sh
machine_name=$(cat /etc/hostname)
ip_address=$(hostname -I|xargs)
# ip_address=$(hostname -I|xargs| tr -d '[:space:]')
date=$(date)
#volume=$(df -Hh|grep root| tr -d '[:space:]')
key=$ip_address
log_file=/home/pi/internet_connection.log
source /home/pi/pyduino/credential/tb.sh
#Fix the problem where CRONTAB does not get the environmental variables in .bashrc
#echo $ACCESS_TOKEN (for debug)
#echo $TB_DOMAIN (for debug)
#curl "http://144.6.225.24:8080/input/$sparkfun_public_key?private_key=$sparkfun_private_key&ip=$ip_address&name=$machine_name&volume=$volume"
#curl "http://monitoring.uqgec.org:8080/devices/ACCESS_TOKE=$ACCESS_TOKEN&key=$key&value=$ip_address"
#tb_domain=$(cat /home/pi/pyduino/credential/tb_domain)
#access_token=$(cat /home/pi/pyduino/credential/access_token)

curl -v -d "{$(cat /etc/hostname): \"$ip_address\"}" $TB_DOMAIN/api/v1/$ACCESS_TOKEN/telemetry --header "Content-Type:application/json"


#echo $date >> $log_file

curl_outcome=$?
#echo $curl_outcome  >> $log_file

sleep 1


wget -q --spider http://google.com

wget_outcome=$?

#echo $wget_outcome  >> $log_file

sleep 1


echo -e "GET http://google.com HTTP/1.0\n\n" | nc google.com 80 > /dev/null 2>&1

echo_outcome=$?

#echo $echo_outcome  >> $log_file

sleep 1
if [ $curl_outcome -eq 0 ]  &&  [ $wget_outcome -eq 0 ]  &&  [ $echo_outcome -eq 0 ]  ; then
    echo "${date} ${curl_outcome}  ${wget_outcome}  ${echo_outcome}  Online 2"  >> $log_file
else
    echo "${date} ${curl_outcome}  ${wget_outcome}  ${echo_outcome}  offline 2"  >> $log_file
fi

