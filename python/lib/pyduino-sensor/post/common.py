"""This module contain simple and common methods used in sensor post process package."""


def normalise(value, min_, max_):
    # type: (int|float, int|float, int|float) -> int|float
    """Map a value to between 0 and 1.

    Args:
        value (int | float): Value to normalize.
        min_ (int | float): Lower limit mapped to 0.
        max_ (int | float): Upper limit to be mapped to 1.

    Returns:
        float: Value between 0 and 1.
    """
    return (value - min_) / (max_ - min_)
