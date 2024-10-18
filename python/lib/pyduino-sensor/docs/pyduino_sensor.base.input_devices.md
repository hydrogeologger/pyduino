<!-- markdownlint-disable -->

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/base/input_devices.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `pyduino_sensor.base.input_devices`
This module contains base classes for input devices which access RPI GPIO hardware.
Not for direct import.

This module is used in submodules, and is preferrable to import them i.e.
`pyduino_sensor.davis`

Dependencies:
- gpiozero.input_devices : DigitalInputDevice for pin interrupt.


## Table of Contents
- [`PulseDeviceBase`](./pyduino_sensor.base.input_devices.md#class-pulsedevicebase): A class to represent a device implementing pin Interrupts.
	- [`PulseDeviceBase.__init__`](./pyduino_sensor.base.input_devices.md#constructor-pulsedevicebase__init__): Constructs all the necessary attributes for the PulseSensor object.
	- [`PulseDeviceBase.begin`](./pyduino_sensor.base.input_devices.md#method-pulsedevicebasebegin): Setup interrupt for pin trigger callback.
	- [`PulseDeviceBase.end`](./pyduino_sensor.base.input_devices.md#method-pulsedevicebaseend): Detach interrupt for pin trigger callback.
	- [`PulseDeviceBase.get_count`](./pyduino_sensor.base.input_devices.md#method-pulsedevicebaseget_count): Getter for counter.
	- [`PulseDeviceBase.reset`](./pyduino_sensor.base.input_devices.md#method-pulsedevicebasereset): Resets counter to zero.
	- [`PulseDeviceBase.update`](./pyduino_sensor.base.input_devices.md#method-pulsedevicebaseupdate): Increment pulse counter by one.




---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/base/input_devices.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `PulseDeviceBase`
A class to represent a device implementing pin Interrupts.


**Attributes:**

- <b>`name`</b> (str): Name of sensor.
- <b>`debug`</b> (bool): Debugging mode flag.

Methods:

In addition of `SensorBase()` methods

- `begin()`:
        Setup interrupt for pin trigger callback.
- `end()`:
        Detach interrupt for pin trigger callback.
- `update()`:
        Increment pulse counter by one.
- `reset()`:
        Resets pulse counter.
- `get_count()`:
        Getter pulse counter.


<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/base/input_devices.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `PulseDeviceBase.__init__`

```python
PulseDeviceBase(name, pin, pull_up=True, debounce=None, debug=False, **kwargs)
```

Constructs all the necessary attributes for the PulseSensor object.

Base on the Button class of gpiozero, pull_up = True means the
reading pin default state is high, so connect one pin to GND
and one pin to the reading pin.


**Args:**

- <b>`name`</b> (str): Name of sensor.
- <b>`pin`</b> (int): GPIO BCM pin to be attached to interrupt.
- <b>`pull_up`</b> (bool, optional): GPIO pin state.  
    True: pin pulled high, False: pin pulled low. Defaults to True.
- <b>`debounce`</b> (float | None, optional): Debounce of pin in seconds.
    If None, no software bounce compensation will be performed.  
    Otherwise, this is the length of time (in seconds) that
    the component will ignore changes in state after an initial
    change. Defaults to None.
- <b>`debug`</b> (bool, optional): Debuging mode flag. Defaults to False.





---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/base/input_devices.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `PulseDeviceBase.begin`

```python
begin()
```

Setup interrupt for pin trigger callback.

Required for counter to be updated.


---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/base/input_devices.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `PulseDeviceBase.end`

```python
end()
```

Detach interrupt for pin trigger callback.


---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/base/input_devices.py#L90"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `PulseDeviceBase.get_count`

```python
get_count()
```

Getter for counter.


---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/base/input_devices.py#L86"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `PulseDeviceBase.reset`

```python
reset()
```

Resets counter to zero.


---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/base/input_devices.py#L80"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `PulseDeviceBase.update`

```python
update()
```

Increment pulse counter by one.



