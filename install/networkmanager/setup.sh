#!/bin/bash

# Script to setup NetworkManager for systems that employs NetworkManager instead
# of wpa_supplicant to manage networks.

# References
# https://networkmanager.dev
# https://wiki.archlinux.org/title/NetworkManager

## NMCLI NOTES for connecting to eduroam
# nmcli connection add type wifi con-name "eduroam" ifname wlan0 ssid "eduroam" wifi-sec.key-mgmt wpa-eap 802-1x.system-ca-certs no 802-1x.eap "peap" 802-1x.phase2-auth mschapv2 802-1x.identity "exampleemail@brandeis.edu" 802-1x.password "examplepassword123"
# nmcli connection up eduroam --ask

function setup_eduroam_nmcli() {
    echo "Setting up eduroam connection with NetworkManager..."
    local eduroam_username
    local eduroam_password
    local eduroam_password2
    local eduroam_hashed_password

    if [ $# -eq 2 ]; then
        eduroam_username="$1"
        eduroam_password="$2"
    else
        return 1
    fi

    # MD4 Hashed password doesn't work for NM, use wpa_passphrase
    eduroam_hashed_password=$(wpa_passphrase "eduroam" "${eduroam_password}" | awk -F= '/[^#]psk=/ { printf $2 }' OFS='\t')

    nmcli connection add \
        type wifi \
        con-name "eduroam" \
        ifname wlan0 \
        ssid "eduroam" \
        wifi-sec.key-mgmt wpa-eap \
        802-1x.system-ca-certs no \
        802-1x.eap "peap" \
        802-1x.phase2-auth mschapv2 \
        802-1x.identity "$eduroam_username" \
        802-1x.password "$eduroam_hashed_password"
}

function setup_eduroam_nmcli_prompt() {
    local eduroam_username
    local eduroam_password

    while true; do
        # Get username for eduroam
        read -r -p "Enter eduroam username: " eduroam_username

        # Get password for eduroam and hash user input
        # turn off terminal echoing
        read -s -r -p "Enter eduroam password: " eduroam_password
        echo
        read -s -r -p "Repeat eduroam password: " eduroam_password2
        echo # Turn it back on
        [ "$eduroam_password" = "$eduroam_password2" ] && break
        echo "Please try again."
    done

    setup_eduroam_nmcli "$eduroam_username" "$eduroam_password"
    nmcli connection up eduroam --ask
}

echo "Setting up wireless..."
if [ $# -eq 0 ]; then
    setup_eduroam_nmcli_prompt
fi
