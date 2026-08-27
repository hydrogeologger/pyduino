<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.sources.utils`
Common utility and shared resources for the postprocess.sources subpackage.


## Table of Contents
- [`LocationMetadata`](./postprocess.sources.utils.md#class-locationmetadata): Stores geographical metadata for general locations.
	- [`LocationMetadata.__init__`](./postprocess.sources.utils.md#constructor-locationmetadata__init__): Initialise location metadata.
- [`haversine_distance`](./postprocess.sources.utils.md#function-haversine_distance): Computes great-circle distance between two geographic coordinates.
- [`is_valid_coordinates`](./postprocess.sources.utils.md#function-is_valid_coordinates): Check whether a value is a valid (latitude, longitude) coordinate pair.


**Global Variables**
---------------
- **TYPE_CHECKING** = False

<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `is_valid_coordinates`

```python
is_valid_coordinates(lat_lon)
```

Check whether a value is a valid (latitude, longitude) coordinate pair.

Latitude must be in [-90, 90] and longitude in [-180, 180].


**Args:**

- <b>`lat_lon`</b> (tuple[float, float]): A coordinate pair (latitude, longitude)
    in decimal degrees, where both values are numeric.


**Returns:**

True if `lat_lon` contains valid coordinates.


**Raises:**

- <b>`TypeError`</b>: If `lat_lon` is not a tuple or either coordinate is not an
    integer or float.
- <b>`ValueError`</b>: If `lat_lon` does not contain exactly two values or either
    coordinate is outside its valid range.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L92"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `haversine_distance`

```python
haversine_distance(coord1, coord2, radius=6371.0)
```

Computes great-circle distance between two geographic coordinates.

Applies the Haversine formula to find the shortest spherical distance between
points. Converts inputs from decimal degrees to radians, validates bounds, 
and scales the angular separation by the specified planetary radius.


**Args:**

- <b>`coord1`</b> (tuple): Startpoint coordinates (latitude, longitude).
- <b>`coord2`</b> (tuple): Endpoint coordinates (latitude, longitude).
- <b>`radius`</b> (float, Optional): Sphere radius. Defaults to 6371.0 (Earth kilometers).


**Returns:**

- <b>`float`</b>: Great-circle distance in the same unit as radius.

TypeError: Coordinates is not a tuple or either coordinate is not an
    integer or float.
ValueError: Coordinates does not contain exactly two values or either
    coordinate is outside its valid range latitudes exceed [-90, 90] or
    longitudes exceed [-180, 180].



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `LocationMetadata`
Stores geographical metadata for general locations.


**Attributes:**

- <b>`lat`</b> (float): Latitude in decimal degrees.
- <b>`lon`</b> (float): Longitude in decimal degrees.
- <b>`elevation`</b> (float or None): Elevation above sea level in metres.
- <b>`name`</b> (str): The common descriptor or name of the location.


<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `LocationMetadata.__init__`

```python
LocationMetadata(latitude, longitude, elevation=None, name='')
```

Initialise location metadata.


**Args:**

- <b>`latitude`</b> (float): Latitude of the station in GDA94.
- <b>`longitude`</b>: Longitude of the station in GDA94.
- <b>`elevation`</b> (float, Optional): Elevation measured as metre above sea level.
    Defaults to None.
- <b>`name`</b> (str, Optional): Common descriptor or name of the location.
    Defaults to "".



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> LocationMetadata.coordinates

Coordinates in (latitude, longitude). (Read-only)





