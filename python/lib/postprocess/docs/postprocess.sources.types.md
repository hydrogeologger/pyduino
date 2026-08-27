<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/sources/types.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.sources.types`
Shared type definitions for the postprocess.sources subpackage.


## Table of Contents
- [`Coordinates`](./postprocess.sources.types.md#class-coordinates): Represents a geographic point on Earth using coordinate geometry.
	- [`Coordinates.round`](./postprocess.sources.types.md#method-coordinatesround): Round the latitude and longitude to the given number of decimal places.
	- [`Coordinates.validate_decimal_degree`](./postprocess.sources.types.md#method-coordinatesvalidate_decimal_degree): Check whether a value is a valid (latitude, longitude) coordinate pair.
- [`LocationBase`](./postprocess.sources.types.md#class-locationbase): Stores geographical metadata for general locations.
	- [`LocationBase.__init__`](./postprocess.sources.types.md#constructor-locationbase__init__): Initialise location metadata.




<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/types.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `Coordinates`
Represents a geographic point on Earth using coordinate geometry.


**Attributes:**

- <b>`latitude`</b> (float): The angular distance relative to the equator.
- <b>`longitude`</b> (float): The angular distance relative to the prime meridian.





<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/types.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Coordinates.round`

```python
round(ndigits=4)
```

Round the latitude and longitude to the given number of decimal places.

A single number applies to both coordinates. A tuple can be used to set
different precision for latitude and longitude. Use ``None`` to leave a
coordinate unchanged.


**Args:**

- <b>`ndigits`</b> (int, tuple, or None): Number of decimal places to use.
    A tuple specifies the precision for latitude and longitude,
    respectively. Defaults to 4.


**Returns:**

- <b>`Coordinates`</b>: The rounded coordinates. Returns the same instance if
    ``ndigits`` is ``None``.


**Raises:**

- <b>`ValueError`</b>: If a precision is less than 1 or the tuple does not
    contain exactly two values.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/types.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Coordinates.validate_decimal_degree`

```python
validate_decimal_degree(lat_lon)
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



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/types.py#L129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `LocationBase`
Stores geographical metadata for general locations.


**Attributes:**

- <b>`latitude`</b> (float): Latitude in decimal degrees. Positive values indicate
    north of the Equator; negative values indicate south.
- <b>`longitude`</b> (float): Longitude in decimal degrees. Positive values indicate
    east of the Prime Meridian; negative values indicate west.
- <b>`elevation_m`</b> (float or None): Elevation above sea level in metres.
- <b>`name`</b> (str): The common descriptor or name of the location.


<a href="../../../../python/lib/postprocess/src/postprocess/sources/types.py#L141"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `LocationBase.__init__`

```python
LocationBase(latitude, longitude, elevation_m=None, name='')
```

Initialise location metadata.


**Args:**

- <b>`latitude`</b> (float): Latitude in decimal degrees. Positive values indicate
    north of the Equator; negative values indicate south.
- <b>`longitude`</b> (float): Longitude in decimal degrees. Positive values indicate
    east of the Prime Meridian; negative values indicate west.
- <b>`elevation_m`</b> (float, Optional): Elevation measured as metre above sea level.
    Defaults to None.
- <b>`name`</b> (str, Optional): Common descriptor or name of the location.
    Defaults to "".



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> LocationBase.coordinates

Coordinates in (latitude, longitude). (Read-only)





