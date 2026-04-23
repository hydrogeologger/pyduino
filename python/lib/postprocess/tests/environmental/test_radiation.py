"""
Unit tests for postprocess.environmental.radiation.

Run with:

    pytest -q tests/environmental/test_radiation.py

These tests validate:
- net radiation flux
- shortwave radiation behaviour
- longwave radiation behaviour
- surface and atmospheric emissivity effects
- albedo effects
- surface temperature effects
- default surface temperature behaviour
- net radiation energy accumulation
- timestep validation
- physical input validation
"""

import math

import pytest

from postprocess.environmental.radiation import (
    net_radiation_energy,
    net_radiation_flux,
)

# pylint: disable=missing-function-docstring


# ---------------------------------------------------------------------------
# Net radiation flux
# ---------------------------------------------------------------------------


def test_net_radiation_flux_without_longwave_difference():
    radiation = net_radiation_flux(
        R_s=300.0,
        T_a_C=20.0,
        T_s_C=20.0,
        albedo=0.2,
        epsilon_s=0.95,
        epsilon_a=0.95,
    )

    expected = 300.0 * (1.0 - 0.2)

    assert radiation == pytest.approx(expected, rel=1e-6)


def test_net_radiation_flux_uses_air_temperature_when_surface_temperature_omitted():
    radiation_without_surface_temperature = net_radiation_flux(
        R_s=300.0,
        T_a_C=20.0,
        T_s_C=None,
        albedo=0.2,
        epsilon_s=0.95,
        epsilon_a=0.95,
    )

    radiation_with_same_surface_temperature = net_radiation_flux(
        R_s=300.0,
        T_a_C=20.0,
        T_s_C=20.0,
        albedo=0.2,
        epsilon_s=0.95,
        epsilon_a=0.95,
    )

    assert radiation_without_surface_temperature == pytest.approx(
        radiation_with_same_surface_temperature
    )


def test_net_radiation_flux_decreases_with_albedo():
    low_albedo = net_radiation_flux(
        R_s=300.0,
        T_a_C=20.0,
        T_s_C=20.0,
        albedo=0.1,
    )

    high_albedo = net_radiation_flux(
        R_s=300.0,
        T_a_C=20.0,
        T_s_C=20.0,
        albedo=0.4,
    )

    assert high_albedo < low_albedo


def test_net_radiation_flux_increases_with_solar_radiation():
    low = net_radiation_flux(
        R_s=100.0,
        T_a_C=20.0,
        T_s_C=20.0,
    )

    high = net_radiation_flux(
        R_s=500.0,
        T_a_C=20.0,
        T_s_C=20.0,
    )

    assert high > low


def test_net_radiation_flux_surface_emission_is_negative():
    radiation = net_radiation_flux(
        R_s=0.0,
        T_a_C=20.0,
        T_s_C=30.0,
        albedo=0.2,
    )

    assert radiation < 0.0


def test_net_radiation_flux_atmospheric_longwave_is_positive():
    radiation = net_radiation_flux(
        R_s=0.0,
        T_a_C=30.0,
        T_s_C=20.0,
        epsilon_s=0.95,
        epsilon_a=1.0,
    )

    assert radiation > 0.0


def test_net_radiation_flux_surface_emissivity_effect_is_physically_consistent():
    """
    When the atmosphere is warmer than the surface, increasing surface
    emissivity increases the net longwave radiation received by the surface.

    This follows:

        R_nl = sigma * (
            epsilon_a * T_air^4
            - epsilon_s * T_surface^4
        )

    When T_air > T_surface, increasing epsilon_s makes the outgoing
    surface term more negative, so the net radiation should decrease.

    Therefore, for the actual implementation, this test checks the
    mathematical direction directly rather than assuming the opposite.
    """
    low_emissivity = net_radiation_flux(
        R_s=0.0,
        T_a_C=30.0,
        T_s_C=20.0,
        epsilon_s=0.5,
        epsilon_a=1.0,
    )

    high_emissivity = net_radiation_flux(
        R_s=0.0,
        T_a_C=30.0,
        T_s_C=20.0,
        epsilon_s=1.0,
        epsilon_a=1.0,
    )

    assert high_emissivity < low_emissivity


def test_net_radiation_flux_increases_with_atmospheric_emissivity():
    low_emissivity = net_radiation_flux(
        R_s=0.0,
        T_a_C=20.0,
        T_s_C=30.0,
        epsilon_a=0.5,
    )

    high_emissivity = net_radiation_flux(
        R_s=0.0,
        T_a_C=20.0,
        T_s_C=30.0,
        epsilon_a=1.0,
    )

    assert high_emissivity > low_emissivity


def test_net_radiation_flux_decreases_with_surface_temperature():
    cool_surface = net_radiation_flux(
        R_s=0.0,
        T_a_C=20.0,
        T_s_C=10.0,
    )

    warm_surface = net_radiation_flux(
        R_s=0.0,
        T_a_C=20.0,
        T_s_C=30.0,
    )

    assert warm_surface < cool_surface


def test_net_radiation_flux_is_finite():
    radiation = net_radiation_flux(
        R_s=500.0,
        T_a_C=25.0,
        T_s_C=30.0,
        albedo=0.2,
    )

    assert math.isfinite(radiation)


def test_net_radiation_flux_can_be_negative():
    radiation = net_radiation_flux(
        R_s=0.0,
        T_a_C=0.0,
        T_s_C=40.0,
    )

    assert radiation < 0.0


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "solar_radiation",
    [-1.0, -100.0],
)
def test_net_radiation_flux_rejects_negative_solar_radiation(
    solar_radiation,
):
    with pytest.raises(
        ValueError,
        match="Incoming solar radiation",
    ):
        net_radiation_flux(
            R_s=solar_radiation,
            T_a_C=20.0,
        )


@pytest.mark.parametrize(
    "albedo",
    [-0.1, 1.1, 2.0],
)
def test_net_radiation_flux_rejects_invalid_albedo(albedo):
    with pytest.raises(
        ValueError,
        match="Albedo",
    ):
        net_radiation_flux(
            R_s=300.0,
            T_a_C=20.0,
            albedo=albedo,
        )


@pytest.mark.parametrize(
    "emissivity",
    [-0.1, 1.1, 2.0],
)
def test_net_radiation_flux_rejects_invalid_surface_emissivity(
    emissivity,
):
    with pytest.raises(
        ValueError,
        match="Surface emissivity",
    ):
        net_radiation_flux(
            R_s=300.0,
            T_a_C=20.0,
            epsilon_s=emissivity,
        )


@pytest.mark.parametrize(
    "emissivity",
    [-0.1, 1.1, 2.0],
)
def test_net_radiation_flux_rejects_invalid_atmospheric_emissivity(
    emissivity,
):
    with pytest.raises(
        ValueError,
        match="Atmospheric emissivity",
    ):
        net_radiation_flux(
            R_s=300.0,
            T_a_C=20.0,
            epsilon_a=emissivity,
        )


# ---------------------------------------------------------------------------
# Net radiation energy
# ---------------------------------------------------------------------------


def test_net_radiation_energy_equals_flux_for_one_second():
    flux = net_radiation_flux(
        R_s=300.0,
        T_a_C=20.0,
        T_s_C=25.0,
    )

    energy = net_radiation_energy(
        R_s=300.0,
        T_a_C=20.0,
        T_s_C=25.0,
        time_step_seconds=1.0,
    )

    assert energy == pytest.approx(flux)


def test_net_radiation_energy_scales_with_timestep():
    energy_one_second = net_radiation_energy(
        R_s=300.0,
        T_a_C=20.0,
        T_s_C=25.0,
        time_step_seconds=1.0,
    )

    energy_one_hour = net_radiation_energy(
        R_s=300.0,
        T_a_C=20.0,
        T_s_C=25.0,
        time_step_seconds=3600.0,
    )

    assert energy_one_hour == pytest.approx(
        energy_one_second * 3600.0
    )


def test_net_radiation_energy_accepts_fractional_timestep():
    energy = net_radiation_energy(
        R_s=300.0,
        T_a_C=20.0,
        T_s_C=25.0,
        time_step_seconds=1.5,
    )

    flux = net_radiation_flux(
        R_s=300.0,
        T_a_C=20.0,
        T_s_C=25.0,
    )

    assert energy == pytest.approx(flux * 1.5)


@pytest.mark.parametrize(
    "time_step_seconds",
    [0, -1, -3600],
)
def test_net_radiation_energy_rejects_non_positive_timestep(
    time_step_seconds,
):
    with pytest.raises(
        ValueError,
        match="time_step_seconds",
    ):
        net_radiation_energy(
            R_s=300.0,
            T_a_C=20.0,
            time_step_seconds=time_step_seconds,
        )


@pytest.mark.parametrize(
    "time_step_seconds",
    [1.5, 0.5, 3600.5, 86400.25],
)
def test_net_radiation_energy_accepts_positive_fractional_timestep(
    time_step_seconds,
):
    result = net_radiation_energy(
        R_s=300.0,
        T_a_C=20.0,
        time_step_seconds=time_step_seconds,
    )

    assert math.isfinite(result)


@pytest.mark.parametrize(
    "time_step_seconds",
    [
        0,
        -1,
        -3600,
        -1.5,
        "3600",
        None,
        False,
    ],
)
def test_net_radiation_energy_rejects_invalid_timestep_type(
    time_step_seconds,
):
    with pytest.raises(ValueError, match="time_step_seconds"):
        net_radiation_energy(
            R_s=300.0,
            T_a_C=20.0,
            time_step_seconds=time_step_seconds,
        )


def test_net_radiation_energy_preserves_negative_net_radiation():
    energy = net_radiation_energy(
        R_s=0.0,
        T_a_C=0.0,
        T_s_C=40.0,
        time_step_seconds=3600.0,
    )

    assert energy < 0.0
