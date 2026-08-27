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
- [`SILOStationMetadata`](./postprocess.sources.silo.md#class-silostationmetadata): SILO Longpaddock BOM Station Metadata.
	- [`SILOStationMetadata.__init__`](./postprocess.sources.silo.md#constructor-silostationmetadata__init__): Constructor for SILO longpaddock station info.
- [`extract_timeseries_dataframe`](./postprocess.sources.silo.md#function-extract_timeseries_dataframe): Extract timeseries data from SILO API point data response into DataFrame.
- [`find_nearby_stations`](./postprocess.sources.silo.md#function-find_nearby_stations): Return nearby SILO stations relative to a station or coordinates.
- [`get_location_meta`](./postprocess.sources.silo.md#function-get_location_meta): Get station info from retrieved point or drill data.
- [`get_nearby_stations`](./postprocess.sources.silo.md#function-get_nearby_stations): Return SILO stations within a radius of a reference station.
- [`get_point_data`](./postprocess.sources.silo.md#function-get_point_data): Retrieve climate data from the SILO point dataset.


**Global Variables**
---------------
- **TYPE_CHECKING** = False

<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `get_point_data`

```python
get_point_data(
    location,
    start,
    finish,
    comment='R',
    username='noemail@net.com',
    timeout=(5, 30)
)
```

Retrieve climate data from the SILO point dataset.

Station numbers query the Patched Point Dataset, while coordinate pairs
query the Data Drill Dataset. Station data may be supplemented by
interpolated estimates when observed data are missing.


**Args:**

- <b>`location`</b> (int | str | tuple): SILO/Bureau of Meteorology station number
    or a ``(latitude, longitude)`` coordinate pair.
- <b>`start`</b> (str | int | date): Start date in ``YYYYMMDD`` format or python date object.
- <b>`finish`</b> (str | int | date): End date in ``YYYYMMDD`` format or python date object.
- <b>`comment`</b> (str): String of SILO climate variable codes to request.
    For example, "RXN" requests daily rainfall, maximum temperature,
    and minimum temperature.

    Available climate variables:
    - `R` — Daily rainfall (mm)
    - `X` — Maximum temperature (°C)
    - `N` — Minimum temperature (°C)
    - `V` — Vapour pressure (hPa)
    - `D` — Vapour pressure deficit
    - `E` — Class A pan evaporation (mm)
    - `S` — Synthetic evaporation estimate (mm)
    - `C` — Combined evaporation (mm)
    - `L` — Morton's shallow lake evaporation (mm)
    - `J` — Solar radiation (MJ/m²)
    - `H` — Relative humidity at maximum temperature (%)
    - `G` — Relative humidity at minimum temperature (%)
    - `F` — FAO56 short-crop evapotranspiration (mm)
    - `T` — ASCE tall-crop evapotranspiration (mm)
    - `A` — Morton's areal actual evapotranspiration (mm)
    - `P` — Morton's point potential evapotranspiration (mm)
    - `W` — Morton's wet-environment areal potential evapotranspiration (mm)
    - `M` — Mean sea level pressure (hPa)

- <b>`username`</b> (str): SILO API username or registered email address to be contacted by
    SILO for any access problems or critical information updates.
- <b>`timeout`</b> (float or tuple): Request timeout in seconds. A single value
    sets the same timeout for connecting and receiving data; a
    ``(connect, read)`` tuple sets them separately. Defaults to
    ``(5, 30)``.


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

<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py#L197"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `get_location_meta`

```python
get_location_meta(point_data)
```

Get station info from retrieved point or drill data.


**Args:**

- <b>`point_data`</b> (dict): JSON response from point data API request.


**Returns:**

- <b>`SILOStationMetadata or LocationMetadata`</b>: Location metadata object.
- <b>`None`</b>: If no metadata was found.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py#L230"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `get_nearby_stations`

```python
get_nearby_stations(station_id, radius=50, sortby=None, timeout=(5, 30))
```

Return SILO stations within a radius of a reference station.

Queries the SILO Patched Point Dataset API and parses the response into
a list of station dictionaries.


**Args:**

- <b>`station_id`</b> (int or str): Reference SILO BOM station number.
- <b>`radius`</b> (float): Search radius in kilometres. Defaults to 50.
- <b>`sortby`</b> (str, optional): Sort field. Currently, only ``"name"`` has
    been observed to return results; ``"ID"`` and ``"dist"`` return
    an empty response. If None, the API's default ordering is used.
    Defaults to None.
- <b>`timeout`</b> (float or tuple): Request timeout in seconds. A single value
    sets the same timeout for connecting and receiving data; a
    ``(connect, read)`` tuple sets them separately. Defaults to
    ``(5, 30)``.


**Returns:**

- <b>`list[dict]`</b>: A list of nearby stations, or an empty list if no stations are found.
    Each station dictionary contains the following keys:

    - ``number`` (int): SILO station number.
    - ``name`` (str): Station name.
    - ``latitude`` (float): Latitude of the station in GDA94.
    - ``longitude`` (float): Longitude of the station in GDA94.
    - ``elevation`` (float): Station elevation in metres.
    - ``state`` (str): Australian state or territory.
    - ``distance_km`` (float): Distance from the reference station
      in kilometres, as reported by SILO.


**Raises:**

- <b>`requests.HTTPError`</b>: If the SILO API returns an unsuccessful HTTP
    status code.
- <b>`requests.RequestException`</b>: If the request fails.
- <b>`ValueError`</b>: If the SILO response has an unexpected format or
    contains invalid station data.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py#L324"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `find_nearby_stations`

```python
find_nearby_stations(location, radius=50, timeout=(5, 30))
```

Return nearby SILO stations relative to a station or coordinates.

Coordinate-based searches use BOM station 15603 (Kulgera) as the SILO
reference station, then calculate Haversine distances from the supplied
coordinates and filter results by radius.


**Args:**

- <b>`location`</b> (str, int or tuple): Reference SILO station number or a
    (latitude, longitude) coordinate pair.
- <b>`radius`</b> (float): Search radius in kilometres. Defaults to 50.
- <b>`timeout`</b> (float or tuple): Request timeout in seconds. A single value
    sets the same timeout for connecting and receiving data; a
    ``(connect, read)`` tuple sets them separately. Defaults to
    ``(5, 30)``.


**Returns:**

    list[dict]: A list of nearby stations, or an empty list if no stations are found.
        Each station dictionary contains the following keys:

        - ``number`` (int): SILO station number.
        - ``name`` (str): Station name.
        - ``latitude`` (float): Latitude of the station in GDA94.
        - ``longitude`` (float): Longitude of the station in GDA94.
        - ``elevation`` (float): Station elevation in metres.
        - ``state`` (str): Australian state or territory.
        - ``distance_km`` (float): Distance from the reference station
            or coordinates in kilometres.


**Raises:**

- <b>`ValueError`</b>: If location is a coordinate pair with invalid values.
- <b>`requests.HTTPError`</b>: If the SILO API returns an unsuccessful HTTP
    status code.
- <b>`requests.RequestException`</b>: If the request fails.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py#L394"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `extract_timeseries_dataframe`

```python
extract_timeseries_dataframe(point_data)
```

Extract timeseries data from SILO API point data response into DataFrame.


**Args:**

- <b>`point_data`</b> (dict): JSON response from the SILO get point data API.


**Raises:**

- <b>`ValueError`</b>: JSON response is empty.
- <b>`KeyError`</b>: Timeseries data is missing from JSON response.


**Returns:**

- <b>`pandas.DataFrame`</b>: A DataFrame containing timeseries data.
    With column headers containing field names and data code source.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `SILOStationMetadata`
SILO Longpaddock BOM Station Metadata.


**Attributes:**

- <b>`number`</b> (int or str): Beauro of Meteorology station number.
- <b>`name`</b> (str): Name of the station.
    Inherited from :class:`LocationMetadata`.
- <b>`latitude`</b> (float): Latitude of the station in GDA94.
    Inherited from :class:`LocationMetadata`.
- <b>`longitude`</b> (float): Longitude of the station in GDA94.
    Inherited from :class:`LocationMetadata`.
- <b>`elevation`</b> (float): Elevation of station, measured as metres above sea level.
    Inherited from :class:`LocationMetadata`.
- <b>`state`</b> (str or None): State in which station is located.
- <b>`coordinates`</b> (tuple): Coordinates in (latitude, longitude).
    Inherited from :class:`LocationMetadata`.


<a href="../../../../python/lib/postprocess/src/postprocess/sources/silo.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `SILOStationMetadata.__init__`

```python
SILOStationMetadata(number, name, latitude, longitude, elevation, state)
```

Constructor for SILO longpaddock station info.


**Args:**

- <b>`number`</b> (int or str): Beauro of Meteorology station number
- <b>`name`</b> (str): Name of the station.
- <b>`latitude`</b> (float): Latitude of the station in GDA94.
- <b>`longitude`</b>: Longitude of the station in GDA94.
- <b>`elevation`</b> (float): Elevation of station, measured as metres above sea level.
- <b>`state`</b> (str): State in which station is located.



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> SILOStationMetadata.coordinates

Coordinates in (latitude, longitude). (Read-only)





