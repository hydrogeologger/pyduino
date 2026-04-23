"""Open Meteo API module

Dependencies:
- requests : For http POST request
- pandas : For dataframe support

Reference:
- https://open-meteo.com/
"""
from datetime import date, datetime

import pandas as _pd
import requests as _requests

try:
    # Python 3+
    from urllib.parse import urljoin as _urljoin
    from urllib.parse import urlunparse as _urlunparse
except ImportError:
    # Python 2.X
    from urlparse import urljoin as _urljoin  # type: ignore
    from urlparse import urlunparse as _urlunparse  # type: ignore

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


def _is_valid_coordinates(pair):
    # type: (tuple) -> bool
    """Check if a value is a valid (latitude, longitude) coordinate pair.

    Args:
        pair (tuple): (lat, lon) where both values are numeric.

    Returns:
        bool: True if valid coordinates, False otherwise.

    Notes:
        Latitude must be in [-90, 90] and longitude in [-180, 180].
    """
    if not isinstance(pair, tuple) or len(pair) != 2:
        return False
    lat, lon = pair
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        return False
    # pylint: disable-next=superfluous-parens
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        return False
    return True


def get_historical(coords, start_date, end_date, hourly=None, daily=None, tz=None, timeout=10):
    # type: (tuple|list[tuple], date|str, date|str, list|str | None, list|str|None, str|None, int) -> dict # pylint: disable=line-too-long
    """Fetch historical weather data for one or more coordinates.

    Args:
        coords (tuple | list): A single (latitude, longitude) tuple or a list of such tuples.
        start_date (date | str): Start date in "YYYY-MM-DD" format or as a date object.
        end_date (date | str): End date in "YYYY-MM-DD" format or as a date object.
        hourly (list | str, optional): Hourly variables to request, either as a list or
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

        daily (list | str, optional): Daily variables to request, either as a list or
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

        tz (str, optional): Timezone (IANA string). Defaults to API standard if not provided.
        timeout (int, optional): Request timeout in seconds. Defaults to 10.

    Returns:
        dict: JSON response from the Open-Meteo historical weather API.

    Raises:
        ValueError: If coordinates are empty or invalid.
        TypeError: If coordinates are not a tuple or list of tuples.
        HTTPError: If the API request fails.

    Reference:
        - https://open-meteo.com/en/docs/historical-weather-api
    """
    if not coords:
        raise ValueError("Coordinates cannot be empty!")
    if not isinstance(coords, (tuple, list)):
        raise TypeError(
            "Coordinates must tuple (lat, lon) Deg or list of tuples")
    if isinstance(coords, list):
        for pair in coords:
            if not _is_valid_coordinates(pair):
                raise ValueError(
                    "Coordinates must be valid tuple in degrees: (lat, lon)")
    elif not _is_valid_coordinates(coords):
        raise ValueError(
            "Coordinates must be valid tuple in degrees: (lat, lon)")

    url = _OpenMeteoUrl(subdomain="archive-api", path="/v1/archive")
    params = {}
    headers = {'Accept': 'application/json'}

    if isinstance(start_date, date):
        # datetime is sublcass of date, # pylint: disable-next=unidiomatic-typecheck
        params["start_date"] = start_date.isoformat("%Y-%m-%d")

    if isinstance(end_date, date):
        # datetime is sublcass of date, # pylint: disable-next=unidiomatic-typecheck
        params["end_date"] = end_date.isoformat("%Y-%m-%d")

    params["latitude"] = ",".join([str(lat) for lat, _ in coords]) if isinstance(
        coords, list) else coords[0]
    params["longitude"] = ",".join([str(lon) for _, lon in coords]) if isinstance(
        coords, list) else coords[1]
    params["hourly"] = hourly
    params["daily"] = daily
    params["timezone"] = tz

    response = _requests.get(url=url.absolute,
                             params=params,
                             headers=headers,
                             timeout=timeout)
    if response.status_code == 200:
        return response.json()
    response.raise_for_status()


def extract_hourly_dataframe(data):
    # type: (dict) -> _pd.DataFrame
    """Extract hourly timeseries data from Open-Meteo API JSON into DataFrame.

    Args:
        data (dict): Parsed JSON response from the Open-Meteo API.
            Must contain a "hourly" key with a mapping of variable names to
            equal-length lists. Expected to include a "time" field containing
            ISO date strings.

    Returns:
        pandas.DataFrame: DataFrame indexed by datetime (derived from "time"),
        where each row represents a single day and columns correspond to
        variables in `data["hourly"]`.

    Raises:
        KeyError: If "hourly" or "time" is missing from the input.
        ValueError: If the data cannot be converted into a DataFrame (e.g.,
            mismatched list lengths or invalid date formats).

    Notes:
        - Assumes all arrays in `data["hourly"]` are of equal length.
        - The "time" field is converted to pandas datetime and set as index.
    """
    if "hourly" not in data:
        raise KeyError("Missing 'hourly' key in input data")
    if "time" not in data["hourly"]:
        raise KeyError("Missing 'hourly' key in hourly data")
    df = _pd.DataFrame(data=data["hourly"])
    df.set_index(keys="time", inplace=True)
    df.index = _pd.to_datetime(arg=df.index,
                               utc=(data["timezone"] == "GMT"),
                               format="ISO8601")
    df.columns = _pd.MultiIndex.from_tuples(
        [(col, data["hourly_units"].get(col, ""))
         for col in df.columns],
        names=["field", "unit"]
    )
    return df


def extract_daily_dataframe(data):
    # type: (dict) -> _pd.DataFrame
    """Extract daily timeseries data from Open-Meteo API JSON into DataFrame.

    Args:
        data (dict): Parsed JSON response from the Open-Meteo API.
            Must contain a "daily" key with a mapping of variable names to
            equal-length lists. Expected to include a "time" field containing
            ISO date strings.

    Returns:
        pandas.DataFrame: DataFrame indexed by datetime (derived from "time"),
        where each row represents a single day and columns correspond to
        variables in `data["daily"]`.

    Raises:
        KeyError: If "daily" or "time" is missing from the input.
        ValueError: If the data cannot be converted into a DataFrame (e.g.,
            mismatched list lengths or invalid date formats).

    Notes:
        - Assumes all arrays in `data["daily"]` are of equal length.
        - The "time" field is converted to pandas datetime and set as index.
    """
    if "daily" not in data:
        raise KeyError("Missing 'daily' key in input data")
    if "time" not in data["daily"]:
        raise KeyError("Missing 'time' key in daily data")

    df = _pd.DataFrame(data=data["daily"])
    df.set_index(keys="time", inplace=True)
    df.index = _pd.to_datetime(arg=df.index,
                               utc=(data["timezone"] == "GMT"),
                               format="ISO8601").map(datetime.date)
    df.columns = _pd.MultiIndex.from_tuples(
        [(col, data["daily_units"].get(col, ""))
         for col in df.columns],
        names=["field", "unit"]
    )
    return df
