"""Tests for atmospheric humidity calculations."""

import pytest

from postprocess.environmental.atmospheric import (
    calculate_specific_humidity,
    partial_vapor_pressure,
    saturation_vapor_pressure,
    soil_surface_vapor_pressure_deficit,
    vapor_pressure_deficit,
)


# pylint: disable=missing-function-docstring


def test_partial_vapor_pressure_rejects_invalid_relative_humidity():
    with pytest.raises(ValueError):
        partial_vapor_pressure(20.0, -1.0)

    with pytest.raises(ValueError):
        partial_vapor_pressure(20.0, 101.0)


@pytest.mark.parametrize(
    "temperature,rh,expected",
    [
        (20.0, 0.0, 0.0),
        (20.0, 50.0, 1169.0),
        (20.0, 100.0, 2338.0),
    ],
)
def test_partial_vapor_pressure(temperature, rh, expected):
    pressure = partial_vapor_pressure(temperature, rh)

    assert pressure == pytest.approx(expected, rel=0.02)


def test_partial_vapor_pressure_scales_with_relative_humidity():
    saturation = saturation_vapor_pressure(20.0)

    half = partial_vapor_pressure(20.0, 50.0)
    full = partial_vapor_pressure(20.0, 100.0)

    assert half == pytest.approx(saturation * 0.5, rel=1e-6)
    assert full == pytest.approx(saturation, rel=1e-6)


def test_vapor_pressure_deficit_at_saturation():
    vpd = vapor_pressure_deficit(
        T_air=20.0,
        RH=100.0,
    )

    assert vpd == pytest.approx(0.0, abs=1e-6)


def test_vapor_pressure_deficit_at_fifty_percent_rh():
    vpd = vapor_pressure_deficit(
        T_air=20.0,
        RH=50.0,
    )

    assert vpd == pytest.approx(1169.0, rel=0.02)


def test_vapor_pressure_deficit_increases_as_rh_decreases():
    vpd_80 = soil_surface_vapor_pressure_deficit(
        T_air=20.0,
        RH=80.0,
        T_surface=20.0,
    )

    vpd_50 = soil_surface_vapor_pressure_deficit(
        T_air=20.0,
        RH=50.0,
        T_surface=20.0,
    )

    vpd_20 = soil_surface_vapor_pressure_deficit(
        T_air=20.0,
        RH=20.0,
        T_surface=20.0,
    )

    assert vpd_20 > vpd_50 > vpd_80


def test_vapor_pressure_deficit_can_account_for_surface_temperature():
    vpd_cold_surface = soil_surface_vapor_pressure_deficit(
        T_surface=15.0,
        T_air=20.0,
        RH=50.0,
    )

    vpd_warm_surface = soil_surface_vapor_pressure_deficit(
        T_surface=25.0,
        T_air=20.0,
        RH=50.0,
    )

    assert vpd_warm_surface > vpd_cold_surface


def test_soil_surface_vapor_pressure_deficit_at_saturation():
    vpd = soil_surface_vapor_pressure_deficit(
        T_air=20.0,
        RH=100.0,
        T_surface=20.0,
    )

    assert vpd == pytest.approx(0.0, abs=1e-6)


def test_soil_surface_vapor_pressure_deficit_at_fifty_percent_rh():
    vpd = soil_surface_vapor_pressure_deficit(
        T_air=20.0,
        RH=50.0,
        T_surface=20.0,
    )

    expected = (
        saturation_vapor_pressure(20.0)
        - partial_vapor_pressure(20.0, 50.0)
    )

    assert vpd == pytest.approx(expected, rel=1e-6)


def test_soil_surface_vapor_pressure_deficit_defaults_surface_temperature_to_air():
    vpd = soil_surface_vapor_pressure_deficit(
        T_air=20.0,
        RH=50.0,
    )

    expected = (
        saturation_vapor_pressure(20.0)
        - partial_vapor_pressure(20.0, 50.0)
    )

    assert vpd == pytest.approx(expected, rel=1e-6)


@pytest.mark.parametrize(
    "rh",
    [0.0, 20.0, 50.0, 80.0, 100.0],
)
def test_soil_surface_vapor_pressure_deficit_decreases_with_relative_humidity(rh):
    vpd = soil_surface_vapor_pressure_deficit(
        T_air=20.0,
        RH=rh,
        T_surface=20.0,
    )

    expected = (
        saturation_vapor_pressure(20.0)
        - partial_vapor_pressure(20.0, rh)
    )

    assert vpd == pytest.approx(expected, rel=1e-6)


def test_soil_surface_vapor_pressure_deficit_increases_with_surface_temperature():
    cold_surface = soil_surface_vapor_pressure_deficit(
        T_air=20.0,
        RH=50.0,
        T_surface=15.0,
    )

    warm_surface = soil_surface_vapor_pressure_deficit(
        T_air=20.0,
        RH=50.0,
        T_surface=25.0,
    )

    assert warm_surface > cold_surface


def test_soil_surface_vapor_pressure_deficit_uses_air_temperature_for_actual_vapor_pressure():
    vpd = soil_surface_vapor_pressure_deficit(
        T_air=20.0,
        RH=50.0,
        T_surface=30.0,
    )

    expected_actual = partial_vapor_pressure(20.0, 50.0)
    expected_surface_saturation = saturation_vapor_pressure(30.0)

    expected = expected_surface_saturation - expected_actual

    assert vpd == pytest.approx(expected, rel=1e-6)


def test_soil_surface_vapor_pressure_deficit_rejects_invalid_relative_humidity():
    with pytest.raises(ValueError):
        soil_surface_vapor_pressure_deficit(
            T_air=20.0,
            RH=-1.0,
            T_surface=20.0,
        )

    with pytest.raises(ValueError):
        soil_surface_vapor_pressure_deficit(
            T_air=20.0,
            RH=101.0,
            T_surface=20.0,
        )


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
