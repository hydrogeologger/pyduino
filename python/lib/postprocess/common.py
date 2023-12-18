"""This module contain simple and common methods used in postprocess package."""

__all__ = ["calculate_delta", "normalise", "normalize"]


from datetime import datetime
from typing import Iterable


def calculate_delta(values, ref, abs_=False):
    # type: (Iterable, any, bool) -> list|int|float
    """
    Calculates the difference (delta) between a single reference value from \
        a set of values.

    Args:
        values (Iterable): dataset, i.e. list containing data to be operated on.
        ref (any): Reference value for difference calculation
        abs_ (bool, optional): Flag determining result is absolute values. \
            Defaults to False.

    Returns:
        list | int | float: List of delta values.
    """
    if isinstance(values, Iterable):
        delta = []
        if all(isinstance(value, datetime) for value in values):
            for date_ in values:
                value = (date_ - ref).total_seconds()
                delta.append(value)
        else:
            delta = [(value - ref) for value in values]
    else:
        delta = values - ref

    if abs_:
        if isinstance(delta, Iterable):
            for i, val in enumerate(delta):
                delta[i] = abs(val)
        else:
            delta = abs(delta)
    return delta


def normalise(value, low, high):
    # type: (int|float, int|float, int|float) -> int|float
    """
    Normalises a value between 0 and 1.

    Args:
        value (int | float): Value to normalize.
        low (int | float): _description_
        high (int | float): _description_

    Returns:
        int | float: Value between 0 and 1.
    """
    return (value - low) / (high - low)

# Alias of normalise
normalize = normalise
