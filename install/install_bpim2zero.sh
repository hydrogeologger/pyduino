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

# Include common
# shellcheck source=/dev/null
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"


function create_board_file() {
    mkdir -p /var/lib/bananapi
    echo "BOARD=bpi-m2z" > /var/lib/bananapi/board.sh
    echo "BOARD_AUTO=bpi-m2z" >> /var/lib/bananapi/board.sh
    echo "BOARD_OLD=bpi-m64" >> /var/lib/bananapi/board.sh
}


function create_primary_serial_symbolic_link() {
    echo "Generating primary serial symbolic link..."
    transfer_conf_files_from_path "$(dirname "${BASH_SOURCE[0]}")/board/bpim2zero/files"
    # Following softlink is temporary for current session
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


function install_bontango_bpi_wiringpi2() {
    local CLONE_DIR
    CLONE_DIR="/home/${SUDO_USER:-$USER}/BPI-WiringPi2"

    echo "Downloading and installing BPI-WiringPi2..."
    # clone repo
    git clone "https://github.com/bontango/BPI-WiringPi2.git" "$CLONE_DIR"

    # Change owner of directory to current user
    chown -R ${SUDO_USER:-$USER}:${SUDO_USER:-$USER} "$CLONE_DIR"

    # Build and install
    cd "$CLONE_DIR" || { echo "Unable to enter $CLONE_DIR"; return 1; }
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
    local CLONE_DIR
    CLONE_DIR="/home/${SUDO_USER:-$USER}/RPi.Gpio"

    echo "Downloading and installing GrazerComputerClub fork of SINOVOIP RPi.Gpio module..."
    git clone "https://github.com/GrazerComputerClub/RPi.GPIO.git" "$CLONE_DIR"

    # Change owner of directory to current user
    chown -R ${SUDO_USER:-$USER}:${SUDO_USER:-$USER} "$CLONE_DIR"

    # Build and install
    cd "$CLONE_DIR" || { echo "Unable to enter $CLONE_DIR"; return 1; }

    install_rpi_gpio
    return_to_base_dir
}


function apply_sudo_python_gpio_fix() {
    if [ -f "/usr/bin/python" ]; then
        echo "Apply python not having sudo access to GPIO fix."

        # Create copy of python with different setuid permissions
        cp "/usr/bin/python" "/usr/bin/python-as-root"
        chmod 4775 "/usr/bin/python-as-root"

        # Change shebang of avrdude-rpi autoreset file to use sudoed python
        sed -i "1 s/python.*/python-as-root/" "/usr/bin/autoreset"
    fi
}


apt update
get_declared_args_python_version "$@"
create_board_file
configure_default_boot_overlay
create_primary_serial_symbolic_link
install_packages "dos2unix python-is-python3 python3-serial arduino-mk"
install_avrdude_rpi_autoreset
apply_sudo_python_gpio_fix
apply_avrdudeconf_missing_fix
install_GrazerComputerClub_rpi_gpio_pymodule
install_bontango_bpi_wiringpi2
create_thingsboard_ip_report_credentials
create_empty_crontab_template
add_report_ip_to_thingsboard_to_cron
# shellcheck source=/dev/null
# Enable bluetooth as PAN
source "$(dirname "${BASH_SOURCE[0]}")/bluetooth_pan/install.sh"
# shellcheck source=/dev/null
# Configure device as USB gadget
source "$(dirname "${BASH_SOURCE[0]}")/ssh_over_usb/install_armbian.sh"
# shellcheck source=/dev/null
# Configure eduroam
source "$(dirname "${BASH_SOURCE[0]}")/wpasupplicant/install_armbian.sh" --name "eduroam" --reset


if [ "$ASK_TO_REBOOT" = true ]; then do_finish; fi
