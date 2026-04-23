"""Unit tests for the resistance-form Penman-Monteith equation.

Run with:

    pytest -q tests/environmental/test_penman_monteith.py
"""

import pytest

from postprocess.environmental.evapotranspiration import penman_monteith


# ---------------------------------------------------------------------------
# Equation correctness
# ---------------------------------------------------------------------------


def test_matches_penman_monteith_equation():
    """Verify the implementation against the Penman-Monteith equation."""
    delta = 188.0
    rn = 300.0
    g = 30.0
    vpd = 1000.0
    r_a = 100.0
    r_s = 70.0
    gamma = 66.0
    lambda_ = 2.45e6
    rho_a = 1.204
    c_p = 1013.0

    result = penman_monteith(
        delta=delta,
        Rn=rn,
        G=g,
        vpd=vpd,
        r_a=r_a,
        r_s=r_s,
        gamma=gamma,
        lambda_=lambda_,
        rho_a=rho_a,
        c_p=c_p,
    )

    available_energy = rn - g

    expected_latent_energy_flux = (
        delta * available_energy
        + rho_a * c_p * (vpd / r_a)
    ) / (
        delta + gamma * (1.0 + r_s / r_a)
    )

    expected_et = expected_latent_energy_flux / lambda_

    assert result == pytest.approx(expected_et, rel=1e-12)


def test_matches_penman_monteith_expected_value():
    """Verify the implementation against a known numerical result."""
    result = penman_monteith(
        delta=188.0,
        Rn=300.0,
        G=30.0,
        vpd=1000.0,
        r_a=100.0,
        r_s=70.0,
        gamma=66.0,
    )

    expected_et = 8.559806387578349e-05

    assert result == pytest.approx(expected_et, rel=1e-6)


# ---------------------------------------------------------------------------
# Physical behaviour
# ---------------------------------------------------------------------------


def test_returns_positive_et_under_typical_conditions():
    """Typical positive radiation and VPD should produce positive ET."""
    result = penman_monteith(
        delta=188.0,
        Rn=300.0,
        G=30.0,
        vpd=1000.0,
        r_a=100.0,
        r_s=70.0,
        gamma=66.0,
    )

    assert result > 0.0


def test_increases_with_net_radiation():
    """Increasing available net radiation should increase ET."""
    low = penman_monteith(
        delta=188.0,
        Rn=100.0,
        G=0.0,
        vpd=500.0,
        r_a=100.0,
        r_s=70.0,
        gamma=66.0,
    )

    high = penman_monteith(
        delta=188.0,
        Rn=300.0,
        G=0.0,
        vpd=500.0,
        r_a=100.0,
        r_s=70.0,
        gamma=66.0,
    )

    assert high > low


def test_increases_with_vpd():
    """Increasing vapour pressure deficit should increase ET."""
    low = penman_monteith(
        delta=188.0,
        Rn=200.0,
        G=0.0,
        vpd=500.0,
        r_a=100.0,
        r_s=70.0,
        gamma=66.0,
    )

    high = penman_monteith(
        delta=188.0,
        Rn=200.0,
        G=0.0,
        vpd=1500.0,
        r_a=100.0,
        r_s=70.0,
        gamma=66.0,
    )

    assert high > low


def test_increasing_aerodynamic_resistance_reduces_et():
    """Increasing aerodynamic resistance should reduce ET under positive VPD."""
    low_resistance = penman_monteith(
        delta=188.0,
        Rn=200.0,
        G=0.0,
        vpd=1000.0,
        r_a=50.0,
        r_s=70.0,
        gamma=66.0,
    )

    high_resistance = penman_monteith(
        delta=188.0,
        Rn=200.0,
        G=0.0,
        vpd=1000.0,
        r_a=200.0,
        r_s=70.0,
        gamma=66.0,
    )

    assert low_resistance > high_resistance


def test_decreases_with_surface_resistance():
    """Increasing surface resistance should reduce ET."""
    low = penman_monteith(
        delta=188.0,
        Rn=300.0,
        G=0.0,
        vpd=1000.0,
        r_a=100.0,
        r_s=20.0,
        gamma=66.0,
    )

    high = penman_monteith(
        delta=188.0,
        Rn=300.0,
        G=0.0,
        vpd=1000.0,
        r_a=100.0,
        r_s=200.0,
        gamma=66.0,
    )

    assert low > high


def test_soil_heat_flux_reduces_et():
    """Increasing soil heat flux should reduce available energy and ET."""
    low_g = penman_monteith(
        delta=188.0,
        Rn=300.0,
        G=0.0,
        vpd=1000.0,
        r_a=100.0,
        r_s=70.0,
        gamma=66.0,
    )

    high_g = penman_monteith(
        delta=188.0,
        Rn=300.0,
        G=100.0,
        vpd=1000.0,
        r_a=100.0,
        r_s=70.0,
        gamma=66.0,
    )

    assert low_g > high_g


def test_latent_heat_scales_et_inversely():
    """ET should scale inversely with latent heat of vaporisation."""
    default_lambda = penman_monteith(
        delta=188.0,
        Rn=300.0,
        G=30.0,
        vpd=1000.0,
        r_a=100.0,
        r_s=70.0,
        gamma=66.0,
        lambda_=2.45e6,
    )

    double_lambda = penman_monteith(
        delta=188.0,
        Rn=300.0,
        G=30.0,
        vpd=1000.0,
        r_a=100.0,
        r_s=70.0,
        gamma=66.0,
        lambda_=4.90e6,
    )

    assert double_lambda == pytest.approx(default_lambda / 2.0)


# ---------------------------------------------------------------------------
# Component and boundary behaviour
# ---------------------------------------------------------------------------


def test_zero_vpd_retains_radiative_component():
    """With zero VPD, ET should contain only the radiative contribution."""
    result = penman_monteith(
        delta=188.0,
        Rn=300.0,
        G=30.0,
        vpd=0.0,
        r_a=100.0,
        r_s=70.0,
        gamma=66.0,
    )

    expected = (
        188.0 * (300.0 - 30.0)
        / (188.0 + 66.0 * (1.0 + 70.0 / 100.0))
        / 2.45e6
    )

    assert result == pytest.approx(expected)


def test_zero_available_energy_retains_aerodynamic_component():
    """With Rn equal to G, positive VPD should produce aerodynamic ET."""
    result = penman_monteith(
        delta=188.0,
        Rn=100.0,
        G=100.0,
        vpd=1000.0,
        r_a=100.0,
        r_s=70.0,
        gamma=66.0,
    )

    assert result > 0.0


def test_zero_energy_and_zero_vpd_produce_zero_et():
    """Zero available energy and zero VPD should produce zero ET."""
    result = penman_monteith(
        delta=188.0,
        Rn=0.0,
        G=0.0,
        vpd=0.0,
        r_a=100.0,
        r_s=70.0,
        gamma=66.0,
    )

    assert result == pytest.approx(0.0)


def test_allows_zero_surface_resistance():
    """Zero surface resistance should be valid."""
    result = penman_monteith(
        delta=188.0,
        Rn=200.0,
        G=0.0,
        vpd=1000.0,
        r_a=100.0,
        r_s=0.0,
        gamma=66.0,
    )

    assert result > 0.0


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


def test_rejects_zero_aerodynamic_resistance():
    """Aerodynamic resistance must be strictly positive."""
    with pytest.raises(ValueError):
        penman_monteith(
            delta=188.0,
            Rn=200.0,
            G=0.0,
            vpd=1000.0,
            r_a=0.0,
            r_s=70.0,
            gamma=66.0,
        )


def test_rejects_negative_aerodynamic_resistance():
    """Aerodynamic resistance cannot be negative."""
    with pytest.raises(ValueError):
        penman_monteith(
            delta=188.0,
            Rn=200.0,
            G=0.0,
            vpd=1000.0,
            r_a=-10.0,
            r_s=70.0,
            gamma=66.0,
        )


def test_rejects_negative_surface_resistance():
    """Surface resistance cannot be negative."""
    with pytest.raises(ValueError):
        penman_monteith(
            delta=188.0,
            Rn=200.0,
            G=0.0,
            vpd=1000.0,
            r_a=100.0,
            r_s=-1.0,
            gamma=66.0,
        )


def test_rejects_non_positive_latent_heat():
    """Latent heat must be positive."""
    with pytest.raises(ValueError):
        penman_monteith(
            delta=188.0,
            Rn=200.0,
            G=0.0,
            vpd=1000.0,
            r_a=100.0,
            r_s=70.0,
            gamma=66.0,
            lambda_=0.0,
        )


def test_rejects_negative_delta():
    """Delta cannot be negative."""
    with pytest.raises(ValueError):
        penman_monteith(
            delta=-1.0,
            Rn=200.0,
            G=0.0,
            vpd=1000.0,
            r_a=100.0,
            r_s=70.0,
            gamma=66.0,
        )


def test_rejects_negative_gamma():
    """Psychrometric constant cannot be negative."""
    with pytest.raises(ValueError):
        penman_monteith(
            delta=188.0,
            Rn=200.0,
            G=0.0,
            vpd=1000.0,
            r_a=100.0,
            r_s=70.0,
            gamma=-1.0,
        )


def test_rejects_non_positive_air_density():
    """Air density must be positive."""
    with pytest.raises(ValueError):
        penman_monteith(
            delta=188.0,
            Rn=200.0,
            G=0.0,
            vpd=1000.0,
            r_a=100.0,
            r_s=70.0,
            gamma=66.0,
            rho_a=0.0,
        )


def test_rejects_non_positive_specific_heat():
    """Specific heat capacity must be positive."""
    with pytest.raises(ValueError):
        penman_monteith(
            delta=188.0,
            Rn=200.0,
            G=0.0,
            vpd=1000.0,
            r_a=100.0,
            r_s=70.0,
            gamma=66.0,
            c_p=0.0,
        )
