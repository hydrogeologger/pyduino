#!/bin/bash

###
#
# Setup script to configure Bananapi M2 Zero from scratch to a default operational state
#
###

# Check if script is running as root
if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

BASE_DIR=$(pwd)

# Include common
# shellcheck source=SCRIPTDIR/common.sh
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"


function create_board_file() {
    mkdir -p /var/lib/bananapi
    echo "BOARD=bpi-m2z" > /var/lib/bananapi/board.sh
    echo "BOARD_AUTO=bpi-m2z" >> /var/lib/bananapi/board.sh
    echo "BOARD_OLD=bpi-m64" >> /var/lib/bananapi/board.sh
}


function create_primary_serial_symbolic_link() {
    echo "Generating primary serial symbolic link..."
    ln -s /dev/ttyS3 /dev/serial0
}


function configure_default_boot_overlay() {
    echo "Setting boot default hardware overlay..."
    # Documentation can be found at /boot/dtb/overlay/README.sun8i-h3-overlays
    # https://github.com/armbian/sunxi-DT-overlays/blob/master/sun8i-h3/README.sun8i-h3-overlays
    local CMDLINE_FILE
    local OVERLAYS
    CMDLINE_FILE="/boot/armbianEnv.txt"
    OVERLAYS="pps-gpio pwm uart3 w1-gpio"

    sed -i "s/^overlays=.*/overlays=$OVERLAYS/" "$CMDLINE_FILE"
    if ! grep -q "overlays" "$CMDLINE_FILE"; then
        echo "overlays=$OVERLAYS" >> "$CMDLINE_FILE";
    fi
}

function return_to_base_dir() {
    cd "$BASE_DIR" || echo "Unable to enter $BASE_DIR" || return 2
}

function install_bontango_bpi_wiringpi2() {
    echo "Downloading and installing BPI-WiringPi2..."
    # clone repo
    git clone "https://github.com/bontango/BPI-WiringPi2.git" "/home/pi/BPI-WiringPi2"

    cd "/home/pi/BPI-WiringPi2" || echo "Unable to enter /home/pi/BPI-WiringPi2" || return 2
    ./build

    return_to_base_dir
}


function install_rpi_gpio() {
    install_packages "python3-dev"
    # sudo CFLAGS="-fcommon" python3 setup.py install
    local F_CFLAG
    local gcc_version
    gcc_version="$(version "$(gcc -dumpfullversion)")"
    if [ "$gcc_version" -ge "$(version "10.1.0")" ]; then
        # workaround for issue https://sourceforge.net/p/raspberry-gpio-python/tickets/187/
        F_CFLAG="CFLAGS=-fcommon"
    fi
    if [ "$F_PYTHON2" ]; then
        eval $F_CFLAG python2 setup.py install
        eval $F_CFLAG python2 setup.py install
    fi
    if [ "$F_PYTHON3" ]; then
        eval $F_CFLAG python3 setup.py install
        eval $F_CFLAG python3 setup.py install
    fi
    if [ ! "$F_PYTHON2" ] && [ ! "$F_PYTHON3" ]; then
        eval $F_CFLAG python setup.py install
        eval $F_CFLAG python setup.py install
    fi
}


function install_GrazerComputerClub_rpi_gpio_pymodule() {
    echo "Downloading and installing GrazerComputerClub fork of SINOVOIP RPi.Gpio module..."
    git clone "https://github.com/GrazerComputerClub/RPi.GPIO.git" "/home/pi/RPi.GPIO"

    # Build and install
    cd "/home/pi/RPi.GPIO" || echo "Unable to enter /home/pi/RPi.GPIO" || return 2

    install_rpi_gpio
    return_to_base_dir
}

apt update
install_packages "python-is-python3"
get_declared_args_python_version "$@"
create_board_file
configure_default_boot_overlay
create_primary_serial_symbolic_link
install_GrazerComputerClub_rpi_gpio_pymodule
install_bontango_bpi_wiringpi2
# Enable bluetooth as PAN
# shellcheck source=SCRIPTDIR/bluetooth_pan/install.sh
source "$(dirname "${BASH_SOURCE[0]}")/bluetooth_pan/install.sh"
# Configure device as USB gadget
# shellcheck source=SCRIPTDIR/ssh_over_usb/install_armbian.sh
source "$(dirname "${BASH_SOURCE[0]}")/ssh_over_usb/install_armbian.sh"
# Configure eduroam
# shellcheck source=SCRIPTDIR/wpasupplicant/install_armbian.sh
source "$(dirname "${BASH_SOURCE[0]}")/wpasupplicant/install_armbian.sh" --name "eduroam" --reset

if [ "$ASK_TO_REBOOT" = true ]; then do_finish; fi
