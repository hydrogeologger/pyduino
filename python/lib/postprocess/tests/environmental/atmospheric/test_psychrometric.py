"""Tests for atmospheric psychrometric calculations."""

import pytest

from postprocess.environmental.atmospheric import (
    psychrometric_constant,
    specific_heat_capacity_air,
)


# pylint: disable=missing-function-docstring


def test_psychrometric_constant_at_standard_conditions():
    gamma = psychrometric_constant(
        P=101325.0,
        temp=20.0,
    )

    assert gamma == pytest.approx(67.0, rel=0.03)


def test_psychrometric_constant_increases_with_pressure():
    low_pressure = psychrometric_constant(90000.0, 20.0)
    high_pressure = psychrometric_constant(105000.0, 20.0)

    assert high_pressure > low_pressure


def test_air_specific_heat_capacity_is_positive():
    for temperature in [-20.0, 0.0, 20.0, 40.0]:
        cp = specific_heat_capacity_air(T=temperature)

        assert cp > 0.0


def test_air_specific_heat_capacity_dry_air_temperature_dependence():
    cp_cold = specific_heat_capacity_air(T=0.0)
    cp_warm = specific_heat_capacity_air(T=40.0)

    assert cp_warm > cp_cold


@pytest.mark.parametrize(
    ("temperature", "expected"),
    [
        (0.0, 1002.5),
        (25.0, 1005.0),
        (40.0, 1006.5),
    ],
)
def test_air_specific_heat_capacity_dry_air(temperature, expected):
    cp = specific_heat_capacity_air(T=temperature)

    assert cp == pytest.approx(expected)


def test_air_specific_heat_capacity_zero_relative_humidity_equals_dry_air():
    cp_none = specific_heat_capacity_air(
        T=20.0,
        RH=None,
    )

    cp_zero = specific_heat_capacity_air(
        T=20.0,
        RH=0.0,
    )

    assert cp_zero == pytest.approx(cp_none)


def test_air_specific_heat_capacity_increases_with_relative_humidity():
    cp_dry = specific_heat_capacity_air(T=20.0, RH=0.0)
    cp_moist = specific_heat_capacity_air(T=20.0, RH=50.0)
    cp_humid = specific_heat_capacity_air(T=20.0, RH=90.0)

    assert cp_moist > cp_dry
    assert cp_humid > cp_moist


def test_air_specific_heat_capacity_uses_atmospheric_pressure():
    cp_standard = specific_heat_capacity_air(
        T=20.0,
        RH=50.0,
        P=101325.0,
    )

    cp_lower_pressure = specific_heat_capacity_air(
        T=20.0,
        RH=50.0,
        P=90000.0,
    )

    assert cp_lower_pressure > cp_standard


@pytest.mark.parametrize(
    "relative_humidity",
    [-1.0, 100.1, 150.0],
)
def test_air_specific_heat_capacity_rejects_invalid_relative_humidity(
    relative_humidity,
):
    with pytest.raises(ValueError, match="RH must be between"):
        specific_heat_capacity_air(
            T=20.0,
            RH=relative_humidity,
        )


def test_air_specific_heat_capacity_rejects_vapor_pressure_above_atmospheric_pressure():
    with pytest.raises(
        ValueError,
        match="Actual vapor pressure cannot exceed",
    ):
        specific_heat_capacity_air(
            T=100.0,
            RH=100.0,
            P=1000.0,
        )


@pytest.mark.parametrize(
    "pressure",
    [0.0, -1.0, -101325.0],
)
def test_air_specific_heat_capacity_rejects_invalid_pressure(pressure):
    with pytest.raises(ValueError, match="Atmospheric pressure"):
        specific_heat_capacity_air(
            T=20.0,
            RH=50.0,
            P=pressure,
        )
