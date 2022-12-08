#!/bin/bash

# Script for initial setup/configuration of either RaspberryPI or BananaPI system
# https://raspberrypi.stackexchange.com/a/71587
# try bluez-5.50-1.2~deb10u3

# Check if script is running as root
if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

# Code snippet from https://github.com/bablokb/pi-btnap
BT_CONF_DNSMASQ="0"       # do not install dnsmasq (supported values: 0|1)
BT_CONF_HIDDEN="0"        # system is permanently discoverable/pairable
                          # supported values: 0|1

function bluez_noinputnooutput_bug_workaround() {    
    local CONF_FILE="/home/pi/bt-agent-pins.conf"
    readonly CONF_FILE

    echo "Implementing bluez NoInputNoOutput bug workaround..."

    # Create pin file to allow all passcode for all device mac
    echo "* *" > "$CONF_FILE"

    # Change bt-agent launch parameter
    # sed -i -e "s/^[^#]\(.*\)\(NoInputNoOutput\)/# \1\2/" \
    #         -e "s/^\#\s*\(.*\)\(DisplayOnly\)\(.*\)/\1\2\3/" \
    #         /etc/systemd/system/bt-agent.service
    sed -i -e "s/NoInputNoOutput/DisplayOnly -p ${CONF_FILE//\//\\/}/" \
            /etc/systemd/system/bt-agent.service
}

# shellcheck source=/dev/null
source "$(dirname "${BASH_SOURCE[0]}")/../common.sh"

# --- basic packages   ------------------------------------------------------
PACKAGES="bluetooth bluez bluez-tools"
[ "$BT_CONF_DNSMASQ" = "1" ] && PACKAGES+=" dnsmasq"

# shellcheck disable=SC2086  # Specifically want word splitting
install_packages $PACKAGES

transfer_conf_files_from_path "$(dirname "${BASH_SOURCE[0]}")/files"

# Copy system and network files
# cp -rv ./common/bluetooth_pan/files/. /
# cp -r -v "$(dirname "$0")/$FILE_PATH/." /

# sudo rm /etc/systemd/network/pan0.* && sudo rm /etc/systemd/system/bt*
# sudo rm /etc/systemd/system/bt*

chmod 644 /etc/systemd/system/bt-agent.service
chmod 644 /etc/systemd/system/bt-network.service
chown root:root /etc/systemd/system/bt-agent.service
chown root:root /etc/systemd/system/bt-network.service

echo "" # Empty to print newline
echo "Would you like you implement bluez NoInputNoOutput pairing workaround?"
select option in "Yes" "No"; do
    case $option in
        Yes ) bluez_noinputnooutput_bug_workaround; break;;
        No ) true; break;;
    esac
done


# Unblock bluetooth
rfkill unblock bluetooth

# Enable and start bluetooth personal area network as service
systemctl enable systemd-networkd
systemctl enable bt-agent
systemctl enable bt-network
systemctl start systemd-networkd
systemctl start bt-agent
systemctl start bt-network

# Set bluetooth network to be discoverable
bt-adapter --set Discoverable 1

if [ $BT_CONF_HIDDEN -eq 0 ]; then
    sed -i -e "/DiscoverableTimeout/s/^.*$/DiscoverableTimeout = 0/" \
            -e "/PairableTimeout/s/^.*$/PairableTimeout = 0/" \
            /etc/bluetooth/main.conf
else
    sed -i -e "/DiscoverableTimeout/s/^.*$/#DiscoverableTimeout = 0/" \
            -e "/PairableTimeout/s/^.*$/#PairableTimeout = 0/" \
            /etc/bluetooth/main.conf
fi

## Some problems when enabling systemd-networkd,
# it also enables systemd-networkd-wait-online which expects interfaces to be
# connected and waits for it to connect.
# https://wiki.archlinux.org/title/systemd-networkd
# Non fullproof workaround, disable the service
systemctl stop systemd-networkd-wait-online.service
systemctl disable systemd-networkd-wait-online.service
