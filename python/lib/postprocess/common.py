"""This module contain simple and common methods used in postprocess package."""

__all__ = ["calculate_delta", "normalise"]


from datetime import datetime
from typing import Any as _Any
from typing import Iterable as _Iterable


def calculate_delta(values, ref, abs_=False):
    # type: (_Iterable, _Any, bool|None) -> list[int|float]|int|float
    """Calculates the difference (delta) between a single reference value from a set of values.

    Args:
        values (Iterable): dataset, i.e. list containing data to be operated on.
        ref (any): Reference value for difference calculation
        abs_ (bool, optional): Flag determining result is absolute values.
            Defaults to False.

    Returns:
        list[int|float]|int|float: List of delta values.
    """
    if isinstance(values, _Iterable):
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
        if isinstance(delta, _Iterable):
            for i, val in enumerate(delta):
                delta[i] = abs(val)
        else:
            delta = abs(delta)
    return delta


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
