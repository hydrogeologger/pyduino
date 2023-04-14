#!/bin/bash

###
#
# Setup script to configure Raspberry Pi from scratch to a default operational state
#
###

# Check if script is running as root
if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

# Include common
# shellcheck source=/dev/null
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"


function install_wiringpi() {
    local CLONE_DIR
    CLONE_DIR="/home/${SUDO_USER:-$USER}/WiringPi"

    echo "Downloading and installing WiringPi..."
    # clone repo
    git clone "https://github.com/WiringPi/WiringPi" "$CLONE_DIR"

    # Change owner of directory to current user
    chown -R ${SUDO_USER:-$USER}:${SUDO_USER:-$USER} "$CLONE_DIR"

    # Build and install
    cd "$CLONE_DIR" || { echo "Unable to enter $CLONE_DIR"; return 1; }
    ./build

    return_to_base_dir
}


if ! get_declared_args_python_version "$@"; then
    show_no_python_version_declared_message
    exit 1
fi
apt update
#TODO: configure_default_boot_overlay
install_packages "vim"
configure_vimrc
install_packages "git tmux autossh tightvncserver"
install_packages "mplayer"
if [ "$F_PYTHON2" ]; then
    install_packages "python-is-python2 python2-pip"
    install_packages "python-serial"
    # install_packages "python-rpi.gpio python2-gpiozero"
    pip install paho-mqtt
fi
if [ "$F_PYTHON3" ]; then
    install_packages "python-is-python3 python3-pip"
    install_packages "python3-serial"
    # install_packages "python3-rpi.gpio python3-gpiozero"
    pip3 install paho-mqtt
fi
# Fix arduino-mk Java Depency, Java11 only supported on ARM 7+, install java8 for ARM v6
if grep -q "^model name\s*:\s*ARMv6" "/proc/cpuinfo"; then
    # for RPI Zero W
    install_packages "openjdk-8-jre-headless openjdk-8-jre"
fi
install_packages "arduino-mk"
install_avrdude_rpi_autoreset
apply_avrdudeconf_missing_fix
install_wiringpi
create_thingsboard_ip_report_credentials
create_empty_crontab_template
add_report_ip_to_thingsboard_to_cron
# shellcheck source=/dev/null
# Enable bluetooth as PAN
source "$(dirname "${BASH_SOURCE[0]}")/bluetooth_pan/install.sh"
# shellcheck source=/dev/null
# Configure device as USB gadget
source "$(dirname "${BASH_SOURCE[0]}")/ssh_over_usb/install_raspbian.sh"
# shellcheck source=/dev/null
# Configure eduroam
source "$(dirname "${BASH_SOURCE[0]}")/wpasupplicant/install.sh" --name "eduroam" --reset


if [ "$ASK_TO_REBOOT" = true ]; then do_finish; fi
