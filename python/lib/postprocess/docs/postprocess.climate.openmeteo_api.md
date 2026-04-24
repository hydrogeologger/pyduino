<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/climate/openmeteo_api.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.climate.openmeteo_api`
Open Meteo API module

Dependencies:  
- requests : For http POST request
- pandas : For dataframe support


**Reference:**

- https://open-meteo.com/


## Table of Contents
- [`extract_daily_dataframe`](./postprocess.climate.openmeteo_api.md#function-extract_daily_dataframe): Extract daily timeseries data from Open-Meteo API JSON into DataFrame.
- [`extract_hourly_dataframe`](./postprocess.climate.openmeteo_api.md#function-extract_hourly_dataframe): Extract hourly timeseries data from Open-Meteo API JSON into DataFrame.
- [`get_historical`](./postprocess.climate.openmeteo_api.md#function-get_historical): Fetch historical weather data for one or more coordinates.



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/openmeteo_api.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `get_historical`

```python
get_historical(
    coords,
    start_date,
    end_date,
    hourly=None,
    daily=None,
    tz=None,
    timeout=10
)
```

Fetch historical weather data for one or more coordinates.


**Args:**

- <b>`coords`</b> (tuple | list): A single (latitude, longitude) tuple or a list of such tuples.
- <b>`start_date`</b> (date | str): Start date in "YYYY-MM-DD" format or as a date object.
- <b>`end_date`</b> (date | str): End date in "YYYY-MM-DD" format or as a date object.
- <b>`hourly`</b> (list | str, optional): Hourly variables to request, either as a list or
    comma-separated string. See available "Hourly variables" below for full options.

        Temperature
            - temperature_2m
            - apparent_temperature
            - dew_point_2m
            - wet_bulb_temperature_2m

        Humidity & pressure
            - relative_humidity_2m
            - pressure_msl
            - surface_pressure

        Precipitation
            - precipitation
            - rain
            - snowfall
            - precipitation_probability

        Cloud cover
            - cloud_cover
            - cloud_cover_low
            - cloud_cover_mid
            - cloud_cover_high

        Wind
            - wind_speed_10m
            - wind_speed_100m
            - wind_direction_10m
            - wind_direction_100m
            - wind_gusts_10m

        Radiation
            - shortwave_radiation
            - direct_radiation
            - direct_normal_irradiance
            - diffuse_radiation
            - global_tilted_irradiance

        Sunshine
            - sunshine_duration

        Soil (depth layers)
            - soil_temperature_0_to_7cm
            - soil_temperature_7_to_28cm
            - soil_temperature_28_to_100cm
            - soil_temperature_100_to_255cm
            - soil_moisture_0_to_7cm
            - soil_moisture_7_to_28cm
            - soil_moisture_28_to_100cm
            - soil_moisture_100_to_255cm

        Other
            - vapour_pressure_deficit
            - boundary_layer_height

- <b>`daily`</b> (list | str, optional): Daily variables to request, either as a list or
    comma-separated string. See available "Daily variables" below for full options.
        Temperature
            - temperature_2m_max
            - temperature_2m_min
            - apparent_temperature_max
            - apparent_temperature_min

        Precipitation
            - precipitation_sum
            - rain_sum
            - snowfall_sum
            - precipitation_hours

        Wind
            - wind_speed_10m_max
            - wind_gusts_10m_max
            - wind_direction_10m_dominant

        Solar & daylight
            - shortwave_radiation_sum
            - sunshine_duration
            - daylight_duration
            - sunrise
            - sunset

        Weather
            - weather_code

        Evapotranspiration
            - et0_fao_evapotranspiration

- <b>`tz`</b> (str, optional): Timezone (IANA string). Defaults to API standard if not provided.
- <b>`timeout`</b> (int, optional): Request timeout in seconds. Defaults to 10.


**Returns:**

- <b>`dict`</b>: JSON response from the Open-Meteo historical weather API.


**Raises:**

- <b>`ValueError`</b>: If coordinates are empty or invalid.
- <b>`TypeError`</b>: If coordinates are not a tuple or list of tuples.
- <b>`HTTPError`</b>: If the API request fails.


**Reference:**

- https://open-meteo.com/en/docs/historical-weather-api



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/openmeteo_api.py#L227"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `extract_hourly_dataframe`

```python
extract_hourly_dataframe(data)
```

Extract hourly timeseries data from Open-Meteo API JSON into DataFrame.


**Args:**

- <b>`data`</b> (dict): Parsed JSON response from the Open-Meteo API.
    Must contain a "hourly" key with a mapping of variable names to
    equal-length lists. Expected to include a "time" field containing
    ISO date strings.


**Returns:**

- <b>`pandas.DataFrame`</b>: DataFrame indexed by datetime (derived from "time"),
where each row represents a single day and columns correspond to
variables in `data["hourly"]`.


**Raises:**

- <b>`KeyError`</b>: If "hourly" or "time" is missing from the input.
- <b>`ValueError`</b>: If the data cannot be converted into a DataFrame (e.g.,
    mismatched list lengths or invalid date formats).

> [!NOTE] 
> - Assumes all arrays in `data["hourly"]` are of equal length.
> - The "time" field is converted to pandas datetime and set as index.



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/openmeteo_api.py#L268"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `extract_daily_dataframe`

```python
extract_daily_dataframe(data)
```

Extract daily timeseries data from Open-Meteo API JSON into DataFrame.


**Args:**

- <b>`data`</b> (dict): Parsed JSON response from the Open-Meteo API.
    Must contain a "daily" key with a mapping of variable names to
    equal-length lists. Expected to include a "time" field containing
    ISO date strings.


**Returns:**

- <b>`pandas.DataFrame`</b>: DataFrame indexed by datetime (derived from "time"),
where each row represents a single day and columns correspond to
variables in `data["daily"]`.


**Raises:**

- <b>`KeyError`</b>: If "daily" or "time" is missing from the input.
- <b>`ValueError`</b>: If the data cannot be converted into a DataFrame (e.g.,
    mismatched list lengths or invalid date formats).

> [!NOTE] 
> - Assumes all arrays in `data["daily"]` are of equal length.
> - The "time" field is converted to pandas datetime and set as index.



