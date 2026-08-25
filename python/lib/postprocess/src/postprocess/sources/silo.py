"""Utilities for retrieving historical meteorological data from SILO API.

Provides access to SILO datasets for use in post-processing workflows
and meteorological calculations.

Dependencies:
- requests : For http POST request
- pandas : For dataframe support

Example:
```python
# Importing SILO longpaddock as a source
from postprocess.sources import silo
```

Reference:
- <https://www.longpaddock.qld.gov.au/silo/api-documentation/>
- <https://www.longpaddock.qld.gov.au/silo/api-documentation/reference/>
- <https://www.longpaddock.qld.gov.au/silo/about/climate-variables/>
- <https://www.longpaddock.qld.gov.au/silo/about/about-data/>
"""

__all__ = [
    "SILOStationRecord",
    "SILOStation",
    "get_point_data",
    "location_meta_from_data",
    "get_nearby_stations",
    "find_nearby_stations",
    "dataframe_from_data",
]

import datetime as _datetime
from collections import defaultdict as _defaultdict
from typing import (
    TYPE_CHECKING,
    NamedTuple,
    Optional as _Optional,
)

try:
    # Python 3+
    from urllib.parse import urljoin as _urljoin
except ImportError:
    # Python 2.X
    from urlparse import urljoin as _urljoin  # type: ignore

import pandas as _pd
import requests as _requests

from .types import (
    Coordinates,
    LocationBase,
)
from .utils import (
    haversine_distance,
    round_to_nearest_05,
)

if TYPE_CHECKING:
    from datetime import date
    from typing import (
        Any,
        Dict,
        List,
        Tuple,
    )

# pylint: disable=consider-using-f-string

_SILO_BASE_URL = "https://www.longpaddock.qld.gov.au/cgi-bin/silo/"
"""Base URL for SILO API"""

SILOStationRecord = NamedTuple(
    "SILOStationRecord", [
        ("station_id", int),
        ("name", str),
        ("latitude", float),
        ("longitude", float),
        ("state", str),
        ("elevation_m", float),
        ("distance_km", _Optional[float]),
    ]
)
"""Represents a SILO station record.

Attributes:
    station_id (str): SILO Bureau of Meteorology station identifier number.
    name (str): The name of the station.
    latitude (float): Latitude of the station in decimal degrees,
        referenced to the GDA94 (Geocentric Datum of Australia 1994)
        coordinate reference system.
    longitude (float): Longitude of the station in decimal degrees,
        referenced to the GDA94 (Geocentric Datum of Australia 1994)
        coordinate reference system.
    state (str): Australian state or territory abbreviation where
        the station is located.
    elevation_m (float): Elevation of station, measured as metres above sea level.
    distance_km (Optional[float]): Distance from the reference station
        or coordinates in kilometres.
"""


class SILOStation(LocationBase):
    """SILO Longpaddock BOM Station Metadata.

    Attributes:
        station_id (int or str): Bureau of Meteorology station identifier number.
        name (str): Name of the station.
            Inherited from :class:`LocationBase`.
        latitude (float): Latitude of the station in decimal degrees,
            referenced to the GDA94 (Geocentric Datum of Australia 1994)
            coordinate reference system. Inherited from
            :class:`LocationBase`.
        longitude (float): Longitude of the station in decimal degrees,
            referenced to the GDA94 (Geocentric Datum of Australia 1994)
            coordinate reference system. Inherited from
            :class:`LocationBase`.
        elevation_m (float): Elevation of station, measured as metres above sea level.
            Inherited from :class:`LocationBase`.
        state (str): Australian state or territory abbreviation where the station is located.
        coordinates (tuple): Coordinates in (latitude, longitude).
            Inherited from :class:`LocationBase`.
    """

    def __init__(self, station_id, name, latitude, longitude, elevation_m, state):
        # type: (int|str, str, float, float, float, str|None) -> None
        """Constructor for SILO longpaddock station info.

        Args:
            station_id (int or str): Bureau of Meteorology station identifier number
            name (str): Name of the station.
            latitude (float): Latitude of the station in decimal degrees,
                referenced to the GDA94 (Geocentric Datum of Australia 1994)
                coordinate reference system.
            longitude (float): Longitude of the station in decimal degrees,
                referenced to the GDA94 (Geocentric Datum of Australia 1994)
                coordinate reference system.
            elevation_m (float): Elevation of station, measured as metres above sea level.
            state (str): Australian state or territory abbreviation where
                the station is located.
        """
        super(SILOStation, self).__init__(latitude=latitude,
                                          longitude=longitude,
                                          elevation_m=elevation_m,
                                          name=name)
        self.station_id = station_id
        """Bureau of Meteorology Station ID number"""
        self.state = state
        """Australian state or territory abbreviation where the station is located."""


def get_point_data(
    location,  # type: int|str|Tuple[float, float]
    start,  # type: str|int|date
    finish,  # type: str|int|date
    comment="R",  # type: str
    username="noemail@net.com",  # type: str
    timeout=(5, 30),  # type: int|float|Tuple[float, float]
    **params  # type: object
):  # type: (...) -> Dict[str, Any]
    """Retrieve climate data from the SILO point dataset.

    Station numbers query the Patched Point Dataset, while coordinate pairs
    query the Data Drill Dataset. Station data may be supplemented by
    interpolated estimates when observed data are missing.

    Args:
        location (int | str | tuple): SILO/Bureau of Meteorology station number,
            or a geographic coordinate referenced to GDA94 (Geocentric Datum of
            Australia 1994), provided as a ``(latitude, longitude)`` tuple in
            decimal degrees.
        start (str | int | date): Start date in ``YYYYMMDD`` format or python date object.
        finish (str | int | date): End date in ``YYYYMMDD`` format or python date object.
        comment (str): String of SILO climate variable codes to request.
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

        username (str): SILO API username or registered email address to be contacted by
            SILO for any access problems or critical information updates.
        timeout (float or tuple): Request timeout in seconds. A single value
            sets the same timeout for connecting and receiving data; a
            ``(connect, read)`` tuple sets them separately. Defaults to
            ``(5, 30)``.
        **params: Additional API parameters passed through directly.
            Use only for parameters that are not explicitly supported by this
            function.

            Warning: Use with caution
                Parameters may override existing request parameters.

    Returns:
        Dict[str, Any]: Parsed JSON response from the SILO API.

    Raises:
        requests.RequestException: If the SILO API request fails.
        ValueError: If the coordinate pair is invalid or the response contains
            invalid JSON.

    Example:
        >>> data = get_point_data(
        ...     location=40004,
        ...     start="20200101",
        ...     finish="20200131",
        ...     username="your_email@example.com",
        ...     comment="XN",
        ... )
        >>> data["station"]["name"]
        'AMBERLEY AMO'
    """
    if isinstance(start, _datetime.date):
        start = start.strftime("%Y%m%d")
    if isinstance(finish, _datetime.date):
        finish = finish.strftime("%Y%m%d")

    _params = {
        "format": "json",
        "start": start,
        "finish": finish,
        "comment": comment,
        "username": username
    }

    if isinstance(location, tuple):
        Coordinates.validate_decimal_degree(location)
        _params.update({
            "lat": round_to_nearest_05(location[0]),
            "lon": round_to_nearest_05(location[1])
        })
        url = _urljoin(_SILO_BASE_URL, "DataDrillDataset.php")
    else:
        _params["station"] = location
        url = _urljoin(_SILO_BASE_URL, "PatchedPointDataset.php")

    # Additional parameter overrides.
    #! WARNING: **params is a last-resort passthrough and may override parameters defined above.
    _params.update(params)

    headers = {"Accept": "application/json"}
    response = _requests.get(
        url,
        params=_params,
        headers=headers,
        timeout=timeout,
    )

    response.raise_for_status()
    return response.json()


def location_meta_from_data(point_data):
    # type: (Dict) -> SILOStation|LocationBase|None
    """Get station info from retrieved point or drill data.

    Args:
        point_data (dict): JSON response from point data API request.

    Returns:
        SILOStation or LocationBase: Location metadata object.
        None: If no metadata was found.
    """
    # Fall back to location if no station data
    station = point_data.get("station")  # type: Dict[str, Any]
    if station is not None:
        return SILOStation(
            station_id=station.get("number"),
            state=station.get("state"),
            latitude=station.get("latitude"),
            longitude=station.get("longitude"),
            elevation_m=station.get("elevation"),
            name=station.get("name", ""),
        )

    location = point_data.get("location")  # type: Dict[str, Any]
    if location is not None:
        return LocationBase(
            latitude=location.get("latitude"),
            longitude=location.get("longitude"),
            elevation_m=location.get("elevation"),
            name=location.get("name", ""),
        )

    return None


def get_nearby_stations(station_id, radius_km=50, sortby=None, timeout=(5, 30), **params):
    # type: (int|str, float, str, float|Tuple, object) -> List[SILOStationRecord]
    """Return SILO stations within a radius of a reference station.

    Queries the SILO Patched Point Dataset API and parses the response into
    a list SILO stations records.

    Args:
        station_id (int or str): Reference SILO BOM station number.
        radius_km (float): Search radius in kilometres. Defaults to 50.
        sortby (str, optional): Sort field. Currently, only ``"name"`` has
            been observed to return results; ``"ID"`` and ``"dist"`` return
            an empty response. If None, the API's default ordering is used.
            Defaults to None.
        timeout (float or tuple): Request timeout in seconds. A single value
            sets the same timeout for connecting and receiving data; a
            ``(connect, read)`` tuple sets them separately. Defaults to
            ``(5, 30)``.
        **params: Additional API parameters passed through directly.
            Use only for parameters that are not explicitly supported by this
            function.

            Warning: Use with caution
                Parameters may override existing request parameters.

    Returns:
        list[SILOStationRecord]: Stations within the specfiied radius,
            sorted by distance; empty if none are found.
            See the :class:`SILOStationRecord` for mapping.

    Raises:
        requests.HTTPError: If the SILO API returns an unsuccessful HTTP
            status code.
        requests.RequestException: If the request fails.
        ValueError: If the SILO response has an unexpected format or
            contains invalid station data.
    """
    if radius_km <= 0:
        raise ValueError("radius must be greater than zero")

    _params = {
        "format": "near",
        "station": station_id,
        "radius": radius_km,
    }

    if sortby is not None:
        _params["sortby"] = sortby

    # Additional parameter overrides.
    #! WARNING: **params is a last-resort passthrough and may override parameters defined above.
    _params.update(params)

    url = _urljoin(_SILO_BASE_URL, "PatchedPointDataset.php")
    headers = {"Accept": "text/plain"}
    response = _requests.get(
        url,
        params=_params,
        headers=headers,
        timeout=timeout,
    )

    response.raise_for_status()

    # Delegate parsing to our standardized data function
    return _silo_station_records_from_data(response.text)


def _silo_station_records_from_data(text):
    # type: (str) -> List[SILOStationRecord]
    """Parse SILO text response into a list of station records.

    Args:
        text (str): Raw text response from SILO API.

    Returns:
        list[SILOStationRecord]: Parsed station records.
    """
    stations = []
    # Response Text example:
    # Number|Station name            |Latitude|Longitud|Stat|Elevat.|Distance (km)
    #  15526|FINKE POST OFFICE       |-25.5833|134.5667|NT  |  267.0|  0.0
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("Number|"):
            continue

        fields = line.split("|")
        if len(fields) != 7:
            raise ValueError(
                "Unexpected SILO station response format: {!r}".format(line))

        try:
            station = SILOStationRecord(
                station_id=int(fields[0]),
                name=fields[1].strip(),
                latitude=float(fields[2]),
                longitude=float(fields[3]),
                state=fields[4].strip(),
                elevation_m=float(fields[5]),
                distance_km=float(fields[6]),
            )
        except ValueError as err:
            raise ValueError(
                "Invalid SILO station response: {!r}".format(line)) from err

        stations.append(station)

    return stations


def find_nearby_stations(location, radius_km=50, timeout=(5, 30)):
    # type: (str|int|Tuple[float,float], float, float|Tuple[float,float]) -> List[SILOStationRecord]
    """Return nearby SILO stations relative to a station or coordinates.

    Coordinate-based searches use BOM station 15603 (Kulgera) as the SILO
    reference station, then calculate Haversine distances from the supplied
    coordinates and filter results by radius.

    Args:
        location (str, int or tuple): Reference SILO station number or a
            (latitude, longitude) coordinate pair.
        radius_km (float): Search radius in kilometres. Defaults to 50.
        timeout (float or tuple): Request timeout in seconds. A single value
            sets the same timeout for connecting and receiving data; a
            ``(connect, read)`` tuple sets them separately. Defaults to
            ``(5, 30)``.

        Returns:
            list[SILOStationRecord]: Stations within the specfiied radius,
                sorted by distance; empty if none are found.
                See the :class:`SILOStationRecord` for mapping.

    Raises:
        ValueError: If location is a coordinate pair with invalid values.
        requests.HTTPError: If the SILO API returns an unsuccessful HTTP
            status code.
        requests.RequestException: If the request fails.
    """
    # Location is station number
    if not isinstance(location, tuple):
        return get_nearby_stations(station_id=location,
                                   radius_km=radius_km,
                                   sortby=None,
                                   timeout=timeout)

    # Location is coordinates
    Coordinates.validate_decimal_degree(location)

    # Use closest BOM station to geographic centre as reference
    # BOM Site Number: 015603 (Kulgera Weather Station, Northern Territory, Australia)
    # Set reference radius to 10000 km as Mawson Station (300001) is furthest
    # bom station in Australian Antarctic Territory of 6539 km from Kulgera Weather Station
    source_stations = get_nearby_stations(station_id=15603,
                                          radius_km=10000 if radius_km < 1000 else radius_km,
                                          sortby="name",
                                          timeout=timeout)
    # Calculate distance from reference station
    filtered_stations = []  # type: list[SILOStationRecord]
    for station in source_stations:
        distance_km = haversine_distance(
            location,
            (station.latitude, station.longitude),
        )
        distance_km = round(distance_km, 3)
        if distance_km <= radius_km:
            filtered_stations.append(
                station._replace(distance_km=distance_km)
            )

    del source_stations

    # Filter and sort
    filtered_stations.sort(key=lambda station: station.distance_km)
    return filtered_stations


def dataframe_from_data(point_data, include_source=False, ascending=True, date_format="%Y-%m-%d"):
    # type: (Dict, bool, bool, str|None) -> _pd.DataFrame
    """Extract timeseries data from SILO API point data response into DataFrame.

    Args:
        point_data (dict): JSON response from the SILO get point data API.
        include_source (bool, optional): Whether to preserve and include the 'source'
            metadata column alongside the primary 'value' column for each metric.
            Defaults to True.
        ascending (bool, optional): Sort chronological (True) or reverse (False).
            Defaults to True.
        date_format (str, optional): Format string to inform pandas how
            to parse the date (e.g., '%Y-%m-%d' or 'ISO8601'). Defaults to
            '%Y-%m-%d'; pass None to enable automatic inference.

    Raises:
        TypeError: ``point_data`` is not a dictionary.
        ValueError: ``point_data`` is empty.
        KeyError: Timeseries data is missing from ``point_data``.

    Returns:
        pandas.DataFrame: A DataFrame containing time-series data, featuring flat
            column headers containing field names by default, or MultiIndex column
            headers (field name and metric type) when include_source is True.
    """
    if not isinstance(point_data, dict):
        raise TypeError(
            "`point_data` must be a dictionary, got {}".format(type(point_data).__name__))
    if not point_data:
        raise ValueError("Empty data!")

    data = point_data.get("data")  # type: List[Dict[str, Any]]
    if not data:
        raise KeyError("Missing timeseries data.")

    records = _defaultdict(dict)

    # Flatten data into a simple list of flat dictionaries
    for record in data:
        # Use 'date' as a standard column key, and tuples for the other metrics
        date_value = record["date"]
        for var in record["variables"]:
            primary_field = var["variable_code"]
            if include_source:
                records[(primary_field, "value")][date_value] = var["value"]
                records[(primary_field, "source")][date_value] = var["source"]
            else:
                records[primary_field][date_value] = var["value"]

    df = _pd.DataFrame(records)
    df.index = _pd.to_datetime(df.index, format=date_format)
    df.index.name = "date"
    df.columns.names = ["variable", "property"]

    return df.sort_index(ascending=ascending)
