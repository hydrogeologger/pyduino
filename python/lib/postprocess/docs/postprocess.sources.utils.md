<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.sources.utils`
Common utility and shared resources for the postprocess.sources subpackage.


## Table of Contents
- [`haversine_distance`](./postprocess.sources.utils.md#function-haversine_distance): Computes great-circle distance between two geographic coordinates.
- [`round_to_nearest_05`](./postprocess.sources.utils.md#function-round_to_nearest_05): Round value to nearest 0.05.
- [`validate_decimal_degree_coordinates`](./postprocess.sources.utils.md#function-validate_decimal_degree_coordinates): Check whether a value is a valid (latitude, longitude) coordinate pair.


**Global Variables**
---------------
- **TYPE_CHECKING** = False

<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `validate_decimal_degree_coordinates`

```python
validate_decimal_degree_coordinates(lat_lon)
```

Check whether a value is a valid (latitude, longitude) coordinate pair.

Latitude must be in [-90, 90] and longitude in [-180, 180].


**Args:**

- <b>`lat_lon`</b> (tuple[float, float]): A coordinate pair (latitude, longitude)
    in decimal degrees, where both values are numeric.


**Raises:**

- <b>`TypeError`</b>: If ``lat_lon`` is not a tuple or either coordinate is not an
    integer or float.
- <b>`ValueError`</b>: If ``lat_lon`` does not contain exactly two values or either
    coordinate is outside its valid range.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `haversine_distance`

```python
haversine_distance(coord1, coord2, radius=6371.0)
```

Computes great-circle distance between two geographic coordinates.

Applies the Haversine formula to find the shortest spherical distance between
points. Converts inputs from decimal degrees to radians, validates bounds, 
and scales the angular separation by the specified planetary radius.


**Args:**

- <b>`coord1`</b> (tuple): Starting point as (latitude, longitude) coordinate pair in decimal degrees.
- <b>`coord2`</b> (tuple): Ending point as (latitude, longitude) coordinate pair in decimal degrees.
- <b>`radius`</b> (float, Optional): Sphere radius. Defaults to 6371.0 (Earth kilometers).


**Returns:**

- <b>`float`</b>: Great-circle distance in the same unit as radius.

TypeError: Coordinates is not a tuple or either coordinate is not an
    integer or float.
ValueError: Coordinates does not contain exactly two values or either
    coordinate is outside its valid range latitudes exceed [-90, 90] or
    longitudes exceed [-180, 180].



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `round_to_nearest_05`

```python
round_to_nearest_05(x)
```

Round value to nearest 0.05.



