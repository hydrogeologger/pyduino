<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/postprocess/common#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.common`
This module contain simple and common methods used in postprocess package.


## Table of Contents
- [`calculate_delta`](./postprocess.common.md#function-calculate_delta): Calculates the difference (delta) between a single reference value from a set of values.
- [`normalise`](./postprocess.common.md#function-normalise): Map a value to between 0 and 1.



---

<a href="../../../../python/lib/postprocess/postprocess/common/calculate_delta#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

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

- <b>`list | int | float`</b>: List of delta values.



---

<a href="../../../../python/lib/postprocess/postprocess/common/normalise#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

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



