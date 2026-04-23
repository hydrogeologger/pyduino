"""Tests for atmospheric humidity calculations."""

import pytest

from postprocess.environmental.atmospheric import (
    calculate_specific_humidity,
    actual_vapor_pressure,
    saturation_vapor_pressure_tetens,
    vapor_pressure_deficit,
)


# pylint: disable=missing-function-docstring


def test_partial_vapor_pressure_rejects_invalid_relative_humidity():
    with pytest.raises(ValueError):
        actual_vapor_pressure(20.0, -1.0)

    with pytest.raises(ValueError):
        actual_vapor_pressure(20.0, 101.0)


@pytest.mark.parametrize(
    "temperature,rh,expected",
    [
        (20.0, 0.0, 0.0),
        (20.0, 50.0, 1169.0),
        (20.0, 100.0, 2338.0),
    ],
)
def test_partial_vapor_pressure(temperature, rh, expected):
    pressure = actual_vapor_pressure(temperature, rh)

    assert pressure == pytest.approx(expected, rel=0.02)


def test_partial_vapor_pressure_scales_with_relative_humidity():
    saturation = saturation_vapor_pressure_tetens(20.0)

    half = actual_vapor_pressure(20.0, 50.0)
    full = actual_vapor_pressure(20.0, 100.0)

    assert half == pytest.approx(saturation * 0.5, rel=1e-6)
    assert full == pytest.approx(saturation, rel=1e-6)


def test_vapor_pressure_deficit_at_saturation():
    vpd = vapor_pressure_deficit(
        temperature=20.0,
        RH=100.0,
    )

    assert vpd == pytest.approx(0.0, abs=1e-6)


def test_vapor_pressure_deficit_at_fifty_percent_rh():
    vpd = vapor_pressure_deficit(
        temperature=20.0,
        RH=50.0,
    )

    assert vpd == pytest.approx(1169.0, rel=0.02)


def test_calculate_specific_humidity_at_zero_relative_humidity():
    result = calculate_specific_humidity(
        RH=0.0,
        T=20.0,
        P=101325.0,
    )

    assert result == pytest.approx(0.0)


def test_calculate_specific_humidity_is_positive_at_nonzero_humidity():
    result = calculate_specific_humidity(
        RH=50.0,
        T=20.0,
        P=101325.0,
    )

    assert result > 0.0


def test_calculate_specific_humidity_increases_with_relative_humidity():
    dry = calculate_specific_humidity(
        RH=20.0,
        T=20.0,
        P=101325.0,
    )

    humid = calculate_specific_humidity(
        RH=80.0,
        T=20.0,
        P=101325.0,
    )

    assert humid > dry


@pytest.mark.parametrize("pressure", [0.0, -1.0])
def test_calculate_specific_humidity_rejects_invalid_pressure(pressure):
    with pytest.raises(ValueError, match="Atmospheric pressure"):
        calculate_specific_humidity(
            RH=50.0,
            T=20.0,
            P=pressure,
        )
