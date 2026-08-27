<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/sources/openmeteo.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.sources.openmeteo`
Utilities for retrieving meteorological data from the Open-Meteo API.

Provides access to forecast and historical weather data for use in
post-processing workflows.

Historical weather data uses weather reanalysis from ERA5 (0.25°, from 1940)
and ERA5-Land (0.1°, from 1950) and ECMWF IFS (9 km, from 2017).

Dependencies:  
- requests : For http POST request
- pandas : For dataframe support


**Example:**

```python
# Importing opemmeteo module as a source
from postprocess.sources import openmeteo
```


**Reference:**

- https://open-meteo.com/


## Table of Contents
- [`dataframe_from_data`](./postprocess.sources.openmeteo.md#function-dataframe_from_data): Extract timeseries data from Open-Meteo API JSON into DataFrame.
- [`fetch_historical_weather`](./postprocess.sources.openmeteo.md#function-fetch_historical_weather): Fetch historical weather data for one or more coordinates.
- [`location_meta_from_data`](./postprocess.sources.openmeteo.md#function-location_meta_from_data): Get location info metadata from API response json object.
- [`search_locations`](./postprocess.sources.openmeteo.md#function-search_locations): Searches for locations globally using the Open-Meteo Geocoding API.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/openmeteo.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `fetch_historical_weather`

```python
fetch_historical_weather(
    coordinates,
    start_date,
    end_date,
    hourly=None,
    daily=None,
    timezone=None,
    settings=None,
    timeout=(5, 30),
    **params
)
```

Fetch historical weather data for one or more coordinates.


**Args:**

- <b>`coordinates`</b> (tuple | list): A single geographic coordinates in decimal degrees,
    referenced to WGS84 (World Geodetic System 1984) as a
    ``(latitude, longitude)`` tuple, or a list of such coordinates.
- <b>`start_date`</b> (date | str): Start date in ISO 8601 format "YYYY-MM-DD" format
    or as a date object.
- <b>`end_date`</b> (date | str): End date in ISO 8601 format "YYYY-MM-DD" format or
    as a date object.
- <b>`hourly`</b> (list | str, optional): Hourly variables to request, either as a list or
    comma-separated string. See available "Hourly variables" below for full options.

    Temperature
    - 'temperature_2m'
    - 'apparent_temperature'
    - 'dew_point_2m'
    - 'wet_bulb_temperature_2m'

    Humidity & pressure
    - 'relative_humidity_2m'
    - 'pressure_msl'
    - 'surface_pressure'

    Precipitation
    - 'precipitation'
    - 'rain'
    - 'snowfall'
    - 'precipitation_probability'

    Cloud cover
    - 'cloud_cover'
    - 'cloud_cover_low'
    - 'cloud_cover_mid'
    - 'cloud_cover_high'

    Wind
    - 'wind_speed_10m'
    - 'wind_speed_100m'
    - 'wind_direction_10m'
    - 'wind_direction_100m'
    - 'wind_gusts_10m'

    Radiation
    - 'shortwave_radiation'
    - 'direct_radiation'
    - 'direct_normal_irradiance'
    - 'diffuse_radiation'
    - 'global_tilted_irradiance'

    Sunshine
    - 'sunshine_duration'

    Soil (depth layers)
    - 'soil_temperature_0_to_7cm'
    - 'soil_temperature_7_to_28cm'
    - 'soil_temperature_28_to_100cm'
    - 'soil_temperature_100_to_255cm'
    - 'soil_moisture_0_to_7cm'
    - 'soil_moisture_7_to_28cm'
    - 'soil_moisture_28_to_100cm'
    - 'soil_moisture_100_to_255cm'

    Other
    - 'vapour_pressure_deficit'
    - 'boundary_layer_height'

- <b>`daily`</b> (list | str, optional): Daily variables to request, either as a list or
    comma-separated string. See available "Daily variables" below for full options.

    Temperature
    - 'temperature_2m_max'
    - 'temperature_2m_min'
    - 'apparent_temperature_max'
    - 'apparent_temperature_min'

    Precipitation
    - 'precipitation_sum'
    - 'rain_sum'
    - 'snowfall_sum'
    - 'precipitation_hours'

    Wind
    - 'wind_speed_10m_max'
    - 'wind_gusts_10m_max'
    - 'wind_direction_10m_dominant'

    Solar & daylight
    - 'shortwave_radiation_sum'
    - 'sunshine_duration'
    - 'daylight_duration'
    - 'sunrise'
    - 'sunset'

    Weather
    - 'weather_code'

    Evapotranspiration
    - 'et0_fao_evapotranspiration'

- <b>`timezone`</b> (str, optional): Timezone (IANA string).
    Defaults to API standard if not provided.
- <b>`settings`</b> (dict, optional): Settings for API request. See available dictionary
    key value pair.
    - ``temperature_unit``: **'celsius'** or **'fahrenheit'**. Defaults to 'celsius'.
    - ``wind_speed_unit``: **'kmh'**, **'ms'**, **'mph'** or **'kn'**— Knots.
        Defaults to 'kmh'.
    - ``precipitation_unit``: **'mm'** or **'inch'**. Defaults to 'mm'.
    - ``timeformat``: **'iso8601'** or **'unixtime'**. Defaults to 'unixtime'.
        - *iso8601* — Local timezone time (uses flat offsets;
            ignores internal daylight savings time [DST] transitions).
        - *unixtime* — Unix epoch time in seconds in GMT+0
            (recommended for robust, daylight savings time [DST]-safe application parsing).

- <b>`timeout`</b> (int | float | tuple, optional): Request timeout.
    Seconds to wait before giving up. Accepts a single number to set the 
    same time limit for both connecting and receiving data, or a 
    ``(connect, read)`` tuple to set them separately. Defaults to (5, 30).

- <b>`**params`</b>: Additional Open-Meteo API parameters passed through directly.
    Use only for parameters that are not explicitly supported by this
    function.

    > [!WARNING] Use with caution
    > Parameters may override existing request parameters.


**Returns:**

- <b>`dict`</b>: JSON response from the Open-Meteo historical weather API.


**Raises:**

- <b>`ValueError`</b>: If coordinates invalid.
- <b>`TypeError`</b>: If coordinates are not a tuple or list of tuples.
- <b>`requests.HTTPError`</b>: If the network request fails or returns an invalid
    status code.


**Reference:**

- https://open-meteo.com/en/docs/historical-weather-api



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/openmeteo.py#L284"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `location_meta_from_data`

```python
location_meta_from_data(data)
```

Get location info metadata from API response json object.

Coordinates is in decimal degrees, referenced to the WGS84 (World Geodetic System 1994)
coordinate reference system.


**Args:**

- <b>`data`</b> (dict): JSON response from API request.


**Returns:**

- <b>`LocationBase`</b>: Location metadata object, or None if coordinates are missing.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/openmeteo.py#L308"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `dataframe_from_data`

```python
dataframe_from_data(point_data, freq, ascending=True)
```

Extract timeseries data from Open-Meteo API JSON into DataFrame.


**Args:**

- <b>`point_data`</b> (dict): Parsed JSON response from the Open-Meteo API.
    Must contain appropriate key for specified interval granularity
    with a mapping of variable names to equal-length lists.
    Expected to include a "time" field containing ISO date strings.
- <b>`freq`</b> (str): The data interval granularity to extract.
    Valid values are ``hourly`` or ``daily``.
- <b>`ascending`</b> (bool, optional): Sort chronological (True) or reverse (False).
    Defaults to True.


**Returns:**

- <b>`pandas.DataFrame`</b>: A DataFrame containing timeseries data.
    The ``"time"`` values are converted to pandas datetime values and used
    as the index; the remaining fields become MultiIndex DataFrame columns
    structured across two levels: ``"variable"`` and ``"unit"``.


**Warns:**

- <b>`UserWarning`</b>: Triggered when a timestamp falls into a skipped or
    ambiguous daylight savings time (DST) transition window (such as
    AmbiguousTimeError or NonExistentTimeError). Suggests requesting
    data with `unixtime` timeformat.


**Raises:**

- <b>`TypeError`</b>: ``point_data`` is not a dictionary.
- <b>`KeyError`</b>: Timeseries data for specified frequency is not present in ``point_data``.
ValueError:
    - ``point_data`` is empty.
    - Invalid ``freq`` data interval.
    - If the data cannot be converted into a DataFrame
        (e.g. mismatched list lengths or invalid date formats).


**Notes:**

- Assumes all arrays for the specified interval granularity are of equal length.
- The "time" field is converted to pandas datetime and set as index.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/openmeteo.py#L445"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `search_locations`

```python
search_locations(
    name,
    count=10,
    language='en',
    fmt='json',
    country_code=None,
    timeout=(5, 30),
    **params
)
```

Searches for locations globally using the Open-Meteo Geocoding API.

Queries location data (such as coordinates, timezones, elevation, and country
codes) matching the provided location name or postal code.


**Args:**

- <b>`name`</b> (str): Location name or postal code to search for (e.g., 'Hobart' or
    'Los Angeles, California'). Can optionally append a country or
    first-level administrative area after a comma to narrow results.
- <b>`count`</b> (int, optional): The number of search results to return (up to 100
    results max). Defaults to 10.
- <b>`language`</b> (str, optional): Return translated city and country names in this
    language (lower-cased code like 'en', 'de', 'fr'). Defaults to 'en'.
- <b>`fmt`</b> (str, optional): Response format, defaults to 'json' (alternatively
    supports 'protobuf'). Defaults to 'json'.
- <b>`country_code`</b> (str | None, optional): ISO-3166-1 alpha-2 country code to
    unambiguously filter results (e.g., 'AU', 'US', 'DE'). Defaults to None.
- <b>`timeout`</b> (int | float | tuple, optional): Request timeout.
    Seconds to wait before giving up. Accepts a single number to set the 
    same time limit for both connecting and receiving data, or a 
    ``(connect, read)`` tuple to set them separately. Defaults to (5, 30).
- <b>`**params`</b>: Additional Open-Meteo API parameters passed through directly.
    Use only for parameters that are not explicitly supported by this
    function.

    > [!WARNING] Use with caution
    > Parameters may override existing request parameters.


**Returns:**

- <b>`list[dict[str, Any]] or bytes`</b>: A list of matching location dictionaries
    if format is `json`, each item contains:
    - ``id`` (int): Unique location ID.
    - ``name`` (str): Location name.
    - ``latitude``, ``longitude`` (float): Geographical WGS84 coordinates.
    - ``elevation`` (float): Elevation above sea level in meters.
    - ``timezone`` (str): Time zone database identifier (e.g.,
        'Australia/Sydney').
    - ``country_code`` (str): 2-character ISO-3166-1 alpha-2 country code.
    - ``country`` (str): Localized country name.
    - ``population`` (int, optional): Number of inhabitants.
    - ``admin1`` to ``admin4`` (str, optional): Hierarchical administrative
        area names.

    Or raw binary ``bytes`` if format is `protobuf`.


**Raises:**

- <b>`ValueError`</b>: If `fmt` is not one of the supported values (``'json'`` or ``'protobuf'``).
- <b>`requests.HTTPError`</b>: If the network request fails or returns an invalid
    status code.


**Reference:**

- https://open-meteo.com/en/docs/geocoding-api



