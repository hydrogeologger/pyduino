#!/bin/bash

# Common functions to support installation/configuration of pyduino setup for armbian
# systems

function enable_uart1() {
    # Found NetworkManager was handling bluetooth hci0 devices, when NM is
    # disabled, bluetooth is not powered on, need to manually enable uart1 
    # and uart1-rtscts which bluetooth chip is connected to.
    # Documentation can be found at /boot/dtb/overlay/README.sun8i-h3-overlays
    # https://github.com/armbian/sunxi-DT-overlays/blob/master/sun8i-h3/README.sun8i-h3-overlays

    local CMDLINE_FILE="/boot/armbianEnv.txt"
    readonly CMDLINE_FILE
    
    # Add uart1 overlay to boot environment
    sed -i "s/^overlays=\(.*\)$/overlays=uart1 \1/" "$CMDLINE_FILE"
    if ! grep -q "overlays" "$CMDLINE_FILE"; then
        echo "overlays=uart1" >> "$CMDLINE_FILE";
    fi
    
    # Enable RTS and CTS pins
    sed -i "s/^param_uart1_rtscts=.*$/param_uart1_rtscts=1/" "$CMDLINE_FILE"
    if ! grep -q "param_uart1_rtscts" "$CMDLINE_FILE"; then
        echo "param_uart1_rtscts=1" >> "$CMDLINE_FILE";
    fi
}