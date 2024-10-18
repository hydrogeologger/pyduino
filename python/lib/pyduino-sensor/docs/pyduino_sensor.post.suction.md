<!-- markdownlint-disable -->

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/suction.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `pyduino_sensor.post.suction`
This module contains post processing functions for suction sensors.


## Table of Contents
- [`SuctionHeatDissipation`](./pyduino_sensor.post.suction.md#class-suctionheatdissipation): A Class to represent a heat dissipation Suction sensor.
	- [`SuctionHeatDissipation.__init__`](./pyduino_sensor.post.suction.md#constructor-suctionheatdissipation__init__): Constructs all the necessary attributes for Suction sensor object.
	- [`SuctionHeatDissipation.delta_temperature_to_kpa`](./pyduino_sensor.post.suction.md#method-suctionheatdissipationdelta_temperature_to_kpa): Converts a heat dissipation temperature delta to pressure.
	- [`SuctionHeatDissipation.get_kpa`](./pyduino_sensor.post.suction.md#method-suctionheatdissipationget_kpa): Converts a heat dissipation temperature delta to pressure.




---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/suction.py#L7"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `SuctionHeatDissipation`
A Class to represent a heat dissipation Suction sensor.


**Attributes:**

- <b>`name`</b> (str): Name of sensor.
- <b>`debug`</b> (bool): Debugging mode flag.
- <b>`dry_dt`</b> (int | float): Dry condition differential temperature value.
- <b>`wet_dt`</b> (int | float): Saturated wet condition differential temperature value.

Methods:

In addition of `SensorBase()` methods.


<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/suction.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `SuctionHeatDissipation.__init__`

```python
SuctionHeatDissipation(name, dry, wet, **kwargs)
```

Constructs all the necessary attributes for Suction sensor object.


**Args:**

- <b>`name`</b> (str): Name of sensor.
- <b>`dry`</b> (int | float): Dry condition differential temperature value.
- <b>`wet`</b> (int | float): Saturated wet condition differential temperature value.

Keyword Args:
    debug (bool, optional): Debuging mode flag. Defaults to False.





---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/suction.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `SuctionHeatDissipation.delta_temperature_to_kpa`

```python
delta_temperature_to_kpa(value, dry, wet)
```

Converts a heat dissipation temperature delta to pressure.


**Args:**

- <b>`value`</b> (float): Differenential temperature measurement.
- <b>`dry`</b> (float, optional): Dry condition differential temperature value.
- <b>`wet`</b> (float, optional): Wet condition differential temperature value.


**Returns:**

- <b>`float`</b>: Suction (kPa).


---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/suction.py#L37"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `SuctionHeatDissipation.get_kpa`

```python
get_kpa(value)
```

Converts a heat dissipation temperature delta to pressure.


**Args:**

- <b>`value`</b> (float): Differenential temperature measurement.


**Returns:**

- <b>`float`</b>: Suction (kPa).



