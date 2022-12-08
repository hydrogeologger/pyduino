#!/bin/bash

# Script to setup RPI as ethernet gadget over usb, i.e. SSH over USB

# Check if script is running as root
if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

function enable_ssh_over_usb() {
    echo "Configuring RPI for SSH over USB..."

    local CONFIG_FILE
    local CMDLINE_FILE
    CONFIG_FILE="/boot/config.txt"
    CMDLINE_FILE="/boot/cmdline.txt"

    if ! grep -q "^dtoverlay=dwc2$" "$CONFIG_FILE"; then
        printf "\n# Enable Ethernet USB Gadget (SSH Over USB)\ndtoverlay=dwc2" >> "$CONFIG_FILE"
    fi

    sed -i "/.*modules-load=dwc2,g_ether.*/! s/rootwait/rootwait modules-load=dwc2,g_ether/" "$CMDLINE_FILE"

    # shellcheck disable=SC2034  # unused variable used in same shell by other script
    ASK_TO_REBOOT=true
}


enable_ssh_over_usb
systemctl restart avahi-daemon