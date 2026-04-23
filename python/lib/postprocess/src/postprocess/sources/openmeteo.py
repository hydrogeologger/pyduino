"""Utilities for retrieving meteorological data from the Open-Meteo API.

Provides access to forecast and historical weather data for use in
post-processing workflows.

Dependencies:
- requests : For http POST request
- pandas : For dataframe support

Example:
```python
# Importing opemmeteo module as a source
from postprocess.sources import openmeteo
```

Reference:
- https://open-meteo.com/
"""
from datetime import date
from typing import TYPE_CHECKING

import pandas as _pd
import requests as _requests

try:
    # Python 3+
    from urllib.parse import urljoin as _urljoin
except ImportError:
    # Python 2.X
    from urlparse import urljoin as _urljoin  # type: ignore

from .utils import (
    LocationMetadata,
    is_valid_coordinates,
)

if TYPE_CHECKING:
    from typing import Tuple, Dict, Literal

# pylint: disable=consider-using-f-string


class _OpenMeteoUrl(object):
    """Builds Open-Meteo URLs from components."""
    SCHEME = "https"
    """Default Open-Meteo URL Scheme"""
    DOMAIN = "open-meteo.com"
    """Open-Meteo domain"""

    def __init__(self, subdomain, path):
        self.netloc = "{}.{}".format(subdomain, self.__class__.DOMAIN)
        self.path = path

    @property
    def base(self):
        """Return the base URL (scheme + netloc)."""
        return "{}://{}".format(self.__class__.SCHEME, self.netloc)

    @property
    def absolute(self):
        """Return the full URL by joining base URL and path."""
        return _urljoin(self.base, self.path)


def get_historical(coordinates, start_date, end_date, hourly=None, daily=None, tz=None, settings=None, timeout=(5, 30)):  # pylint: disable=line-too-long
    # type: (Tuple[float, float]|list[Tuple[float, float]], date|str, date|str, list|str | None, list|str|None, str|None, dict[str, str]|None, int) -> dict # pylint: disable=line-too-long
    """Fetch historical weather data for one or more coordinates.

    Args:
        coordinates (tuple | list): A single decimal degree coordinate (latitude, longitude) tuple
            or a list of coordinates.
        start_date (date | str): Start date in ISO 8601 format "YYYY-MM-DD" format or as a date object.
        end_date (date | str): End date in ISO 8601 format "YYYY-MM-DD" format or as a date object.
        hourly (list | str, optional): Hourly variables to request, either as a list or
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

        daily (list | str, optional): Daily variables to request, either as a list or
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

        tz (str, optional): Timezone (IANA string).
            Defaults to API standard if not provided.
        settings (dict, optional): Settings for API request. See available dictionary
            key value pair.
            - `temperature_unit`: **'celsius'** or **'fahrenheit'**. Defaults to 'celsius'.
            - `wind_speed_unit`: **'kmh'**, **'ms'**, **'mph'** or **'kn'**— Knots. Defaults to 'kmh'.
            - `precipitation_unit`: **'mm'** or **'inch'**. Defaults to 'mm'.
            - `timeformat`: **'iso8601'** or **'unixtime'**. Defaults to 'iso8601'.
                - *iso8601* — Time values will be in local timezone time.
                - *unixtime* — Unix epoch time in seconds, time values will be in GMT+0.

        timeout (int | float | tuple, optional): Request timeout.
            Seconds to wait before giving up. Accepts a single number to set the 
            same time limit for both connecting and receiving data, or a 
            `(connect, read)` tuple to set them separately. Defaults to (5, 30).

    Returns:
        dict: JSON response from the Open-Meteo historical weather API.

    Raises:
        ValueError: If coordinates invalid.
        TypeError: If coordinates are not a tuple or list of tuples.
        HTTPError: If the API request fails.

    Reference:
        - https://open-meteo.com/en/docs/historical-weather-api
    """
    if isinstance(coordinates, tuple):
        is_valid_coordinates(coordinates)
    elif isinstance(coordinates, list):
        for coordinate in coordinates:
            is_valid_coordinates(coordinate)
    else:
        raise TypeError(
            "Coordinates must be a (latitude, longitude) tuple "
            "or a list of coordinate tuples."
        )

    params = {}

    # Convert dates to ISO8601 YYYY-MM-DD format
    if isinstance(start_date, date):
        start_date = start_date.strftime("%Y-%m-%d")
    params["start_date"] = start_date
    if isinstance(end_date, date):
        end_date = end_date.strftime("%Y-%m-%d")
    params["end_date"] = end_date

    params["latitude"] = ",".join([str(lat) for lat, _ in coordinates]) if isinstance(
        coordinates, list) else coordinates[0]
    params["longitude"] = ",".join([str(lon) for _, lon in coordinates]) if isinstance(
        coordinates, list) else coordinates[1]
    if hourly:
        params["hourly"] = ",".join(hourly) if isinstance(
            hourly, (list, tuple)) else hourly
    if daily:
        params["daily"] = ",".join(daily) if isinstance(
            daily, (list, tuple)) else daily
    if tz:
        params["timezone"] = tz

    # API settings
    if settings and isinstance(settings, dict):
        params["temperature_unit"] = settings.get("temperature_unit",
                                                  "celsius")
        params["wind_speed_unit"] = settings.get("wind_speed_unit", "kmh")
        params["precipitation_unit"] = settings.get("precipitation_unit", "mm")
        params["timeformat"] = settings.get("timeformat", "iso8601")

    url = _OpenMeteoUrl(subdomain="archive-api", path="/v1/archive")
    headers = {'Accept': 'application/json'}
    response = _requests.get(url=url.absolute,
                             params=params,
                             headers=headers,
                             timeout=timeout)
    response.raise_for_status()
    if response.status_code == 200:
        return response.json()


def get_location_meta(data):
    # type: (Dict) -> LocationMetadata|None
    """Get location info metadata from API response json object.

    Args:
        data (dict): JSON response from API request.

    Returns:
        LocationMetadata: Location metadata object
    """
    return LocationMetadata(
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        elevation=data.get("elevation")
    )


def extract_timeseries_dataframe(data, freq):
    # type: (dict, Literal["hourly", "daily"]) -> _pd.DataFrame
    """Extract timeseries data from Open-Meteo API JSON into DataFrame.

    Args:
        data (dict): Parsed JSON response from the Open-Meteo API.
            Must contain appropriate key for specified interval granularity
            with a mapping of variable names to equal-length lists.
            Expected to include a "time" field containing ISO date strings.
        freq (str): The data interval granularity to extract.
            Valid values are ``hourly`` or ``daily``.

    Returns:
        pandas.DataFrame: A DataFrame containing timeseries data.
            The `"time"` values are converted to pandas datetime values and used
            as the index; the remaining fields become DataFrame columns.

    Raises:
        KeyError: Timeseries data for specified frequency is not present in `data`.
        ValueError:
            - Invalid ``freq`` data interval
            - If the data cannot be converted into a DataFrame
                (e.g. mismatched list lengths or invalid date formats).

    Notes:
        - Assumes all arrays for the specified interval granularity are of equal length.
        - The "time" field is converted to pandas datetime and set as index.
    """
    if isinstance(freq, str):
        freq = freq.lower()
    if not freq in {"hourly", "daily"}:
        raise ValueError(
            "Invalid freq: {!r}. Expected 'hourly' or 'daily'.".format(freq))

    if freq not in data:
        raise KeyError("Missing '{!r}' timeseries in input data".format(freq))
    if "time" not in data[freq]:
        raise KeyError("Missing 'time' key in {} data".format(freq))

    df = _pd.DataFrame(data=data[freq])
    unit_key = "{}_units".format(freq)
    if data[unit_key].get("time", "").lower() == "iso8601":
        df["time"] = _pd.to_datetime(arg=df["time"],
                                     utc=(data["timezone"] == "GMT"),
                                     format="ISO8601")
        if df["time"].dt.tz is None:
            df["time"] = df["time"].dt.tz_localize(data.get("timezone"))
    else:
        df["time"] = _pd.to_datetime(arg=df["time"],
                                     unit="s")
        df["time"] = df["time"].dt.tz_localize(
            "UTC").dt.tz_convert(data.get("timezone"))

    df.set_index(keys="time", inplace=True)
    df.columns = _pd.MultiIndex.from_tuples(
        [(col, data[unit_key].get(col, ""))
            for col in df.columns],
        names=["field", "unit"]
    )
    return df
