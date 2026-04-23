"""
Unit tests for postprocess.environmental.resistance.

Run with:

    pytest -q tests/environmental/test_resistance.py

These tests validate:
- aerodynamic resistance
- soil surface resistance
"""

import math

import pytest

from postprocess.environmental.resistance import (
    aerodynamic_resistance,
    estimate_soil_surface_resistance,
)

# ---------------------------------------------------------------------------
# aerodynamic_resistance
# ---------------------------------------------------------------------------


class TestAerodynamicResistance:
    """Tests for aerodynamic_resistance."""

    def test_returns_positive_resistance(self):
        """Aerodynamic resistance should always be positive for valid inputs."""
        result = aerodynamic_resistance(u=2.0)

        assert result > 0.0
        assert math.isfinite(result)

    def test_default_parameters_match_expected_formula(self):
        """Default calculation should match the logarithmic wind-profile formula."""
        u = 2.0
        z_u = 2.0
        z_h = 2.0
        z_om = 0.001
        z_oh = 0.001
        d = 1e-4
        k = 0.41

        expected = (
            math.log((z_u - d) / z_om)
            * math.log((z_h - d) / z_oh)
            / (k**2 * u)
        )

        result = aerodynamic_resistance(u=u)

        assert result == pytest.approx(expected)

    def test_resistance_decreases_as_wind_speed_increases(self):
        """Higher wind speed should reduce aerodynamic resistance."""
        low_wind = aerodynamic_resistance(u=1.0)
        high_wind = aerodynamic_resistance(u=4.0)

        assert high_wind < low_wind

    def test_resistance_scales_inversely_with_wind_speed(self):
        """Resistance should scale as 1/u for otherwise identical inputs."""
        r1 = aerodynamic_resistance(u=1.0)
        r2 = aerodynamic_resistance(u=2.0)
        r4 = aerodynamic_resistance(u=4.0)

        assert r1 == pytest.approx(2.0 * r2)
        assert r2 == pytest.approx(2.0 * r4)

    def test_z_h_defaults_to_z_u(self):
        """When z_h is omitted, it should use z_u."""
        result_default = aerodynamic_resistance(
            u=2.0,
            z_u=2.0,
        )

        result_explicit = aerodynamic_resistance(
            u=2.0,
            z_u=2.0,
            z_h=2.0,
        )

        assert result_default == pytest.approx(result_explicit)

    def test_different_measurement_heights_change_resistance(self):
        """Changing heat/humidity measurement height should affect resistance."""
        result_2m = aerodynamic_resistance(
            u=2.0,
            z_u=2.0,
            z_h=2.0,
        )

        result_10m = aerodynamic_resistance(
            u=2.0,
            z_u=10.0,
            z_h=10.0,
        )

        assert result_10m != result_2m
        assert result_10m > result_2m

    def test_roughness_length_affects_resistance(self):
        """Changing roughness lengths should change aerodynamic resistance."""
        smooth = aerodynamic_resistance(
            u=2.0,
            z_om=0.001,
            z_oh=0.001,
        )

        rough = aerodynamic_resistance(
            u=2.0,
            z_om=0.01,
            z_oh=0.01,
        )

        assert rough != smooth
        assert rough < smooth

    def test_displacement_affects_resistance(self):
        """Changing zero-plane displacement should affect resistance."""
        no_displacement = aerodynamic_resistance(
            u=2.0,
            d=0.0,
        )

        displacement = aerodynamic_resistance(
            u=2.0,
            d=0.1,
        )

        assert displacement != no_displacement

    @pytest.mark.parametrize("wind_speed", [0.0, -0.1, -1.0])
    def test_rejects_non_positive_wind_speed(self, wind_speed):
        """Wind speed must be greater than zero."""
        with pytest.raises(ValueError, match="wind speed"):
            aerodynamic_resistance(u=wind_speed)

    def test_rejects_z_u_equal_to_displacement(self):
        """Wind measurement height must exceed displacement height."""
        with pytest.raises(ValueError, match="z_m.*greater than.*d"):
            aerodynamic_resistance(
                u=2.0,
                z_u=0.1,
                d=0.1,
            )

    def test_rejects_z_u_below_displacement(self):
        """Wind measurement height cannot be below displacement height."""
        with pytest.raises(ValueError, match="z_m.*greater than.*d"):
            aerodynamic_resistance(
                u=2.0,
                z_u=0.05,
                d=0.1,
            )

    def test_rejects_z_h_equal_to_displacement(self):
        """Heat measurement height must exceed displacement height."""
        with pytest.raises(ValueError, match="z_h.*greater than.*d"):
            aerodynamic_resistance(
                u=2.0,
                z_h=0.1,
                d=0.1,
            )

    def test_rejects_z_h_below_displacement(self):
        """Heat measurement height cannot be below displacement height."""
        with pytest.raises(ValueError, match="z_h.*greater than.*d"):
            aerodynamic_resistance(
                u=2.0,
                z_h=0.05,
                d=0.1,
            )

    def test_rejects_non_positive_momentum_roughness(self):
        """Momentum roughness length must be positive."""
        with pytest.raises(ValueError, match="z_om"):
            aerodynamic_resistance(
                u=2.0,
                z_om=0.0,
            )

    def test_rejects_negative_momentum_roughness(self):
        """Negative momentum roughness length is invalid."""
        with pytest.raises(ValueError, match="z_om"):
            aerodynamic_resistance(
                u=2.0,
                z_om=-0.001,
            )

    def test_rejects_non_positive_heat_roughness(self):
        """Heat roughness length must be positive."""
        with pytest.raises(ValueError, match="z_oh"):
            aerodynamic_resistance(
                u=2.0,
                z_oh=0.0,
            )

    def test_rejects_negative_heat_roughness(self):
        """Negative heat roughness length is invalid."""
        with pytest.raises(ValueError, match="z_oh"):
            aerodynamic_resistance(
                u=2.0,
                z_oh=-0.001,
            )

    def test_rejects_momentum_roughness_equal_to_available_height(self):
        """z_om must be less than z_u - d."""
        with pytest.raises(ValueError, match="z_om must be less"):
            aerodynamic_resistance(
                u=2.0,
                z_u=2.0,
                z_om=1.9999,
                d=0.0,
            )

    def test_rejects_momentum_roughness_above_available_height(self):
        """z_om cannot exceed the available wind-profile height."""
        with pytest.raises(ValueError, match="z_om must be less"):
            aerodynamic_resistance(
                u=2.0,
                z_u=2.0,
                z_om=2.0,
                d=0.0,
            )

    def test_rejects_heat_roughness_equal_to_available_height(self):
        """z_oh must be less than z_h - d."""
        with pytest.raises(ValueError, match="z_oh must be less"):
            aerodynamic_resistance(
                u=2.0,
                z_h=2.0,
                z_oh=1.9999,
                d=0.0,
            )

    def test_rejects_heat_roughness_above_available_height(self):
        """z_oh cannot exceed the available heat-profile height."""
        with pytest.raises(ValueError, match="z_oh must be less"):
            aerodynamic_resistance(
                u=2.0,
                z_h=2.0,
                z_oh=2.0,
                d=0.0,
            )


# ---------------------------------------------------------------------------
# estimate_soil_surface_resistance
# ---------------------------------------------------------------------------


class TestEstimateSoilSurfaceResistance:
    """Tests for estimate_soil_surface_resistance."""

    def test_returns_positive_resistance(self):
        """Resistance should be positive with the default parameters."""
        result = estimate_soil_surface_resistance(vwc=0.25)

        assert result > 0.0
        assert math.isfinite(result)

    def test_field_capacity_returns_rs_min(self):
        """At field capacity, soil resistance should equal rs_min."""
        result = estimate_soil_surface_resistance(
            vwc=0.35,
            theta_fc=0.35,
            theta_evap_min=0.10,
            rs_min=50.0,
            k_s=4.0,
        )

        assert result == pytest.approx(50.0)

    def test_wetter_soil_has_lower_resistance(self):
        """Increasing soil moisture should reduce resistance."""
        dry = estimate_soil_surface_resistance(vwc=0.15)
        wet = estimate_soil_surface_resistance(vwc=0.30)

        assert wet < dry

    def test_drier_soil_has_higher_resistance(self):
        """Decreasing soil moisture should increase resistance."""
        wet = estimate_soil_surface_resistance(vwc=0.30)
        dry = estimate_soil_surface_resistance(vwc=0.15)

        assert dry > wet

    def test_resistance_increases_exponentially_with_dryness(self):
        """Result should follow the documented exponential drying equation."""
        vwc = 0.20
        theta_fc = 0.35
        theta_evap_min = 0.10
        rs_min = 50.0
        k_s = 4.0

        dryness = (
            (theta_fc - vwc)
            / (theta_fc - theta_evap_min)
        )

        expected = rs_min * math.exp(k_s * dryness)

        result = estimate_soil_surface_resistance(
            vwc=vwc,
            theta_fc=theta_fc,
            theta_evap_min=theta_evap_min,
            rs_min=rs_min,
            k_s=k_s,
        )

        assert result == pytest.approx(expected)

    def test_minimum_evaporation_water_content_is_clamped(self):
        """VWC below theta_evap_min should be clamped to theta_evap_min."""
        at_minimum = estimate_soil_surface_resistance(
            vwc=0.10,
            theta_fc=0.35,
            theta_evap_min=0.10,
        )

        below_minimum = estimate_soil_surface_resistance(
            vwc=0.0,
            theta_fc=0.35,
            theta_evap_min=0.10,
        )

        assert below_minimum == pytest.approx(at_minimum)

    def test_field_capacity_above_input_is_clamped(self):
        """VWC above field capacity should be clamped to field capacity."""
        at_field_capacity = estimate_soil_surface_resistance(
            vwc=0.35,
            theta_fc=0.35,
            theta_evap_min=0.10,
        )

        above_field_capacity = estimate_soil_surface_resistance(
            vwc=0.50,
            theta_fc=0.35,
            theta_evap_min=0.10,
        )

        assert above_field_capacity == pytest.approx(at_field_capacity)

    def test_vwc_between_bounds_is_not_clamped(self):
        """VWC inside the model range should be used directly."""
        result = estimate_soil_surface_resistance(
            vwc=0.25,
            theta_fc=0.35,
            theta_evap_min=0.10,
            rs_min=50.0,
            k_s=4.0,
        )

        dryness = (0.35 - 0.25) / (0.35 - 0.10)
        expected = 50.0 * math.exp(4.0 * dryness)

        assert result == pytest.approx(expected)

    def test_zero_k_s_gives_constant_rs_min(self):
        """With k_s=0, soil dryness should have no effect."""
        wet = estimate_soil_surface_resistance(
            vwc=0.15,
            k_s=0.0,
            rs_min=50.0,
        )

        dry = estimate_soil_surface_resistance(
            vwc=0.30,
            k_s=0.0,
            rs_min=50.0,
        )

        assert wet == pytest.approx(50.0)
        assert dry == pytest.approx(50.0)

    def test_zero_rs_min_gives_zero_resistance(self):
        """With rs_min=0, the exponential result remains zero."""
        result = estimate_soil_surface_resistance(
            vwc=0.20,
            rs_min=0.0,
        )

        assert result == pytest.approx(0.0)

    @pytest.mark.parametrize("vwc", [-0.1, -1.0, 1.01, 2.0])
    def test_rejects_vwc_outside_physical_range(self, vwc):
        """VWC must be within the physical 0-1 range."""
        with pytest.raises(ValueError, match="vwc must be between"):
            estimate_soil_surface_resistance(vwc=vwc)

    @pytest.mark.parametrize(
        "vwc",
        [
            float("nan"),
            float("inf"),
            float("-inf"),
        ],
    )
    def test_rejects_non_finite_vwc(self, vwc):
        """VWC must be finite."""
        with pytest.raises(ValueError, match="vwc must be a finite"):
            estimate_soil_surface_resistance(vwc=vwc)

    @pytest.mark.parametrize("theta_fc", [-0.1, 1.01])
    def test_rejects_invalid_field_capacity(self, theta_fc):
        """Field capacity must be between 0 and 1."""
        with pytest.raises(ValueError, match="theta_fc must be between"):
            estimate_soil_surface_resistance(
                vwc=0.25,
                theta_fc=theta_fc,
            )

    @pytest.mark.parametrize("theta_evap_min", [-0.1, 1.01])
    def test_rejects_invalid_evaporation_minimum(self, theta_evap_min):
        """Minimum evaporation water content must be between 0 and 1."""
        with pytest.raises(
            ValueError,
            match="theta_evap_min must be between",
        ):
            estimate_soil_surface_resistance(
                vwc=0.25,
                theta_evap_min=theta_evap_min,
            )

    def test_rejects_equal_theta_bounds(self):
        """Field capacity must be greater than the evaporation minimum."""
        with pytest.raises(
            ValueError,
            match="theta_fc must be greater than",
        ):
            estimate_soil_surface_resistance(
                vwc=0.25,
                theta_fc=0.20,
                theta_evap_min=0.20,
            )

    def test_rejects_field_capacity_below_evaporation_minimum(self):
        """Field capacity cannot be below the evaporation minimum."""
        with pytest.raises(
            ValueError,
            match="theta_fc must be greater than",
        ):
            estimate_soil_surface_resistance(
                vwc=0.25,
                theta_fc=0.10,
                theta_evap_min=0.20,
            )

    def test_rejects_negative_rs_min(self):
        """Minimum resistance cannot be negative."""
        with pytest.raises(
            ValueError,
            match="rs_min must be non-negative",
        ):
            estimate_soil_surface_resistance(
                vwc=0.25,
                rs_min=-1.0,
            )

    def test_rejects_negative_k_s(self):
        """Drying sensitivity cannot be negative."""
        with pytest.raises(
            ValueError,
            match="k_s must be non-negative",
        ):
            estimate_soil_surface_resistance(
                vwc=0.25,
                k_s=-1.0,
            )


# ---------------------------------------------------------------------------
# Combined physical behavior
# ---------------------------------------------------------------------------


def test_wet_soil_has_lower_resistance_than_dry_soil():
    """A wet soil surface should provide less resistance to evaporation."""
    wet_resistance = estimate_soil_surface_resistance(
        vwc=0.35,
        theta_fc=0.35,
        theta_evap_min=0.10,
    )

    dry_resistance = estimate_soil_surface_resistance(
        vwc=0.10,
        theta_fc=0.35,
        theta_evap_min=0.10,
    )

    assert wet_resistance < dry_resistance


def test_higher_wind_reduces_aerodynamic_resistance():
    """Higher wind should make turbulent transfer easier."""
    resistance_low_wind = aerodynamic_resistance(u=1.0)
    resistance_high_wind = aerodynamic_resistance(u=5.0)

    assert resistance_high_wind < resistance_low_wind
