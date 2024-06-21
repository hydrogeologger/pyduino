"""This module provides helper functions for pyduino datalogger.

Dependencies:
- pySerial : Communication with secondary MCU.
- gpiozero.output_devices : DigitalOutputDevice for GPIO access.
"""

import subprocess as _subprocess
import time as _time

from gpiozero.output_devices import DigitalOutputDevice as _DigitalOutputDevice
from serial import Serial as _Serial

RPI_RESET_PIN_BCM = 27  # GPIO/BCM pin number to reset arduino


def reset_arduino(pin=RPI_RESET_PIN_BCM, hold_time=5):
    # type: (int|None, int|None) -> None
    """Resets secondary MCU.

    Args:
        pin (int, optional): GPIO BCM PIN. Defaults to RPI_RESET_PIN_BCM.
        hold_time (int, optional): Time to hold reset line for in seconds,
            minimum is 2 seconds. Defaults to 5.
    """
    arduino_reset = _DigitalOutputDevice(
        pin=pin, active_high=False, initial_value=None)
    arduino_reset.on()
    # Minimum 2 seconds required
    _time.sleep(max(hold_time if hold_time else 2, 2))
    arduino_reset.off()
    arduino_reset.close()


def arduino_comms_is_good(serial_obj):
    # type: (_Serial) -> bool
    """Test communication between RPI and secondary MCU.

    Args:
        serial_obj (Serial): Serial object.

    Returns:
        bool: True if comms is good, False otherwise.
    """
    try:
        serial_obj.reset_input_buffer()
    except AttributeError:
        serial_obj.flushInput()  # type:ignore for pySerial < 3.0
    serial_obj.write("abc".encode())
    if serial_obj.readline().decode() != "abc\r\n":
        return False
    return True


def comms_check_reset_arduino(serial_obj, delay=3, reset_pin=RPI_RESET_PIN_BCM, reset_time=5):
    # type: (_Serial, int|None, int|None, int|None) -> bool
    """Verify comms between RPI and secondary MCU with auto MCU reset.

    Args:
        serial_obj (Serial): Serial object.
        delay (int, optional): Delay after mcu reset to let things settle in seconds. Defaults to 3.
        reset_pin (int, optional): GPIO BCM PIN. Defaults to RPI_RESET_PIN_BCM.
        reset_time (int, optional): Time to hold reset line for in seconds. Defaults to 5.

    Returns:
        bool: True if mcu is reset, False otherwise.
    """
    if not arduino_comms_is_good(serial_obj=serial_obj):
        reset_arduino(pin=reset_pin, hold_time=reset_time)
        reset_arduino()
        # give arduino time to settle
        _time.sleep(max(delay if delay else 1, 1))
        return True
    return False


def exec_remote_command_subprocess(hostname, command,
                                   username=None, password=None, key_path=None, debug=False):
    # type: (str, str, str|None, str|None, str|None, bool|None) -> tuple[str,str,int]
    """Executes a command on a remote host using the system's ssh client via subprocess.

    Args:
        hostname (str): The hostname or IP address of the remote machine.
        command (str): The command to execute on the remote host.
        username (str): The username for SSH authentication.
        password (str, optional): The password for password-based authentication.
                                  Use with caution as it can expose credentials.
        key_path (str, optional): The path to the private SSH key for key-based authentication.
        debug (bool, optional): Print error to stdout.

    Returns:
        tuple: A tuple containing (stdout, stderr, exitcode) from the remote command.
    """
    if username:
        ssh_cmd = ["ssh", f"{username}@{hostname}", command]
    else:
        ssh_cmd = ["ssh", f"{hostname}", command]

    if password:
        # Using sshpass for password-based authentication (requires sshpass installed)
        ssh_cmd = ["sshpass", "-p", password] + ssh_cmd
    elif key_path:
        ssh_cmd.insert(1, "-i")
        ssh_cmd.insert(2, key_path)

    try:
        process = _subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,  # Decode stdout/stderr as text
            check=True   # Raise CalledProcessError for non-zero exit codes
        )
        return process.stdout, process.stderr, 0
    except _subprocess.CalledProcessError as err:
        if debug:
            # print(f"Error: Command failed with exit code {err.returncode}")
            print(f"Error executing command: {err}")
            print(f"Stderr: {err.stderr}")
        return "", err.stderr, err.returncode
    except FileNotFoundError:
        if debug:
            print(
                "Error: 'ssh' or 'sshpass' command not found. Ensure they are in your PATH.")
        return "", "Command not found error.", 127
