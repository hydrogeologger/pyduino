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
    # TODO: consider using wpa_passphrase
    eduroam_hashed_password=$(echo -n "${eduroam_password}" | iconv -t utf16le | openssl dgst -md4 -provider legacy)
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
    sed -i "/^\s*ssid=\"eduroam\"/{n; s/\(\s*\).*/\1priority=1/}" $WPA_CONF
    # Priority for eduroam
    sed -i "/ssid=\"[^e][^d][^u][^r][^o][^a][^m]\"/ n; {n; s/\(\s*\)priority=[0-9]*/\1priority=0/}" $WPA_CONF

    ASK_TO_REBOOT=true
}

function setup_normal_wpa() {
    local ssid_name
    local ssid_psk

    if [ $# -eq 2 ]; then
        ssid_name="$1"
        ssid_psk="$2"
    else
        # Request SSID from user
        read -r -p "Enter SSID Name: " ssid_name

        # Request SSID password from user, echo turned off
        read -s -r -p "Enter password for $ssid_name: " ssid_psk
        echo # Turn echo back on
    fi

    # Update ssid, Skip line matching ssid="eduroam"
    sed -i "/ssid=\"eduroam\"/ n; s/ssid=\".*\"/ssid=\"$ssid_name\"/" $WPA_CONF

    # Update psk for ssid
    sed -i "/^\s*psk=\".*\"/s/psk=\"<psk>\"$/psk=\"$ssid_psk\"/" $WPA_CONF

    # Change network priority
    sed -i "/^\s*ssid=\"$ssid_name\"/{n; s/\(\s*\).*/\1priority=1/}" $WPA_CONF
    sed -i "/^\s*ssid=\"eduroam\"/{n; s/\(\s*\).*/\1priority=0/}" $WPA_CONF

    # sed "/^\s*ssid=\"$ssid_name\"/{ n; s/\(\s*priority\)\=.*/\1=2/; t; /a priority=2 }" $WPA_CONF
    # sed "/Line1/{N; /\nString$/b; s/\n/\nString\n/}" file
    # sed "/^\s*ssid=\"$ssid_name\"/{N; /\(\s*\)priority=.*$/b; s/\n/\nString\n/}" $WPA_CONF

    # shellcheck disable=SC2034  # unused variable used in same shell by other script
    ASK_TO_REBOOT=true
}

function force_wpasupplicant_connect() {
    local IFACE="$1"
    if [ -z "$IFACE" ]; then
        echo "Usage: force_wpasupplicant_connect <interface> [wpa_supplicant.conf]"
        return 1
    fi

    echo "Force current wpa_supplicant config connection..."

    # Enable wlan0 interface
    echo "Bringing up interface $IFACE..."
    ip link set "$IFACE" up || ifconfig "$IFACE" up

    # Check if NetworkManager is managing the interface
    if command -v nmcli >/dev/null 2>&1 && nmcli device status | grep -q "^$IFACE.*connected"; then
        echo "NetworkManager detected. Reconnecting $IFACE..."
        nmcli device disconnect "$IFACE"
        sleep 1
        nmcli device connect "$IFACE"
        return 0
    fi

    # Check if systemd service exists for this interface
    if systemctl list-units --type=service | grep -q "wpa_supplicant@$IFACE.service"; then
        echo "systemd-managed wpa_supplicant detected. Restarting service..."
        systemctl restart "wpa_supplicant@$IFACE"
    else
        # Manual wpa_supplicant
        echo "Manual wpa_supplicant detected. Reloading manually..."
        # Terminate any running manual wpa_supplicant
        wpa_cli -i "$IFACE" terminate 2>/dev/null || true
        rm -f "/var/run/wpa_supplicant/$IFACE"
        # Start wpa_supplicant in background with updated config
        # sudo wpa_supplicant -B -i "$IFACE" -c "$WPA_CONF" -D nl80211
        wpa_supplicant -B -i "$IFACE" -c "$WPA_CONF"
    fi

    # Force load new wpa_supplicant.conf for current session
    # wpa_cli -i wlan0 terminate
    # Optional: remove old socket file to avoid conflicts
    # rm -f /var/run/wpa_supplicant/wlan0

    # Reload wpa_supplicant config safely
    # Option 1: Interface-specific systemd service
    # systemctl restart wpa_supplicant@wlan0

    # Option 2: Minimal disruption (if systemd-managed)
    # wpa_cli -i wlan0 reconfigure

    # Option 3: Manual, can clash with existing wpa_supplicant
    # wpa_supplicant -B -i wlan0 -c "$WPA_CONF"

    # Give it a few seconds to associate
    sleep 3

    # Force DHCP client to renew IP address
    echo "Renewing DHCP for $IFACE..."
    dhclient -r "$IFACE"
    sleep 1
    timeout 10 dhclient -1 "$IFACE" # Try once, exit if no lease, Force max 10 seconds
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
    force_wpasupplicant_connect wlan0
fi