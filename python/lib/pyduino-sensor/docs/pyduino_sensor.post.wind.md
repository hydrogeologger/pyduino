<!-- markdownlint-disable -->

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/wind.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `pyduino_sensor.post.wind`
This module contains post processing functions for wind sensors.


## Table of Contents
- [`WindDirection`](./pyduino_sensor.post.wind.md#class-winddirection): A Class to represent an analog Wind Direction sensor.
	- [`WindDirection.__init__`](./pyduino_sensor.post.wind.md#constructor-winddirection__init__): Constructs all the necessary attributes for the Davis Wind Anemometer Direction object.
	- [`WindDirection.adc_to_degree_radius`](./pyduino_sensor.post.wind.md#method-winddirectionadc_to_degree_radius): Convert ADC value to approximate angles in degrees radius.
	- [`WindDirection.get_calibrated_direction`](./pyduino_sensor.post.wind.md#method-winddirectionget_calibrated_direction): Gets calibrated direction of wind vane in degrees radius (clockwise).




---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/wind.py#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `WindDirection`
A Class to represent an analog Wind Direction sensor.

Default orientation for direction is Clockwise.


**Attributes:**

- <b>`name`</b> (str): Name of sensor.
- <b>`debug`</b> (bool): Debugging mode flag.
- <b>`offset (float) `</b>: Angle offset of wind vane in degrees radius.
    (Positive: Clockwise, Negative: Counter-clockwise)

Methods:

In addition of `SensorBase()` methods.

- `adc_to_degree(adc_raw)`:
        Calculates the angle from ADC value in degrees radius.
- `get_calibrated_direction(adc_raw)`:
        Get calibrated angle from ADC value in degrees radius.


<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/wind.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `WindDirection.__init__`

```python
WindDirection(name, offset=0, n_adc_bits=10, **kwargs)
```

Constructs all the necessary attributes for the Davis Wind Anemometer Direction object.


**Args:**

- <b>`name`</b> (str): Name of sensor.
- <b>`offset`</b> (float, optional): Angle offset of wind vane in degrees
    radius in clockwise direction. Defaults to 0.  
    Clockwise - Positive value. Counter-Clockwise - Negative value.
- <b>`n_adc_bits`</b> (int, optional): Resolution of ADC i.e 10bit = 10. Defaults to 10.

Keyword Args:
    debug (bool, optional): Debuging mode flag. Defaults to False.





---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/wind.py#L46"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `WindDirection.adc_to_degree_radius`

```python
adc_to_degree_radius(adc_raw, clockwise=True)
```

Convert ADC value to approximate angles in degrees radius.

Mapping function.

From http://cactus.io/hookups/weather/anemometer/davis/hookup-arduino-to-davis-anemometer
North : 0/MAX ADC
East : 1/4 * MAX ADC
South : 1/2 * MAX ADC
West : 3/4 * MAX ADC


**Args:**

- <b>`adc_raw`</b> (int | float): ADC measurement of anemometer.
- <b>`clockwise`</b> (bool, optional): Direction of results to be returned.  
        True: Clockwise, False: Counter-Clockwise.
        Defaults to True.


**Returns:**

- <b>`float`</b>: Clockwise angle in degrees radius unless clockwise is false.


---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/wind.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `WindDirection.get_calibrated_direction`

```python
get_calibrated_direction(adc_raw)
```

Gets calibrated direction of wind vane in degrees radius (clockwise).



