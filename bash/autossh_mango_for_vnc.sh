#!/bin/bash
## following parameters needs to be defined in bashrc
#ssh_port_on_sftp_uqgec=1997
#ssh_monitoring_port_on_sftp_uqgec=20003
#uqgec_ssh_address=www.xxxud.edu.au
#uqgec_data_server=xxxx.abc.org
#uqgec_phant_server=xxx.abc.:8090
#vnc_server_address=abc.eait.uq.edu.au
#vnc_monitoring_port=20009
#vnc_ssh_forward_port=1985
#vnc_forward_port=1986


source ~/pyduino/bash/pyduino_variables.sh
#AUTOSSH_DEBUG=1 AUTOSSH_LOGLEVEL=7 AUTOSSH_LOGFILE=/home/pi/autossh_debug_vnc autossh -M ${vnc_monitoring_port} -f -o "ServerAliveInterval=12000" -o "ServerAliveCountMax=10"  -o "ExitOnForwardFailure=Yes" -i ~/.ssh/id_rsa_sftp_uqgec -N sftp@${uqgec_ssh_address} -R ${ssh_port_on_sftp_uqgec}:localhost:22 -C
AUTOSSH_DEBUG=1 AUTOSSH_LOGLEVEL=7 AUTOSSH_LOGFILE=/home/pi/autossh_debug_vnc autossh -M ${vnc_monitoring_port} -f -o "ServerAliveInterval=12000" -o "ServerAliveCountMax=10"  -o "ExitOnForwardFailure=Yes" -N uqczhan2@${vnc_server_address} -R ${vnc_ssh_forward_port}:localhost:22 -R ${vnc_forward_port}:localhost:5901 -C

