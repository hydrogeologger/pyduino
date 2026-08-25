"""Tests for utility functions used by meteorological data sources."""

import pytest

from postprocess.sources.utils import (
    round_to_nearest_05,
)

@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0.00, 0.00),
        (0.01, 0.00),
        (0.02, 0.00),
        (0.03, 0.05),
        (0.05, 0.05),
        (0.06, 0.05),
        (0.07, 0.05),
        (0.08, 0.10),
        (1.00, 1.00),
        (1.02, 1.00),
        (1.03, 1.05),
        (1.07, 1.05),
        (1.08, 1.10),
        (-0.02, 0.00),
        (-0.03, -0.05),
        (-1.02, -1.00),
        (-1.03, -1.05),
    ],
)
def test_rounds_to_nearest_05(value, expected):
    """Round values to the nearest 0.05."""
    assert round_to_nearest_05(value) == expected
