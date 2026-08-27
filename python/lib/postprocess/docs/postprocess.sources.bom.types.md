<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/types.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.sources.bom.types`
Shared type definitions for the postprocess.sources.bom subpackage.


**References:**

- https://www.bom.gov.au/climate/data/lists_by_element/stations.txt


## Table of Contents
- [`BOMStationBase`](./postprocess.sources.bom.types.md#class-bomstationbase): Base Bureau of Meteorology Station Metadata.
	- [`BOMStationBase.__init__`](./postprocess.sources.bom.types.md#constructor-bomstationbase__init__): Constructor for BOM station info.
- [`BOMStationRecord`](./postprocess.sources.bom.types.md#class-bomstationrecord): BOMStationRecord(station_id, region, name, start_date, end_date, latitude, longitude, source, state, elevation_m, barometer_height_m, wmo_id)




<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/types.py"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `BOMStationRecord`
BOMStationRecord(station_id, region, name, start_date, end_date, latitude, longitude, source, state, elevation_m, barometer_height_m, wmo_id)






<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/types.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `BOMStationBase`
Base Bureau of Meteorology Station Metadata.


**Attributes:**

- <b>`station_id`</b> (int or str): Bureau of Meteorology station identifier number.
- <b>`name`</b> (str): Name of the station.
    Inherited from :class:`LocationBase`.
- <b>`latitude`</b> (float): Latitude of the station in decimal degrees,
    referenced to the GDA94 (Geocentric Datum of Australia 1994)
    coordinate reference system. Inherited from
    :class:`LocationBase`.
- <b>`longitude`</b> (float): Longitude of the station in decimal degrees,
    referenced to the GDA94 (Geocentric Datum of Australia 1994)
    coordinate reference system. Inherited from
    :class:`LocationBase`.
- <b>`state`</b> (str): Australian state or territory abbreviation where
    the station is located.
- <b>`elevation_m`</b> (float or None): Elevation of station,
    measured as metres above sea level.
    Inherited from :class:`LocationBase`.
- <b>`coordinates`</b> (tuple): Coordinates in (latitude, longitude).
    Inherited from :class:`LocationBase`.


<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/types.py#L89"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `BOMStationBase.__init__`

```python
BOMStationBase(station_id, name, latitude, longitude, state, elevation_m=None)
```

Constructor for BOM station info.


**Args:**

- <b>`station_id`</b> (int or str): Bureau of Meteorology station identifier number
- <b>`name`</b> (str): Name of the station.
- <b>`latitude`</b> (float): Latitude of the station in decimal degrees,
    referenced to the GDA94 (Geocentric Datum of Australia 1994)
    coordinate reference system.
- <b>`longitude`</b> (float): Longitude of the station in decimal degrees,
    referenced to the GDA94 (Geocentric Datum of Australia 1994)
    coordinate reference system.
- <b>`state`</b> (str): Australian state or territory abbreviation where
    the station is located.
- <b>`elevation_m`</b> (float, optional): Elevation of station,
    measured as metres above sea level.



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> BOMStationBase.coordinates

Coordinates in (latitude, longitude). (Read-only)





