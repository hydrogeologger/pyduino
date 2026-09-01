<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.conversion`
Utilities for converting between common units and rates.


## Table of Contents
- [`celsius_to_kelvin`](./postprocess.conversion.md#function-celsius_to_kelvin): Convert a temperature from degrees Celsius to Kelvin.
- [`kelvin_to_celsius`](./postprocess.conversion.md#function-kelvin_to_celsius): Convert a temperature from Kelvin to degrees Celsius.
- [`per_second_to_daily`](./postprocess.conversion.md#function-per_second_to_daily): Convert a per-second rate to an equivalent daily rate.
- [`per_second_to_hourly`](./postprocess.conversion.md#function-per_second_to_hourly): Convert a per-second rate to an equivalent hourly rate.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L4"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `celsius_to_kelvin`

```python
celsius_to_kelvin(value)
```

Convert a temperature from degrees Celsius to Kelvin.


**Args:**

- <b>`value`</b>: Temperature in degrees Celsius.


**Returns:**

Temperature in Kelvin.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `kelvin_to_celsius`

```python
kelvin_to_celsius(value)
```

Convert a temperature from Kelvin to degrees Celsius.


**Args:**

- <b>`value`</b>: Temperature in Kelvin.


**Returns:**

Temperature in degrees Celsius.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `per_second_to_hourly`

```python
per_second_to_hourly(value_per_second)
```

Convert a per-second rate to an equivalent hourly rate.

This conversion assumes the input represents a rate accumulated
continuously over time.


**Args:**

- <b>`value_per_second`</b>: Value or rate measured per second.


**Returns:**

Equivalent value or rate measured per hour.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/conversion.py#L46"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `per_second_to_daily`

```python
per_second_to_daily(value_per_second)
```

Convert a per-second rate to an equivalent daily rate.

This conversion assumes the input represents a rate accumulated
continuously over time.


**Args:**

- <b>`value_per_second`</b>: Value or rate measured per second.


**Returns:**

Equivalent value or rate measured per day.



