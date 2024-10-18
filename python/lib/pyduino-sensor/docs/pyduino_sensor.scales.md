<!-- markdownlint-disable -->

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/scales.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `pyduino_sensor.scales`
This module provides helper functions to communicate with Scale devices.

Dependencies:
- pyserial : Used for serial communication.


## Table of Contents
- [`OhausScale`](./pyduino_sensor.scales.md#class-ohausscale): A Class to represent an Ohaus Scale with serial interface.
	- [`OhausScale.__init__`](./pyduino_sensor.scales.md#constructor-ohausscale__init__): Constructs all the necessary attributes for Ohaus Scale object.
	- [`OhausScale.get_weight`](./pyduino_sensor.scales.md#method-ohausscaleget_weight): Get weight reading from scale, auto open and close serial device.




---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/scales.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `OhausScale`
A Class to represent an Ohaus Scale with serial interface.


**Attributes:**

- <b>`name`</b> (str): Name of sensor.
- <b>`debug`</b> (bool): Debugging mode flag.

Methods:

In addition of `SensorBase()` methods.

- `get_weight()`:
        Get weight reading from scale.


<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/scales.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `OhausScale.__init__`

```python
OhausScale(name, port, baudrate=9600, timeout=10, **kwargs)
```

Constructs all the necessary attributes for Ohaus Scale object.


**Args:**

- <b>`name`</b> (_type_): User given name.
- <b>`port`</b> (_type_): Serial Port.
- <b>`baudrate`</b> (int, optional): _description_. Defaults to 9600.
- <b>`timeout`</b> (int, optional): _description_. Defaults to 10.

Keyword Args:
- <b>`debug`</b> (bool, optional): Debuging mode flag. Defaults to False.





---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/scales.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `OhausScale.get_weight`

```python
get_weight(max_tries=5, tolerance=2, delay=1, interval=1)
```

Get weight reading from scale, auto open and close serial device.


**Args:**

- <b>`max_tries`</b> (int, optional): Maximum tries to read scale. Defaults to 5.
- <b>`tolerance`</b> (float, optional): Edge case reading resolution.
    Tolerance is ignored if max_tries=1. Defaults to 2.
- <b>`delay`</b> (float, optional): Delay post serial device initialization. Defaults to 1.
- <b>`interval`</b> (float, optional): Delay between serial write. Defaults to 1.


**Raises:**

- <b>`errors.`</b>: Re-raise errors.
- <b>`RuntimeError`</b>: Exceeded maximum number of tries reading weight within tolerance.


**Returns:**

- <b>`namedtuple`</b> (value, unit): Scale value and unit.



