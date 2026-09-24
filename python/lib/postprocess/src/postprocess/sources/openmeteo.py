"""Utilities for retrieving meteorological data from the Open-Meteo API.

Provides access to forecast and historical weather data for use in
post-processing workflows.

Historical weather data uses weather reanalysis from ERA5 (0.25°, from 1940)
and ERA5-Land (0.1°, from 1950) and ECMWF IFS (9 km, from 2017).

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

import datetime as _datetime
import warnings as _warnings
from typing import TYPE_CHECKING

import pandas as _pd
import requests as _requests

try:
    # Python 3+
    from urllib.parse import urljoin as _urljoin
except ImportError:
    # Python 2.X
    from urlparse import (  # pyright: ignore[reportMissingImports]
        urljoin as _urljoin,
    )

from .types import (
    Coordinates,
    LocationBase,
)
from .utils import URLBuilder as _URLBuilder

__all__ = [
    "LocationBase",
    "fetch_historical_weather",
    "location_meta_from_data",
    "dataframe_from_data",
]

if TYPE_CHECKING:
    from datetime import date
    from typing import (
        Any,
        Dict,
        Literal,
        Tuple,
    )

# pylint: disable=consider-using-f-string


URL_OPENMETEO = _URLBuilder(
    domain="open-meteo.com",
    scheme="https"
)


def fetch_historical_weather(
    coordinates,  # type: Tuple[float,float]|list[Tuple[float,float]]
    start_date,  # type: date|str
    end_date,  # type: date|str
    hourly=None,  # type: list|str|None
    daily=None,  # type: list|str|None
    timezone=None,  # type: str|None
    settings=None,  # type: dict[str, str]|None
    timeout=(5, 30),  # type: tuple|float
    **params  # type: object
):
    # type: (...) -> dict
    """Fetch historical weather data for one or more coordinates.

    Args:
        coordinates (tuple | list): A single geographic coordinates in decimal degrees,
            referenced to WGS84 (World Geodetic System 1984) as a
            ``(latitude, longitude)`` tuple, or a list of such coordinates.
        start_date (date | str): Start date in ISO 8601 format "YYYY-MM-DD" format
            or as a date object.
        end_date (date | str): End date in ISO 8601 format "YYYY-MM-DD" format or
            as a date object.
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

        timezone (str, optional): Timezone (IANA string).
            Defaults to API standard if not provided.
        settings (dict, optional): Settings for API request. See available dictionary
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

        timeout (int | float | tuple, optional): Request timeout.
            Seconds to wait before giving up. Accepts a single number to set the 
            same time limit for both connecting and receiving data, or a 
            ``(connect, read)`` tuple to set them separately. Defaults to (5, 30).

        **params: Additional Open-Meteo API parameters passed through directly.
            Use only for parameters that are not explicitly supported by this
            function.

            Warning: Use with caution
                Parameters may override existing request parameters.

    Returns:
        dict: JSON response from the Open-Meteo historical weather API.

    Raises:
        ValueError: If coordinates invalid.
        TypeError: If coordinates are not a tuple or list of tuples.
        requests.HTTPError: If the network request fails or returns an invalid
            status code.

    Reference:
        - https://open-meteo.com/en/docs/historical-weather-api
    """
    if isinstance(coordinates, tuple):
        Coordinates.validate_decimal_degree(coordinates)
    elif isinstance(coordinates, list):
        for coordinate in coordinates:
            Coordinates.validate_decimal_degree(coordinate)
    else:
        raise TypeError(
            "Coordinates must be a (latitude, longitude) tuple "
            "or a list of coordinate tuples."
        )

    _params = {}

    _params["latitude"] = ",".join([str(lat) for lat, _ in coordinates]) if isinstance(
        coordinates, list) else coordinates[0]
    _params["longitude"] = ",".join([str(lon) for _, lon in coordinates]) if isinstance(
        coordinates, list) else coordinates[1]

    # Convert dates to ISO8601 YYYY-MM-DD format
    if isinstance(start_date, _datetime.date):
        start_date = start_date.strftime("%Y-%m-%d")
    _params["start_date"] = start_date
    if isinstance(end_date, _datetime.date):
        end_date = end_date.strftime("%Y-%m-%d")
    _params["end_date"] = end_date

    if hourly:
        _params["hourly"] = ",".join(hourly) if isinstance(
            hourly, (list, tuple)) else hourly
    if daily:
        _params["daily"] = ",".join(daily) if isinstance(
            daily, (list, tuple)) else daily
    if timezone:
        _params["timezone"] = timezone

    # API settings
    _params["timeformat"] = "unixtime"
    if settings and isinstance(settings, dict):
        _params["temperature_unit"] = settings.get("temperature_unit",
                                                   "celsius")
        _params["wind_speed_unit"] = settings.get("wind_speed_unit", "kmh")
        _params["precipitation_unit"] = settings.get(
            "precipitation_unit", "mm")
        _params["timeformat"] = settings.get("timeformat", "unixtime")

    # Additional Open-Meteo parameters.
    #! WARNING: **params is a last-resort passthrough and may override parameters defined above.
    _params.update(params)

    headers = {'Accept': 'application/json'}
    response = _requests.get(
        url=URL_OPENMETEO.resolve_subdomain(
            subdomain="archive-api",
            path="/v1/archive",
        ),
        params=_params,
        headers=headers,
        timeout=timeout
    )
    response.raise_for_status()
    if response.status_code == 200:
        return response.json()


def location_meta_from_data(data):
    # type: (Dict) -> LocationBase|None
    """Get location info metadata from API response json object.

    Coordinates is in decimal degrees, referenced to the WGS84 (World Geodetic System 1994)
    coordinate reference system.

    Args:
        data (dict): JSON response from API request.

    Returns:
        LocationBase: Location metadata object, or None if coordinates are missing.
    """
    # If core location fields aren't present, return None
    if not data or "latitude" not in data or "longitude" not in data:
        return None

    return LocationBase(
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        elevation_m=data.get("elevation")
    )


def dataframe_from_data(point_data, freq, ascending=True):
    # type: (dict, Literal["hourly", "daily"], bool) -> _pd.DataFrame
    """Extract timeseries data from Open-Meteo API JSON into DataFrame.

    Args:
        point_data (dict): Parsed JSON response from the Open-Meteo API.
            Must contain appropriate key for specified interval granularity
            with a mapping of variable names to equal-length lists.
            Expected to include a "time" field containing ISO date strings.
        freq (str): The data interval granularity to extract.
            Valid values are ``hourly`` or ``daily``.
        ascending (bool, optional): Sort chronological (True) or reverse (False).
            Defaults to True.

    Returns:
        pandas.DataFrame: A DataFrame containing timeseries data.
            The ``"time"`` values are converted to pandas datetime values and used
            as the index; the remaining fields become MultiIndex DataFrame columns
            structured across two levels: ``"variable"`` and ``"unit"``.

    Warns:
        UserWarning: Triggered when a timestamp falls into a skipped or
            ambiguous daylight savings time (DST) transition window (such as
            AmbiguousTimeError or NonExistentTimeError). Suggests requesting
            data with `unixtime` timeformat.

    Raises:
        TypeError: ``point_data`` is not a dictionary.
        KeyError: Timeseries data for specified frequency is not present in ``point_data``.
        ValueError:
            - ``point_data`` is empty.
            - Invalid ``freq`` data interval.
            - If the data cannot be converted into a DataFrame
                (e.g. mismatched list lengths or invalid date formats).

    Notes:
        - Assumes all arrays for the specified interval granularity are of equal length.
        - The "time" field is converted to pandas datetime and set as index.
    """
    if not isinstance(point_data, dict):
        raise TypeError(
            "`point_data` must be a dictionary, got {}".format(type(point_data).__name__))
    if not point_data:
        raise ValueError("Empty `point_data`!")

    if isinstance(freq, str):
        freq = freq.lower()
    if not freq in {"hourly", "daily"}:
        raise ValueError(
            "Invalid freq: {!r}. Expected 'hourly' or 'daily'.".format(freq))

    ts_payload = point_data.get(freq)
    if not ts_payload:
        raise KeyError("Missing {!r} timeseries in input data".format(freq))

    # Shallow copy of timeseries data to avoid mutating original
    ts_data = ts_payload.copy()
    if "time" not in ts_data:
        raise KeyError("Missing 'time' key in {} data".format(freq))

    timestamps = ts_data.pop("time", [])  # Extract `time`

    # Enforce strict length matching to prevent pandas broadcasting/empty quirks
    len_timestamps = len(timestamps)
    for col, records in ts_data.items():
        len_records = len(records)
        if len_records != len_timestamps:
            raise ValueError(
                "Length of `{col}` ({len_records}) does not match length "
                "of index ({len_timestamps})".format(
                    col=col,
                    len_records=len_records,
                    len_timestamps=len_timestamps
                )
            )

    data_units = point_data.get("{}_units".format(freq), {})
    timezone = point_data.get("timezone")
    time_unit = data_units.get("time", "").lower()

    if time_unit == "unixtime":
        # `time_unit == "unixtime"`
        idx = _pd.to_datetime(
            arg=timestamps,
            utc=True,
            unit="s",
        )  # type: _pd.DatetimeIndex
        if timezone:
            idx = idx.tz_convert(timezone)

    else:
        # `time_unit == "iso8601"`
        idx = _pd.to_datetime(
            arg=timestamps,
            utc=(timezone == "GMT"),
            format="ISO8601",
        )  # type: _pd.DatetimeIndex

        try:
            if timezone and not idx.tz:
                idx = idx.tz_localize(timezone)
        except Exception as err:  # pylint: disable=broad-exception-caught
            err_name = type(err).__name__
            err_msg = str(err).lower()

            is_time_error = (
                err_name in ("NonExistentTimeError", "AmbiguousTimeError") or
                (isinstance(err, ValueError) and (
                    "nonexistent" in err_msg or "ambiguous" in err_msg
                ))
            )

            if is_time_error:
                # Warning message now includes err_type using .format()
                warning_msg = (
                    "Failed to make timestamp timezone-aware using timezone "
                    "'{tz}' [{err_type}]: {error}\n"
                    "💡 Consider requesting data with `unixtime` timeformat to "
                    "avoid daylight savings time (DST) transition issues."
                ).format(tz=timezone, err_type=err_name, error=err)

                _warnings.warn(warning_msg, UserWarning, stacklevel=2)
            else:
                raise

    # In-place key transformation to tuples -> (variable_name, unit)
    # This avoids building a new dictionary and avoids throwaway pandas indexes
    for col in list(ts_data.keys()):
        ts_data[(col, data_units.get(col, ""))] = ts_data.pop(col)

    df = _pd.DataFrame(data=ts_data, index=idx)
    df.index.name = "time"
    df.columns.names = ["variable", "unit"]

    return df.sort_index(ascending=ascending)


def search_locations(
    name,  # type: str
    count=10,  # type: int
    language="en",  # type: str
    fmt="json",  # type: Literal["json", "protobuf"]
    country_code=None,  # type: str|None
    timeout=(5, 30),  # type: tuple|float
    **params,  # type: Any
):
    # type: (...) -> list[Dict[str, Any]]|bytes
    """Searches for locations globally using the Open-Meteo Geocoding API.

    Queries location data (such as coordinates, timezones, elevation, and country
    codes) matching the provided location name or postal code.

    Args:
        name (str): Location name or postal code to search for (e.g., 'Hobart' or
            'Los Angeles, California'). Can optionally append a country or
            first-level administrative area after a comma to narrow results.
        count (int, optional): The number of search results to return (up to 100
            results max). Defaults to 10.
        language (str, optional): Return translated city and country names in this
            language (lower-cased code like 'en', 'de', 'fr'). Defaults to 'en'.
        fmt (str, optional): Response format, defaults to 'json' (alternatively
            supports 'protobuf'). Defaults to 'json'.
        country_code (str | None, optional): ISO-3166-1 alpha-2 country code to
            unambiguously filter results (e.g., 'AU', 'US', 'DE'). Defaults to None.
        timeout (int | float | tuple, optional): Request timeout.
            Seconds to wait before giving up. Accepts a single number to set the 
            same time limit for both connecting and receiving data, or a 
            ``(connect, read)`` tuple to set them separately. Defaults to (5, 30).
        **params: Additional Open-Meteo API parameters passed through directly.
            Use only for parameters that are not explicitly supported by this
            function.

            Warning: Use with caution
                Parameters may override existing request parameters.

    Returns:
        list[dict[str, Any]] or bytes: A list of matching location dictionaries
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

    Raises:
        ValueError: If `fmt` is not one of the supported values (``'json'`` or ``'protobuf'``).
        requests.HTTPError: If the network request fails or returns an invalid
            status code.

    Reference:
        - https://open-meteo.com/en/docs/geocoding-api
    """

    if isinstance(fmt, str):
        fmt = fmt.lower()
    if not fmt in {"json", "protobuf"}:
        raise ValueError(
            "Invalid fmt: {!r}. Expected 'json' or 'protobuf'.".format(fmt))

    _params = {
        "name": name,
        "count": count,
        "language": language.lower(),
        "format": fmt,
    }
    if country_code:
        _params["countryCode"] = country_code

    # Additional Open-Meteo parameters.
    #! WARNING: **params is a last-resort passthrough and may override parameters defined above.
    _params.update(params)

    headers = {
        "Accept": "application/json" if fmt == "json" else "application/x-protobuf"
    }
    response = _requests.get(
        url=URL_OPENMETEO.resolve_subdomain(
            subdomain="geocoding-api",
            path="/v1/search",
        ),
        params=_params,
        headers=headers,
        timeout=timeout
    )
    response.raise_for_status()

    if fmt == "protobuf":
        return response.content
    data = response.json()  # type: dict
    return data.get("results", [])
