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
        """Aerodynamic resistance should be positive for valid inputs."""
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

    def test_resistance_scales_inversely_with_wind_speed(self):
        """Aerodynamic resistance should scale inversely with wind speed (1/u)."""
        low_wind = aerodynamic_resistance(u=1.0)
        medium_wind = aerodynamic_resistance(u=2.0)
        high_wind = aerodynamic_resistance(u=4.0)

        assert high_wind < low_wind
        assert low_wind == pytest.approx(2.0 * medium_wind)
        assert medium_wind == pytest.approx(2.0 * high_wind)

    def test_z_h_defaults_to_z_u(self):
        """Use z_u as the heat measurement height when z_h is omitted."""
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

    def test_greater_measurement_height_increases_resistance(self):
        """Increasing measurement heights should increase aerodynamic resistance."""
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

        assert result_10m > result_2m

    def test_increasing_roughness_lengths_reduces_aerodynamic_resistance(self):
        """Increasing roughness lengths should reduce resistance in the log-profile model."""
        smooth_surface = aerodynamic_resistance(
            u=2.0,
            z_om=0.001,
            z_oh=0.001,
        )
        rough_surface = aerodynamic_resistance(
            u=2.0,
            z_om=0.01,
            z_oh=0.01,
        )

        assert rough_surface < smooth_surface

    def test_increasing_zero_plane_displacement_reduces_resistance(self):
        """Increasing zero-plane displacement should reduce resistance in the model."""
        no_displacement = aerodynamic_resistance(
            u=2.0,
            d=0.0,
        )
        displacement = aerodynamic_resistance(
            u=2.0,
            d=0.1,
        )

        assert displacement < no_displacement

    @pytest.mark.parametrize("wind_speed", [0.0, -0.1, -1.0])
    def test_rejects_non_positive_wind_speed(self, wind_speed):
        """Wind speed must be greater than zero."""
        with pytest.raises(ValueError, match="wind speed"):
            aerodynamic_resistance(u=wind_speed)

    @pytest.mark.parametrize(
        ("parameter", "message"),
        [
            ("z_u", r"z_m.*greater than.*d"),
            ("z_h", r"z_h.*greater than.*d"),
        ],
    )
    def test_rejects_measurement_height_at_or_below_displacement(
        self,
        parameter,
        message,
    ):
        """Measurement heights must be greater than displacement height."""
        with pytest.raises(ValueError, match=message):
            aerodynamic_resistance(
                u=2.0,
                d=0.1,
                **{parameter: 0.1},
            )

    @pytest.mark.parametrize(
        ("parameter", "message"),
        [
            ("z_om", "z_om"),
            ("z_oh", "z_oh"),
        ],
    )
    def test_rejects_non_positive_roughness_lengths(
        self,
        parameter,
        message,
    ):
        """Roughness lengths must be greater than zero."""
        with pytest.raises(ValueError, match=message):
            aerodynamic_resistance(
                u=2.0,
                **{parameter: 0.0},
            )

    @pytest.mark.parametrize(
        ("parameter", "height_parameter", "message"),
        [
            ("z_om", "z_u", "z_om must be less"),
            ("z_oh", "z_h", "z_oh must be less"),
        ],
    )
    def test_rejects_roughness_lengths_at_or_above_available_height(
        self,
        parameter,
        height_parameter,
        message,
    ):
        """Roughness lengths must be less than available profile height."""
        with pytest.raises(ValueError, match=message):
            aerodynamic_resistance(
                u=2.0,
                d=0.0,
                **{
                    height_parameter: 2.0,
                    parameter: 2.0,
                },
            )


# ---------------------------------------------------------------------------
# estimate_soil_surface_resistance
# ---------------------------------------------------------------------------


class TestEstimateSoilSurfaceResistance:
    """Tests for estimate_soil_surface_resistance."""

    def test_returns_positive_finite_value(self):
        """Soil surface resistance should be positive and finite."""
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

    def test_soil_resistance_increases_with_dryness(self):
        """Drier soil should have greater surface resistance."""
        wet = estimate_soil_surface_resistance(vwc=0.30)
        dry = estimate_soil_surface_resistance(vwc=0.15)

        assert dry > wet

    def test_matches_exponential_formula(self):
        """Calculate resistance using the documented exponential equation."""
        vwc = 0.20
        theta_fc = 0.35
        theta_evap_min = 0.10
        rs_min = 50.0
        k_s = 4.0

        dryness = (theta_fc - vwc) / (theta_fc - theta_evap_min)
        expected = rs_min * math.exp(k_s * dryness)

        result = estimate_soil_surface_resistance(
            vwc=vwc,
            theta_fc=theta_fc,
            theta_evap_min=theta_evap_min,
            rs_min=rs_min,
            k_s=k_s,
        )

        assert result == pytest.approx(expected)

    def test_intermediate_soil_moisture_produces_intermediate_resistance(self):
        """Intermediate soil moisture should produce resistance between the boundary values."""
        field_capacity = estimate_soil_surface_resistance(
            vwc=0.35,
            theta_fc=0.35,
            theta_evap_min=0.10,
        )
        intermediate = estimate_soil_surface_resistance(
            vwc=0.25,
            theta_fc=0.35,
            theta_evap_min=0.10,
        )
        minimum_moisture = estimate_soil_surface_resistance(
            vwc=0.10,
            theta_fc=0.35,
            theta_evap_min=0.10,
        )

        assert field_capacity < intermediate < minimum_moisture

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

    def test_zero_k_s_gives_constant_rs_min(self):
        """With k_s=0, soil moisture should have no effect."""
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
        """With rs_min=0, resistance should remain zero."""
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

    @pytest.mark.parametrize(
        ("parameter", "value", "message"),
        [
            ("theta_fc", -0.1, "theta_fc must be between"),
            ("theta_fc", 1.01, "theta_fc must be between"),
            ("theta_evap_min", -0.1, "theta_evap_min must be between"),
            ("theta_evap_min", 1.01, "theta_evap_min must be between"),
        ],
    )
    def test_rejects_invalid_soil_water_parameters(
        self,
        parameter,
        value,
        message,
    ):
        """Soil water parameters must be within the physical range."""
        with pytest.raises(ValueError, match=message):
            estimate_soil_surface_resistance(
                vwc=0.25,
                **{parameter: value},
            )

    @pytest.mark.parametrize(
        ("theta_fc", "theta_evap_min"),
        [
            (0.20, 0.20),
            (0.10, 0.20),
        ],
    )
    def test_rejects_invalid_theta_bounds(
        self,
        theta_fc,
        theta_evap_min,
    ):
        """Field capacity must be greater than evaporation minimum."""
        with pytest.raises(
            ValueError,
            match="theta_fc must be greater than",
        ):
            estimate_soil_surface_resistance(
                vwc=0.25,
                theta_fc=theta_fc,
                theta_evap_min=theta_evap_min,
            )

    @pytest.mark.parametrize(
        ("parameter", "value", "message"),
        [
            ("rs_min", -1.0, "rs_min must be non-negative"),
            ("k_s", -1.0, "k_s must be non-negative"),
        ],
    )
    def test_rejects_negative_resistance_parameters(
        self,
        parameter,
        value,
        message,
    ):
        """Resistance model parameters must be non-negative."""
        with pytest.raises(ValueError, match=message):
            estimate_soil_surface_resistance(
                vwc=0.25,
                **{parameter: value},
            )
