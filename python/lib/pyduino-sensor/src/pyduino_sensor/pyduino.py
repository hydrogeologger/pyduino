"""This module provides helper functions for pyduino datalogger.

Dependencies:
- pySerial : Communication with secondary MCU.
- gpiozero.output_devices : DigitalOutputDevice for GPIO access.
"""

import time as _time
from serial import Serial as _Serial
from gpiozero.output_devices import DigitalOutputDevice as _DigitalOutputDevice


RPI_RESET_PIN_BCM = 27  # GPIO/BCM pin number to reset arduino


def reset_arduino(pin=RPI_RESET_PIN_BCM, hold_time=5):
    # type:(int|None, int|None) -> None
    """Resets secondary MCU.

    Args:
        pin (int, optional): GPIO BCM PIN. Defaults to RPI_RESET_PIN_BCM.
        hold_time (int, optional): Time to hold reset line for in seconds, \
                minimum is 2 seconds. Defaults to 5.
    """
    arduino_reset = _DigitalOutputDevice(
        pin=pin, active_high=False, initial_value=None)
    arduino_reset.on()
    hold_time = max(hold_time, 2)  # Minimum 2 seconds required
    _time.sleep(hold_time)
    arduino_reset.off()
    arduino_reset.close()


def check_arduino_comms(serial_obj):
    # type:(_Serial) -> None
    """Verify communication between RPI and secondary MCU.

    Args:
        serial_obj (Serial): Serial object.
    """
    command = "abc"
    serial_obj.write(command.encode())
    msg = serial_obj.readline().decode()
    if msg != "abc\r\n":
        print("Failed Handshake: No Response, resetting mcu")
        reset_arduino()
        _time.sleep(5)  # give arduino time to configure it self
