<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/cdio.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.sources.bom.cdio`
Client for accessing historical climate and weather observations
from the Australian Bureau of Meteorology's Climate Data Online service.

This is an unofficial, community-developed interface and is not
affiliated with, endorsed by, or officially supported by the Bureau
of Meteorology.

Use of Bureau of Meteorology data is subject to the applicable
copyright, licensing, and terms-of-use requirements. See the
Bureau's copyright notice for details:  

https://www.bom.gov.au/copyright

Obtained by reverse engineering API access: https://www.bom.gov.au/climate/data/index.shtml


**References:**

- https://www.bom.gov.au/climate/cdo/about/cdo-faqs.shtml
- https://www.bom.gov.au/climate/cdo/about/site-num.shtml
- https://www.bom.gov.au/climate/cdo/about/about-directory.shtml
- https://www.bom.gov.au/climate/data/
- https://www.bom.gov.au//climate/cdo/about/sitedata.shtml
- https://www.bom.gov.au/climate/data/stations/


## Table of Contents
- [`DWOStation`](./postprocess.sources.bom.cdio.md#class-dwostation): DWOStation(dwo_id, station_id, name, state, distance_km, is_open)
- [`Location`](./postprocess.sources.bom.cdio.md#class-location): Represents a geographic location returned from BOM gazetteer.
	- [`Location.__init__`](./postprocess.sources.bom.cdio.md#constructor-location__init__): Initializes a Location.
	- [`Location.from_string`](./postprocess.sources.bom.cdio.md#classmethod-locationfrom_string): Creates a Location from a matching location record.
	- [`Location.to_bom_string`](./postprocess.sources.bom.cdio.md#method-locationto_bom_string): Return this location in the format expected by BOM.
- [`StationFinder`](./postprocess.sources.bom.cdio.md#class-stationfinder): An execution system mirroring the BOM Climate Data Online Text Tool Guide.
	- [`StationFinder.find_matching_locations`](./postprocess.sources.bom.cdio.md#method-stationfinderfind_matching_locations): Find locations matching town names using the BOM gazetteer.
	- [`StationFinder.find_nearest_stations`](./postprocess.sources.bom.cdio.md#method-stationfinderfind_nearest_stations): Find BOM weather stations near a location.
- [`WeatherObservationsClient`](./postprocess.sources.bom.cdio.md#class-weatherobservationsclient): Client for finding stations and retrieving BOM daily weather observations.
	- [`WeatherObservationsClient.__init__`](./postprocess.sources.bom.cdio.md#constructor-weatherobservationsclient__init__)
	- [`WeatherObservationsClient.find_nearest_stations`](./postprocess.sources.bom.cdio.md#classmethod-weatherobservationsclientfind_nearest_stations): Find stations with daily weather observations near a location.
	- [`WeatherObservationsClient.load_observations`](./postprocess.sources.bom.cdio.md#method-weatherobservationsclientload_observations): Load weather observations for a station over a range of dates.
	- [`WeatherObservationsClient.set_station`](./postprocess.sources.bom.cdio.md#method-weatherobservationsclientset_station): Set the station used for daily weather observations.


**Global Variables**
---------------
- **NCC_OBS_CODES** = {136: {'name': 'Daily rainfall', 'element_group': 'rainfall', 'element_type': 2, 'element_order': 'daily', 'description': 'Daily rainfall data and graphs for a selected year. Data download for one or all years.', 'web_map_layer': 'IDC10002-d'}, 139: {'name': 'Monthly rainfall', 'element_group': 'rainfall', 'element_type': 2, 'element_order': 'monthly', 'description': 'Monthly rainfall data and graphs for all available years.', 'web_map_layer': 'IDC10002'}, 36: {'name': 'Monthly mean maximum temperature', 'element_group': 'temperature', 'element_type': 3, 'element_order': 'monthly', 'description': 'Mean maximum temperature data and graphs for all available years.', 'web_map_layer': 'IDC10008'}, 38: {'name': 'Monthly mean minimum temperature', 'element_group': 'temperature', 'element_type': 3, 'element_order': 'monthly', 'description': 'Mean minimum temperature data and graphs for all available years.', 'web_map_layer': 'IDC10003'}, 40: {'name': 'Monthly highest temperature', 'element_group': 'temperature', 'element_type': 3, 'element_order': 'monthly', 'description': 'Highest temperature data and graphs for all available years.', 'web_map_layer': 'IDC10006'}, 41: {'name': 'Monthly lowest maximum temperature', 'element_group': 'temperature', 'element_type': 3, 'element_order': 'monthly', 'description': 'Lowest maximum temperature data and graphs for all available years.', 'web_map_layer': 'IDC10004'}, 42: {'name': 'Monthly highest minimum temperature', 'element_group': 'temperature', 'element_type': 3, 'element_order': 'monthly', 'description': 'Highest minimum temperature data and graphs for all available years.', 'web_map_layer': 'IDC10007'}, 43: {'name': 'Monthly lowest temperature', 'element_group': 'temperature', 'element_type': 3, 'element_order': 'monthly', 'description': 'Lowest temperature data and graphs for all available years.', 'web_map_layer': 'IDC10005'}, 201: {'name': 'Daily weather observations', 'element_group': 'weather', 'element_type': 1, 'element_order': 'daily', 'description': 'Daily weather observations data for the last month. Links to data for the previous year. Data may be from a number of stations.', 'web_map_layer': 'IDC10001'}, 200: {'name': 'Monthly climate statistics', 'element_group': 'weather', 'element_type': 1, 'element_order': 'statistics', 'description': 'Monthly climate statistics and graphs for all available years.', 'web_map_layer': 'IDC10000'}, 202: {'name': 'Daily climate calendar', 'element_group': 'weather', 'element_type': 1, 'element_order': 'calendar', 'description': 'Calendar of daily statistics showing typical weather for each day and some weather history.', 'web_map_layer': 'IDC10000-d'}, 122: {'name': 'Daily maximum temperature', 'element_group': 'temperature', 'element_type': 3, 'element_order': 'daily', 'description': 'Daily maximum temperature data and graphs for a selected year. Data download for one or all years.', 'web_map_layer': 'IDC10025'}, 123: {'name': 'Daily minimum temperature', 'element_group': 'temperature', 'element_type': 3, 'element_order': 'daily', 'description': 'Daily minimum temperature data and graphs for a selected year. Data download for one or all years.', 'web_map_layer': 'IDC10024'}, 193: {'name': 'Daily solar exposure', 'element_group': 'solar', 'element_type': 4, 'element_order': 'daily', 'description': 'Daily solar exposure data and graphs for a selected year. Data download for one or all years.', 'web_map_layer': 'IDCJAC0016-d'}, 203: {'name': 'Monthly solar exposure', 'element_group': 'solar', 'element_type': 4, 'element_order': 'monthly', 'description': 'Monthly mean daily solar exposure data and graphs for all available years.', 'web_map_layer': 'IDCJAC0016'}}


<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/cdio.py"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `DWOStation`
DWOStation(dwo_id, station_id, name, state, distance_km, is_open)






<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/cdio.py#L253"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `Location`
Represents a geographic location returned from BOM gazetteer.

This class extends :class:`LocationBase`.


**Attributes:**

- <b>`state`</b> (str): Australian state or territory abbreviation.


<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/cdio.py#L262"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `Location.__init__`

```python
Location(name, state, latitude, longitude)
```

Initializes a Location.


**Args:**

- <b>`name`</b> (str): Name of the location.
- <b>`state`</b> (str): Australian state or territory abbreviation.
- <b>`latitude`</b> (float): Latitude in decimal degrees.
- <b>`longitude`</b> (float): Longitude in decimal degrees.



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> Location.coordinates

Coordinates in (latitude, longitude). (Read-only)




<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/cdio.py#L289"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>classmethod</kbd> `Location.from_string`

```python
from_string(value)
```

Creates a Location from a matching location record.

Expected value:  
```
'Melbourne, VIC, 37.84°S, 144.98°E'
```


**Args:**

- <b>`value`</b> (str): Location string returned by
    :meth:`find_matching_locations`.


**Returns:**

- <b>`Location`</b>: A Location instance containing the parsed location data.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/cdio.py#L315"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Location.to_bom_string`

```python
to_bom_string()
```

Return this location in the format expected by BOM.

The latitude is converted to a positive value because the BOM
Climate Data Online service expects Southern Hemisphere latitudes
as positive values. The longitude retains its signed value.


**Returns:**

- <b>`str`</b>: BOM location record containing the location name, state,
    latitude, and longitude in the format expected by the
    Climate Data Online service.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/cdio.py#L401"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `StationFinder`
An execution system mirroring the BOM Climate Data Online Text Tool Guide.

Resolves arbitrary text inputs into specific Australian Gazetteer towns,
which are then used to discover and isolate local weather stations.





<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/cdio.py#L408"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `StationFinder.find_matching_locations`

```python
find_matching_locations(location_name, timeout=(5, 30))
```

Find locations matching town names using the BOM gazetteer.

Matches part or all of a location name and returns matching town strings
along with their corresponding coordinates.


**Args:**

- <b>`location_name`</b> (str): Name or partial name of the location to search
    for.
- <b>`timeout`</b> (float | tuple[float, float], optional): Request timeout in
    seconds. A single value specifies the total timeout; a tuple
    specifies separate connect and read timeouts. Defaults to
    ``(5, 30)``.


**Returns:**

- <b>`list[Location]`</b>: Locations matching ``location_name``. Returns an
    empty list if the BOM service returns no matching locations.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/cdio.py#L454"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `StationFinder.find_nearest_stations`

```python
find_nearest_stations(
    nccObsCode,
    location,
    radius_km=50,
    open_only=True,
    timeout=(5, 30)
)
```

Find BOM weather stations near a location.


**Args:**

- <b>`nccObsCode`</b> (int): BOM National Climate Center observation
    product code.

    Available Weather & Climate Codes:
    - 201: Daily Observations
    - 202: Daily Statistics
    - 200: Monthly Statistics

    Available Rainfall Codes:
    - 136: Daily Rainfall (mm)
    - 139: Monthly Rainfall (mm)

    Available Temperature Codes:
    - 122: Daily Maximum Temperature (°C)
    - 123: Daily Minimum Temperature (°C)
    - 36 : Monthly Mean Maximum Temperature (°C)
    - 38 : Monthly Mean Minimum Temperature (°C)
    - 40 : Monthly Highest Temperature (°C)
    - 43 : Monthly Lowest Temperature (°C)
    - 41 : Monthly Lowest Maximum Temperature (°C)
    - 42 : Monthly Highest Minimum Temperature (°C)

    Available Solar & Sunshine Codes:
    - 193: Daily Solar Exposure (MJ/m²)
    - 203: Monthly Mean Daily Solar Exposure (MJ/m²)

- <b>`location`</b> (Coordinates | Location | str | int): Location used to search
    for nearby stations. A string is interpreted as a location name,
    a ``(latitude, longitude)`` tuple as geographic coordinates, and
    an integer as a BOM station identifier.
- <b>`radius_km`</b> (float, optional): Search radius in kilometres. Defaults to
    ``50``.
- <b>`open_only`</b> (bool, optional): Whether to return only stations that are
    currently open. Defaults to ``True``.
- <b>`timeout`</b> (float | tuple[float, float], optional): Request timeout in
    seconds. A single value specifies the total timeout; a tuple
    specifies separate connect and read timeouts. Defaults to
    ``(5, 30)``.


**Returns:**

- <b>`list[DWOStation]`</b>: BOM weather stations matching the search criteria,
    optionally restricted to open stations. Returns an
    empty list if the BOM service returns no matching stations.


**Raises:**

- <b>`ValueError`</b>: Invalid ``ncc_obs_code``.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/cdio.py#L643"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `WeatherObservationsClient`
Client for finding stations and retrieving BOM daily weather observations.


<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/cdio.py#L648"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `WeatherObservationsClient.__init__`

```python
WeatherObservationsClient()
```

*No documentation found.*


<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> WeatherObservationsClient.station

The station used for daily weather observations.




<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/cdio.py#L657"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>classmethod</kbd> `WeatherObservationsClient.find_nearest_stations`

```python
find_nearest_stations(location, radius_km=50, open_only=True, timeout=(5, 30))
```

Find stations with daily weather observations near a location.


**Args:**

- <b>`location`</b> (Coordinates | Location | str | int): Location used to search
    for nearby stations. A string is interpreted as a location name,
    a ``(latitude, longitude)`` tuple as geographic coordinates, and
    an integer as a BOM station identifier.
- <b>`radius_km`</b> (float, optional): Search radius in kilometres. Defaults to
    ``50``.
- <b>`open_only`</b> (bool, optional): Whether to return only stations that are
    currently open. Defaults to ``True``.
- <b>`timeout`</b> (float | tuple[float, float], optional): Request timeout in
    seconds. A single value specifies the total timeout; a tuple
    specifies separate connect and read timeouts. Defaults to
    ``(5, 30)``.


**Returns:**

- <b>`list[DWOStation]`</b>: A list of nearby stations providing daily
    weather observations. Returns an empty list if none is found.


**See Also:**

:meth:`StationFinder.find_matching_locations`
:meth:`StationFinder.find_nearest_stations`


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/cdio.py#L719"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `WeatherObservationsClient.load_observations`

```python
load_observations(
    start_date,
    end_date,
    as_single_dataframe=True,
    ascending=True,
    timeout=(5, 30)
)
```

Load weather observations for a station over a range of dates.

The data is stored in separate files for each month. The given dates
are therefore expanded to cover their entire months. For example, a
start date of 2024-03-15 will load data starting from March 1, and an
end date of 2024-06-10 will load data through June 30.

> [!NOTE] 
> BOM provides approximately 14 months of daily weather observation data
> from the current date. Older observations may not be available.


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

- <b>`TypeError`</b>: If `start_date` or `end_date` is not a date or datetime.
ValueError:
    - `station` is not set.
    - `end_date` is before `start_date`.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/bom/cdio.py#L697"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `WeatherObservationsClient.set_station`

```python
set_station(station)
```

Set the station used for daily weather observations.


**Args:**

- <b>`station`</b> (DWOStation or int): A ``DWOStation`` record or an open BOM
    station ID.


**Raises:**

- <b>`ValueError`</b>: If no station is found for the given station ID.
- <b>`TypeError`</b>: If ``station`` is not a ``DWOStation`` or ``int``.



