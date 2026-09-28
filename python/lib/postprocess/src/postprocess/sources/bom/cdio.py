"""Client for accessing historical climate and weather observations
from the Australian Bureau of Meteorology's Climate Data Online service.

This is an unofficial, community-developed interface and is not
affiliated with, endorsed by, or officially supported by the Bureau
of Meteorology.

Use of Bureau of Meteorology data is subject to the applicable
copyright, licensing, and terms-of-use requirements. See the
Bureau's copyright notice for details:

https://www.bom.gov.au/copyright

Obtained by reverse engineering API access: https://www.bom.gov.au/climate/data/index.shtml

References:
- https://www.bom.gov.au/climate/cdo/about/cdo-faqs.shtml
- https://www.bom.gov.au/climate/cdo/about/site-num.shtml
- https://www.bom.gov.au/climate/cdo/about/about-directory.shtml
- https://www.bom.gov.au/climate/data/
- https://www.bom.gov.au//climate/cdo/about/sitedata.shtml
- https://www.bom.gov.au/climate/data/stations/
"""

__all__ = [
    # Constants / Dictionaries
    "NCC_OBS_CODES",

    # Records & Data Structures
    "Location",
    "DWOStation",

    # Utilities & Finders
    "StationFinder",

    # Main Client
    "WeatherObservationsClient",
]

import calendar as _calendar
import datetime as _datetime
import io as _io
import logging as _logging
import random as _random
from typing import NamedTuple, TYPE_CHECKING

import pandas as _pd
import requests as _requests

from ..types import (
    Coordinates,
    LocationBase,
)
from ..utils import (
    URLBuilder as _URLBuilder,
    generate_monthly_dates as _generate_montly_dates,
)

if TYPE_CHECKING:
    from datetime import date, datetime

# pylint: disable=consider-using-f-string

logger = _logging.getLogger(__name__)

NCC_OBS_CODES = {
    136: {
        "name": "Daily rainfall",
        "element_group": "rainfall",
        "element_type": 2,
        "element_order": "daily",
        "description": (
            "Daily rainfall data and graphs for a selected year. "
            "Data download for one or all years."
        ),
        "web_map_layer": "IDC10002-d",
    },

    139: {
        "name": "Monthly rainfall",
        "element_group": "rainfall",
        "element_type": 2,
        "element_order": "monthly",
        "description": (
            "Monthly rainfall data and graphs for all available years."
        ),
        "web_map_layer": "IDC10002",
    },

    36: {
        "name": "Monthly mean maximum temperature",
        "element_group": "temperature",
        "element_type": 3,
        "element_order": "monthly",
        "description": (
            "Mean maximum temperature data and graphs "
            "for all available years."
        ),
        "web_map_layer": "IDC10008",
    },

    38: {
        "name": "Monthly mean minimum temperature",
        "element_group": "temperature",
        "element_type": 3,
        "element_order": "monthly",
        "description": (
            "Mean minimum temperature data and graphs "
            "for all available years."
        ),
        "web_map_layer": "IDC10003",
    },

    40: {
        "name": "Monthly highest temperature",
        "element_group": "temperature",
        "element_type": 3,
        "element_order": "monthly",
        "description": (
            "Highest temperature data and graphs "
            "for all available years."
        ),
        "web_map_layer": "IDC10006",
    },

    41: {
        "name": "Monthly lowest maximum temperature",
        "element_group": "temperature",
        "element_type": 3,
        "element_order": "monthly",
        "description": (
            "Lowest maximum temperature data and graphs "
            "for all available years."
        ),
        "web_map_layer": "IDC10004",
    },

    42: {
        "name": "Monthly highest minimum temperature",
        "element_group": "temperature",
        "element_type": 3,
        "element_order": "monthly",
        "description": (
            "Highest minimum temperature data and graphs "
            "for all available years."
        ),
        "web_map_layer": "IDC10007",
    },

    43: {
        "name": "Monthly lowest temperature",
        "element_group": "temperature",
        "element_type": 3,
        "element_order": "monthly",
        "description": (
            "Lowest temperature data and graphs "
            "for all available years."
        ),
        "web_map_layer": "IDC10005",
    },

    201: {
        "name": "Daily weather observations",
        "element_group": "weather",
        "element_type": 1,
        "element_order": "daily",
        "description": (
            "Daily weather observations data for the last month. "
            "Links to data for the previous year. "
            "Data may be from a number of stations."
        ),
        "web_map_layer": "IDC10001",
    },

    200: {
        "name": "Monthly climate statistics",
        "element_group": "weather",
        "element_type": 1,
        "element_order": "statistics",
        "description": (
            "Monthly climate statistics and graphs "
            "for all available years."
        ),
        "web_map_layer": "IDC10000",
    },

    202: {
        "name": "Daily climate calendar",
        "element_group": "weather",
        "element_type": 1,
        "element_order": "calendar",
        "description": (
            "Calendar of daily statistics showing typical weather "
            "for each day and some weather history."
        ),
        "web_map_layer": "IDC10000-d",
    },

    122: {
        "name": "Daily maximum temperature",
        "element_group": "temperature",
        "element_type": 3,
        "element_order": "daily",
        "description": (
            "Daily maximum temperature data and graphs "
            "for a selected year. "
            "Data download for one or all years."
        ),
        "web_map_layer": "IDC10025",
    },

    123: {
        "name": "Daily minimum temperature",
        "element_group": "temperature",
        "element_type": 3,
        "element_order": "daily",
        "description": (
            "Daily minimum temperature data and graphs "
            "for a selected year. "
            "Data download for one or all years."
        ),
        "web_map_layer": "IDC10024",
    },

    193: {
        "name": "Daily solar exposure",
        "element_group": "solar",
        "element_type": 4,
        "element_order": "daily",
        "description": (
            "Daily solar exposure data and graphs "
            "for a selected year. "
            "Data download for one or all years."
        ),
        "web_map_layer": "IDCJAC0016-d",
    },

    203: {
        "name": "Monthly solar exposure",
        "element_group": "solar",
        "element_type": 4,
        "element_order": "monthly",
        "description": (
            "Monthly mean daily solar exposure data and graphs "
            "for all available years."
        ),
        "web_map_layer": "IDCJAC0016",
    },
}
"""Known available National Climate Center Observation Code dictionary lookup."""


class Location(LocationBase):
    """Represents a geographic location returned from BOM gazetteer.

    This class extends :class:`LocationBase`.

    Attributes:
        state (str): Australian state or territory abbreviation.
    """

    def __init__(self, name, state, latitude, longitude):
        # type: (str, str, float, float) -> None
        """Initializes a Location.

        Args:
            name (str): Name of the location.
            state (str): Australian state or territory abbreviation.
            latitude (float): Latitude in decimal degrees.
            longitude (float): Longitude in decimal degrees.
        """
        super().__init__(name=name, latitude=latitude, longitude=longitude)
        self.state = state

    def __str__(self):
        # type: () -> str
        """Returns the location in the BOM string format.

        Returns:
            str: The location formatted as a BOM location record.
        """
        return "{name},{state},{latitude},{longitude}".format(
            name=self.name,
            state=self.state,
            latitude=self.latitude,
            longitude=self.longitude,
        )

    @classmethod
    def from_string(cls, value):
        # type: (str) -> "Location"
        """Creates a Location from a matching location record.

        Expected value:
        ```
        'Melbourne, VIC, 37.84°S, 144.98°E'
        ```

        Args:
            value (str): Location string returned by
                :meth:`find_matching_locations`.

        Returns:
            Location: A Location instance containing the parsed location data.
        """
        name, state, latitude, longitude = value.split(",")

        return cls(
            name=name.strip(),
            state=state.strip(),
            latitude=cls._parse_coordinate(latitude),
            longitude=cls._parse_coordinate(longitude)
        )

    def to_bom_string(self):
        # type: (...) -> str
        """Return this location in the format expected by BOM.

        The latitude is converted to a positive value because the BOM
        Climate Data Online service expects Southern Hemisphere latitudes
        as positive values. The longitude retains its signed value.

        Returns:
            str: BOM location record containing the location name, state,
                latitude, and longitude in the format expected by the
                Climate Data Online service.
        """
        return "{name},{state},{latitude},{longitude}".format(
            name=self.name,
            state=self.state,
            latitude=abs(self.latitude),
            longitude=self.longitude,
        )

    @staticmethod
    def _parse_coordinate(value):
        # type: (str) -> float
        """Parse a BOM coordinate with a hemisphere suffix.

        Args:
            value (str): Coordinate such as ``'37.84°S'`` or ``'144.98°E'``.

        Returns:
            float: Signed decimal degrees.

        Raises:
            ValueError: If the coordinate has an unsupported hemisphere.
        """
        try:
            coordinate = value.rstrip()
            hemisphere = coordinate[-1].upper()  # get hemisphere suffix
            # Strip hemisphere suffix '°S', '°E', '°N' or '°W'
            degrees = float(coordinate[:-2].strip())
        except (ValueError, TypeError, IndexError, AttributeError) as e:
            raise ValueError("Invalid coordinate format") from e

        if hemisphere in ("S", "W"):
            return -degrees
        if hemisphere in ("N", "E"):
            return degrees

        raise ValueError(
            "Invalid coordinate hemisphere: {!r}".format(hemisphere)
        )


DWOStation = NamedTuple(
    "DWOStation", [
        ("dwo_id", int),
        ("station_id", int),
        ("name", str),
        ("state", str),
        ("distance_km", float),
        ("is_open", bool),
    ]
)
"""Bureau of Meteorology weather station returned by BOM Climate Data station search.

Attributes:
    dwo_id (int): Bureau of Meteorology daily weather observation station
        identifier.
    station_id (int): Bureau of Meteorology station identifier.
    name (str): Name of the weather station.
    state (str): Australian state or territory abbreviation where the
        station is located.
    distance_km (float): Distance from the searched location to the
        station in kilometres.
    is_open (bool): Whether the station is listed as open by the Bureau
        of Meteorology.
"""


_URL_BOM_CDIO = _URLBuilder(
    domain="bom.gov.au",
    subdomain="reg",
    path="jsp/ncc/cdio/weatherData/av"
)
"""BOM Climate Data Online URL"""


class StationFinder(object):
    """An execution system mirroring the BOM Climate Data Online Text Tool Guide.

    Resolves arbitrary text inputs into specific Australian Gazetteer towns,
    which are then used to discover and isolate local weather stations.
    """

    @staticmethod
    def find_matching_locations(location_name, timeout=(5, 30)):
        # type: (str, tuple[float,float]) -> list[Location]
        """Find locations matching town names using the BOM gazetteer.

        Matches part or all of a location name and returns matching town strings
        along with their corresponding coordinates.

        Args:
            location_name (str): Name or partial name of the location to search
                for.
            timeout (float | tuple[float, float], optional): Request timeout in
                seconds. A single value specifies the total timeout; a tuple
                specifies separate connect and read timeouts. Defaults to
                ``(5, 30)``.

        Returns:
            list[Location]: Locations matching ``location_name``. Returns an
                empty list if the BOM service returns no matching locations.
        """
        params = {
            # `p_stn_num is not used for gazetteer search thus hardcoded to 86071
            "p_stn_num": 86071,
            "p_display_type": "gazetteer",
            # `p_nccObsCode` is not used for gazetteer search thus hardcoded to 139
            "p_nccObsCode": 139,
            "p_locSearch": location_name,
            "p_state": "ALL",
            "sid": _random.random()
        }
        headers = {"Accept": "text/html; charset=ISO-8859-1"}
        response = _requests.get(
            url=_URL_BOM_CDIO.base_url,
            params=params,
            headers=headers,
            timeout=timeout
        )
        response.raise_for_status()
        if response.status_code == 200:
            if response.text == "Empty resultset" or response.text.startswith("<!DOCTYPE"):
                return []
            return [
                Location.from_string(record)
                for record in response.text.rstrip("||").split("||")
            ]

    @staticmethod
    def find_nearest_stations(
        nccObsCode,  # type: int
        location,  # type: Location|str|tuple[float,float]|int
        radius_km=50,  # type: float
        open_only=True,  # type: bool
        timeout=(5, 30),  # type: float|tuple
    ):  # type: (...) -> list[DWOStation]
        """Find BOM weather stations near a location.

        Args:
            nccObsCode (int): BOM National Climate Center observation
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

            location (Coordinates | Location | str | int): Location used to search
                for nearby stations. A string is interpreted as a location name,
                a ``(latitude, longitude)`` tuple as geographic coordinates, and
                an integer as a BOM station identifier.
            radius_km (float, optional): Search radius in kilometres. Defaults to
                ``50``.
            open_only (bool, optional): Whether to return only stations that are
                currently open. Defaults to ``True``.
            timeout (float | tuple[float, float], optional): Request timeout in
                seconds. A single value specifies the total timeout; a tuple
                specifies separate connect and read timeouts. Defaults to
                ``(5, 30)``.

        Returns:
            list[DWOStation]: BOM weather stations matching the search criteria,
                optionally restricted to open stations. Returns an
                empty list if the BOM service returns no matching stations.

        Raises:
            ValueError: Invalid ``ncc_obs_code``.
        """
        # pylint: disable=invalid-name
        if nccObsCode not in NCC_OBS_CODES:
            raise ValueError(
                "Invalid `nccObsCode`: {nccObsCode}. "
                "Choose from {codes}".format(
                    nccObsCode=nccObsCode,
                    codes=sorted(NCC_OBS_CODES.keys())
                )
            )
        _nccObsCode = nccObsCode
        _nccObsCode = 200 if _nccObsCode == 202 else _nccObsCode

        params = {
            # `p_stn_num` is not not used, hard code 86071. param encoded in `p_match`
            "p_stn_num": 86071,
            # `p_nccObsCode is not used, hardcoded to 139. param encoded in `p_match`
            "p_nccObsCode": 139,
            "sid": _random.random()
        }

        if isinstance(location, tuple):
            Coordinates.validate_decimal_degree(location)
            latitude, longitude = location

            if not -90 <= latitude <= 0:
                raise ValueError(
                    "Latitude must be in the Southern Hemisphere "
                    "(-90 <= latitude <= 0)."
                )

            if not 0 <= longitude <= 180:
                raise ValueError(
                    "Longitude must be in the Eastern Hemisphere "
                    "(0 <= longitude <= 180)."
                )

            params["p_display_type"] = "nearest10_tab2"
            match_mode = "LATLON"
            p_match = "{radius},,{lat},{lon},,".format(
                radius=radius_km,
                # Convert signed southern latitude to BOM's positive format
                lat=abs(latitude),
                lon=longitude,
            )
        elif isinstance(location, int) or (
            isinstance(location, str) and location.isdigit()
        ):
            params["p_display_type"] = "nearest10_tab2"
            match_mode = "S_NUM"
            p_match = "{radius},{station_id},,,,".format(
                radius=radius_km,
                station_id=location,
            )
        else:
            params["p_display_type"] = "nearest10_tab1"
            match_mode = "LATLON"
            p_match = "{location},,".format(
                location=(
                    location.to_bom_string()
                    if isinstance(location, Location) else location
                ),
            )

        p_match = p_match + "{match_mode},{_nccObsCode}".format(
            match_mode=match_mode,
            _nccObsCode=_nccObsCode,
        )
        params["p_match"] = p_match

        headers = {"Accept": "text/html; charset=ISO-8859-1"}
        response = _requests.get(
            url=_URL_BOM_CDIO.base_url,
            params=params,
            headers=headers,
            timeout=timeout
        )
        response.raise_for_status()

        if response.status_code == 200:
            if response.text == "Empty resultset" or response.text.startswith("<!DOCTYPE"):
                return []
            return [
                station
                for station in (
                    StationFinder._parse_dwo_station_record(record)
                    for record in response.text.rstrip("||").split("||")
                )
                if not open_only or station.is_open
            ]

    @staticmethod
    def _parse_dwo_station_record(record):
        # type: (str) -> DWOStation
        """Parse a BOM weather station search record.

        Expected record format:
        ```
        # Open station
        '3015_90035 Colac (Mt Gellibrand) VIC (112.2km away)    '
        # Closed station
        '3103_85301 Yanakie VIC (149.9km away)'
        ```

        Args:
            record (str): Raw DWO station record returned by the BOM
                Climate Data Online service.

        Returns:
            DWOStation: Parsed BOM weather station information.
        """
        # Open stations have four consecutive spaces at end of token.
        is_open = record.endswith("    ")
        record = record.strip()

        identifiers, name_state_distance = record.split(" ", 1)
        dwo_id, station_id = identifiers.split("_")

        # Discard last token which should be "away)"
        name, state, distance, _ = name_state_distance.rsplit(" ", 3)
        distance = distance[:-2].strip("()")  # Remove 'km' suffix and brackets

        return DWOStation(
            dwo_id=int(dwo_id),
            station_id=int(station_id),
            name=name,
            state=state,
            distance_km=float(distance),
            is_open=is_open,
        )


class WeatherObservationsClient(object):
    """Client for finding stations and retrieving BOM daily weather observations."""
    __NCC_OBS_CODE = 201
    """National Climate Centre observation code for daily weather observation"""

    def __init__(self):
        self._station = None  # type: DWOStation

    @property
    def station(self):
        # type: (...) -> DWOStation|None
        """The station used for daily weather observations."""
        return self._station

    @classmethod
    def find_nearest_stations(
        cls,
        location,  # type: Location|str|tuple[float,float]|int
        radius_km=50,  # type: float
        open_only=True,  # type: bool
        timeout=(5, 30),  # type: float|tuple
    ):  # type: (...) -> list[DWOStation]
        """Find stations with daily weather observations near a location.

        Args:
            location (Coordinates | Location | str | int): Location used to search
                for nearby stations. A string is interpreted as a location name,
                a ``(latitude, longitude)`` tuple as geographic coordinates, and
                an integer as a BOM station identifier.
            radius_km (float, optional): Search radius in kilometres. Defaults to
                ``50``.
            open_only (bool, optional): Whether to return only stations that are
                currently open. Defaults to ``True``.
            timeout (float | tuple[float, float], optional): Request timeout in
                seconds. A single value specifies the total timeout; a tuple
                specifies separate connect and read timeouts. Defaults to
                ``(5, 30)``.

        Returns:
            list[DWOStation]: A list of nearby stations providing daily
                weather observations. Returns an empty list if none is found.

        See Also:
            :meth:`StationFinder.find_matching_locations`
            :meth:`StationFinder.find_nearest_stations`
        """
        return StationFinder.find_nearest_stations(
            nccObsCode=cls.__NCC_OBS_CODE,
            location=location,
            radius_km=radius_km,
            open_only=open_only,
            timeout=timeout
        )

    def set_station(self, station):
        # type: (DWOStation|int) -> None
        """Set the station used for daily weather observations.

        Args:
            station (DWOStation or int): A ``DWOStation`` record or an open BOM
                station ID.

        Raises:
            ValueError: If no station is found for the given station ID.
            TypeError: If ``station`` is not a ``DWOStation`` or ``int``.
        """
        if isinstance(station, int):
            stations = self.find_nearest_stations(station)
            if not stations:
                raise ValueError("No station found for the given station id.")
            station = stations[0]
        if not isinstance(station, DWOStation):
            raise TypeError(
                "`station` must be a valid `DWOStation`.")
        self._station = station

    def load_observations(self,
                          start_date,  # type: date|datetime
                          end_date,  # type: date|datetime
                          as_single_dataframe=True,  # type: bool
                          ascending=True,  # type: bool
                          timeout=(5, 30)  # type: float|tuple[float, float]
                          ):  # type: (...) -> _pd.DataFrame|dict[str, _pd.DataFrame]
        """Load weather observations for a station over a range of dates.

        The data is stored in separate files for each month. The given dates
        are therefore expanded to cover their entire months. For example, a
        start date of 2024-03-15 will load data starting from March 1, and an
        end date of 2024-06-10 will load data through June 30.

        Note:
            BOM provides approximately 14 months of daily weather observation data
            from the current date. Older observations may not be available.

        Args:
            start_date (date or datetime): First date to load. If a datetime
                is given, only its date is used.
            end_date (date or datetime): Last date to load. If a datetime is
                given, only its date is used.
            as_single_dataframe (bool, optional): If True, combine all monthly
                data into one DataFrame. If False, return a dictionary containing
                a separate DataFrame for each successfully loaded monthly file,
                using the filename as the dictionary key. Defaults to True.
            ascending (bool, optional): Sort chronological (True) or reverse (False).
                Defaults to True.
            timeout (float, optional): Number of seconds to wait for an FTP
                operation before timing out. Defaults to 30.

        Returns:
            pandas.DataFrame: When `as_single_dataframe` is True. The
                DataFrame contains all successfully loaded observations, uses
                `Date` as its index, and has flattened column names. If no
                monthly files could be loaded, an empty DataFrame is returned.
            dict[str, pandas.DataFrame]: When `as_single_dataframe` is False.
                Each key is the filename of a successfully loaded monthly file,
                and its value is the corresponding DataFrame. Each DataFrame
                uses `Date` as its index and has flattened column names. If no
                monthly files could be loaded, an empty dictionary is returned.

        Raises:
            TypeError: If `start_date` or `end_date` is not a date or datetime.
            ValueError:
                - `station` is not set.
                - `end_date` is before `start_date`.
        """
        if self.station is None:
            raise ValueError(
                "Station must be set before performing this operation.")
        if not isinstance(start_date, _datetime.date):
            raise TypeError("`start_date` must be a `date`")
        if not isinstance(end_date, _datetime.date):
            raise TypeError("`end_date` must be a `date`")

        if isinstance(start_date, _datetime.datetime):
            start_date = start_date.date()
        if isinstance(end_date, _datetime.datetime):
            end_date = end_date.date()
        start_date = start_date.replace(day=1)
        end_date = end_date.replace(
            day=_calendar.monthrange(end_date.year, end_date.month)[1]
        )
        if end_date < start_date:
            raise ValueError(
                "`end_date` must be greater than or equal to `start_date`")

        bom_url = _URLBuilder(
            domain=_URL_BOM_CDIO.netloc,
            path="/climate/dwo/"
        )

        monthly_dataframes = {}  # type: dict[str, _pd.DataFrame]

        for current_date in _generate_montly_dates(
            start_date=start_date,
            end_date=end_date,
            end_date_behaviour="unique"
        ):
            yyyymm = current_date.strftime("%Y%m")
            filename_stem = "IDCJDW{dwo_id}.{yyyymm}".format(
                dwo_id=self.station.dwo_id,
                yyyymm=yyyymm
            )
            filename = filename_stem + ".csv"

            try:
                response = _requests.get(
                    url=bom_url.resolve(
                        "{yyyymm}/text/{filename}".format(
                            yyyymm=yyyymm,
                            filename=filename,
                        )
                    ),
                    timeout=timeout,
                )
                response.raise_for_status()
            except _requests.RequestException as err:
                logger.warning("Failed to retrieve %s: %s", filename, err)
                raise

            if response.status_code == 200:
                logger.info("Retrieved %s", filename)
                # csv_data = _io.StringIO(response.text)
                # Use BytesIO with response.content for faster C-engine parsing
                csv_data = _io.BytesIO(response.content)
                df = _pd.read_csv(csv_data,
                                  encoding="cp1252",
                                  skiprows=8,  # ! Skip some initial rows
                                  usecols=range(1, 22),
                                  skipinitialspace=True,
                                  index_col=0,
                                  parse_dates=[0],
                                  date_format="%Y-%m-%d")
                if ascending:
                    monthly_dataframes[yyyymm] = df
                else:
                    monthly_dataframes[yyyymm] = df.sort_index(
                        ascending=ascending
                    )
        if as_single_dataframe:
            if not monthly_dataframes:
                return _pd.DataFrame()

            merged_df = _pd.concat(
                monthly_dataframes.values(),
                ignore_index=False
            )
            return merged_df.sort_index(ascending=ascending)
        return monthly_dataframes
