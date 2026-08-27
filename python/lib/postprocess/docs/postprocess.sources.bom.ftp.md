<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/ftp.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.sources.bom.ftp`
Access historical climate and weather observation data from the
Australian Bureau of Meteorology's anonymous FTP service.

This is an unofficial, community-developed interface and is not
affiliated with, endorsed by, or officially supported by the Bureau
of Meteorology.

Use of Bureau of Meteorology data is subject to the applicable
copyright, licensing, and terms-of-use requirements. See the
Bureau's copyright notice for details:  

https://www.bom.gov.au/copyright


**References:**

- https://www.bom.gov.au/catalogue/anon-ftp.shtml
- ftp://ftp.bom.gov.au/anon2/home/ncc/metadata/sitelists/stations.zip
- https://www.bom.gov.au/climate/cdo/about/site-num.shtml


## Table of Contents
- [`BOMStationDistanceRecord`](./postprocess.sources.bom.ftp.md#class-bomstationdistancerecord): BOMStationDistanceRecord(distance_km, station)
- [`DailyWeatherObservations`](./postprocess.sources.bom.ftp.md#class-dailyweatherobservations): Client for accessing daily weather observations via FTP.
	- [`DailyWeatherObservations.__init__`](./postprocess.sources.bom.ftp.md#constructor-dailyweatherobservations__init__)
	- [`DailyWeatherObservations.fetch_stations_list`](./postprocess.sources.bom.ftp.md#classmethod-dailyweatherobservationsfetch_stations_list): Fetch the list of weather stations from the BOM FTP server.
	- [`DailyWeatherObservations.find_nearby_stations`](./postprocess.sources.bom.ftp.md#method-dailyweatherobservationsfind_nearby_stations): Find weather stations within a given distance of a location.
	- [`DailyWeatherObservations.load_observations`](./postprocess.sources.bom.ftp.md#method-dailyweatherobservationsload_observations): Load weather observations for a station over a range of dates.
	- [`DailyWeatherObservations.load_observations_for_station`](./postprocess.sources.bom.ftp.md#classmethod-dailyweatherobservationsload_observations_for_station): Load weather observations for a station over a range of dates.
	- [`DailyWeatherObservations.resolve_station`](./postprocess.sources.bom.ftp.md#method-dailyweatherobservationsresolve_station): Resolve a BOM weather station from a station ID, name, or coordinates.
	- [`DailyWeatherObservations.set_station`](./postprocess.sources.bom.ftp.md#method-dailyweatherobservationsset_station): Set the station used for daily weather observations.
- [`slugify_bom_ftp_segment`](./postprocess.sources.bom.ftp.md#function-slugify_bom_ftp_segment): Converts a raw BOM data string into a lowercase, filesystem-safe slug.


**Global Variables**
---------------
- **BOM_FTP_DOMAIN** = ftp.bom.gov.au
- **BOM_FTP_ANON_GEN_DIR** = /anon/gen
- **BOM_FTP_ANON2_HOME_DIR** = /anon2/home

<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/ftp.py#L562"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `slugify_bom_ftp_segment`

```python
slugify_bom_ftp_segment(text_segment)
```

Converts a raw BOM data string into a lowercase, filesystem-safe slug.

Maps spaces directly to underscores and strips illegal punctuation while
explicitly preserving structural characters (hyphens, parentheses, and 
consecutive spacing) required by the BOM FTP server.


**Args:**

- <b>`text_segment`</b>: The raw station name, state, or text block to process.


**Returns:**

The normalized, lowercase slug string.


**Examples:**

```python
>>> slugify_bom_ftp_segment("Holsworthy - Defence")
'holsworthy_-_defence'
>>> slugify_bom_ftp_segment("TAS ")
'tas_'
```



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/ftp.py"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `BOMStationDistanceRecord`
BOMStationDistanceRecord(distance_km, station)






<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/ftp.py#L86"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `DailyWeatherObservations`
Client for accessing daily weather observations via FTP.

Provides access to station information and historical observation data,
including current daily weather observations, published through the
Bureau of Meteorology's anonymous FTP service.


<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/ftp.py#L103"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `DailyWeatherObservations.__init__`

```python
DailyWeatherObservations()
```

*No documentation found.*


<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> DailyWeatherObservations.station

The station used for daily weather observations.




<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/ftp.py#L112"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>classmethod</kbd> `DailyWeatherObservations.fetch_stations_list`

```python
fetch_stations_list(timeout=30)
```

Fetch the list of weather stations from the BOM FTP server.

The downloaded station information is used to replace the existing
station cache and its lookup dictionaries. The cache is only updated
after the station list has been successfully downloaded and parsed.


**Args:**

- <b>`timeout`</b> (float, optional): Number of seconds to wait for an FTP
    operation before timing out. Defaults to 30.


**Returns:**

- <b>`DailyWeatherObservations`</b>: A new instance of the class after the
    station cache has been refreshed.


**Raises:**

- <b>`RuntimeError`</b>: If the BOM FTP server does not allow the station
    list to be retrieved.
- <b>`ValueError`</b>: If a station record contains invalid data.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/ftp.py#L357"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `DailyWeatherObservations.find_nearby_stations`

```python
find_nearby_stations(location, radius_km=50)
```

Find weather stations within a given distance of a location.

The location can be specified using a station name, station ID, or a
pair of latitude and longitude coordinates. The returned stations are
sorted from nearest to farthest.


**Args:**

- <b>`location`</b> (str, int, tuple[float, float]): Reference location used
    to calculate distances. A string is interpreted as a station
    name, an integer as a station ID, and a tuple as decimal-degree
    coordinates in the form ``(latitude, longitude)``.
- <b>`radius_km`</b> (float, optional): Maximum distance from the reference
    location, in kilometres. Stations farther away are not
    included. Defaults to 50.


**Returns:**

- <b>`list[BOMStationDistanceRecord]`</b>: A list of stations within
    ``radius_km`` of the reference location, sorted by distance
    from nearest to farthest. Returns an empty list if no stations
    are within the specified radius or the reference location
    cannot be resolved.


**Raises:**

- <b>`ValueError`</b>: If the coordinates are invalid or the reference
    location cannot be resolved to a station.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/ftp.py#L498"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `DailyWeatherObservations.load_observations`

```python
load_observations(
    start_date,
    end_date,
    as_single_dataframe=True,
    ascending=True,
    timeout=30
)
```

Load weather observations for a station over a range of dates.

The data is stored in separate files for each month. The given dates
are therefore expanded to cover their entire months. For example, a
start date of 2024-03-15 will load data starting from March 1, and an
end date of 2024-06-10 will load data through June 30.


**Args:**

- <b>`start_date`</b> (date or datetime): First date to load. If a datetime
    is given, only its date is used.
- <b>`end_date`</b> (date or datetime): Last date to load. If a datetime is
    given, only its date is used.
- <b>`as_single_dataframe`</b> (bool, optional): If True, combine all monthly
    data into one DataFrame. If False, return a dictionary containing
    a separate DataFrame for each successfully loaded monthly file,
    using the filename as the dictionary key. Defaults to True.
- <b>`ascending`</b> (bool, optional): Sort chronological (True) or reverse (False).
    Defaults to True.
- <b>`timeout`</b> (float, optional): Number of seconds to wait for an FTP
    operation before timing out. Defaults to 30.


**Returns:**

- <b>`pandas.DataFrame`</b>: When `as_single_dataframe` is True. The
    DataFrame contains all successfully loaded observations, uses
    `Date` as its index, and has flattened column names. If no
    monthly files could be loaded, an empty DataFrame is returned.
- <b>`dict[str, pandas.DataFrame]`</b>: When `as_single_dataframe` is False.
    Each key is the filename of a successfully loaded monthly file,
    and its value is the corresponding DataFrame. Each DataFrame
    uses `Date` as its index and has flattened column names. If no
    monthly files could be loaded, an empty dictionary is returned.


**Raises:**

- <b>`ValueError`</b>: If no station has been set (i.e., `self.station` is
    `None`), or if `end_date` is before `start_date`.
- <b>`TypeError`</b>: If `start_date` or `end_date` is not a `date` or
    `datetime` object.


**See Also:**

:meth:`load_observations_for_station`


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/ftp.py#L205"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>classmethod</kbd> `DailyWeatherObservations.load_observations_for_station`

```python
load_observations_for_station(
    station_name,
    state,
    start_date,
    end_date,
    as_single_dataframe=True,
    ascending=True,
    timeout=30
)
```

Load weather observations for a station over a range of dates.

The data is stored in separate files for each month. The given dates
are therefore expanded to cover their entire months. For example, a
start date of 2024-03-15 will load data starting from March 1, and an
end date of 2024-06-10 will load data through June 30.


**Args:**

- <b>`station_name`</b> (str): Name of the weather station.
- <b>`state`</b> (str): Australian state or territory abbreviation where the
    station is located.
- <b>`start_date`</b> (date or datetime): First date to load. If a datetime
    is given, only its date is used.
- <b>`end_date`</b> (date or datetime): Last date to load. If a datetime is
    given, only its date is used.
- <b>`as_single_dataframe`</b> (bool, optional): If True, combine all monthly
    data into one DataFrame. If False, return a dictionary containing
    a separate DataFrame for each successfully loaded monthly file,
    using the filename as the dictionary key. Defaults to True.
- <b>`ascending`</b> (bool, optional): Sort chronological (True) or reverse (False).
    Defaults to True.
- <b>`timeout`</b> (float, optional): Number of seconds to wait for an FTP
    operation before timing out. Defaults to 30.


**Returns:**

- <b>`pandas.DataFrame`</b>: When `as_single_dataframe` is True. The
    DataFrame contains all successfully loaded observations, uses
    `Date` as its index, and has flattened column names. If no
    monthly files could be loaded, an empty DataFrame is returned.
- <b>`dict[str, pandas.DataFrame]`</b>: When `as_single_dataframe` is False.
    Each key is the filename of a successfully loaded monthly file,
    and its value is the corresponding DataFrame. Each DataFrame
    uses `Date` as its index and has flattened column names. If no
    monthly files could be loaded, an empty dictionary is returned.


**Raises:**

- <b>`TypeError`</b>: If `start_date` or `end_date` is not a date or datetime.
- <b>`ValueError`</b>: If `station_name` or `state` is empty, or if
    `end_date` is before `start_date`.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/ftp.py#L446"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `DailyWeatherObservations.resolve_station`

```python
resolve_station(location, set_station=False)
```

Resolve a BOM weather station from a station ID, name, or coordinates.


**Args:**

- <b>`location`</b> (str, int, tuple): Station ID, station name, or a
    ``(latitude, longitude)`` tuple. Numeric strings are treated
    as station IDs.
- <b>`set_station`</b> (bool): If ``True``, set the resolved station as
    the current station. Defaults to ``False``.


**Returns:**

- <b>`BOMStationBase or None`</b>: The resolved station, or ``None`` if no
    matching station is found.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/ftp.py#L422"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `DailyWeatherObservations.set_station`

```python
set_station(station)
```

Set the station used for daily weather observations.


**Args:**

- <b>`station`</b> (BOMStationBase or int): A ``BOMStationBase`` record or an open BOM
    station ID.


**Raises:**

- <b>`ValueError`</b>: If no station is found for the given station ID.
- <b>`TypeError`</b>: If ``station`` is not a ``BOMStationBase`` or ``int``.



