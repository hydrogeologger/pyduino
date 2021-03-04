#!/bin/bash
## following parameters needs to be defined in bashrc
#ssh_port_on_sftp_uqgec=1997
#ssh_monitoring_port_on_sftp_uqgec=20003
#uqgec_ssh_address=www.xxxud.edu.au
#uqgec_data_server=xxxx.abc.org
#uqgec_phant_server=xxx.abc.:8090


sleep 80
source ~/pyduino/bash/pyduino_variables.sh
ssh-keygen -f "/home/pi/.ssh/known_hosts" -R ${ssh_address_second_channel}  # this line is executed in case when the ip in uqgec is changed
AUTOSSH_DEBUG=1 AUTOSSH_LOGLEVEL=7 AUTOSSH_LOGFILE=/home/pi/autossh_debug_2 \
    autossh -M ${ssh_monitoring_port_second_channel}  -f  -o "StrictHostKeyChecking=no" -o "ServerAliveInterval=12000" \
    -o "ServerAliveCountMax=10"  -o "ExitOnForwardFailure=Yes"  \
    -i ${ssh_credential_path_second_channel} \
    -N ${ssh_username_second_channel}@${ssh_address_second_channel} \
    -R ${ssh_port_second_channel}:localhost:22  -C

