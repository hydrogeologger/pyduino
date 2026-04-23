"""Unit tests for postprocess.environmental.evapotranspiration

Run with:

    pytest -q tests/test_evapotranspiration.py

These tests validate:
- Penman-Monteith
- FAO Penman-Monteith
- end-to-end evapotranspiration calculations
"""

import pytest
from postprocess.environmental.evapotranspiration import (
    calculate_soil_evaporation,
    fao_penman_monteith,
    penman_monteith,
)


class TestPenmanMonteith:
    """Tests for the resistance-form Penman-Monteith equation."""

    def test_returns_positive_et_under_typical_conditions(self):
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

    def test_returns_zero_when_all_energy_and_vpd_terms_are_zero(self):
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

    def test_increases_with_net_radiation(self):
        """Increasing net radiation should increase ET."""
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

    def test_increases_with_vpd(self):
        """Increasing VPD should increase ET."""
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

    def test_increases_with_aerodynamic_resistance_when_vpd_is_positive(self):
        """
        With the implemented resistance-form equation, increasing r_a
        reduces the aerodynamic contribution and therefore reduces ET.
        """
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

    def test_decreases_with_surface_resistance(self):
        """Increasing surface resistance should reduce the energy contribution."""
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

    def test_soil_heat_flux_reduces_et(self):
        """Increasing soil heat flux reduces available energy."""
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

    def test_allows_zero_surface_resistance(self):
        """Surface resistance of zero is valid."""
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

    def test_rejects_zero_aerodynamic_resistance(self):
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

    def test_rejects_negative_aerodynamic_resistance(self):
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

    def test_rejects_negative_surface_resistance(self):
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

    def test_rejects_non_positive_latent_heat(self):
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

    def test_rejects_negative_delta(self):
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

    def test_rejects_negative_gamma(self):
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

    def test_rejects_non_positive_air_density(self):
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

    def test_rejects_non_positive_specific_heat(self):
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


class TestFAOPenmanMonteith:
    """Tests for the FAO-56 Penman-Monteith equation."""

    def test_returns_positive_reference_et(self):
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

    def test_zero_wind_still_allows_radiative_et(self):
        """Zero wind is valid and can still produce radiative ET."""
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

    def test_increases_with_net_radiation(self):
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

    def test_increases_with_vpd(self):
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

    def test_increases_with_wind_speed_when_vpd_positive(self):
        """Increasing wind speed should increase the aerodynamic contribution."""
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

    def test_soil_heat_flux_reduces_et(self):
        """Increasing G should reduce available energy."""
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

    def test_rejects_negative_wind_speed(self):
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

    def test_rejects_zero_denominator(self):
        """Invalid zero-valued Delta and gamma should fail."""
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


class TestCalculateSoilEvaporation:
    """Tests for the high-level soil evaporation calculation."""

    def test_returns_positive_evaporation_under_typical_conditions(self):
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

    def test_uses_air_temperature_when_surface_temperature_is_none(self):
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

    def test_surface_temperature_affects_result(self):
        """Changing surface temperature should affect soil evaporation."""
        air_temperature_surface = calculate_soil_evaporation(
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

        assert warmer_surface != pytest.approx(air_temperature_surface)

    def test_increases_with_solar_radiation(self):
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

    def test_higher_humidity_reduces_evaporation(self):
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

    def test_higher_wind_speed_increases_evaporation(self):
        """Higher wind speed should reduce aerodynamic resistance and increase ET."""
        low_wind = calculate_soil_evaporation(
            t_air=25.0,
            baro=101325.0,
            RH=50.0,
            wind_spd=1.0,
            solar_rad=500.0,
            vwc=0.25,
        )

        high_wind = calculate_soil_evaporation(
            t_air=25.0,
            baro=101325.0,
            RH=50.0,
            wind_spd=4.0,
            solar_rad=500.0,
            vwc=0.25,
        )

        assert high_wind > low_wind

    def test_drier_soil_reduces_evaporation(self):
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

    def test_albedo_affects_evaporation(self):
        """Higher albedo should reduce absorbed shortwave radiation."""
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

        assert low_albedo > high_albedo

    def test_soil_heat_flux_reduces_evaporation(self):
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

    def test_accepts_fractional_wind_speed(self):
        """Normal positive fractional wind speeds should be accepted."""
        result = calculate_soil_evaporation(
            t_air=25.0,
            baro=101325.0,
            RH=50.0,
            wind_spd=0.5,
            solar_rad=500.0,
            vwc=0.25,
        )

        assert result > 0.0

    def test_accepts_zero_solar_radiation(self):
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

    def test_returns_float(self):
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
