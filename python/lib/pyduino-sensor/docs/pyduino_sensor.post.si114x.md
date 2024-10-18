<!-- markdownlint-disable -->

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\post\si114x.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `pyduino_sensor.post.si114x`
This module contains post processing functions for SI114X sensors. 



---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\post\si114x.py#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SI114X`
A Class to represent a Si114x Ultraviolet (UV) Index, Gesture, Proximity,     and Ambient Light sensor. 



**Attributes:**
 
 - <b>`name`</b> (str):  Name of sensor. 
 - <b>`debug`</b> (bool):  Debugging mode flag. 

Methods: 

In addition of `SensorBase()` methods. 

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\post\si114x.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(name, high_range=True, **kwargs)
```

Constructs all the necessary attributes for Suction sensor object. 



**Args:**
 
 - <b>`name`</b> (str):  Name of sensor. 
 - <b>`high_range`</b> (bool, optional):  Sensor configured to use high signal                     range ie. for direct sunlight. Defaults to True. 

Keyword Args: 
 - <b>`debug`</b> (bool, optional):  Debuging mode flag. Defaults to True. 




---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\post\si114x.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `calculate`

```python
calculate(adc, gain, typical)
```

Transform Silicon Lab SI1145 ADC value to another unit. 



**Args:**
 
 - <b>`adc`</b> (int):  ADC values as read from SI114X register. 
 - <b>`typical`</b> (float):  Typical value for unit conversion. 



**Returns:**
 
 - <b>`(int | float)`</b>:  User decided unit. 

---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\post\si114x.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `calculate_intensity_from_typical`

```python
calculate_intensity_from_typical(type_, value, high_range=True)
```

Calculate intensity value from typical SI114X specifications. 



**Args:**
 
 - <b>`type_`</b> (str):  Data type, allowable (`'ir'|'vis'|'uv'`). 
 - <b>`value`</b> (int):  Value as read from SI114X register. 
 - <b>`high_range`</b> (bool, optional):  Sensor configured to use high signal                     range ie. for direct sunlight. Defaults to True. 



**Raises:**
 
 - <b>`ValueError`</b>:  Incorrect "type" declared. 



**Returns:**
 
 - <b>`(float)`</b>:  Intensity (W/m^2). 

---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\post\si114x.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `calculate_uv_index`

```python
calculate_uv_index(value)
```

Converts Silicon Lab SI114X UV reading to UV Index. 



**Args:**
 
 - <b>`value`</b> (int):  ADC reading from SI114X registers. 



**Returns:**
 
 - <b>`(float)`</b>:  UV Index (unitless). 

---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\post\si114x.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ir_intensity`

```python
ir_intensity(adc)
```

Converts Silicon Lab SI114X ADC value to intensity (W/m^2). 



**Args:**
 
 - <b>`adc`</b> (int):  ADC reading from SI114X registers. 



**Returns:**
 
 - <b>`(int | float)`</b>:  Intensity (W/m^2). 

---

<a href="..\..\..\..\python\lib\pyduino-sensor\src\pyduino_sensor\post\si114x.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `vis_intensity`

```python
vis_intensity(adc)
```

Converts Silicon Lab SI114X ADC value to intensity (W/m^2). 



**Args:**
 
 - <b>`adc`</b> (int):  ADC reading from SI114X registers. 



**Returns:**
 
 - <b>`(int | float)`</b>:  Intensity (W/m^2). 


