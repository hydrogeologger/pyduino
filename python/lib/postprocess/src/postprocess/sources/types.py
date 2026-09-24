"""Shared type definitions for the postprocess.sources subpackage."""

from typing import TYPE_CHECKING, NamedTuple


__all__ = [
    "Coordinates",
    "LocationMetadata",
]

if TYPE_CHECKING:
    from typing import Tuple

# pylint: disable=consider-using-f-string

# pylint: disable-next=invalid-name
Coordinates = NamedTuple("Coordinates", [
    ("latitude", float),
    ("longitude", float)
])
"""
Represents a geographic point on Earth using coordinate geometry.

Attributes:
    latitude (float): The angular distance relative to the equator.
    longitude (float): The angular distance relative to the prime meridian.
"""


class LocationMetadata(object):
    """Stores geographical metadata for general locations.

    Attributes:
        latitude (float): Latitude in decimal degrees. Positive values indicate
            north of the Equator; negative values indicate south.
        longitude (float): Longitude in decimal degrees. Positive values indicate
            east of the Prime Meridian; negative values indicate west.
        elevation (float or None): Elevation above sea level in metres.
        name (str): The common descriptor or name of the location.
    """

    def __init__(self, latitude, longitude, elevation=None, name=""):
        # type: (float, float, float|None, str) -> None
        """Initialise location metadata.

        Args:
            latitude (float): Latitude in decimal degrees. Positive values indicate
                north of the Equator; negative values indicate south.
            longitude (float): Longitude in decimal degrees. Positive values indicate
                east of the Prime Meridian; negative values indicate west.
            elevation (float, Optional): Elevation measured as metre above sea level.
                Defaults to None.
            name (str, Optional): Common descriptor or name of the location.
                Defaults to "".
        """
        self.latitude = latitude
        """Latitiude in decimal degree"""
        self.longitude = longitude
        """Longitude in decimal degree"""
        self.elevation = elevation
        """Elevation in metres above sea level"""
        self.name = name
        """Location name"""

    @property
    def coordinates(self):
        # type: (...) -> Tuple[float, float]
        """Coordinates in (latitude, longitude). (Read-only)"""
        return Coordinates(latitude=self.latitude, longitude=self.longitude)
