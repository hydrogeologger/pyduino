#!/bin/bash

# Script to setup Armbian system as ethernet gadget over usb, i.e. SSH over USB
# https://gist.github.com/nikp123/c658b31c45288b55141c9d19ede78e6c
# https://forum.armbian.com/topic/6057-orange-pi-zero-plus-as-an-ethernet-gadget/
# http://trac.gateworks.com/wiki/linux/OTG
# Only usbhost0 needs to be enabled as bare minimum

# Check if script is running as root
if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

function enable_ssh_over_usb() {
    local CONFIG_FILE
    local CMDLINE_FILE
    local USB_DEVICE_MODE

    CONFIG_FILE="/etc/modules"
    CMDLINE_FILE="/boot/armbianEnv.txt"

    # Acceptable modes (g_serial|g_ether|g_cdc)
    # g_ether: usb device appear as ethernet device
    # g_serial: usb device appera as serial device
    # g_cdc: usb device appears as composite ethernet and serial device
    USB_DEVICE_MODE="g_ether"

    echo "Configuring Arbmian device as $USB_DEVICE_MODE gadget for SSH over USB..."


    if ! grep -q "^modules-load=dwc2,g_.*$" "$CMDLINE_FILE"; then
        ## add line
        sed -i -e "/^overlays=.*$/a modules-load=dwc2,$USB_DEVICE_MODE" "$CMDLINE_FILE"
    else
        # replace line
        sed -i "s/^modules-load=.*$/modules-load=dwc2,$USB_DEVICE_MODE/" "$CMDLINE_FILE"
    fi

    # Change default usb device behavior
    sed -i "/^$USB_DEVICE_MODE$/! s/^g_.*$/$USB_DEVICE_MODE/" "$CONFIG_FILE"

    # TODO: Examine with g_ether only show inet6, and g_cdc does not show inet or inet6
    #       from ifconfig

    # shellcheck disable=SC2034  # unused variable used in same shell by other script
    ASK_TO_REBOOT=true
}


# shellcheck source=SCRIPTDIR/../common.sh
source "$(dirname "${BASH_SOURCE[0]}")/../common.sh"
# shellcheck source-path=SCRIPTDIR
# source "$(dirname "$0")/../common.sh"

transfer_conf_files_from_path "$(dirname "${BASH_SOURCE[0]}")/files"
enable_ssh_over_usb

install_packages avahi-daemon

# modprobe g_ether