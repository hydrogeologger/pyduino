#!/bin/bash

# Script to setup wpa_supplicant, on Armbian OS (i.e. BananaPi)
# Armbian uses NetworkManager as default to manage connections

# References
# https://wiki.archlinux.org/title/Network_configuration/Wireless#WPA2_Enterprise

## NMCLI NOTES for connecting to eduroam
# nmcli connection add type wifi con-name "eduroam" ifname wlan0 ssid "eduroam" wifi-sec.key-mgmt wpa-eap 802-1x.system-ca-certs no 802-1x.eap "peap" 802-1x.phase2-auth mschapv2 802-1x.identity "exampleemail@brandeis.edu" 802-1x.password "examplepassword123"
# nmcli connection up eduroam --ask


# Check if script is running as root
if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi


function setup_eduroam_nmcli() {
    echo "Setting up eduroam connection with NetworkManager..."
    local eduroam_username
    local eduroam_password
    local eduroam_hashed_password

    # Get username for eduroam
    read -r -p "Enter eduroam username: " eduroam_username

    # Get password for eduroam and hash user input
    # turn off terminal echoing
    read -s -r -p "Enter eduroam password: " eduroam_password
    echo # Turn it back on

    # Hashed password doesn't appear to work
    # Convert password to utf16 little endian hashed password
    # eduroam_hashed_password=$(echo -n "${eduroam_password}" | iconv -t utf16le | openssl md4)
    # eduroam_hashed_password=${eduroam_hashed_password#"(stdin)= "}


    nmcli connection add type wifi con-name "eduroam" ifname wlan0 \
            ssid "eduroam" wifi-sec.key-mgmt wpa-eap 802-1x.system-ca-certs no \
            802-1x.eap "peap" 802-1x.phase2-auth mschapv2 \
            802-1x.identity "$eduroam_username" 802-1x.password "$eduroam_password";
            # 802-1x.identity "$eduroam_username" 802-1x.password "hash:$eduroam_hashed_password"

    nmcli connection up eduroam --ask
}

function setup_dhcpcd_and_dependencies() {
    echo "Configuring DHCP client..."

    local CONF="/etc/dhcpcd.conf"
    readonly CONF

    install_packages "dhcpcd5"

    # Reconfigure /etc/resolv.conf to be dynamically updated
    # dpkg-reconfigure resolvconf
    # /etc/resolv.conf -> ../run/resolvconf/resolv.conf
    rm /etc/resolv.conf
    ln -s "../run/resolvconf/resolv.conf" "/etc/resolv.conf"

    # Use hardware (MAC) address of the interface as the identifier instead of DHCP unique identifyer (DUID)
    sed -i -e "s/^#clientid$/clientid/" -e "s/^duid$/#duid/" $CONF
    # sed -i -e "s/^#clientid$/clientid/" -e "s/^duid$/#duid/:q" $CONF

    # Enable dhcpcd wpasupplicant hook for dhcpcd to use wpasupplicant for automatic
    # connection
    #https://wiki.archlinux.org/title/dhcpcd#Hooks
    ln -s /usr/share/dhcpcd/hooks/10-wpa_supplicant /usr/lib/dhcpcd/dhcpcd-hooks/10-wpa_supplicant

    systemctl restart dhcpcd.service
}

function resolvconf_disable_dynamic_update() {
    unlink /etc/resolv.conf

    touch /etc/resolv.conf
    chown root:root /etc/resolv.conf
    chmod 644 /etc/resolv.conf
}

function disable_network_manager_dependencies() {
    echo "Disabling NetworkManager and removing eduroam connection..."

    # connections config stored in /etc/NetworkManager/system-connections
    local NM_CONF="/etc/NetworkManager/system-connections/eduroam.nmconnection"
    readonly NM_CONF

    # Edit/delete eduroam config from NetworkManager connections

    # Remove username and password
    sed -i -e "s/identity=.*/identity=@uq.edu.au/" \
            -e "s/password=.*/password=password/" $NM_CONF

    # Delete eduroam connection from NetworkManager
    # nmcli connection delete eduroam

    # LC_ALL=C nmcli --fields UUID,TIMESTAMP-REAL,TYPE con show | grep wifi |  awk '{print $1}' | while read line; \
    # 		do nmcli con delete uuid  $line; done > /dev/null

    sudo systemctl stop NetworkManager.service
    sudo systemctl disable NetworkManager.service
    # sudo systemctl disable NetworkManager-wait-online NetworkManager-dispatcher NetworkManager
}

function wpasupplicant_connect() {
    echo "Connecting to eduroam with wpasupplicant..."
    # Enable wlan0 interface
    ifconfig wlan0 up

    # Force load new wpa_supplicant.conf for current session
    # rm /var/run/wpa_supplicant/wlan0
    wpa_cli terminate
    systemctl restart wpa_supplicant.service
    wpa_supplicant -B -i wlan0 -c "$WPA_CONF"

    # Force DHCP client to renew IP address
    dhclient -r wlan0
}


# shellcheck source=SCRIPTDIR/install.sh
source "$(dirname "${BASH_SOURCE[0]}")/install.sh" "$@"
# shellcheck source=/dev/null
# source "$(dirname "$0")/install.sh"

systemctl disable wpa_supplicant
setup_dhcpcd_and_dependencies
disable_network_manager_dependencies
wpasupplicant_connect

# renable bluetooth?
# https://bbs.archlinux.org/viewtopic.php?id=171357
# https://bbs.archlinux.org/viewtopic.php?id=198718
# https://bbs.archlinux.org/viewtopic.php?id=247566
# https://superuser.com/questions/154587/is-there-a-way-to-refresh-the-current-configuration-used-by-modprobe-with-a-newl
# https://community.home-assistant.io/t/bluetooth-controller-keeps-going-down-reboot-fixes/275468/13
#** https://forum.armbian.com/topic/11990-orangepi-win-plus-no-bluetooth-adapter/
#TODO: Check if hci_uart is in boot/armbianEnv.txt before removing NetworkManager
# https://bbs.archlinux.org/viewtopic.php?id=126603
# https://askubuntu.com/questions/1217252/boot-process-hangs-at-systemd-networkd-wait-online
# https://unix.stackexchange.com/questions/205321/where-should-i-put-hciconfig-hci0-up-for-start-up
# https://forum.armbian.com/topic/16839-bpi-m2-zero-cant-get-spi-to-show/