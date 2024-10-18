<!-- markdownlint-disable -->

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\davis.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `pyduino_sensor.davis`
This is a wrapper for Davis Weather Instruments Sensors. 

Dependencies: 
- gpiozero : Used by PulseDeviceBase 



---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\davis.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Rain`
A Class to represent a Davis Tipping Bucket Rain Gauge. 



**Attributes:**
 
 - <b>`name`</b> (str):  Name of sensor. 
 - <b>`debug`</b> (bool):  Debugging mode flag. 

Methods: 

In addition of `PulseDeviceBase()` methods 


- `get_cumulative()`:         Getter for cumulative rain in millilitres (mm). 

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\davis.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(name, pin, debounce=0.001, resolution=0.2, **kwargs)
```

Constructs all the necessary attributes for the Davis Rain Tip Bucket object. 



**Args:**
 
 - <b>`name`</b> (str):  Name of sensor. 
 - <b>`pin`</b> (int):  GPIO BCM pin to be attached to interrupt. 
 - <b>`debounce`</b> (float | None, optional):  Debounce of pin in seconds.                     If None, no software bounce compensation will be performed.  Otherwise, this is the length of time (in seconds) that                     the component will ignore changes in state after an initial                     change. Defaults to 0.001. 
 - <b>`resolution`</b> (float, optional):  Resolution of tip bucket in millimetres (mm).                     Defaults to 0.2. 

Keyword Args: 
 - <b>`debug`</b> (bool, optional):  Debuging mode flag. Defaults to True. 


---

#### <kbd>property</kbd> resolution

Getter for bucket resolution. 



---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\davis.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_cumulative`

```python
get_cumulative(reset=True)
```

Getter for cumulative rain. 

Will reset counter 



**Args:**
 
 - <b>`reset`</b> (bool, optional):  Reset counter. Defaults to True. 



**Returns:**
 
 - <b>`float`</b>:  Cumulative rain in mililitres (mm). 


---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\davis.py#L81"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `WindSpeed`
A Class to represent a Davis Anemometer Wind Speed sensor. 



**Attributes:**
 
 - <b>`name`</b> (str):  Name of sensor. 
 - <b>`debug`</b> (bool):  Debugging mode flag. 

Methods: 

In addition of `PulseDeviceBase()` methods. 


- `calculate_average()`:             Calculate wind speed in km/hr. 
- `get_average()`:             Getter for average wind speed in km/hr, will reset counter. 

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\davis.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(name, pin, debounce=None, **kwargs)
```

Constructs all the necessary attributes for the Davis Wind Anemometer Speed object. 



**Args:**
 
 - <b>`name`</b> (str):  Name of sensor. 
 - <b>`pin`</b> (int):  GPIO BCM pin to be attached to interrupt. 
 - <b>`pull_up`</b> (bool, optional):  GPIO pin state.                     True: pin pulled high, False: pin pulled low. Defaults to True. 
 - <b>`debounce`</b> (float | None, optional):  Debounce of pin in seconds.                     If None, no software bounce compensation will be performed.  Otherwise, this is the length of time (in seconds) that                     the component will ignore changes in state after an initial                     change. Defaults to None. 

Keyword Args: 
 - <b>`debug`</b> (bool, optional):  Debuging mode flag. Defaults to True. 




---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\davis.py#L120"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `begin`

```python
begin()
```

Start wind speed capture. 

---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\davis.py#L133"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `calculate_average`

```python
calculate_average(elapsed_time)
```

Calculate average wind speed. 

Based on Davis tech document  V = P*(2.25/T) the speed is in MPh 

 P = no. of pulses per sample period 

 T = sample period in seconds 



**Args:**
 
 - <b>`elapsed_time`</b> (float | int):  Elapsed time in seconds. 



**Returns:**
 
 - <b>`float`</b>:  Average wind speed in km/hr. 

---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\davis.py#L153"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_average`

```python
get_average(reset=True)
```

Getter for average wind speed. 

Counter reset dependant on reset argument. 



**Args:**
 
 - <b>`reset`</b> (bool, optional):  Reset counter. Defaults to True. 



**Returns:**
 
 - <b>`float`</b>:  Average wind speed (km/hr). 

---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\davis.py#L125"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `reset`

```python
reset()
```

Reset counter and set timestamp. 


