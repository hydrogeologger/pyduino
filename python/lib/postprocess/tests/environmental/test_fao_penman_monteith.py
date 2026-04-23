"""Unit tests for the FAO-56 Penman-Monteith equation.

Run with:

    pytest -q tests/environmental/test_fao_penman_monteith.py
"""

import pytest

from postprocess.environmental.evapotranspiration import (
    fao_penman_monteith,
)


# ---------------------------------------------------------------------------
# Equation correctness
# ---------------------------------------------------------------------------

def test_matches_fao_penman_monteith_equation():
    """Verify the implementation against the FAO-56 PM equation."""
    T = 25.0
    u_2 = 2.0
    delta = 0.188
    Rn = 10.0
    G = 0.0
    vpd = 1.5
    gamma = 0.066

    result = fao_penman_monteith(
        T=T,
        u_2=u_2,
        delta=delta,
        Rn=Rn,
        G=G,
        vpd=vpd,
        gamma=gamma,
    )

    expected = (
        0.408 * delta * (Rn - G)
        + gamma
        * (900.0 / (T + 273.0))
        * u_2
        * vpd
    ) / (
        delta + gamma * (1.0 + 0.34 * u_2)
    )

    assert result == pytest.approx(expected, rel=1e-12)


def test_matches_fao_penman_monteith_expected_value():
    """Verify the output against a known FAO-56 PM reference value."""
    result = fao_penman_monteith(
        T=25.0,
        u_2=2.0,
        delta=0.188,
        Rn=10.0,
        G=0.0,
        vpd=1.5,
        gamma=0.066,
    )

    expected_et = 4.567139243780808

    assert result == pytest.approx(expected_et, rel=1e-6)


# ---------------------------------------------------------------------------
# Physical behaviour
# ---------------------------------------------------------------------------

def test_returns_positive_reference_et():
    """Typical conditions should produce positive reference ET."""
    result = fao_penman_monteith(
        T=25.0,
        u_2=2.0,
        delta=0.188,
        Rn=10.0,
        G=0.0,
        vpd=1.5,
        gamma=0.066,
    )

    assert result > 0.0


def test_increases_with_net_radiation():
    """Increasing net radiation should increase FAO ET."""
    low = fao_penman_monteith(
        T=25.0,
        u_2=2.0,
        delta=0.188,
        Rn=5.0,
        G=0.0,
        vpd=1.5,
        gamma=0.066,
    )

    high = fao_penman_monteith(
        T=25.0,
        u_2=2.0,
        delta=0.188,
        Rn=15.0,
        G=0.0,
        vpd=1.5,
        gamma=0.066,
    )

    assert high > low


def test_increases_with_vpd():
    """Increasing VPD should increase FAO ET."""
    low = fao_penman_monteith(
        T=25.0,
        u_2=2.0,
        delta=0.188,
        Rn=10.0,
        G=0.0,
        vpd=0.5,
        gamma=0.066,
    )

    high = fao_penman_monteith(
        T=25.0,
        u_2=2.0,
        delta=0.188,
        Rn=10.0,
        G=0.0,
        vpd=2.0,
        gamma=0.066,
    )

    assert high > low


def test_increases_with_wind_speed_when_vpd_positive():
    """Increasing wind speed should increase ET when VPD is positive."""
    low = fao_penman_monteith(
        T=25.0,
        u_2=1.0,
        delta=0.188,
        Rn=10.0,
        G=0.0,
        vpd=2.0,
        gamma=0.066,
    )

    high = fao_penman_monteith(
        T=25.0,
        u_2=4.0,
        delta=0.188,
        Rn=10.0,
        G=0.0,
        vpd=2.0,
        gamma=0.066,
    )

    assert high > low


def test_soil_heat_flux_reduces_et():
    """Increasing soil heat flux should reduce available energy and ET."""
    low_g = fao_penman_monteith(
        T=25.0,
        u_2=2.0,
        delta=0.188,
        Rn=10.0,
        G=0.0,
        vpd=1.5,
        gamma=0.066,
    )

    high_g = fao_penman_monteith(
        T=25.0,
        u_2=2.0,
        delta=0.188,
        Rn=10.0,
        G=5.0,
        vpd=1.5,
        gamma=0.066,
    )

    assert low_g > high_g


def test_zero_vpd_leaves_only_radiative_component():
    """With zero VPD, ET should contain only the radiative component."""
    result = fao_penman_monteith(
        T=25.0,
        u_2=2.0,
        delta=0.188,
        Rn=10.0,
        G=0.0,
        vpd=0.0,
        gamma=0.066,
    )

    expected = (
        0.408 * 0.188 * (10.0 - 0.0)
        / (
            0.188
            + 0.066 * (1.0 + 0.34 * 2.0)
        )
    )

    assert result == pytest.approx(expected)


def test_zero_available_energy_still_allows_aerodynamic_et():
    """Positive VPD should produce ET when Rn equals G."""
    result = fao_penman_monteith(
        T=25.0,
        u_2=2.0,
        delta=0.188,
        Rn=5.0,
        G=5.0,
        vpd=1.5,
        gamma=0.066,
    )

    assert result > 0.0


# ---------------------------------------------------------------------------
# Valid boundary conditions
# ---------------------------------------------------------------------------

def test_zero_wind_still_allows_radiative_et():
    """Zero wind is valid and radiative ET can still occur."""
    result = fao_penman_monteith(
        T=25.0,
        u_2=0.0,
        delta=0.188,
        Rn=10.0,
        G=0.0,
        vpd=1.5,
        gamma=0.066,
    )

    assert result > 0.0


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

def test_rejects_negative_wind_speed():
    """Wind speed cannot be negative."""
    with pytest.raises(ValueError):
        fao_penman_monteith(
            T=25.0,
            u_2=-1.0,
            delta=0.188,
            Rn=10.0,
            G=0.0,
            vpd=1.5,
            gamma=0.066,
        )


def test_rejects_zero_denominator():
    """Zero Delta and gamma should produce an invalid denominator."""
    with pytest.raises(ValueError):
        fao_penman_monteith(
            T=25.0,
            u_2=2.0,
            delta=0.0,
            Rn=10.0,
            G=0.0,
            vpd=1.5,
            gamma=0.0,
        )
