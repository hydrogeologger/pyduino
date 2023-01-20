#!/bin/bash

# Script to edit hostname


# Check if script is running as root
if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

function get_hostname() {
    tr -d " \t\n\r" < /etc/hostname
}

function do_hostname() {
    CURRENT_HOSTNAME=$(get_hostname)
    if [ $# -eq 0 ]; then
        whiptail --msgbox "\
            Please note: RFCs mandate that a hostname's labels \
            may contain only the ASCII letters 'a' through 'z' (case-insensitive),
            the digits '0' through '9', and the hyphen.
            Hostname labels cannot begin or end with a hyphen.
            No other symbols, punctuation characters, or blank spaces are permitted. \
            Do not use underscores (_) as it will not be parsed by dns.\
            " 20 70 1
        NEW_HOSTNAME=$(whiptail --inputbox "Please enter a hostname" 20 60 "$CURRENT_HOSTNAME" 3>&1 1>&2 2>&3)
    else
        NEW_HOSTNAME="$1"
        true
    fi
    # shellcheck disable=SC2181  # indirect checking from above whiptail, do not add anything
    # in between
    if [ "$?" -eq 0 ]; then
        # Set static hostname
        if [ "$INIT" = "systemd" ] && systemctl -q is-active dbus && ! ischroot; then
            hostnamectl set-hostname "$NEW_HOSTNAME" 2> /dev/null
        else
            echo "$NEW_HOSTNAME" > /etc/hostname
        fi
        sed -i "s/127\.0\.1\.1.*$CURRENT_HOSTNAME/127.0.1.1\t$NEW_HOSTNAME/g" /etc/hosts

        # Update transient hostname
        sysctl kernel.hostname="$NEW_HOSTNAME"
        systemctl restart systemd-hostnamed

        # shellcheck disable=SC2034  # unused variable used in same shell by other script
        ASK_TO_REBOOT=true
    fi
}

function hostname_reset_prompt() {
    echo "What are you setting up?"
    select option in "RaspberryPi" "BananaPi M2 Zero" "Other"; do
        case $option in
            "RaspberryPi" )
                do_hostname "raspberrypi";
                break;;
            "BananaPi M2 Zero" )
                do_hostname "bananapim2zero";
                break;;
            "Other" )
                do_hostname;
                break;;
        esac
    done
}

# make sure filename supplied as command line arg else die
[ $# -gt 1 ] && { echo "Usage: $0 hostname"; exit 1; }

if [ $# -eq 0 ]; then
    hostname_reset_prompt
else
    do_hostname "$1"
fi