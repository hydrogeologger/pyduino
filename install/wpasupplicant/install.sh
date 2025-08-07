#!/bin/bash

# Script to setup wpa_supplicant


# Check if script is running as root
if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi


readonly WPA_CONF="/etc/wpa_supplicant/wpa_supplicant.conf"
# WPA_CONF="./wpa_supplicant.conf"

## Source ##
# shellcheck source=SCRIPTDIR/../common.sh
source "$(dirname "${BASH_SOURCE[0]}")/../common.sh"

usage() {
    echo "Usage: install    [ -n | --name SSID Name ]
                  [ -u | --user Username ]
                  [ -p | --password Password ]
                  [ -r | --reset ]
                  [ -d | --debug ]"
    exit 2
}


function reset_wpa_supplicant_file() {
    echo "Resetting wpa_supplicant.conf file..."
    transfer_conf_files_from_path "$(dirname "${BASH_SOURCE[0]}")/files"
    
    chmod 600 $WPA_CONF
    chown root:root $WPA_CONF
}

function setup_eduroam_wpa() {
    local eduroam_username
    local eduroam_password
    local eduroam_password2
    local eduroam_hashed_password

    if [ $# -eq 2 ]; then
        eduroam_username="$1"
        eduroam_password="$2"
    else
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
    fi

    # Convert password to utf16 little endian hashed password
    # https://wiki.archlinux.org/title/Wpa_supplicant#802.1x/radius
    # As of openssl 3.x.x, md4 provider moved to legacy, Attempt to use MD4 with the legacy provider
    if openssl dgst -md4 -provider legacy /dev/null &>/dev/null; then
        eduroam_hashed_password=$(echo -n "${eduroam_password}" | iconv -t utf16le | openssl dgst -md4 -provider legacy)
    else
        eduroam_hashed_password=$(echo -n "${eduroam_password}" | iconv -t utf16le | openssl md4)
    fi
    eduroam_hashed_password=${eduroam_hashed_password#"(stdin)= "}


    # Edit wpa_supplicant.conf with username and hashed password
    # sed -i "s/identity.*/identity=\"$eduroam_username\"/" $CONF
    # sed -i "s/password.*/password=hash:$eduroam_hashed_password/" $CONF
    sed -i -e "s/identity=\".*\"/identity=\"$eduroam_username\"/" \
            -e "s/password=.*/password=hash:$eduroam_hashed_password/" $WPA_CONF

    # Notes for blanking details
    # sed -i  "s/identity.*/identity=\"\"/" $CONF
    # sed -i  "s/password.*/password=\"\"/" $CONF

    # Change network priority
    # sed -i "s/priority=[0-9]*/priority=1/" $CONF
    # priority for normal APN
    # sed -i "/^\s*ssid=\"eduroam\"/{n; s/\(\s*\).*/\1priority=1/}" $WPA_CONF
    # Priority for eduroam
    # sed -i "/ssid=\"[^e][^d][^u][^r][^o][^a][^m]\"/ n; {n; s/\(\s*\)priority=[0-9]*/\1priority=0/}" $WPA_CONF

    ASK_TO_REBOOT=true
}

function setup_normal_wpa() {
    local ssid_name
    local ssid_psk
    local ssid_psk2
    local wpa_passphrase_output
    local show_raw_psk

    if [ $# -eq 2 ]; then
        ssid_name="$1"
        ssid_psk="$2"
    else
        while true; do
            # Request SSID from user
            read -r -p "Enter SSID Name: " ssid_name

            # Request SSID password from user, echo turned off
            read -s -r -p "Enter password for $ssid_name: " ssid_psk
            echo
            read -s -r -p "Repeat password for $ssid_name: " ssid_psk2
            echo # Turn it back on
            [ "$ssid_psk" = "$ssid_psk2" ] && break
            echo "Please try again."
        done
    fi

    # Update ssid, Skip line matching ssid="eduroam"
    sed -i "/ssid=\"eduroam\"/ n; s/ssid=\".*\"/ssid=\"$ssid_name\"/" $WPA_CONF

    # Update psk for ssid
    read -r -p "Store unhashed password in wpa_supplicant? [Y/N] " show_raw_psk
    if printf "%s\n" "$show_raw_psk" | grep -Eq "$(locale yesexpr)"; then
        sed -i "/^\s*#psk=\".*\"/s/psk=.*$/psk=\"$ssid_psk\"/" $WPA_CONF
    else
        sed -i "/^\s*#psk=\".*\"/s/psk=.*$/psk=\"apn_password\"/" $WPA_CONF
    fi
    wpa_passphrase_output=$(wpa_passphrase "$ssid_name" "$ssid_psk")
    # echo -e "$wpa_passphrase_output"
    ssid_psk=${wpa_passphrase_output/*psk=/}
    ssid_psk=${ssid_psk/?\}/}
    # echo "\"$ssid_psk\""
    sed -i "/^\s*psk=.*/s/psk=.*$/psk=$ssid_psk/" $WPA_CONF

    # Change network priority
    # sed -i "/^\s*ssid=\"$ssid_name\"/{n; s/\(\s*\).*/\1priority=1/}" $WPA_CONF
    # sed -i "/^\s*ssid=\"eduroam\"/{n; s/\(\s*\).*/\1priority=0/}" $WPA_CONF

    # sed "/^\s*ssid=\"$ssid_name\"/{ n; s/\(\s*priority\)\=.*/\1=2/; t; /a priority=2 }" $WPA_CONF
    # sed "/Line1/{N; /\nString$/b; s/\n/\nString\n/}" file
    # sed "/^\s*ssid=\"$ssid_name\"/{N; /\(\s*\)priority=.*$/b; s/\n/\nString\n/}" $WPA_CONF

    # shellcheck disable=SC2034  # unused variable used in same shell by other script
    ASK_TO_REBOOT=true
}

function force_wpasupplicant_connect() {
    echo "Force current wpa_supplicant config connection..."
    # Enable wlan0 interface
    ifconfig wlan0 up

    # Force load new wpa_supplicant.conf for current session
    # rm /var/run/wpa_supplicant/wlan0
    wpa_cli -i wlan0 terminate
    systemctl restart wpa_supplicant.service
    wpa_supplicant -B -i wlan0 -c "$WPA_CONF"

    # Force DHCP client to renew IP address
    dhclient -r wlan0
}

function interactive_wpasupplicant_setup() {
    echo "What are you setting up?"
    select option in "Reset" "Eduroam" "Other" "Nothing" "Exit"; do
        case $option in
            Reset ) reset_wpa_supplicant_file;;
            Eduroam ) setup_eduroam_wpa; break;;
            Other ) setup_normal_wpa; break;;
            Nothing ) break;;
            Exit ) exit 0;;
        esac
    done
}

# --- basic packages   ------------------------------------------------------
# PACKAGES+=" wpasupplicant"

# cp -v ./files/etc/wpa_supplicant/wpa_supplicant.conf $CONF


## MAIN ##
function main() {
    local PARSED_ARGUMENTS
    local PARSED_ARGUMENTS_VALID
    local F_NAME=""
    local F_USER=""
    local F_PSK=""
    local F_RESET=false
    PARSED_ARGUMENTS=$(getopt -n install -o drn:u:p: --long debug,reset,name:,user:,password: -- "$@")
    PARSED_ARGUMENTS_VALID=$?
    if [ "$PARSED_ARGUMENTS_VALID" != 0 ]; then
        usage
    fi
    eval set -- "$PARSED_ARGUMENTS"

    while test "X$1" != "X--"; do
        case "$1" in
            -n|--name)
                F_NAME="$2"
                shift
                ;;
            -u|--user)
                F_USER="$2"
                shift
                ;;
            -p|--password)
                F_PSK="$2"
                shift
                ;;
            -d|--debug)
                echo "PARSED_ARGUMENTS is $PARSED_ARGUMENTS"
                ;;
            -r|--reset)
                F_RESET=true
                ;;
            # -- means the end of the arguments; drop this, and break out of the while loop
            --) shift; break;;
            # If invalid options were passed, then getopt should have reported an error,
            # which we checked as VALID_ARGUMENTS when getopt was called...
            *)
                echo "Unexpected option: $1 - this should not happen."
                usage
                ;;
            esac
        shift
    done
    shift #get rid of the '--'

    if [[ $F_NAME == "eduroam" ]]; then
        if $F_RESET; then reset_wpa_supplicant_file; fi
        echo "Setting up connection for $F_NAME..."
        if [[ $F_USER != "" && $F_PSK != "" ]]; then
            setup_eduroam_wpa "$F_USER" "$F_PSK"
        else
            setup_eduroam_wpa
        fi
    elif [[ $F_NAME != "" && $F_NAME != "eduroam" ]]; then
        if $F_RESET; then reset_wpa_supplicant_file; fi
        echo "setting up connection for $F_NAME..."
        if [[ $F_PSK != "" ]]; then
            setup_normal_wpa "$F_NAME" "$F_PSK"
        else
            setup_normal_wpa
        fi
    else
        usage
    fi
}

echo "Setting up wireless..."
if [ $# -eq 0 ]; then
    interactive_wpasupplicant_setup
else
    main "$@"
fi

# Force wpa_supplicant config connect if file not sourced
if test ${#BASH_SOURCE[@]} -eq 1; then
    force_wpasupplicant_connect
fi