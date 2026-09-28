"""Access historical climate and weather observation data from the
Australian Bureau of Meteorology's anonymous FTP service.

This is an unofficial, community-developed interface and is not
affiliated with, endorsed by, or officially supported by the Bureau
of Meteorology.

Use of Bureau of Meteorology data is subject to the applicable
copyright, licensing, and terms-of-use requirements. See the
Bureau's copyright notice for details:

https://www.bom.gov.au/copyright

References:
- https://www.bom.gov.au/catalogue/anon-ftp.shtml
- ftp://ftp.bom.gov.au/anon2/home/ncc/metadata/sitelists/stations.zip
- https://www.bom.gov.au/climate/cdo/about/site-num.shtml
"""

__all__ = [
    # Constants
    "BOM_FTP_DOMAIN",
    "BOM_FTP_ANON_GEN_DIR",
    "BOM_FTP_ANON2_HOME_DIR",

    # Clients & Utilities
    "DailyWeatherObservations",

    # Records & Data Structures
    "BOMStationRecord",
    "BOMStationBase",
    "BOMStationDistanceRecord",

    # Functions
    "slugify_bom_ftp_segment",
]

import calendar as _calendar
import datetime as _datetime
import ftplib as _ftplib
import io as _io
import logging as _logging
import posixpath as _posixpath
import re as _re
from typing import (
    TYPE_CHECKING,
    NamedTuple,
)

import pandas as _pd

from ...pandas_utils import flatten_column_headers as _flatten_column_headers
from ..types import Coordinates
from ..utils import (
    generate_monthly_dates as _generate_montly_dates,
    haversine_distance as _haversine_distance,
)
from .types import (
    BOMStationBase,
    BOMStationRecord,
)

if TYPE_CHECKING:
    from datetime import (
        date,
        datetime,
    )
    from typing import Tuple

# pylint: disable=consider-using-f-string

logger = _logging.getLogger(__name__)

BOMStationDistanceRecord = NamedTuple(
    "BOMStationDistanceRecord", [
        ("distance_km", float),
        ("station", BOMStationRecord),
    ],
)

BOM_FTP_DOMAIN = "ftp.bom.gov.au"
BOM_FTP_ANON_GEN_DIR = "/anon/gen"
BOM_FTP_ANON2_HOME_DIR = "/anon2/home"


class DailyWeatherObservations:
    """Client for accessing daily weather observations via FTP.

    Provides access to station information and historical observation data,
    including current daily weather observations, published through the
    Bureau of Meteorology's anonymous FTP service.
    """

    _BASE_DIR = _posixpath.join(BOM_FTP_ANON_GEN_DIR,
                                "clim_data/IDCKWCDEA0/tables",
                                )

    stations_list = []  # type: list[BOMStationRecord]
    stations_by_id = {}
    stations_by_name = {}
    stations_by_coordinates = {}

    def __init__(self):
        self._station = None  # type: BOMStationBase|None

    @property
    def station(self):
        # type: (...) -> BOMStationBase|None
        """The station used for daily weather observations."""
        return self._station

    @classmethod
    def fetch_stations_list(cls, timeout=30):
        # type: (float) -> DailyWeatherObservations
        """Fetch the list of weather stations from the BOM FTP server.

        The downloaded station information is used to replace the existing
        station cache and its lookup dictionaries. The cache is only updated
        after the station list has been successfully downloaded and parsed.

        Args:
            timeout (float, optional): Number of seconds to wait for an FTP
                operation before timing out. Defaults to 30.

        Returns:
            DailyWeatherObservations: A new instance of the class after the
                station cache has been refreshed.

        Raises:
            RuntimeError: If the BOM FTP server does not allow the station
                list to be retrieved.
            ValueError: If a station record contains invalid data.
        """
        ftp = _ftplib.FTP(host=BOM_FTP_DOMAIN, timeout=timeout)
        try:
            ftp.login()  # Anonymous access
            ftp.cwd(cls._BASE_DIR)

            _stations_list = []

            with _io.BytesIO() as file_buffer:
                # Download data into buffer
                ftp.retrbinary("RETR stations_db.txt", file_buffer.write)
                file_buffer.seek(0)

                with _io.TextIOWrapper(
                    file_buffer,
                    encoding="utf-8"
                ) as text_stream:
                    for line in text_stream:
                        if not line.strip():  # Skip empty lines if any exist
                            continue
                        record = BOMStationRecord(
                            station_id=int(line[0:6]),
                            state=line[8:11].rstrip(),
                            region=line[12:18].rstrip(),
                            name=line[18:59].rstrip(),
                            # Extract the complete 17-character date interval block
                            # Example Active: "19400101.."
                            # Example Closed: "19400101.20261231"
                            start_date=line[59:67],
                            end_date="",
                            latitude=float(line[75:83]),
                            longitude=float(line[84:92]),
                            source="",
                            elevation_m=None,
                            barometer_height_m=None,
                            wmo_id=None,
                        )
                        _stations_list.append(record)
        except _ftplib.error_perm as err:
            raise RuntimeError(
                "Unable to retrieve the BOM station list"
            ) from err
        finally:
            try:
                ftp.quit()
            except Exception:  # pylint: disable=broad-exception-caught
                ftp.close()

        # Replace and update lookup cache
        cls.stations_list[:] = _stations_list

        # Update cached lookup dictionary
        cls.stations_by_id.clear()
        cls.stations_by_id.update(
            (station.station_id, station)
            for station in cls.stations_list
        )
        cls.stations_by_name.clear()
        cls.stations_by_name.update(
            (station.name.lower(), station)
            for station in cls.stations_list
        )
        cls.stations_by_coordinates.clear()
        cls.stations_by_coordinates.update(
            (Coordinates(
                latitude=station.latitude,
                longitude=station.longitude
            ).round(4), station)
            for station in cls.stations_list
        )
        return cls()

    @classmethod
    def load_observations_for_station(
        cls,
        station_name,  # type: str
        state,  # type: str
        start_date,  # type: date|datetime
        end_date,  # type: date|datetime
        as_single_dataframe=True,  # type: bool
        ascending=True,  # type: bool
        timeout=30  # type:float|None
    ):  # type (...) -> _pd.DataFrame|dict[_pd.DataFrame]
        """Load weather observations for a station over a range of dates.

        The data is stored in separate files for each month. The given dates
        are therefore expanded to cover their entire months. For example, a
        start date of 2024-03-15 will load data starting from March 1, and an
        end date of 2024-06-10 will load data through June 30.

        Args:
            station_name (str): Name of the weather station.
            state (str): Australian state or territory abbreviation where the
                station is located.
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
            ValueError: If `station_name` or `state` is empty, or if
                `end_date` is before `start_date`.
        """
        if not isinstance(start_date, _datetime.date):
            raise TypeError("`start_date` must be a `date`")
        if not isinstance(end_date, _datetime.date):
            raise TypeError("`end_date` must be a `date`")
        if not station_name:
            raise ValueError("`station_name` must not be empty")
        if not state:
            raise ValueError("`state` must not be empty")

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

        station_name_slug = slugify_bom_ftp_segment(station_name)
        dir_path = _posixpath.join(
            cls._BASE_DIR,
            slugify_bom_ftp_segment(state),
            station_name_slug,
        )

        monthly_dataframes = {}  # type: dict[str, _pd.DataFrame]
        ftp = _ftplib.FTP(host=BOM_FTP_DOMAIN, timeout=timeout)
        try:
            ftp.login()  # Anonymous access
            ftp.cwd(dir_path)

            for current_date in _generate_montly_dates(
                start_date=start_date,
                end_date=end_date,
                end_date_behaviour="unique"
            ):
                yyyymm = current_date.strftime("%Y%m")
                filename_stem = "{name}-{yyyymm}".format(
                    name=station_name_slug,
                    yyyymm=yyyymm
                )
                filename = filename_stem + ".csv"

                try:
                    with _io.BytesIO() as flo:
                        ftp.retrbinary(
                            "RETR {filename}".format(filename=filename),
                            flo.write
                        )
                        flo.seek(0)
                        df = _pd.read_csv(
                            flo,
                            encoding="cp1252",
                            #  encoding="iso-8859-1",
                            skiprows=9,  # Skip the initial rows
                            # Uses the rows index after skipping as headers
                            header=[0, 1, 2, 3],
                            index_col=1,  # Designate column index as row index
                            #  usecols=range(1,22),
                            skipinitialspace=True,
                            parse_dates=[1],
                            date_format="%d/%m/%Y",
                        )

                        # Remove last row, contains subtotals row
                        df.drop(df.index[-1], inplace=True)
                        # Flatten column headers
                        if not as_single_dataframe:
                            df.columns = _flatten_column_headers(df.columns)
                            df.index.name = "Date"
                            if not ascending:
                                df.sort_index(ascending=ascending)
                except _ftplib.error_perm as err:
                    logger.warning(
                        "Failed to retrieve %s: %s. Skipping.",
                        filename, err
                    )
                else:
                    monthly_dataframes[filename_stem] = df
                    logger.info("Retrieved %s", filename)
        finally:
            try:
                ftp.quit()
            except Exception:  # pylint: disable=broad-exception-caught
                ftp.close()

        if as_single_dataframe:
            if not monthly_dataframes:
                return _pd.DataFrame()
            merged_df = _pd.concat(
                monthly_dataframes.values(),
                ignore_index=False
            )
            merged_df.columns = _flatten_column_headers(merged_df.columns)
            merged_df.index.name = "Date"
            return merged_df.sort_index(ascending=ascending)
        return monthly_dataframes

    def find_nearby_stations(self, location, radius_km=50):
        # type: (str|int|Tuple[float,float], float) -> list[BOMStationDistanceRecord]
        """Find weather stations within a given distance of a location.

        The location can be specified using a station name, station ID, or a
        pair of latitude and longitude coordinates. The returned stations are
        sorted from nearest to farthest.

        Args:
            location (str, int, tuple[float, float]): Reference location used
                to calculate distances. A string is interpreted as a station
                name, an integer as a station ID, and a tuple as decimal-degree
                coordinates in the form ``(latitude, longitude)``.
            radius_km (float, optional): Maximum distance from the reference
                location, in kilometres. Stations farther away are not
                included. Defaults to 50.

        Returns:
            list[BOMStationDistanceRecord]: A list of stations within
                ``radius_km`` of the reference location, sorted by distance
                from nearest to farthest. Returns an empty list if no stations
                are within the specified radius or the reference location
                cannot be resolved.

        Raises:
            ValueError: If the coordinates are invalid or the reference
                location cannot be resolved to a station.
        """
        reference_coordinates = None

        if isinstance(location, tuple):
            Coordinates.validate_decimal_degree(location)
            reference_coordinates = location
        else:
            ref_station = self.resolve_station(
                location=location,
                set_station=False
            )
            if isinstance(ref_station, BOMStationBase):
                reference_coordinates = ref_station.coordinates
            else:
                raise ValueError(
                    "Unable to resolve reference station from location: {!r}".format(
                        location)
                )

        if reference_coordinates is None:
            return []

        # Calculate distance and filter stations
        filtered_stations = []  # type: list[BOMStationDistanceRecord]
        for station in self.stations_list:
            distance_km = _haversine_distance(reference_coordinates,
                                              (station.latitude, station.longitude))
            distance_km = round(distance_km, 3)
            if distance_km <= radius_km:
                filtered_stations.append(
                    BOMStationDistanceRecord(
                        distance_km=distance_km,
                        station=station
                    )
                )
        filtered_stations.sort(key=lambda record: record.distance_km)
        return filtered_stations

    def set_station(self, station):
        # type: (BOMStationBase|int) -> None
        """Set the station used for daily weather observations.

        Args:
            station (BOMStationBase or int): A ``BOMStationBase`` record or an open BOM
                station ID.

        Raises:
            ValueError: If no station is found for the given station ID.
            TypeError: If ``station`` is not a ``BOMStationBase`` or ``int``.
        """
        if isinstance(station, int):
            station = self.resolve_station(
                location=station,
                set_station=False
            )
            if station is None:
                raise ValueError("No station found for the given station id.")
        if not isinstance(station, BOMStationBase):
            raise TypeError(
                "`station` must be a valid `BOMStationBase`.")
        self._station = station

    def resolve_station(self, location, set_station=False):
        # type: (str|int|Tuple[float,float], bool) -> BOMStationBase|None
        """Resolve a BOM weather station from a station ID, name, or coordinates.

        Args:
            location (str, int, tuple): Station ID, station name, or a
                ``(latitude, longitude)`` tuple. Numeric strings are treated
                as station IDs.
            set_station (bool): If ``True``, set the resolved station as
                the current station. Defaults to ``False``.

        Returns:
            BOMStationBase or None: The resolved station, or ``None`` if no
                matching station is found.
        """

        found_station_record = None  # type: BOMStationRecord|None

        if isinstance(location, str):
            if location.isdigit():
                found_station_record = self.stations_by_id.get(int(location))
            else:
                found_station_record = self.stations_by_name.get(
                    location.lower())
        elif isinstance(location, int):
            found_station_record = self.stations_by_id.get(location)
        elif isinstance(location, tuple):
            Coordinates.validate_decimal_degree(location)
            lat, lon = location
            if lat is None or lon is None:
                return None

            found_station_record = self.stations_by_coordinates.get(
                Coordinates(lat, lon).round(4))
        else:
            return None

        if found_station_record is None:
            return None

        found_station = BOMStationBase(
            station_id=found_station_record.station_id,
            name=found_station_record.name,
            latitude=found_station_record.latitude,
            longitude=found_station_record.longitude,
            state=found_station_record.state,
        )

        if set_station:
            self._station = found_station
        return found_station

    def load_observations(self,
                          start_date,  # type: date|datetime
                          end_date,  # type: date|datetime
                          as_single_dataframe=True,  # type: bool
                          ascending=True,  # type: bool
                          timeout=30  # type: float
                          ):  # type: (...) -> _pd.DataFrame|dict[_pd.DataFrame]
        """Load weather observations for a station over a range of dates.

            The data is stored in separate files for each month. The given dates
            are therefore expanded to cover their entire months. For example, a
            start date of 2024-03-15 will load data starting from March 1, and an
            end date of 2024-06-10 will load data through June 30.

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
                ValueError: If no station has been set (i.e., `self.station` is
                    `None`), or if `end_date` is before `start_date`.
                TypeError: If `start_date` or `end_date` is not a `date` or
                    `datetime` object.

            See Also:
                :meth:`load_observations_for_station`
            """
        if self.station is None:
            raise ValueError(
                "Station must be set before performing this operation."
            )

        return self.load_observations_for_station(
            station_name=self.station.name,
            state=self.station.state,
            start_date=start_date,
            end_date=end_date,
            as_single_dataframe=as_single_dataframe,
            ascending=ascending,
            timeout=timeout,
        )


def slugify_bom_ftp_segment(text_segment):
    # type: (str) -> str
    """Converts a raw BOM data string into a lowercase, filesystem-safe slug.

    Maps spaces directly to underscores and strips illegal punctuation while
    explicitly preserving structural characters (hyphens, parentheses, and 
    consecutive spacing) required by the BOM FTP server.

    Args:
        text_segment: The raw station name, state, or text block to process.

    Returns:
        The normalized, lowercase slug string.

    Examples:
        >>> slugify_bom_ftp_segment("Holsworthy - Defence")
        'holsworthy_-_defence'
        >>> slugify_bom_ftp_segment("TAS ")
        'tas_'
    """
    # 1. Standardise casing
    slug = text_segment.lower()

    # 2. Strip out illegal symbols
    slug = slug.replace(".", "")

    # 3. Map spaces to underscores to preserve structural database padding
    slug = slug.replace(" ", "_")

    # 3. Replace remaining illegal symbols
    slug = _re.sub(r"[^a-z0-9_()\-]", "_", slug)

    return slug
