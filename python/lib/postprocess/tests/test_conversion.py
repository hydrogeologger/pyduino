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
    per_second_to_hourly,
    hourly_to_per_second,
    per_second_to_daily,
    daily_to_per_second,
    hourly_to_daily,
    daily_to_hourly,
    kmh_to_ms,
    ms_to_kmh,
    cardinal_to_degrees,
)

# pylint: disable=missing-function-docstring


def test_temperature_conversion_and_round_trip():
    """Verify temperature conversion math and round-trip preservation."""
    assert celsius_to_kelvin(0) == pytest.approx(273.15)
    assert kelvin_to_celsius(273.15) == pytest.approx(0.0)
    assert kelvin_to_celsius(celsius_to_kelvin(25.5)) == pytest.approx(25.5)


def test_rate_conversion_and_round_trip():
    """Verify rate scaling math (second, hourly, daily) and round-trips."""
    # Second <-> Hourly
    assert per_second_to_hourly(1) == pytest.approx(3600.0)
    assert hourly_to_per_second(3600.0) == pytest.approx(1.0)
    assert hourly_to_per_second(
        per_second_to_hourly(5.0)) == pytest.approx(5.0)

    # Second <-> Daily
    assert per_second_to_daily(1) == pytest.approx(86400.0)
    assert daily_to_per_second(86400.0) == pytest.approx(1.0)
    assert daily_to_per_second(per_second_to_daily(5.0)) == pytest.approx(5.0)

    # Hourly <-> Daily
    assert hourly_to_daily(10) == pytest.approx(240.0)
    assert daily_to_hourly(240) == pytest.approx(10.0)
    assert daily_to_hourly(hourly_to_daily(12.5)) == pytest.approx(12.5)


def test_speed_conversion_and_round_trip():
    """Verify speed unit conversion math and round-trip preservation."""
    assert kmh_to_ms(36.0) == pytest.approx(10.0)
    assert ms_to_kmh(10.0) == pytest.approx(36.0)
    assert ms_to_kmh(kmh_to_ms(72.5)) == pytest.approx(72.5)


@pytest.mark.parametrize(
    ("input_val", "expected"),
    [
        ("N", 0.0),
        ("ne", 45.0),       # Validates case-insensitivity
        ("  SW  ", 225.0),   # Validates whitespace stripping
        ("INVALID", None),   # Out-of-bounds check
        (None, None),        # Type safety check
        (123, None),         # Type safety check
    ],
)
def test_cardinal_to_degrees_handling(input_val, expected):
    """Verify cardinal direction lookup, string normalization, and safe failure."""
    assert cardinal_to_degrees(input_val) == (
        pytest.approx(expected) if expected is not None else None
    )
