"""Unit tests for the high-level soil evaporation calculation.

Run with:

    pytest -q tests/environmental/test_soil_evaporation.py
"""

import pytest

from postprocess.environmental.evapotranspiration import (
    calculate_soil_evaporation,
)


def test_accepts_zero_solar_radiation():
    """Zero incoming solar radiation is valid."""
    result = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=2.0,
        solar_rad=0.0,
        vwc=0.25,
    )

    assert isinstance(result, float)


def test_accepts_fractional_wind_speed():
    """Normal positive fractional wind speeds should be accepted."""
    result = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=0.5,
        solar_rad=500.0,
        vwc=0.25,
    )

    assert isinstance(result, float)


def test_returns_float():
    """The high-level function should return a floating-point ET flux."""
    result = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=2.0,
        solar_rad=500.0,
        vwc=0.25,
    )

    assert isinstance(result, float)


def test_uses_air_temperature_when_surface_temperature_is_none():
    """None surface temperature should use air temperature."""
    implicit = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=2.0,
        solar_rad=500.0,
        vwc=0.25,
        t_surface=None,
    )

    explicit = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=2.0,
        solar_rad=500.0,
        vwc=0.25,
        t_surface=25.0,
    )

    assert implicit == pytest.approx(explicit)


def test_returns_positive_evaporation_under_typical_conditions():
    """Typical warm, moist, sunny conditions should produce ET."""
    result = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=2.0,
        solar_rad=500.0,
        vwc=0.25,
    )

    assert result > 0.0


def test_warmer_surface_temperature_increases_evaporation():
    """Higher soil-surface temperature should increase soil evaporation."""
    cooler_surface = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=2.0,
        solar_rad=500.0,
        vwc=0.25,
        t_surface=25.0,
    )

    warmer_surface = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=2.0,
        solar_rad=500.0,
        vwc=0.25,
        t_surface=35.0,
    )

    assert warmer_surface > cooler_surface


def test_increased_solar_radiation_increases_evaporation():
    """More incoming solar radiation should generally increase ET."""
    low = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=2.0,
        solar_rad=200.0,
        vwc=0.25,
    )

    high = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=2.0,
        solar_rad=700.0,
        vwc=0.25,
    )

    assert high > low


def test_higher_humidity_reduces_evaporation():
    """Higher RH should reduce the surface vapour pressure deficit."""
    dry_air = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=30.0,
        wind_spd=2.0,
        solar_rad=500.0,
        vwc=0.25,
    )

    humid_air = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=80.0,
        wind_spd=2.0,
        solar_rad=500.0,
        vwc=0.25,
    )

    assert dry_air > humid_air


def test_higher_wind_speed_increases_evaporation_when_aerodynamic_demand_is_high():
    """Higher wind speed should increase ET under high aerodynamic demand."""
    low_wind = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=30.0,
        wind_spd=1.0,
        solar_rad=100.0,
        vwc=0.25,
    )

    high_wind = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=30.0,
        wind_spd=4.0,
        solar_rad=100.0,
        vwc=0.25,
    )

    assert high_wind > low_wind


def test_drier_soil_reduces_evaporation():
    """Lower VWC should increase soil resistance and reduce ET."""
    wet = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=2.0,
        solar_rad=500.0,
        vwc=0.30,
    )

    dry = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=2.0,
        solar_rad=500.0,
        vwc=0.12,
    )

    assert wet > dry


def test_higher_albedo_reduces_evaporation():
    """Higher surface albedo should bsorbed shortwave radiation, reducing soil evaporation."""
    low_albedo = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=2.0,
        solar_rad=500.0,
        vwc=0.25,
        albedo=0.10,
    )

    high_albedo = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=2.0,
        solar_rad=500.0,
        vwc=0.25,
        albedo=0.50,
    )

    assert high_albedo < low_albedo


def test_soil_heat_flux_reduces_evaporation():
    """Positive soil heat flux removes energy from the surface."""
    no_heat_flux = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=2.0,
        solar_rad=500.0,
        vwc=0.25,
        soil_heat_flux=0.0,
    )

    positive_heat_flux = calculate_soil_evaporation(
        t_air=25.0,
        baro=101325.0,
        RH=50.0,
        wind_spd=2.0,
        solar_rad=500.0,
        vwc=0.25,
        soil_heat_flux=100.0,
    )

    assert no_heat_flux > positive_heat_flux
