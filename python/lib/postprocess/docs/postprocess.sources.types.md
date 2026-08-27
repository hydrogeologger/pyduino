<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/sources/types.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.sources.types`
Shared type definitions for the postprocess.sources subpackage.


## Table of Contents
- [`Coordinates`](./postprocess.sources.types.md#class-coordinates): Coordinates(latitude, longitude)
- [`LocationMetadata`](./postprocess.sources.types.md#class-locationmetadata): Stores geographical metadata for general locations.
	- [`LocationMetadata.__init__`](./postprocess.sources.types.md#constructor-locationmetadata__init__): Initialise location metadata.


**Global Variables**
---------------
- **TYPE_CHECKING** = False


<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/types.py"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `Coordinates`
Coordinates(latitude, longitude)






<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/types.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `LocationMetadata`
Stores geographical metadata for general locations.


**Attributes:**

- <b>`latitude`</b> (float): Latitude in decimal degrees. Positive values indicate
    north of the Equator; negative values indicate south.
- <b>`longitude`</b> (float): Longitude in decimal degrees. Positive values indicate
    east of the Prime Meridian; negative values indicate west.
- <b>`elevation`</b> (float or None): Elevation above sea level in metres.
- <b>`name`</b> (str): The common descriptor or name of the location.


<a href="../../../../python/lib/postprocess/src/postprocess/sources/types.py#L42"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `LocationMetadata.__init__`

```python
LocationMetadata(latitude, longitude, elevation=None, name='')
```

Initialise location metadata.


**Args:**

- <b>`latitude`</b> (float): Latitude in decimal degrees. Positive values indicate
    north of the Equator; negative values indicate south.
- <b>`longitude`</b> (float): Longitude in decimal degrees. Positive values indicate
    east of the Prime Meridian; negative values indicate west.
- <b>`elevation`</b> (float, Optional): Elevation measured as metre above sea level.
    Defaults to None.
- <b>`name`</b> (str, Optional): Common descriptor or name of the location.
    Defaults to "".



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> LocationMetadata.coordinates

Coordinates in (latitude, longitude). (Read-only)





