"""Utilities for converting between common units and rates."""


def celsius_to_kelvin(value):
    # type: (int|float) -> float
    """Convert a temperature from degrees Celsius to Kelvin.

    Args:
        value: Temperature in degrees Celsius.

    Returns:
        Temperature in Kelvin.
    """
    return value + 273.15


def kelvin_to_celsius(value):
    # type: (int|float) -> float
    """Convert a temperature from Kelvin to degrees Celsius.

    Args:
        value: Temperature in Kelvin.

    Returns:
        Temperature in degrees Celsius.
    """
    return value - 273.15


def per_second_to_hourly(value_per_second):
    # type: (int|float) -> float
    """Convert a per-second rate to an equivalent hourly rate.

    This conversion assumes the input represents a rate accumulated
    continuously over time.

    Args:
        value_per_second: Value or rate measured per second.

    Returns:
        Equivalent value or rate measured per hour.
    """
    return value_per_second * 3600.0


def per_second_to_daily(value_per_second):
    # type: (int|float) -> float
    """Convert a per-second rate to an equivalent daily rate.

    This conversion assumes the input represents a rate accumulated
    continuously over time.

    Args:
        value_per_second: Value or rate measured per second.

    Returns:
        Equivalent value or rate measured per day.
    """
    return value_per_second * 86400.0
