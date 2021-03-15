

in *~/.bashrc* put in

```
if [ -f ~/pyduino/bash/pyduino_variables.sh ]; then
   source  ~/pyduino/bash/pyduino_variables.sh
fi
```

in *~/pyduino/bash/pyduino_variables* put in

```
#!/bin/bash
### below are the variables for pyduino, put in /home/pi/arduino/bash/arduino_variables.sh
# becareful that ssh_port_on_sftp_uqgec ssh_monitoring_port_on_sftp_uqgec and ssh_monitoring_port_on_sftp_uqgec+1 should be unique for all the ports for the server. for example, if one client is using ssh_port_on_sftp_uqgec=1999 ssh_monitoring_port_on_sftp_uqgec=20008, the second client should never use ssh_monitoring_port_on_sftp_uqgec=20009 as the previous client uses 20009 as returing heartbeating port
# also note that there is no space on both side of '='


ssh_username_first_channel=sftp
ssh_port_first_channel=1967
ssh_monitoring_port_first_channel=20017
ssh_address_first_channel=www.abc.def
ssh_credential_path_first_channel=/home/pi/.ssh/id_rsa_sftp_uqgec

ssh_username_second_channel=sftp
ssh_port_second_channel=1967
ssh_monitoring_port_second_channel=20015
ssh_address_second_channel=www.xyz.cloud.edu.au
ssh_credential_path_second_channel=/home/pi/.ssh/abc

secondary_data_server=www.xxx.cloud.edu.au

vnc_server_address=xxx.uq.edu.au
vnc_monitoring_port=20009
vnc_ssh_forward_port=1985
vnc_forward_port=1986


ssh_scp_photo_address=username@servername:/address/to/server/name/
local_photo_address=/home/pi/

```


