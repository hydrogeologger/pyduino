<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.sources.silo`
Utilities for retrieving historical meteorological data from SILO API.

Provides access to SILO datasets for use in post-processing workflows
and meteorological calculations.

Dependencies:  
- requests : For http POST request
- pandas : For dataframe support


**Example:**

```python
# Importing SILO longpaddock as a source
from postprocess.sources import silo
```


**Reference:**

- <https://www.longpaddock.qld.gov.au/silo/api-documentation/>
- <https://www.longpaddock.qld.gov.au/silo/api-documentation/reference/>
- <https://www.longpaddock.qld.gov.au/silo/about/climate-variables/>
- <https://www.longpaddock.qld.gov.au/silo/about/about-data/>


## Table of Contents
- [`SILOStation`](./postprocess.sources.silo.md#class-silostation): SILO Longpaddock BOM Station Metadata.
	- [`SILOStation.__init__`](./postprocess.sources.silo.md#constructor-silostation__init__): Constructor for SILO longpaddock station info.
- [`SILOStationRecord`](./postprocess.sources.silo.md#class-silostationrecord): SILOStationRecord(station_id, name, latitude, longitude, state, elevation_m, distance_km)
- [`dataframe_from_data`](./postprocess.sources.silo.md#function-dataframe_from_data): Extract timeseries data from SILO API point data response into DataFrame.
- [`find_nearby_stations`](./postprocess.sources.silo.md#function-find_nearby_stations): Return nearby SILO stations relative to a station or coordinates.
- [`get_nearby_stations`](./postprocess.sources.silo.md#function-get_nearby_stations): Return SILO stations within a radius of a reference station.
- [`get_point_data`](./postprocess.sources.silo.md#function-get_point_data): Retrieve climate data from the SILO point dataset.
- [`location_meta_from_data`](./postprocess.sources.silo.md#function-location_meta_from_data): Get station info from retrieved point or drill data.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py#L153"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `get_point_data`

```python
get_point_data(
    location,
    start,
    finish,
    comment='R',
    username='noemail@net.com',
    timeout=(5, 30),
    **params
)
```

Retrieve climate data from the SILO point dataset.

Station numbers query the Patched Point Dataset, while coordinate pairs
query the Data Drill Dataset. Station data may be supplemented by
interpolated estimates when observed data are missing.


**Args:**

- <b>`location`</b> (int | str | tuple): SILO/Bureau of Meteorology station number,
    or a geographic coordinate referenced to GDA94 (Geocentric Datum of
    Australia 1994), provided as a ``(latitude, longitude)`` tuple in
    decimal degrees.
- <b>`start`</b> (str | int | date): Start date in ``YYYYMMDD`` format or python date object.
- <b>`finish`</b> (str | int | date): End date in ``YYYYMMDD`` format or python date object.
- <b>`comment`</b> (str): String of SILO climate variable codes to request.
    For example, "RXN" requests daily rainfall, maximum temperature,
    and minimum temperature.

    Available climate variables:
    - ``R`` — Daily rainfall (mm)
    - ``X`` — Maximum temperature (°C)
    - ``N`` — Minimum temperature (°C)
    - ``V`` — Vapour pressure (hPa)
    - ``D`` — Vapour pressure deficit
    - ``E`` — Class A pan evaporation (mm)
    - ``S`` — Synthetic evaporation estimate (mm)
    - ``C`` — Combined evaporation (mm)
    - ``L`` — Morton's shallow lake evaporation (mm)
    - ``J`` — Solar radiation (MJ/m²)
    - ``H`` — Relative humidity at maximum temperature (%)
    - ``G`` — Relative humidity at minimum temperature (%)
    - ``F`` — FAO56 short-crop evapotranspiration (mm)
    - ``T`` — ASCE tall-crop evapotranspiration (mm)
    - ``A`` — Morton's areal actual evapotranspiration (mm)
    - ``P`` — Morton's point potential evapotranspiration (mm)
    - ``W`` — Morton's wet-environment areal potential evapotranspiration (mm)
    - ``M`` — Mean sea level pressure (hPa)

- <b>`username`</b> (str): SILO API username or registered email address to be contacted by
    SILO for any access problems or critical information updates.
- <b>`timeout`</b> (float or tuple): Request timeout in seconds. A single value
    sets the same timeout for connecting and receiving data; a
    ``(connect, read)`` tuple sets them separately. Defaults to
    ``(5, 30)``.
**params: Additional API parameters passed through directly.
    Use only for parameters that are not explicitly supported by this
    function.

    > [!WARNING] Use with caution
    > Parameters may override existing request parameters.


**Returns:**

- <b>`Dict[str, Any]`</b>: Parsed JSON response from the SILO API.


**Raises:**

- <b>`requests.RequestException`</b>: If the SILO API request fails.
- <b>`ValueError`</b>: If the coordinate pair is invalid or the response contains
    invalid JSON.


**Example:**

```python
>>> data = get_point_data(
...     location=40004,
...     start="20200101",
...     finish="20200131",
...     username="your_email@example.com",
...     comment="XN",
... )
>>> data["station"]["name"]
'AMBERLEY AMO'
```



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py#L271"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `location_meta_from_data`

```python
location_meta_from_data(point_data)
```

Get station info from retrieved point or drill data.


**Args:**

- <b>`point_data`</b> (dict): JSON response from point data API request.


**Returns:**

- <b>`SILOStation or LocationBase`</b>: Location metadata object.
- <b>`None`</b>: If no metadata was found.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py#L306"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `get_nearby_stations`

```python
get_nearby_stations(
    station_id,
    radius_km=50,
    sortby=None,
    timeout=(5, 30),
    **params
)
```

Return SILO stations within a radius of a reference station.

Queries the SILO Patched Point Dataset API and parses the response into
a list SILO stations records.


**Args:**

- <b>`station_id`</b> (int or str): Reference SILO BOM station number.
- <b>`radius_km`</b> (float): Search radius in kilometres. Defaults to 50.
- <b>`sortby`</b> (str, optional): Sort field. Currently, only ``"name"`` has
    been observed to return results; ``"ID"`` and ``"dist"`` return
    an empty response. If None, the API's default ordering is used.
    Defaults to None.
- <b>`timeout`</b> (float or tuple): Request timeout in seconds. A single value
    sets the same timeout for connecting and receiving data; a
    ``(connect, read)`` tuple sets them separately. Defaults to
    ``(5, 30)``.
**params: Additional API parameters passed through directly.
    Use only for parameters that are not explicitly supported by this
    function.

    > [!WARNING] Use with caution
    > Parameters may override existing request parameters.


**Returns:**

- <b>`list[SILOStationRecord]`</b>: Stations within the specfiied radius,
    sorted by distance; empty if none are found.
    See the :class:`SILOStationRecord` for mapping.


**Raises:**

- <b>`requests.HTTPError`</b>: If the SILO API returns an unsuccessful HTTP
    status code.
- <b>`requests.RequestException`</b>: If the request fails.
- <b>`ValueError`</b>: If the SILO response has an unexpected format or
    contains invalid station data.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py#L417"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `find_nearby_stations`

```python
find_nearby_stations(location, radius_km=50, timeout=(5, 30))
```

Return nearby SILO stations relative to a station or coordinates.

Coordinate-based searches use BOM station 15603 (Kulgera) as the SILO
reference station, then calculate Haversine distances from the supplied
coordinates and filter results by radius.


**Args:**

- <b>`location`</b> (str, int or tuple): Reference SILO station number or a
    (latitude, longitude) coordinate pair.
- <b>`radius_km`</b> (float): Search radius in kilometres. Defaults to 50.
- <b>`timeout`</b> (float or tuple): Request timeout in seconds. A single value
    sets the same timeout for connecting and receiving data; a
    ``(connect, read)`` tuple sets them separately. Defaults to
    ``(5, 30)``.


**Returns:**

    list[SILOStationRecord]: Stations within the specfiied radius,
        sorted by distance; empty if none are found.
        See the :class:`SILOStationRecord` for mapping.


**Raises:**

- <b>`ValueError`</b>: If location is a coordinate pair with invalid values.
- <b>`requests.HTTPError`</b>: If the SILO API returns an unsuccessful HTTP
    status code.
- <b>`requests.RequestException`</b>: If the request fails.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py#L483"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `dataframe_from_data`

```python
dataframe_from_data(
    point_data,
    include_source=False,
    ascending=True,
    date_format='%Y-%m-%d'
)
```

Extract timeseries data from SILO API point data response into DataFrame.


**Args:**

- <b>`point_data`</b> (dict): JSON response from the SILO get point data API.
- <b>`include_source`</b> (bool, optional): Whether to preserve and include the 'source'
    metadata column alongside the primary 'value' column for each metric.
    Defaults to True.
- <b>`ascending`</b> (bool, optional): Sort chronological (True) or reverse (False).
    Defaults to True.
- <b>`date_format`</b> (str, optional): Format string to inform pandas how
    to parse the date (e.g., '%Y-%m-%d' or 'ISO8601'). Defaults to
    '%Y-%m-%d'; pass None to enable automatic inference.


**Raises:**

- <b>`TypeError`</b>: ``point_data`` is not a dictionary.
- <b>`ValueError`</b>: ``point_data`` is empty.
- <b>`KeyError`</b>: Timeseries data is missing from ``point_data``.


**Returns:**

- <b>`pandas.DataFrame`</b>: A DataFrame containing time-series data, featuring flat
    column headers containing field names by default, or MultiIndex column
    headers (field name and metric type) when include_source is True.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `SILOStationRecord`
SILOStationRecord(station_id, name, latitude, longitude, state, elevation_m, distance_km)






<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py#L104"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `SILOStation`
SILO Longpaddock BOM Station Metadata.


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
- <b>`elevation_m`</b> (float): Elevation of station, measured as metres above sea level.
    Inherited from :class:`LocationBase`.
- <b>`state`</b> (str): Australian state or territory abbreviation where the station is located.
- <b>`coordinates`</b> (tuple): Coordinates in (latitude, longitude).
    Inherited from :class:`LocationBase`.


<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py#L126"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `SILOStation.__init__`

```python
SILOStation(station_id, name, latitude, longitude, elevation_m, state)
```

Constructor for SILO longpaddock station info.


**Args:**

- <b>`station_id`</b> (int or str): Bureau of Meteorology station identifier number
- <b>`name`</b> (str): Name of the station.
- <b>`latitude`</b> (float): Latitude of the station in decimal degrees,
    referenced to the GDA94 (Geocentric Datum of Australia 1994)
    coordinate reference system.
- <b>`longitude`</b> (float): Longitude of the station in decimal degrees,
    referenced to the GDA94 (Geocentric Datum of Australia 1994)
    coordinate reference system.
- <b>`elevation_m`</b> (float): Elevation of station, measured as metres above sea level.
- <b>`state`</b> (str): Australian state or territory abbreviation where
    the station is located.



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> SILOStation.coordinates

Coordinates in (latitude, longitude). (Read-only)





