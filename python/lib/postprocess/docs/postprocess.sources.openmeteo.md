<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/sources/openmeteo.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.sources.openmeteo`
Utilities for retrieving meteorological data from the Open-Meteo API.

Provides access to forecast and historical weather data for use in
post-processing workflows.

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
- [`extract_timeseries_dataframe`](./postprocess.sources.openmeteo.md#function-extract_timeseries_dataframe): Extract timeseries data from Open-Meteo API JSON into DataFrame.
- [`get_historical`](./postprocess.sources.openmeteo.md#function-get_historical): Fetch historical weather data for one or more coordinates.
- [`get_location_meta`](./postprocess.sources.openmeteo.md#function-get_location_meta): Get location info metadata from API response json object.


**Global Variables**
---------------
- **TYPE_CHECKING** = False

<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/openmeteo.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `get_historical`

```python
get_historical(
    coordinates,
    start_date,
    end_date,
    hourly=None,
    daily=None,
    tz=None,
    settings=None,
    timeout=(5, 30)
)
```

Fetch historical weather data for one or more coordinates.


**Args:**

- <b>`coordinates`</b> (tuple | list): A single decimal degree coordinate (latitude, longitude) tuple
    or a list of coordinates.
- <b>`start_date`</b> (date | str): Start date in ISO 8601 format "YYYY-MM-DD" format or as a date object.
- <b>`end_date`</b> (date | str): End date in ISO 8601 format "YYYY-MM-DD" format or as a date object.
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

- <b>`tz`</b> (str, optional): Timezone (IANA string).
    Defaults to API standard if not provided.
- <b>`settings`</b> (dict, optional): Settings for API request. See available dictionary
    key value pair.
    - `temperature_unit`: **'celsius'** or **'fahrenheit'**. Defaults to 'celsius'.
    - `wind_speed_unit`: **'kmh'**, **'ms'**, **'mph'** or **'kn'**— Knots. Defaults to 'kmh'.
    - `precipitation_unit`: **'mm'** or **'inch'**. Defaults to 'mm'.
    - `timeformat`: **'iso8601'** or **'unixtime'**. Defaults to 'iso8601'.
        - *iso8601* — Time values will be in local timezone time.
        - *unixtime* — Unix epoch time in seconds, time values will be in GMT+0.

- <b>`timeout`</b> (int | float | tuple, optional): Request timeout.
    Seconds to wait before giving up. Accepts a single number to set the 
    same time limit for both connecting and receiving data, or a 
    `(connect, read)` tuple to set them separately. Defaults to (5, 30).


**Returns:**

- <b>`dict`</b>: JSON response from the Open-Meteo historical weather API.


**Raises:**

- <b>`ValueError`</b>: If coordinates invalid.
- <b>`TypeError`</b>: If coordinates are not a tuple or list of tuples.
- <b>`HTTPError`</b>: If the API request fails.


**Reference:**

- https://open-meteo.com/en/docs/historical-weather-api



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/openmeteo.py#L244"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `get_location_meta`

```python
get_location_meta(data)
```

Get location info metadata from API response json object.


**Args:**

- <b>`data`</b> (dict): JSON response from API request.


**Returns:**

- <b>`LocationMetadata`</b>: Location metadata object



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/openmeteo.py#L261"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `extract_timeseries_dataframe`

```python
extract_timeseries_dataframe(data, freq)
```

Extract timeseries data from Open-Meteo API JSON into DataFrame.


**Args:**

- <b>`data`</b> (dict): Parsed JSON response from the Open-Meteo API.
    Must contain appropriate key for specified interval granularity
    with a mapping of variable names to equal-length lists.
    Expected to include a "time" field containing ISO date strings.
- <b>`freq`</b> (str): The data interval granularity to extract.
    Valid values are ``hourly`` or ``daily``.


**Returns:**

- <b>`pandas.DataFrame`</b>: A DataFrame containing timeseries data.
    The `"time"` values are converted to pandas datetime values and used
    as the index; the remaining fields become DataFrame columns.


**Raises:**

- <b>`KeyError`</b>: Timeseries data for specified frequency is not present in `data`.
ValueError:
    - Invalid ``freq`` data interval
    - If the data cannot be converted into a DataFrame
        (e.g. mismatched list lengths or invalid date formats).

> [!NOTE] 
> - Assumes all arrays for the specified interval granularity are of equal length.
> - The "time" field is converted to pandas datetime and set as index.



