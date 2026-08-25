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

from datetime import date
from typing import TYPE_CHECKING

try:
    # Python 3+
    from urllib.parse import urljoin as _urljoin
except ImportError:
    # Python 2.X
    from urlparse import urljoin as _urljoin  # type: ignore

import requests as _requests
import pandas as _pd

from .utils import (
    LocationMetadata,
    is_valid_coordinates,
    haversine_distance,
)

if TYPE_CHECKING:
    from typing import Any, Dict, List, Tuple

# pylint: disable=consider-using-f-string

_SILO_BASE_URL = "https://www.longpaddock.qld.gov.au/cgi-bin/silo/"
"""Base URL for SILO API"""


class SILOStationMetadata(LocationMetadata):
    """SILO Longpaddock BOM Station Metadata.

    Attributes:
        number (int or str): Beauro of Meteorology station number.
        name (str): Name of the station.
            Inherited from :class:`LocationMetadata`.
        latitude (float): Latitude of the station in GDA94.
            Inherited from :class:`LocationMetadata`.
        longitude (float): Longitude of the station in GDA94.
            Inherited from :class:`LocationMetadata`.
        elevation (float): Elevation of station, measured as metres above sea level.
            Inherited from :class:`LocationMetadata`.
        state (str or None): State in which station is located.
        coordinates (tuple): Coordinates in (latitude, longitude).
            Inherited from :class:`LocationMetadata`.
    """

    def __init__(self, number, name, latitude, longitude, elevation, state):
        # type: (int|str, str, float, float, float, str|None) -> None
        """Constructor for SILO longpaddock station info.

        Args:
            number (int or str): Beauro of Meteorology station number
            name (str): Name of the station.
            latitude (float): Latitude of the station in GDA94.
            longitude: Longitude of the station in GDA94.
            elevation (float): Elevation of station, measured as metres above sea level.
            state (str): State in which station is located.
        """
        super(SILOStationMetadata, self).__init__(latitude=latitude,
                                                  longitude=longitude,
                                                  elevation=elevation,
                                                  name=name)
        self.number = number
        """Station ID number"""
        self.state = state
        """State station is located in"""


def get_point_data(
    location,  # type: int|str|Tuple[float, float]
    start,  # type: str|int|date
    finish,  # type: str|int|date
    comment="R",  # type: str
    username="noemail@net.com",  # type: str
    timeout=(5, 30)  # type: int|float|Tuple[float, float]
):  # type: (...) -> Dict[str, Any]
    """Retrieve climate data from the SILO point dataset.

    Station numbers query the Patched Point Dataset, while coordinate pairs
    query the Data Drill Dataset. Station data may be supplemented by
    interpolated estimates when observed data are missing.

    Args:
        location (int | str | tuple): SILO/Bureau of Meteorology station number
            or a ``(latitude, longitude)`` coordinate pair.
        start (str | int | date): Start date in ``YYYYMMDD`` format or python date object.
        finish (str | int | date): End date in ``YYYYMMDD`` format or python date object.
        comment (str): String of SILO climate variable codes to request.
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

        username (str): SILO API username or registered email address to be contacted by
            SILO for any access problems or critical information updates.
        timeout (float or tuple): Request timeout in seconds. A single value
            sets the same timeout for connecting and receiving data; a
            ``(connect, read)`` tuple sets them separately. Defaults to
            ``(5, 30)``.

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
    if isinstance(start, date):
        start = start.strftime("%Y%m%d")
    if isinstance(finish, date):
        finish = finish.strftime("%Y%m%d")

    params = {
        "format": "json",
        "start": start,
        "finish": finish,
        "comment": comment,
        "username": username
    }

    if isinstance(location, tuple):
        if not is_valid_coordinates(location):
            raise ValueError("Invalid coordinates.")
        params.update({
            "lat": _round_to_nearest_05(location[0]),
            "lon": _round_to_nearest_05(location[1])
        })
        url = _urljoin(_SILO_BASE_URL, "DataDrillDataset.php")
    else:
        params["station"] = location
        url = _urljoin(_SILO_BASE_URL, "PatchedPointDataset.php")

    headers = {"Accept": "application/json"}
    response = _requests.get(
        url,
        params=params,
        headers=headers,
        timeout=timeout,
    )

    response.raise_for_status()
    return response.json()


def get_location_meta(point_data):
    # type: (Dict) -> SILOStationMetadata|LocationMetadata|None
    """Get station info from retrieved point or drill data.

    Args:
        point_data (dict): JSON response from point data API request.

    Returns:
        SILOStationMetadata or LocationMetadata: Location metadata object.
        None: If no metadata was found.
    """
    # Fall back to location if no station data
    station = point_data.get("station")
    if station is not None:
        return SILOStationMetadata(
            number=station.get("number"),
            name=station.get("name", ""),
            latitude=station.get("latitude"),
            longitude=station.get("longitude"),
            elevation=station.get("elevation"),
            state=station.get("state")
        )
    location = point_data.get("location")
    if location is not None:
        return LocationMetadata(
            latitude=location.get("latitude"),
            longitude=location.get("longitude"),
            elevation=location.get("elevation"),
            name=location.get("name", "")
        )
    return None


def get_nearby_stations(station_id, radius=50, sortby=None, timeout=(5, 30)):
    # type: (int|str, float, str, float|Tuple) -> List[Dict]
    """Return SILO stations within a radius of a reference station.

    Queries the SILO Patched Point Dataset API and parses the response into
    a list of station dictionaries.

    Args:
        station_id (int or str): Reference SILO BOM station number.
        radius (float): Search radius in kilometres. Defaults to 50.
        sortby (str, optional): Sort field. Currently, only ``"name"`` has
            been observed to return results; ``"ID"`` and ``"dist"`` return
            an empty response. If None, the API's default ordering is used.
            Defaults to None.
        timeout (float or tuple): Request timeout in seconds. A single value
            sets the same timeout for connecting and receiving data; a
            ``(connect, read)`` tuple sets them separately. Defaults to
            ``(5, 30)``.

    Returns:
        list[dict]: A list of nearby stations, or an empty list if no stations are found.
            Each station dictionary contains the following keys:

            - ``number`` (int): SILO station number.
            - ``name`` (str): Station name.
            - ``latitude`` (float): Latitude of the station in GDA94.
            - ``longitude`` (float): Longitude of the station in GDA94.
            - ``elevation`` (float): Station elevation in metres.
            - ``state`` (str): Australian state or territory.
            - ``distance_km`` (float): Distance from the reference station
              in kilometres, as reported by SILO.

    Raises:
        requests.HTTPError: If the SILO API returns an unsuccessful HTTP
            status code.
        requests.RequestException: If the request fails.
        ValueError: If the SILO response has an unexpected format or
            contains invalid station data.
    """
    if radius <= 0:
        raise ValueError("radius must be greater than zero")

    params = {
        "format": "near",
        "station": station_id,
        "radius": radius,
    }

    if sortby is not None:
        params["sortby"] = sortby

    url = _urljoin(_SILO_BASE_URL, "PatchedPointDataset.php")
    headers = {"Accept": "text/plain"}
    response = _requests.get(
        url,
        params=params,
        headers=headers,
        timeout=timeout,
    )

    response.raise_for_status()
    stations = []

    # Response Text example:
    # Number|Station name            |Latitude|Longitud|Stat|Elevat.|Distance (km)
    #  15526|FINKE POST OFFICE       |-25.5833|134.5667|NT  |  267.0|  0.0
    for line in response.text.splitlines():
        line = line.strip()
        if not line or line.startswith("Number|"):
            continue

        fields = [field.strip() for field in line.split("|")]

        if len(fields) != 7:
            raise ValueError(
                "Unexpected SILO station response format: {!r}".format(line))

        try:
            station = {
                "number": int(fields[0]),
                "name": fields[1],
                "latitude": float(fields[2]),
                "longitude": float(fields[3]),
                "elevation": float(fields[5]),
                "state": fields[4],
                "distance_km": float(fields[6])
            }
        except ValueError as err:
            raise ValueError(
                "Invalid SILO station response: {!r}".format(line)) from err
        stations.append(station)
    return stations


def find_nearby_stations(location, radius=50, timeout=(5, 30)):
    # type: (str|int|Tuple[float,float], float, float|Tuple[float,float]) -> List[Dict]
    """Return nearby SILO stations relative to a station or coordinates.

    Coordinate-based searches use BOM station 15603 (Kulgera) as the SILO
    reference station, then calculate Haversine distances from the supplied
    coordinates and filter results by radius.

    Args:
        location (str, int or tuple): Reference SILO station number or a
            (latitude, longitude) coordinate pair.
        radius (float): Search radius in kilometres. Defaults to 50.
        timeout (float or tuple): Request timeout in seconds. A single value
            sets the same timeout for connecting and receiving data; a
            ``(connect, read)`` tuple sets them separately. Defaults to
            ``(5, 30)``.

        Returns:
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

    Raises:
        ValueError: If location is a coordinate pair with invalid values.
        requests.HTTPError: If the SILO API returns an unsuccessful HTTP
            status code.
        requests.RequestException: If the request fails.
    """
    # Location is station number
    if not isinstance(location, tuple):
        return get_nearby_stations(station_id=location,
                                   radius=radius,
                                   sortby=None,
                                   timeout=timeout)

    # Location is coordinates
    if not is_valid_coordinates(location):
        raise ValueError("Invalid coordinates.")

    # Use closest BOM station to geographic centre as reference
    # BOM Site Number: 015603 (Kulgera Weather Station, Northern Territory, Australia)
    # Set reference radius to 10000 km as Mawson Station (300001) is furthest
    # bom station in Australian Antarctic Territory of 6539 km from Kulgera Weather Station
    stations = get_nearby_stations(station_id=15603,
                                   radius=10000 if radius < 1000 else radius,
                                   sortby="name",
                                   timeout=timeout)
    # Calculate distance from reference station
    for station in stations:
        station["distance_km"] = haversine_distance(
            location,
            (station["latitude"], station["longitude"]),
        )
        station["distance_km"] = round(station["distance_km"], 3)

    # Filter and sort
    stations = [
        station for station in stations if station["distance_km"] <= radius]
    stations.sort(key=lambda station: station["distance_km"])
    return stations


def extract_timeseries_dataframe(point_data):
    # type: (Dict) -> _pd.DataFrame
    """Extract timeseries data from SILO API point data response into DataFrame.

    Args:
        point_data (dict): JSON response from the SILO get point data API.

    Raises:
        ValueError: JSON response is empty.
        KeyError: Timeseries data is missing from JSON response.

    Returns:
        pandas.DataFrame: A DataFrame containing timeseries data.
            With column headers containing field names and data code source.
    """
    if not point_data:
        raise ValueError("Empty data!")

    data = point_data.get("data")

    if data is None:
        raise KeyError("Missing timeseries data.")

    rows = []

    for record in data:
        row = {"date": record["date"]}
        for variable in record["variables"]:
            column = (
                variable["variable_code"],
                variable["source"],
            )
            row[column] = variable["value"]
        rows.append(row)

    df = _pd.DataFrame(rows)

    df["date"] = _pd.to_datetime(df["date"])
    df = df.set_index("date")

    df.columns = _pd.MultiIndex.from_tuples(
        df.columns,
        names=["variable", "source"],
    )
    return df


def _round_to_nearest_05(x):
    """Round value to nearest 0.05."""
    return round(x * 20) / 20
