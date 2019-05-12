

in *~/.bashrc* put in

```
if [ -f ~/pyduino/bash/pyduino_variables.sh ]; then
   source  ~/pyduino/bash/pyduino_variables.sh
fi
```

in *~/pyduino/bash/pyduino_variables* put in

```
#!/bin/bash
### below are the variables for pyduino
# becareful that ssh_port_on_sftp_uqgec ssh_monitoring_port_on_sftp_uqgec and ssh_monitoring_port_on_sftp_uqgec+1 should be unique for all the ports for the server. for example, if one client is using ssh_port_on_sftp_uqgec=1999 ssh_monitoring_port_on_sftp_uqgec=20008, the second client should never use ssh_monitoring_port_on_sftp_uqgec=20009 as the previous client uses 20009 as returing heartbeating port
ssh_port_on_sftp_uqgec=1997
ssh_monitoring_port_on_sftp_uqgec=20003
uqgec_ssh_address=www.xxxud.edu.au
uqgec_data_server=xxxx.abc.org
uqgec_phant_server=xxx.abc.:8090

```
