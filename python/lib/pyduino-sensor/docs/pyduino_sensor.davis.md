<!-- markdownlint-disable -->

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/davis.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `pyduino_sensor.davis`
This is a wrapper for Davis Weather Instruments Sensors.

Dependencies:
- gpiozero : Used by PulseDeviceBase


## Table of Contents
- [`Rain`](./pyduino_sensor.davis.md#class-rain): A Class to represent a Davis Tipping Bucket Rain Gauge.
	- [`Rain.__init__`](./pyduino_sensor.davis.md#constructor-rain__init__): Constructs all the necessary attributes for the Davis Rain Tip Bucket object.
	- [`Rain.get_cumulative`](./pyduino_sensor.davis.md#method-rainget_cumulative): Getter for cumulative rain.
- [`WindSpeed`](./pyduino_sensor.davis.md#class-windspeed): A Class to represent a Davis Anemometer Wind Speed sensor.
	- [`WindSpeed.__init__`](./pyduino_sensor.davis.md#constructor-windspeed__init__): Constructs all the necessary attributes for the Davis Wind Anemometer Speed object.
	- [`WindSpeed.begin`](./pyduino_sensor.davis.md#method-windspeedbegin): Start wind speed capture.
	- [`WindSpeed.calculate_average`](./pyduino_sensor.davis.md#method-windspeedcalculate_average): Calculate average wind speed.
	- [`WindSpeed.get_average`](./pyduino_sensor.davis.md#method-windspeedget_average): Getter for average wind speed.
	- [`WindSpeed.reset`](./pyduino_sensor.davis.md#method-windspeedreset): Reset counter and set timestamp.




---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/davis.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `Rain`
A Class to represent a Davis Tipping Bucket Rain Gauge.


**Attributes:**

- <b>`name`</b> (str): Name of sensor.
- <b>`debug`</b> (bool): Debugging mode flag.

Methods:

In addition of `PulseDeviceBase()` methods

- `get_cumulative()`:
        Getter for cumulative rain in millilitres (mm).


<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/davis.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `Rain.__init__`

```python
Rain(name, pin, debounce=0.001, resolution=0.2, debug=False, **kwargs)
```

Constructs all the necessary attributes for the Davis Rain Tip Bucket object.


**Args:**

- <b>`name`</b> (str): Name of sensor.
- <b>`pin`</b> (int): GPIO BCM pin to be attached to interrupt.
- <b>`debounce`</b> (float | None, optional): Debounce of pin in seconds.
    If None, no software bounce compensation will be performed.  
    Otherwise, this is the length of time (in seconds) that
    the component will ignore changes in state after an initial
    change. Defaults to 0.001.
- <b>`resolution`</b> (float, optional): Resolution of tip bucket in millimetres (mm).
    Defaults to 0.2.
- <b>`debug`</b> (bool, optional): Debuging mode flag. Defaults to False.



---

#### <kbd>property</kbd> Rain.resolution

Getter for bucket resolution.




---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/davis.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Rain.get_cumulative`

```python
get_cumulative(reset=True)
```

Getter for cumulative rain.

Will reset counter


**Args:**

- <b>`reset`</b> (bool, optional): Reset counter. Defaults to True.


**Returns:**

- <b>`float`</b>: Cumulative rain in mililitres (mm).



---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/davis.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `WindSpeed`
A Class to represent a Davis Anemometer Wind Speed sensor.


**Attributes:**

- <b>`name`</b> (str): Name of sensor.
- <b>`debug`</b> (bool): Debugging mode flag.

Methods:

In addition of `PulseDeviceBase()` methods.

- `calculate_average()`:
        Calculate wind speed in km/hr.
- `get_average()`:
        Getter for average wind speed in km/hr, will reset counter.


<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/davis.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `WindSpeed.__init__`

```python
WindSpeed(name, pin, debounce=None, debug=False, **kwargs)
```

Constructs all the necessary attributes for the Davis Wind Anemometer Speed object.


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

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/davis.py#L114"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `WindSpeed.begin`

```python
begin()
```

Start wind speed capture.


---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/davis.py#L127"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `WindSpeed.calculate_average`

```python
calculate_average(elapsed_time)
```

Calculate average wind speed.

Based on Davis tech document
    V = P*(2.25/T) the speed is in MPh

    P = no. of pulses per sample period

    T = sample period in seconds


**Args:**

- <b>`elapsed_time`</b> (float | int): Elapsed time in seconds.


**Returns:**

- <b>`float`</b>: Average wind speed in km/hr.


---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/davis.py#L147"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `WindSpeed.get_average`

```python
get_average(reset=True)
```

Getter for average wind speed.

Counter reset dependant on reset argument.


**Args:**

- <b>`reset`</b> (bool, optional): Reset counter. Defaults to True.


**Returns:**

- <b>`float`</b>: Average wind speed (km/hr).


---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/davis.py#L119"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `WindSpeed.reset`

```python
reset()
```

Reset counter and set timestamp.



