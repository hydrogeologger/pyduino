<!-- markdownlint-disable -->

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\post\suction.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `pyduino_sensor.post.suction`
This module contains post processing functions for suction sensors. 



---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\post\suction.py#L7"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SuctionHeatDissipation`
A Class to represent a heat dissipation Suction sensor. 



**Attributes:**
 
 - <b>`name`</b> (str):  Name of sensor. 
 - <b>`debug`</b> (bool):  Debugging mode flag. 
 - <b>`dry_dt`</b> (int | float):  Dry condition differential temperature value. 
 - <b>`wet_dt`</b> (int | float):  Saturated wet condition differential temperature value. 

Methods: 

In addition of `SensorBase()` methods. 

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\post\suction.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(name, dry, wet, **kwargs)
```

Constructs all the necessary attributes for Suction sensor object. 



**Args:**
 
 - <b>`name`</b> (str):  Name of sensor. 
 - <b>`dry`</b> (int | float):  Dry condition differential temperature value. 
 - <b>`wet`</b> (int | float):  Saturated wet condition differential temperature value. 

Keyword Args: 
 - <b>`debug`</b> (bool, optional):  Debuging mode flag. Defaults to True. 




---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\post\suction.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `delta_temperature_to_kpa`

```python
delta_temperature_to_kpa(value, dry, wet)
```

Converts a heat dissipation temperature delta to pressure. 



**Args:**
 
 - <b>`value`</b> (float):  Differenential temperature measurement. 
 - <b>`dry`</b> (float, optional):  Dry condition differential temperature value. 
 - <b>`wet`</b> (float, optional):  Wet condition differential temperature value. 



**Returns:**
 
 - <b>`float`</b>:  Suction (kPa). 

---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\post\suction.py#L37"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_kpa`

```python
get_kpa(value)
```

Converts a heat dissipation temperature delta to pressure. 



**Args:**
 
 - <b>`value`</b> (float):  Differenential temperature measurement. 



**Returns:**
 
 - <b>`float`</b>:  Suction (kPa). 


