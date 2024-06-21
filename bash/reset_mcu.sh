#!/bin/bash
# This script is inteded to be used to reset the secondary microcontroller

MCU_RESET_PIN=27    # Reset pin, BCM Pin number
TTY_PORT="/dev/serial0"  # Serial port

function WAIT_GPIO() {
    sleep 0.1
}

function setup() {
    # Exports pin to userspace
    if [ ! -d "/sys/class/gpio/gpio$MCU_RESET_PIN" ]; then
        echo "$MCU_RESET_PIN" > /sys/class/gpio/export; WAIT_GPIO
    fi

    # set GPIOs as output
    echo "out" > "/sys/class/gpio/gpio$MCU_RESET_PIN/direction"; WAIT_GPIO
}

function cleanup() {
    # Remove pin from userspace
    if [ -d /sys/class/gpio/gpio${MCU_RESET_PIN} ]; then
        echo "in" > "/sys/class/gpio/gpio$MCU_RESET_PIN/direction"; WAIT_GPIO
        echo "$MCU_RESET_PIN" > /sys/class/gpio/unexport; WAIT_GPIO
    fi
}

function reset_mcu() {
    setup

    echo "Resetting MCU through GPIO$MCU_RESET_PIN..."

    echo "0" > "/sys/class/gpio/gpio$MCU_RESET_PIN/value";
    sleep 3
    # echo "1" > "/sys/class/gpio/gpio$MCU_RESET_PIN/value"; WAIT_GPIO

    cleanup
}

function mcu_comms_is_good() {
    local tty_response
    stty -F "$TTY_PORT" 9600
    WAIT_GPIO
    echo -ne "abc" > "$TTY_PORT"
    read -r -e -s -t 1 tty_response < "$TTY_PORT"
    if [ "$tty_response" == "abc" ]; then
        # echo "MCU serial is responsive."
        return 0 # comms is success
    else
        # echo "MCU serial not responsive!"
        return 1 # comms is failure
    fi
}


# Only perform reset if script is executed and not sourced
if test ${#BASH_SOURCE[@]} -eq 1; then
    reset_mcu
    
    exit 0
fi
