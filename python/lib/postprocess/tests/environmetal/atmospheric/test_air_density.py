"""Tests for atmospheric air-density calculations."""

import pytest

from postprocess.environmental.atmospheric import (
    celsius_to_kelvin,
    dry_air_density,
    partial_vapor_pressure,
    total_air_density,
)


# pylint: disable=missing-function-docstring


def test_dry_air_density_at_standard_conditions():
    density = dry_air_density(
        T=20.0,
        Pa=101325.0,
    )

    expected = 101325.0 / (287.05 * 293.15)

    assert density == pytest.approx(expected, rel=1e-6)


def test_dry_air_density_changes_with_pressure():
    density_standard = dry_air_density(20.0, 101325.0)
    density_high = dry_air_density(20.0, 110000.0)

    assert density_high > density_standard


def test_dry_air_density_changes_with_temperature():
    density_cold = dry_air_density(10.0, 101325.0)
    density_warm = dry_air_density(30.0, 101325.0)

    assert density_cold > density_warm


def test_total_air_density_is_close_to_dry_density_at_zero_rh():
    dry = dry_air_density(T=20.0, Pa=101325.0)
    moist = total_air_density(RH=0.0, T=20.0, Pa=101325.0)

    assert moist == pytest.approx(dry, rel=1e-6)


def test_total_air_density_is_less_than_dry_air_density_at_high_humidity():
    dry = dry_air_density(T=20.0, Pa=101325.0)
    moist = total_air_density(RH=100.0, T=20.0, Pa=101325.0)

    assert moist < dry


def test_total_air_density_humidity_correction():
    temperature = 20.0
    relative_humidity = 50.0
    pressure = 101325.0

    vapor_pressure = partial_vapor_pressure(
        temperature,
        relative_humidity,
    )

    R_d = 287.05
    R_v = 461.5
    temperature_kelvin = celsius_to_kelvin(temperature)

    expected = (
        pressure / (R_d * temperature_kelvin)
        * (
            1.0
            - (vapor_pressure / pressure)
            * (1.0 - R_d / R_v)
        )
    )

    actual = total_air_density(
        relative_humidity,
        temperature,
        pressure,
    )

    assert actual == pytest.approx(expected, rel=1e-5)


@pytest.mark.parametrize("pressure", [0.0, -1.0, -101325.0])
def test_total_air_density_rejects_invalid_pressure(pressure):
    with pytest.raises(ValueError, match="Atmospheric pressure"):
        total_air_density(
            RH=50.0,
            T=20.0,
            Pa=pressure,
        )
