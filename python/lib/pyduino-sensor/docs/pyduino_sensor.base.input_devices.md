<!-- markdownlint-disable -->

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\base\input_devices.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `pyduino_sensor.base.input_devices`
This module contains base classes for input devices which access RPI GPIO hardware. Not for direct import. 

This module is used in submodules, and is preferrable to import them i.e. `pyduino_sensor.davis` 

Dependencies: 
- gpiozero.input_devices : DigitalInputDevice for pin interrupt. 



---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\base\input_devices.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PulseDeviceBase`
A class to represent a device implementing pin Interrupts. 



**Attributes:**
 
 - <b>`name`</b> (str):  Name of sensor. 
 - <b>`debug`</b> (bool):  Debugging mode flag. 

Methods: 

In addition of `SensorBase()` methods 


- `begin()`:             Setup interrupt for pin trigger callback. 
- `end()`:             Detach interrupt for pin trigger callback. 
- `update()`:             Increment pulse counter by one. 
- `reset()`:             Resets pulse counter. 
- `get_count()`:             Getter pulse counter. 

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\base\input_devices.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(name, pin, pull_up=True, debounce=None, debug=True, **kwargs)
```

Constructs all the necessary attributes for the PulseSensor object. 

Base on the Button class of gpiozero, pull_up = True means the reading pin default state is high, so connect one pin to GND and one pin to the reading pin 



**Args:**
 
 - <b>`name`</b> (str):  Name of sensor. 
 - <b>`pin`</b> (int):  GPIO BCM pin to be attached to interrupt. 
 - <b>`pull_up`</b> (bool, optional):  GPIO pin state.                     True: pin pulled high, False: pin pulled low. Defaults to True. 
 - <b>`debounce`</b> (float | None, optional):  Debounce of pin in seconds.                     If None, no software bounce compensation will be performed.  Otherwise, this is the length of time (in seconds) that                     the component will ignore changes in state after an initial                     change. Defaults to None. 

Keyword Args: 
 - <b>`debug`</b> (bool, optional):  Debuging mode flag. Defaults to True. 




---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\base\input_devices.py#L71"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `begin`

```python
begin()
```

Setup interrupt for pin trigger callback. 

Required for counter to be updated. 

---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\base\input_devices.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `end`

```python
end()
```

Detach interrupt for pin trigger callback. 

---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\base\input_devices.py#L92"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_count`

```python
get_count()
```

Getter for counter. 

---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\base\input_devices.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `reset`

```python
reset()
```

Resets counter to zero. 

---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\base\input_devices.py#L82"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update`

```python
update()
```

Increment pulse counter by one. 


