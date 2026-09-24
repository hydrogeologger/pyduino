"""Shared type definitions for the postprocess.sources subpackage."""

from typing import (
    TYPE_CHECKING,
    NamedTuple,
)

__all__ = [
    "Coordinates",
    "LocationBase",
]

if TYPE_CHECKING:
    from typing import Tuple

# pylint: disable=consider-using-f-string

# pylint: disable-next=invalid-name
_Coordinates = NamedTuple("Coordinates", [
    ("latitude", float),
    ("longitude", float),
])


class Coordinates(_Coordinates):
    """
    Represents a geographic point on Earth using coordinate geometry.

    Attributes:
        latitude (float): The angular distance relative to the equator.
        longitude (float): The angular distance relative to the prime meridian.
    """
    __slots__ = ()

    def round(self, ndigits=4):
        # type: (int|tuple[int|None,int|None]|None) -> Coordinates
        """Round the latitude and longitude to the given number of decimal places.

        A single number applies to both coordinates. A tuple can be used to set
        different precision for latitude and longitude. Use ``None`` to leave a
        coordinate unchanged.

        Args:
            ndigits (int, tuple, or None): Number of decimal places to use.
                A tuple specifies the precision for latitude and longitude,
                respectively. Defaults to 4.

        Returns:
            Coordinates: The rounded coordinates. Returns the same instance if
                ``ndigits`` is ``None``.

        Raises:
            ValueError: If a precision is less than 1 or the tuple does not
                contain exactly two values.
        """
        if ndigits is None:
            return self

        if isinstance(ndigits, tuple):
            if len(ndigits) != 2:
                raise ValueError("ndigits must contain exactly two values.")
            ndigits_lat, ndigits_lon = ndigits
        else:
            ndigits_lat = ndigits_lon = ndigits

        if (
            (ndigits_lat is not None and ndigits_lat < 1)
            or (ndigits_lon is not None and ndigits_lon < 1)
        ):
            raise ValueError("Number of decimal places must be at least 1.")

        return Coordinates(
            latitude=(
                self.latitude
                if ndigits_lat is None
                else round(self.latitude, ndigits_lat)
            ),
            longitude=(
                self.longitude
                if ndigits_lon is None
                else round(self.longitude, ndigits_lon)
            )
        )

    @staticmethod
    def validate_decimal_degree(lat_lon):
        # type: (Tuple[float, float]) -> None
        """Check whether a value is a valid (latitude, longitude) coordinate pair.

        Latitude must be in [-90, 90] and longitude in [-180, 180].

        Args:
            lat_lon (tuple[float, float]): A coordinate pair (latitude, longitude)
                in decimal degrees, where both values are numeric.

        Raises:
            TypeError: If ``lat_lon`` is not a tuple or either coordinate is not an
                integer or float.
            ValueError: If ``lat_lon`` does not contain exactly two values or either
                coordinate is outside its valid range.
        """
        if not isinstance(lat_lon, tuple):
            raise TypeError(
                "Coordinates must be a tuple of (latitude, longitude)")
        if len(lat_lon) != 2:
            raise ValueError(
                "Coordinates must contain exactly 2 values: (latitude, longitude)")

        if not all(
            isinstance(value, (int, float)) and not isinstance(value, bool)
            for value in lat_lon
        ):
            raise TypeError(
                "latitude and longitude must each be an int or float")

        lat, lon = lat_lon
        # pylint: disable-next=superfluous-parens
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise ValueError(
                "Invalid coordinates (lat[{lat}], lon[{lon}]); "
                "latitude must be in [-90, 90] "
                "and longitude in [-180, 180].".format(
                    lat=lat,
                    lon=lon,
                )
            )


class LocationBase(object):
    """Stores geographical metadata for general locations.

    Attributes:
        latitude (float): Latitude in decimal degrees. Positive values indicate
            north of the Equator; negative values indicate south.
        longitude (float): Longitude in decimal degrees. Positive values indicate
            east of the Prime Meridian; negative values indicate west.
        elevation_m (float or None): Elevation above sea level in metres.
        name (str): The common descriptor or name of the location.
    """

    def __init__(self, latitude, longitude, elevation_m=None, name=""):
        # type: (float, float, float|None, str) -> None
        """Initialise location metadata.

        Args:
            latitude (float): Latitude in decimal degrees. Positive values indicate
                north of the Equator; negative values indicate south.
            longitude (float): Longitude in decimal degrees. Positive values indicate
                east of the Prime Meridian; negative values indicate west.
            elevation_m (float, Optional): Elevation measured as metre above sea level.
                Defaults to None.
            name (str, Optional): Common descriptor or name of the location.
                Defaults to "".
        """
        self.latitude = latitude
        """Latitiude in decimal degree"""
        self.longitude = longitude
        """Longitude in decimal degree"""
        self.elevation_m = elevation_m
        """Elevation in metres above sea level"""
        self.name = name
        """Location name"""

    def __repr__(self):
        values = ", ".join(
            "{}={!r}".format(key, value)
            for key, value in vars(self).items()
        )
        return "{}({})".format(type(self).__name__, values)

    def __str__(self):
        return self.__repr__()

    @property
    def coordinates(self):
        # type: (...) -> Tuple[float, float]
        """Coordinates in (latitude, longitude). (Read-only)"""
        return Coordinates(latitude=self.latitude, longitude=self.longitude)
