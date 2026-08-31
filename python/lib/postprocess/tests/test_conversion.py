"""
Unit tests for postprocess.conversion

Run with:

    pytest -q tests/test_conversion.py

These tests validate:
- temperature conversions
- rates conversion
"""
import pytest

from postprocess.conversion import (
    celsius_to_kelvin,
    kelvin_to_celsius,
    per_second_to_daily,
    per_second_to_hourly,
)

# pylint: disable=missing-function-docstring

# ---------------------------------------------------------------------------
# Temperature conversion
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("celsius", "expected_kelvin"),
    [
        (0, 273.15),
        (100, 373.15),
        (-40, 233.15),
        (25.5, 298.65),
    ],
)
def test_celsius_to_kelvin(celsius, expected_kelvin):
    """Test conversion from Celsius to Kelvin."""
    assert celsius_to_kelvin(celsius) == pytest.approx(expected_kelvin)


@pytest.mark.parametrize(
    ("kelvin", "expected_celsius"),
    [
        (273.15, 0),
        (373.15, 100),
        (233.15, -40),
        (298.65, 25.5),
    ],
)
def test_kelvin_to_celsius(kelvin, expected_celsius):
    """Test conversion from Kelvin to Celsius."""
    assert kelvin_to_celsius(kelvin) == pytest.approx(expected_celsius)


@pytest.mark.parametrize(
    ("per_second", "expected_hourly"),
    [
        (0, 0),
        (1, 3600),
        (0.5, 1800),
        (2.5, 9000),
    ],
)
def test_per_second_to_hourly(per_second, expected_hourly):
    """Test conversion from a per-second value to an hourly value."""
    assert per_second_to_hourly(per_second) == pytest.approx(expected_hourly)


@pytest.mark.parametrize(
    ("per_second", "expected_daily"),
    [
        (0, 0),
        (1, 86400),
        (0.5, 43200),
        (2.5, 216000),
    ],
)
def test_per_second_to_daily(per_second, expected_daily):
    """Test conversion from a per-second value to a daily value."""
    assert per_second_to_daily(per_second) == pytest.approx(expected_daily)


@pytest.mark.parametrize("celsius", [-273.15, -40, 0, 25.5, 100])
def test_celsius_kelvin_round_trip(celsius):
    """Test that Celsius to Kelvin and back preserves the original value."""
    assert kelvin_to_celsius(celsius_to_kelvin(
        celsius)) == pytest.approx(celsius)


@pytest.mark.parametrize("kelvin", [0, 233.15, 273.15, 298.15, 373.15])
def test_kelvin_celsius_round_trip(kelvin):
    """Test that Kelvin to Celsius and back preserves the original value."""
    assert celsius_to_kelvin(kelvin_to_celsius(kelvin)
                             ) == pytest.approx(kelvin)
