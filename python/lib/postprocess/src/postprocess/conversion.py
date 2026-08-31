"""Utilities for converting between common units and rates."""

__all__ = [
    # Temperature Utilities
    "celsius_to_kelvin",
    "kelvin_to_celsius",

    # Rate Utilities
    "per_second_to_hourly",
    "hourly_to_per_second",
    "per_second_to_daily",
    "daily_to_per_second",
    "hourly_to_daily",
    "daily_to_hourly",

    # Speed Utilities
    "kmh_to_ms",
    "ms_to_kmh",

    # Direction & Bearing Utilities
    "cardinal_to_degrees",

    # Constants
    "CARDINAL_ANGLE_MAP",
]

CARDINAL_ANGLE_MAP = {
    "N": 0.0,
    "NNE": 22.5,
    "NE": 45.0,
    "ENE": 67.5,
    "E": 90.0,
    "ESE": 112.5,
    "SE": 135.0,
    "SSE": 157.5,
    "S": 180.0,
    "SSW": 202.5,
    "SW": 225.0,
    "WSW": 247.5,
    "W": 270.0,
    "WNW": 292.5,
    "NW": 315.0,
    "NNW": 337.5,
}
"""dict[str, float]: A 16-point compass lookup table mapping abbreviated 
cardinal and intercardinal direction strings to their corresponding 
angle in degrees (clockwise from true North, ranging from 0.0 to 337.5).
"""


def celsius_to_kelvin(value):
    # type: (int|float) -> float
    """Convert a temperature from degrees Celsius to Kelvin.

    Args:
        value: Temperature in degrees Celsius.

    Returns:
        float: Temperature in Kelvin.
    """
    return value + 273.15


def kelvin_to_celsius(value):
    # type: (int|float) -> float
    """Convert a temperature from Kelvin to degrees Celsius.

    Args:
        value: Temperature in Kelvin.

    Returns:
        float: Temperature in degrees Celsius.
    """
    return value - 273.15


def per_second_to_hourly(value_per_second):
    # type: (int|float) -> float
    """Convert a per-second rate to an equivalent hourly rate.

    Args:
        value_per_second: Value or rate measured per second.

    Returns:
        float: Equivalent value or rate measured per hour.
    """
    return value_per_second * 3600.0


def hourly_to_per_second(value_per_hour):
    # type: (int|float) -> float
    """Convert an hourly rate to an equivalent per-second rate.

    Args:
        value_per_hour: Value or rate measured per hour.

    Returns:
        float: Equivalent value or rate measured per second.
    """
    return value_per_hour / 3600.0


def per_second_to_daily(value_per_second):
    # type: (int|float) -> float
    """Convert a per-second rate to an equivalent daily rate.

    Args:
        value_per_second: Value or rate measured per second.

    Returns:
        float: Equivalent value or rate measured per day.
    """
    return value_per_second * 86400.0


def daily_to_per_second(value_per_day):
    # type: (int|float) -> float
    """Convert a daily rate to an equivalent per-second rate.

    Args:
        value_per_day: Value or rate measured per day.

    Returns:
        float: Equivalent value or rate measured per second.
    """
    return value_per_day / 86400.0


def hourly_to_daily(value_per_hour):
    # type: (int|float) -> float
    """Convert an hourly rate to an equivalent daily rate.

    Args:
        value_per_hour: Value or rate measured per hour.

    Returns:
        float: Equivalent value or rate measured per day.
    """
    return value_per_hour * 24.0


def daily_to_hourly(value_per_day):
    # type: (int|float) -> float
    """Convert a daily rate to an equivalent hourly rate.

    Args:
        value_per_day: Value or rate measured per day.

    Returns:
        float: Equivalent value or rate measured per hour.
    """
    return value_per_day / 24.0


def kmh_to_ms(speed_kmh):
    # type: (int|float) -> float
    """Convert speed from kilometers per hour (km/h) to meters per second (m/s).

    Args:
        speed_kmh: Speed in kilometers per hour.

    Returns:
        float: Speed in meters per second.
    """
    return speed_kmh / 3.6


def ms_to_kmh(speed_ms):
    # type: (int|float) -> float
    """Convert speed from meters per second (m/s) to kilometers per hour (km/h).

    Args:
        speed_ms: Speed in meters per second.

    Returns:
        float: Speed in kilometers per hour.
    """
    return speed_ms * 3.6


def cardinal_to_degrees(direction):
    # type: (str) -> float | None
    """Convert an abbreviated cardinal direction string to its degree angle.

    Args:
        direction: The cardinal or intercardinal direction abbreviation 
            (e.g., 'N', 'NE', 'SSW').

    Returns:
        float or None: The corresponding angle in degrees, or None if the input is 
            invalid or unrecognized.
    """
    if not isinstance(direction, str):
        return None
    return CARDINAL_ANGLE_MAP.get(direction.strip().upper(), None)
