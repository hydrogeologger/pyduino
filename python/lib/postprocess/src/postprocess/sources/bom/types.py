"""Shared type definitions for the postprocess.sources.bom subpackage.

References:
- https://www.bom.gov.au/climate/data/lists_by_element/stations.txt
"""

__all__ = [
    "BOMStationRecord",
    "BOMStationBase",
]

from typing import (
    NamedTuple,
    Optional,
)

from ..types import LocationBase

BOMStationRecord = NamedTuple(
    "BOMStationRecord", [
        ("station_id", int),
        ("region", str),
        ("name", str),
        ("start_date", str),
        ("end_date", str),
        ("latitude", float),
        ("longitude", float),
        ("source", str),
        ("state", str),
        ("elevation_m", Optional[float]),
        ("barometer_height_m", Optional[float]),
        ("wmo_id", Optional[int]),
    ],
)
"""Bureau of Meteorology station record.

Represents a station listed in the Bureau of Meteorology's station
directory.

Attributes:
    station_id (int): Bureau of Meteorology station identifier.
    region (str): Bureau of Meteorology district code associated with
        the station.
    name (str): Name of the weather station.
    start_date (str): Date on which observations began at the station,
        represented as either ``YYYY`` or ``YYYYMMDD``.
    end_date (str): Date on which observations ended at the station,
        represented as either ``YYYY`` or ``YYYYMMDD``. May contain the
        BOM value indicating that observations are ongoing.
    latitude (float): Station latitude in decimal degrees.
    longitude (float): Station longitude in decimal degrees.
    source (str): Source or method used to determine the station's
        location.
    state (str): Australian state or territory abbreviation where the
        station is located.
    elevation_m (Optional[float]): Station elevation in metres, or
        ``None`` if unavailable.
    barometer_height_m (Optional[float]): Height of the barometer above
        ground level in metres, or ``None`` if unavailable.
    wmo_id (Optional[int]): World Meteorological Organization station
        identifier, or ``None`` if unavailable.
"""


class BOMStationBase(LocationBase):
    """Base Bureau of Meteorology Station Metadata.

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
        state (str): Australian state or territory abbreviation where
            the station is located.
        elevation_m (float or None): Elevation of station,
            measured as metres above sea level.
            Inherited from :class:`LocationBase`.
        coordinates (tuple): Coordinates in (latitude, longitude).
            Inherited from :class:`LocationBase`.
    """

    def __init__(self, station_id, name, latitude, longitude, state, elevation_m=None):
        # type: (int|str, str, float, float, str, float|None) -> None
        """Constructor for BOM station info.

        Args:
            station_id (int or str): Bureau of Meteorology station identifier number
            name (str): Name of the station.
            latitude (float): Latitude of the station in decimal degrees,
                referenced to the GDA94 (Geocentric Datum of Australia 1994)
                coordinate reference system.
            longitude (float): Longitude of the station in decimal degrees,
                referenced to the GDA94 (Geocentric Datum of Australia 1994)
                coordinate reference system.
            state (str): Australian state or territory abbreviation where
                the station is located.
            elevation_m (float, optional): Elevation of station,
                measured as metres above sea level.

        """
        super(BOMStationBase, self).__init__(latitude=latitude,
                                             longitude=longitude,
                                             elevation_m=elevation_m,
                                             name=name)
        self.station_id = station_id
        """Station ID number"""
        self.state = state
        """Australian state or territory abbreviation where the station is located."""
