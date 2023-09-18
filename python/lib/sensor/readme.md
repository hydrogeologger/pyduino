# sensor: Third Party Python Package
This is a wrapper and libraries for built in sensors.

# Usage and API
```python
import sensor
```

# Module: sensor.davis
This is a wrapper for Davis Weather Instruments Sensor

Dependencies:
-------------
gpiozero : Button for button interrupts

Usage:
------
```python
import sensor.davis
```

## Base Methods
### begin()
```python
begin()
```
Starts interrupt to initiate counter.

### end()
```python
end()
```
Detaches interrupt.

### reset()
```python
reset()
```
Resets device counter.

### get_count()
```python
get_count()
```
Returns counter number gpio was triggered.

---

## Class: Rain
Class to support davis rain bucket.

### Initialization
```python
Rain(name, pin, debounce, volume)
```
### Params
* name (str) - Name of sensor
* pin (int) - BCM pin number of GPIO for interrupt attachment
* debounce (float) - Debounce of pin in seconds.  If None (the default), no 
        software bounce compensation will be performed. Otherwise, this is the length of time (in seconds) that the component will ignore changes in state after an initial change.
* volume (float) - Volume of tip bucket in millimeteres (mm)

In addition to base methods. The following methods are available.

### get_volume()
```python
get_volume()
```
Returns the volume per tip of the rain bucket, as configured during initialization.

### get_cumulative()
```python
get_cumulative()
```
Getter for cumulative rain volume in millilitres (mm). Will reset counter.


## Class: WindSpeed
Class to support davis Wind Anemometer - Speed.

### Initialization
```python
WindSpeed(name, pin, debounce)
```
### Params
* name (str) - Name of sensor
* pin (int) - BCM pin number of GPIO for interrupt attachment
* debounce (float) - Debounce of pin in seconds.  If None (the default), no 
        software bounce compensation will be performed. Otherwise, this is the length of time (in seconds) that the component will ignore changes in state after an initial change.

In addition to base methods. The following methods are available.

### get_average()
```python
get_average()
```
Getter for average wind speed in km/hr since last call to `get_average()` or 
`reset()`

### calculate_average()
```python
calculate_average(elapsed_time)
```
Calculate the average wind speed in km/hr over specified `elapsed_time` (sec) period.
Based on Davis tech document
V = P*(2.25/T) the speed is in MPh
P = no. of pulses per sample period
T = sample period in seconds

#### Params
* elapsed_time (int) - Elapsed time in seconds

#### Returns
Average speed in km/hr

---
## Class: WindDirection
Class to support davis Wind Anemometer - Direction.

### Initialization
```python
WindDirection(name, offset, adc_bit_size)
```

#### Params
* name (str) - Name of sensor
* offset (float) - Angleoffset of wind vane in degrees radius, clockwise (pos), ccw (neg)
* adc_bit_size (int) - Resolution of ADC i.e 10bit = 10
* debug (bool) - Enable debugging

In addition to base methods. The following methods are available.

### get_calibrated_direction()
```python
get_calibrated_direction(adc_raw)
```
Returns calibrated wind direction in degrees radius clockwise direction including
offset.

#### Params
* adc_raw (int | float) - ADC value.


### adc_to_degree_radius()
```python
adc_to_degree_radius(adc_raw, clockwise)
```
Convert ADC value to approximate angles in degrees radius, offset is not considered.

#### Params
* adc_raw (int | float) - ADC value
* clocwkise (bool) - Direction of wind vane from ADC reading, Default - True.
        Clockwise: True, Counter-Clockwise: False

---

Usage Example:
-------------
```python
import sensor.davis as davis

rain_tip_bucket = davis.Rain(name="rain", pin=8, debounce=0.001, volume=0.2, debug=False)
wind_speed = davis.WindSpeed(name="wind_speed", pin=18, debounce=None, debug=False)

rain_tip_bucket.begin()
wind_speed.begin()
while True:
    average_wind = wind_speed.get_average()
    rain_period_cumulative = rain_tip_bucket.get_cumulative()
    time.sleep(900) # 15 min interval
```
