"""Common utility and shared resources for the postprocess.sources subpackage."""

from typing import TYPE_CHECKING

__all__ = [
    "validate_decimal_degree_coordinates",
]

if TYPE_CHECKING:
    from typing import Tuple

# pylint: disable=consider-using-f-string


def validate_decimal_degree_coordinates(lat_lon):
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
        raise TypeError("Coordinates must be a tuple of (latitude, longitude)")
    if len(lat_lon) != 2:
        raise ValueError(
            "Coordinates must contain exactly 2 values: (latitude, longitude)")

    if not all(
        isinstance(value, (int, float)) and not isinstance(value, bool)
        for value in lat_lon
    ):
        raise TypeError("latitude and longitude must each be an int or float")

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
