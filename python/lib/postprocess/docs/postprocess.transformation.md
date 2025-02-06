<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/transformation.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.transformation`
Common data transformation utilities.

Provides general-purpose functions for operations such as calculating
differences relative to a reference value and normalising values to a
specified range.


## Table of Contents
- [`calculate_delta`](./postprocess.transformation.md#function-calculate_delta): Calculates the difference (delta) between a single reference value from a set of values.
- [`normalise`](./postprocess.transformation.md#function-normalise): Map a value to between 0 and 1.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/transformation.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `calculate_delta`

```python
calculate_delta(values, ref, abs_=False)
```

Calculates the difference (delta) between a single reference value from a set of values.


**Args:**

- <b>`values`</b> (Iterable): dataset, i.e. list containing data to be operated on.
- <b>`ref`</b> (any): Reference value for difference calculation
- <b>`abs_`</b> (bool, optional): Flag determining result is absolute values.
    Defaults to False.


**Returns:**

- <b>`list[int|float]|int|float`</b>: List of delta values.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/transformation.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `normalise`

```python
normalise(value, min_, max_)
```

Map a value to between 0 and 1.


**Args:**

- <b>`value`</b> (int | float): Value to normalize.
- <b>`min_`</b> (int | float): Lower limit mapped to 0.
- <b>`max_`</b> (int | float): Upper limit to be mapped to 1.


**Returns:**

- <b>`float`</b>: Value between 0 and 1.



