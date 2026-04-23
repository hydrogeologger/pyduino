"""Common utility and shared resources for the postprocess.sources subpackage."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple

# pylint: disable=consider-using-f-string


class LocationMetadata(object):
    """Stores geographical metadata for general locations.

    Attributes:
        lat (float): Latitude in decimal degrees.
        lon (float): Longitude in decimal degrees.
        elevation (float or None): Elevation above sea level in metres.
        name (str): The common descriptor or name of the location.
    """

    def __init__(self, latitude, longitude, elevation=None, name=""):
        # type: (float, float, float|None, str) -> None
        """Initialise location metadata.

        Args:
            latitude (float): Latitude of the station in GDA94.
            longitude: Longitude of the station in GDA94.
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
        return (self.latitude, self.longitude)


def is_valid_coordinates(lat_lon):
    # type: (Tuple[float, float]) -> bool
    """Check whether a value is a valid (latitude, longitude) coordinate pair.

    Latitude must be in [-90, 90] and longitude in [-180, 180].

    Args:
        lat_lon (tuple[float, float]): A coordinate pair (latitude, longitude)
            in decimal degrees, where both values are numeric.

    Returns:
        True if `lat_lon` contains valid coordinates.

    Raises:
        TypeError: If `lat_lon` is not a tuple or either coordinate is not an
            integer or float.
        ValueError: If `lat_lon` does not contain exactly two values or either
            coordinate is outside its valid range.
    """
    if not isinstance(lat_lon, tuple):
        raise TypeError("Coordinates must be a tuple of (latitude, longitude)")
    if len(lat_lon) != 2:
        raise ValueError(
            "Coordinates must contain exactly 2 values: (latitude, longitude)")

    lat, lon = lat_lon
    if not all(isinstance(v, (float, int)) for v in lat_lon):
        raise TypeError("latitude and longitude must each be an int or float")

    # pylint: disable-next=superfluous-parens
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise ValueError("Invalid coordinates (lat[{lat}], lon[{lon}]); "
                         "latitude must be in [-90, 90] "
                         "and longitude in [-180, 180].".format(lat=lat, lon=lon))
    return True
