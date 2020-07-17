#!/bin/bash
## following parameters needs to be defined in bashrc
#ssh_port_on_sftp_uqgec=1997
#ssh_monitoring_port_on_sftp_uqgec=20003
#uqgec_ssh_address=www.xxxud.edu.au
#uqgec_data_server=xxxx.abc.org
#uqgec_phant_server=xxx.abc.:8090


source ~/pyduino/bash/pyduino_variables_second.sh
ssh-keygen -f "/home/pi/.ssh/known_hosts" -R ${uqgec_ssh_address}  # this line is executed in case when the ip in uqgec is changed
AUTOSSH_DEBUG=1 AUTOSSH_LOGLEVEL=7 AUTOSSH_LOGFILE=/home/pi/autossh_debug_3 autossh -M ${ssh_monitoring_port_on_sftp_uqgec} -f  -o "StrictHostKeyChecking=no" -o "ServerAliveInterval=12000" -o "ServerAliveCountMax=10"  -o "ExitOnForwardFailure=Yes"  -i ~/.ssh/id_rsa_sftp_uqgec -N sftp@${uqgec_ssh_address} -R ${ssh_port_on_sftp_uqgec}:localhost:22  -C

