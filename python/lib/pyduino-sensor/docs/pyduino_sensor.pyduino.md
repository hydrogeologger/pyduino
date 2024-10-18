<!-- markdownlint-disable -->

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\pyduino.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `pyduino_sensor.pyduino`
This module provides helper functions for pyduino datalogger. 

Dependencies: 
- pySerial : Communication with secondary MCU. 
- gpiozero.output_devices : DigitalOutputDevice for GPIO access. 

**Global Variables**
---------------
- **RPI_RESET_PIN_BCM**

---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\pyduino.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `reset_arduino`

```python
reset_arduino(pin=27, hold_time=5)
```

Resets secondary MCU. 



**Args:**
 
 - <b>`pin`</b> (int, optional):  GPIO BCM PIN. Defaults to RPI_RESET_PIN_BCM. 
 - <b>`hold_time`</b> (int, optional):  Time to hold reset line for in seconds,                 minimum is 2 seconds. Defaults to 5. 


---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\pyduino.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `check_arduino_comms`

```python
check_arduino_comms(serial_obj)
```

Verify communication between RPI and secondary MCU. 



**Args:**
 
 - <b>`serial_obj`</b> (Serial):  Serial object. 


