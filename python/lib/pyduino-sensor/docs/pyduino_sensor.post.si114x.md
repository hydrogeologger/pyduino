<!-- markdownlint-disable -->

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/si114x.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `pyduino_sensor.post.si114x`
This module contains post processing functions for SI114X sensors.


## Table of Contents
- [`SI114X`](./pyduino_sensor.post.si114x.md#class-si114x): A Class to represent a Si1145/46/47 Ultraviolet (UV) Index, Gesture, Proximity, and Ambient Light sensor.
	- [`SI114X.__init__`](./pyduino_sensor.post.si114x.md#constructor-si114x__init__): Constructs all the necessary attributes for Si1145/46/47 sensor object.
	- [`SI114X.calculate`](./pyduino_sensor.post.si114x.md#method-si114xcalculate): Transform Silicon Lab Si1145/46/47 ADC value to another unit.
	- [`SI114X.calculate_uv_index`](./pyduino_sensor.post.si114x.md#method-si114xcalculate_uv_index): Converts Silicon Lab Si1145/46/47 UV reading to UV Index.
	- [`SI114X.ir_intensity`](./pyduino_sensor.post.si114x.md#method-si114xir_intensity): Converts Silicon Lab Si1145/46/47 ADC value to intensity (W/m^2).
	- [`SI114X.vis_intensity`](./pyduino_sensor.post.si114x.md#method-si114xvis_intensity): Converts Silicon Lab Si1145/46/47 ADC value to intensity (W/m^2).




---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/si114x.py#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `SI114X`
A Class to represent a Si1145/46/47 Ultraviolet (UV) Index, Gesture, Proximity,
and Ambient Light sensor.


**Attributes:**

- <b>`name`</b> (str): Name of sensor.
- <b>`debug`</b> (bool): Debugging mode flag.


**Methods:**


In addition of `SensorBase()` methods.


<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/si114x.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `SI114X.__init__`

```python
SI114X(name, **kwargs)
```

Constructs all the necessary attributes for Si1145/46/47 sensor object.


**Args:**

- <b>`name`</b> (str): Name of sensor.

Keyword Args:  
    debug (bool, optional): Debuging mode flag. Defaults to False.





---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/si114x.py#L80"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `SI114X.calculate`

```python
calculate(adc, typical, range_factor=1.0, gain=1)
```

Transform Silicon Lab Si1145/46/47 ADC value to another unit.


**Args:**

- <b>`adc`</b> (int|float): ADC values as read from register.
- <b>`typical`</b> (float|int): Typical value for unit conversion.
- <b>`range_factor`</b> (float|int, optional): Range scaling factor for ADC. Defaults to 1.
    - 1.0 for normal range mode
    - 14.5 for high range mode
- <b>`gain`</b> (int|float, optional): ADC gain multiplier (1–128), bit-aligned value,
    used for conversion of raw ADC values. Defaults to 1.


**Returns:**

(float): User decided unit.


---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/si114x.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `SI114X.calculate_uv_index`

```python
calculate_uv_index(value)
```

Converts Silicon Lab Si1145/46/47 UV reading to UV Index.


**Args:**

- <b>`value`</b> (int): ADC reading from registers.


**Returns:**

(float): UV Index (unitless).


---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/si114x.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `SI114X.ir_intensity`

```python
ir_intensity(adc, gain=1, high_range=True)
```

Converts Silicon Lab Si1145/46/47 ADC value to intensity (W/m^2).


**Args:**

- <b>`adc`</b> (int): ADC reading from registers.
- <b>`gain`</b> (int|float, optional): ADC gain multiplier (1–128), bit-aligned. Defaults to 1.
- <b>`high_range`</b> (bool, optional): High signal range mode, i.e for direct sunlight.
    Defaults to True.


**Returns:**

(float): Intensity (W/m^2).


---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/si114x.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `SI114X.vis_intensity`

```python
vis_intensity(adc, gain=1, high_range=True)
```

Converts Silicon Lab Si1145/46/47 ADC value to intensity (W/m^2).


**Args:**

- <b>`adc`</b> (int): ADC reading from registers.
- <b>`gain`</b> (int|float, optional): ADC gain multiplier (1–128), bit-aligned. Defaults to 1.
- <b>`high_range`</b> (bool, optional): High signal range mode, i.e for direct sunlight.
    Defaults to True.


**Returns:**

(float): Intensity (W/m^2).



