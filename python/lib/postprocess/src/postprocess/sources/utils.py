"""Common utility and shared resources for the postprocess.sources subpackage."""

from math import (
    atan2 as _atan2,
    cos as _cos,
    radians as _radians,
    sin as _sin,
    sqrt as _sqrt,
)
from typing import TYPE_CHECKING

__all__ = [
    "validate_decimal_degree_coordinates",
    "haversine_distance",
    "round_to_nearest_05",
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


def haversine_distance(coord1, coord2, radius=6371.0):
    # type: (Tuple[float, float], Tuple[float, float], float) -> float
    """Computes great-circle distance between two geographic coordinates.

    Applies the Haversine formula to find the shortest spherical distance between
    points. Converts inputs from decimal degrees to radians, validates bounds, 
    and scales the angular separation by the specified planetary radius.

    Args:
        coord1 (tuple): Starting point as (latitude, longitude) coordinate pair in decimal degrees.
        coord2 (tuple): Ending point as (latitude, longitude) coordinate pair in decimal degrees.
        radius (float, Optional): Sphere radius. Defaults to 6371.0 (Earth kilometers).

    Returns:
        float: Great-circle distance in the same unit as radius.

    TypeError: Coordinates is not a tuple or either coordinate is not an
        integer or float.
    ValueError: Coordinates does not contain exactly two values or either
        coordinate is outside its valid range latitudes exceed [-90, 90] or
        longitudes exceed [-180, 180].
    """
    # Validate coordinates
    validate_decimal_degree_coordinates(coord1)
    validate_decimal_degree_coordinates(coord2)

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Convert degrees to radians
    lat1 = _radians(lat1)
    lon1 = _radians(lon1)
    lat2 = _radians(lat2)
    lon2 = _radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        _sin(dlat / 2) ** 2
        + _cos(lat1) * _cos(lat2) * _sin(dlon / 2) ** 2
    )

    # pylint: disable-next=invalid-name
    if radius is None:
        radius = 6371.0  # Earth radius in kilometres.
    c = 2 * _atan2(_sqrt(a), _sqrt(1 - a))
    return radius * c


def round_to_nearest_05(x):
    """Round value to nearest 0.05."""
    return round(x * 20) / 20
