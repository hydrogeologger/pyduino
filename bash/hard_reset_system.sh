#!/bin/bash
# shellcheck source-path=SCRIPTDIR source=reset_mcu.sh
source "$(dirname "${BASH_SOURCE[0]}")/reset_mcu.sh"

buffer_seconds=10
while [ $buffer_seconds -gt 0 ]; do
   echo -ne "Killing all python processes, shutdown RPI and perform power cycle in ${buffer_seconds}s\033[0K\r"
   sleep 1
   : $((buffer_seconds--))
done

echo -ne "Killing all python processes, shutdown RPI and perform power cycle in ${buffer_seconds}s\033[0K\r\n"
pkill -f python
sleep 5

if ! mcu_comms_is_good; then
    echo "MCU serial not responsive!"
    reset_mcu
    sleep 1
else
    echo "MCU serial is responsive."
fi

echo -ne "RESET" > "$TTY_PORT"
read -r -e -t 1 < "$TTY_PORT"
# sleep 1
sudo /sbin/shutdown -h now
