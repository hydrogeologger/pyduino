<!-- markdownlint-disable -->

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/pyduino.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `pyduino_sensor.pyduino`
This module provides helper functions for pyduino datalogger.

Dependencies:
- pySerial : Communication with secondary MCU.
- gpiozero.output_devices : DigitalOutputDevice for GPIO access.


## Table of Contents
- [`arduino_comms_is_good`](./pyduino_sensor.pyduino.md#function-arduino_comms_is_good): Test communication between RPI and secondary MCU.
- [`comms_check_reset_arduino`](./pyduino_sensor.pyduino.md#function-comms_check_reset_arduino): Verify comms between RPI and secondary MCU with auto MCU reset.
- [`exec_remote_command_subprocess`](./pyduino_sensor.pyduino.md#function-exec_remote_command_subprocess): Executes a command on a remote host using the system's ssh client via subprocess.
- [`reset_arduino`](./pyduino_sensor.pyduino.md#function-reset_arduino): Resets secondary MCU.


**Global Variables**
---------------
- **RPI_RESET_PIN_BCM** = 27

---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/pyduino.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `reset_arduino`

```python
reset_arduino(pin=27, hold_time=5)
```

Resets secondary MCU.


**Args:**

- <b>`pin`</b> (int, optional): GPIO BCM PIN. Defaults to RPI_RESET_PIN_BCM.
- <b>`hold_time`</b> (int, optional): Time to hold reset line for in seconds,
    minimum is 2 seconds. Defaults to 5.



---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/pyduino.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `arduino_comms_is_good`

```python
arduino_comms_is_good(serial_obj)
```

Test communication between RPI and secondary MCU.


**Args:**

- <b>`serial_obj`</b> (Serial): Serial object.


**Returns:**

- <b>`bool`</b>: True if comms is good, False otherwise.



---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/pyduino.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `comms_check_reset_arduino`

```python
comms_check_reset_arduino(serial_obj, delay=3, reset_pin=27, reset_time=5)
```

Verify comms between RPI and secondary MCU with auto MCU reset.


**Args:**

- <b>`serial_obj`</b> (Serial): Serial object.
- <b>`delay`</b> (int, optional): Delay after mcu reset to let things settle in seconds. Defaults to 3.
- <b>`reset_pin`</b> (int, optional): GPIO BCM PIN. Defaults to RPI_RESET_PIN_BCM.
- <b>`reset_time`</b> (int, optional): Time to hold reset line for in seconds. Defaults to 5.


**Returns:**

- <b>`bool`</b>: True if mcu is reset, False otherwise.



---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/pyduino.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `exec_remote_command_subprocess`

```python
exec_remote_command_subprocess(
    hostname,
    command,
    username=None,
    password=None,
    key_path=None,
    debug=False
)
```

Executes a command on a remote host using the system's ssh client via subprocess.


**Args:**

- <b>`hostname`</b> (str): The hostname or IP address of the remote machine.
- <b>`command`</b> (str): The command to execute on the remote host.
- <b>`username`</b> (str): The username for SSH authentication.
- <b>`password`</b> (str, optional): The password for password-based authentication.
                          Use with caution as it can expose credentials.
- <b>`key_path`</b> (str, optional): The path to the private SSH key for key-based authentication.
- <b>`debug`</b> (bool, optional): Print error to stdout.


**Returns:**

- <b>`tuple`</b>: A tuple containing (stdout, stderr, exitcode) from the remote command.



