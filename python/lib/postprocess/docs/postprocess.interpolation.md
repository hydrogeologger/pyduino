<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/postprocess/interpolation#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.interpolation`
Post processing interpolation module.

Provides interpolation class and functions to support interpolation of pandas
dataframe objects.

Dependencies:
- matplotlib
- numpy
- pandas


## Table of Contents
- [`Interpolation`](./postprocess.interpolation.md#class-interpolation): Represents an interpolation object.
	- [`Interpolation.__init__`](./postprocess.interpolation.md#constructor-interpolation__init__): Generator for Interpolation object.
	- [`Interpolation.interpolate_smooth`](./postprocess.interpolation.md#method-interpolationinterpolate_smooth): Performs a smooth spline interpolation.
	- [`Interpolation.swap_index`](./postprocess.interpolation.md#method-interpolationswap_index): Swap DataFrame index between "date_time" and "time_days".




---

<a href="../../../../python/lib/postprocess/postprocess/interpolation/Interpolation#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `Interpolation`
Represents an interpolation object.


**Attributes:**

- <b>`ref_data`</b> (DataFrame|Series): Reference to primary data used for interpolation.
- <b>`df`</b> (DataFrame): Reference to DataFrame for interpolated data storage.


<a href="../../../../python/lib/postprocess/postprocess/interpolation/__init__#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `Interpolation.__init__`

```python
Interpolation(start_time, end_time, interval, ref_data=None)
```

Generator for Interpolation object.


**Args:**

- <b>`start_time`</b> (datetime | int | float): Start time of interpolation
    range. Accepts datetime or time in seconds.
- <b>`end_time`</b> (datetime | int | float): Stop time of interpolation range.
    Accepts datetime or time in seconds.
- <b>`interval`</b> (timedelta | int | float): Interval between timestamps (period).
    Accepts timedelta or time in seconds.
- <b>`ref_data`</b> (DataFrame | Series, optional): Reference data to be
    used for interpolation, able to be overriden at interpolation
    method calls. Defaults to None.


**Raises:**

- <b>`TypeError`</b>: Data provided is not of type DataFrame or Series.
- <b>`ValueError`</b>: Incorrect elapsed time unit attribute.





---

<a href="../../../../python/lib/postprocess/postprocess/interpolation/interpolate_smooth#L99"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Interpolation.interpolate_smooth`

```python
interpolate_smooth(
    data=None,
    key_name=None,
    coef=1e-14,
    preview=False,
    rm_nan=True
)
```

Performs a smooth spline interpolation.


**Args:**

- <b>`data`</b> (DataFrame | Series, optional): Data for interpolation to be
    performed on. Defaults to None.
- <b>`key_name`</b> (str | dict[str,str], optional): key of DataFrame to
    perform interpolation on, not required for Series.
    Provide a dictionatry {"oldkey" : "newkey"} to rename the column
    heading. Defaults to None.
- <b>`coef`</b> (float | int, optional): Smoothing parameter between 0 and 1.
    '0' -> LS-straight line. '1' -> cubic spline
    interpolant. Defaults to 1e-14.
- <b>`preview`</b> (bool, optional): Preview plot of interpolated data
    with original. Defaults to False.
- <b>`rm_nan`</b> (bool, optional): Removes not a number "NaN" values. Defaults to True.


**Raises:**

- <b>`TypeError`</b>: Data provided is not of type DataFrame or Series.
- <b>`RuntimeError`</b>: No data provided for interpolation, either
    during initialization or during interpolation.
- <b>`RuntimeError`</b>: No key_name given if data is DataFrame.


---

<a href="../../../../python/lib/postprocess/postprocess/interpolation/swap_index#L204"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Interpolation.swap_index`

```python
swap_index()
```

Swap DataFrame index between "date_time" and "time_days".


**Returns:**

- <b>`str or bool`</b>: Returns new index key name. False otherwise.



