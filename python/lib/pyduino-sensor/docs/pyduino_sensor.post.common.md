<!-- markdownlint-disable -->

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/common.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `pyduino_sensor.post.common`
This module contain simple and common methods used in sensor post process package.


## Table of Contents
- [`normalise`](./pyduino_sensor.post.common.md#function-normalise): Map a value to between 0 and 1.



---

<a href="../../../../python/lib/pyduino-sensor/src/pyduino_sensor/post/common.py#L4"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

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



