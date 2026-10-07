<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.conversion`
Utilities for converting between common units and rates.


## Table of Contents
- [`cardinal_to_degrees`](./postprocess.conversion.md#function-cardinal_to_degrees): Convert an abbreviated cardinal direction string to its degree angle.
- [`celsius_to_kelvin`](./postprocess.conversion.md#function-celsius_to_kelvin): Convert a temperature from degrees Celsius to Kelvin.
- [`daily_to_hourly`](./postprocess.conversion.md#function-daily_to_hourly): Convert a daily rate to an equivalent hourly rate.
- [`daily_to_per_second`](./postprocess.conversion.md#function-daily_to_per_second): Convert a daily rate to an equivalent per-second rate.
- [`hourly_to_daily`](./postprocess.conversion.md#function-hourly_to_daily): Convert an hourly rate to an equivalent daily rate.
- [`hourly_to_per_second`](./postprocess.conversion.md#function-hourly_to_per_second): Convert an hourly rate to an equivalent per-second rate.
- [`kelvin_to_celsius`](./postprocess.conversion.md#function-kelvin_to_celsius): Convert a temperature from Kelvin to degrees Celsius.
- [`kmh_to_ms`](./postprocess.conversion.md#function-kmh_to_ms): Convert speed from kilometers per hour (km/h) to meters per second (m/s).
- [`ms_to_kmh`](./postprocess.conversion.md#function-ms_to_kmh): Convert speed from meters per second (m/s) to kilometers per hour (km/h).
- [`per_second_to_daily`](./postprocess.conversion.md#function-per_second_to_daily): Convert a per-second rate to an equivalent daily rate.
- [`per_second_to_hourly`](./postprocess.conversion.md#function-per_second_to_hourly): Convert a per-second rate to an equivalent hourly rate.


**Global Variables**
---------------
- **CARDINAL_ANGLE_MAP** = {'N': 0.0, 'NNE': 22.5, 'NE': 45.0, 'ENE': 67.5, 'E': 90.0, 'ESE': 112.5, 'SE': 135.0, 'SSE': 157.5, 'S': 180.0, 'SSW': 202.5, 'SW': 225.0, 'WSW': 247.5, 'W': 270.0, 'WNW': 292.5, 'NW': 315.0, 'NNW': 337.5}

<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `celsius_to_kelvin`

```python
celsius_to_kelvin(value)
```

Convert a temperature from degrees Celsius to Kelvin.


**Args:**

- <b>`value`</b>: Temperature in degrees Celsius.


**Returns:**

- <b>`float`</b>: Temperature in Kelvin.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `kelvin_to_celsius`

```python
kelvin_to_celsius(value)
```

Convert a temperature from Kelvin to degrees Celsius.


**Args:**

- <b>`value`</b>: Temperature in Kelvin.


**Returns:**

- <b>`float`</b>: Temperature in degrees Celsius.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `per_second_to_hourly`

```python
per_second_to_hourly(value_per_second)
```

Convert a per-second rate to an equivalent hourly rate.


**Args:**

- <b>`value_per_second`</b>: Value or rate measured per second.


**Returns:**

- <b>`float`</b>: Equivalent value or rate measured per hour.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L90"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `hourly_to_per_second`

```python
hourly_to_per_second(value_per_hour)
```

Convert an hourly rate to an equivalent per-second rate.


**Args:**

- <b>`value_per_hour`</b>: Value or rate measured per hour.


**Returns:**

- <b>`float`</b>: Equivalent value or rate measured per second.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L103"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `per_second_to_daily`

```python
per_second_to_daily(value_per_second)
```

Convert a per-second rate to an equivalent daily rate.


**Args:**

- <b>`value_per_second`</b>: Value or rate measured per second.


**Returns:**

- <b>`float`</b>: Equivalent value or rate measured per day.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L116"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `daily_to_per_second`

```python
daily_to_per_second(value_per_day)
```

Convert a daily rate to an equivalent per-second rate.


**Args:**

- <b>`value_per_day`</b>: Value or rate measured per day.


**Returns:**

- <b>`float`</b>: Equivalent value or rate measured per second.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `hourly_to_daily`

```python
hourly_to_daily(value_per_hour)
```

Convert an hourly rate to an equivalent daily rate.


**Args:**

- <b>`value_per_hour`</b>: Value or rate measured per hour.


**Returns:**

- <b>`float`</b>: Equivalent value or rate measured per day.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L142"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `daily_to_hourly`

```python
daily_to_hourly(value_per_day)
```

Convert a daily rate to an equivalent hourly rate.


**Args:**

- <b>`value_per_day`</b>: Value or rate measured per day.


**Returns:**

- <b>`float`</b>: Equivalent value or rate measured per hour.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L155"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `kmh_to_ms`

```python
kmh_to_ms(speed_kmh)
```

Convert speed from kilometers per hour (km/h) to meters per second (m/s).


**Args:**

- <b>`speed_kmh`</b>: Speed in kilometers per hour.


**Returns:**

- <b>`float`</b>: Speed in meters per second.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L168"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `ms_to_kmh`

```python
ms_to_kmh(speed_ms)
```

Convert speed from meters per second (m/s) to kilometers per hour (km/h).


**Args:**

- <b>`speed_ms`</b>: Speed in meters per second.


**Returns:**

- <b>`float`</b>: Speed in kilometers per hour.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L181"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `cardinal_to_degrees`

```python
cardinal_to_degrees(direction)
```

Convert an abbreviated cardinal direction string to its degree angle.


**Args:**

- <b>`direction`</b>: The cardinal or intercardinal direction abbreviation 
    (e.g., 'N', 'NE', 'SSW').


**Returns:**

- <b>`float or None`</b>: The corresponding angle in degrees, or None if the input is 
    invalid or unrecognized.



