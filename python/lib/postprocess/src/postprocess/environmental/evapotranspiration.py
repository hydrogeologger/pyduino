"""Methods for calculating evapotranspiration from meteorological data.

Provides implementations of evapotranspiration estimation approaches
using commonly available weather variables.

This module contains the high-level evapotranspiration models and composes
atmospheric, radiation, and resistance calculations provided by the
corresponding environmental modules.
"""

# pylint: disable-next=unused-import
from .atmospheric import (
    dry_air_density,
    latent_heat_of_vaporisation_water,
    psychrometric_constant,
    saturation_vapor_pressure_derivative,
    soil_surface_vapor_pressure_deficit,
    specific_heat_capacity_air,
    total_air_density,
)

from .radiation import (
    net_radiation_flux,
)

from .resistance import (
    aerodynamic_resistance,
    estimate_soil_surface_resistance,
)

# pylint: disable-next=unused-import
from ..conversion import (
    per_second_to_daily,
    per_second_to_hourly,
)

# pylint: disable=consider-using-f-string


def penman_monteith(
    delta, Rn, G, vpd, r_a, r_s, gamma,
    lambda_=2.45e6, rho_a=1.204, c_p=1013.0
):  # pylint: disable=invalid-name
    # type: (float, float, float, float, float, float, float, float, float, float) -> float
    """Compute evapotranspiration rate using the Penman–Monteith equation (resistance form).

    High level Structure:

        ET=(energy term)+(aerodynamic term)

    Penman–Monteith equation (explicit factorised form)

        ET = (1 / λ) * [
            ((Rₙ - G) * Δ) / (Δ + γ * (1 + rₛ / rₐ))
            + (ρₐ * cₚ * (VPD / rₐ)) / (Δ + γ * (1 + rₛ / rₐ))
        ]

    Structure:
        Radiative (energy) term:
            (Rₙ - G)

        Aerodynamic (mass-transfer) term:
            (ρₐ * cₚ * (VPD / rₐ))

        Weighting factors (Energy):
            Δ / (Δ + γ * (1 + rₛ / rₐ))

        Weighting factors (Aerodynamic):
            γ / (Δ + γ * (1 + rₛ / rₐ))


    Equation (symbolic form):

                        [ Δ (Rₙ - G) + ρₐ cₚ (VPD / rₐ) ]
        ET = (1 / λ) *  -----------------------------------
                        [ Δ + γ (1 + rₛ / rₐ) ]

    Where:
        ET  = evapotranspiration rate [kg m⁻² s⁻¹ (equivalently mm/s)]
        λ   = latent heat of vaporisation (≈ 2.45 x 10^6 J/kg @ 100 °C 1 atm)
        Δ   = slope of saturation vapour pressure curve (Pa/°C) or (N/m²/°C)
        Rₙ  = net radiation (W/m²)
        G   = soil heat flux (W/m²)
        ρₐ  = mean air density (kg/m³) (≈ 1.204 kg/m³ at 20°C at sea level)
        cₚ  = specific heat capacity of air (J/kg/°C) (dry air ≈ 1013 J/kg/°C)
        VPD = vapour pressure deficit (eₛ - eₐ)
            eₛ = Saturation vapor pressure (Pa)
            eₐ = Actual vapor pressure of the air (Pa)
        rₐ  = aerodynamic resistance (s/m)
        rₛ  = surface (canopy) resistance (s/m)
        γ   = psychrometric constant (Pa/°C)

    Units:

        The equation produces a mass flux of water:

            ET = kg m⁻² s⁻¹

        This is equivalent to a depth flux of water:

            ET = mm s⁻¹

        Common conversions:
            1 kg m⁻² = 1 mm water depth

    Consistency requirements:
    - Rₙ, G: W m⁻² (J s⁻¹ m⁻²)
    - λ: J kg⁻¹
    - rₐ, rₛ: s m⁻¹
    - Δ, γ: Pa °C⁻¹
    - VPD: Pa

    Args:
        delta (float): Δ, slope of saturation vapour pressure curve (Pa/°C).
        Rn (float): Rₙ, net radiation (W/m²).
        G (float): G, soil heat flux (W/m²).
        vpd (float): VPD = (eₛ - eₐ), Vapor pressure deficit (Pa).
            - eₛ = Saturation vapor pressure
            - eₐ = Actual vapor pressure of the air
        r_a (float): rₐ, aerodynamic resistance (s/m).
        r_s (float): rₛ, surface (canopy) resistance (s/m).
        gamma (float): γ, psychrometric constant (Pa/°C).
        lambda_ (float, optional): λ, latent heat of vaporisation (J/kg).
            Defaults to 2.45 x 10^6 J/kg.
        rho_a (float, optional): ρₐ, Air density (kg/m³).
            Defaults to (dry air) 1.204 kg/m³.
        c_p (float, optional): cₚ, specific heat capacity of air (J/kg/°C).
            Defaults to dry air 1013 J/kg/°C.

    Returns:
        float: ET, evapotranspiration rate in kg m⁻² s⁻¹ (equivalently mm/s).
    """
    if r_a <= 0:
        raise ValueError("aerodynamic_resistance must be > 0")
    if lambda_ <= 0:
        raise ValueError("latent_heat_vaporisation must be > 0")
    if r_s < 0:
        raise ValueError("surface_resistance must be >= 0")
    if delta < 0:
        raise ValueError("delta must be >= 0")
    if gamma < 0:
        raise ValueError("gamma must be >= 0")
    if rho_a <= 0:
        raise ValueError("air_density must be > 0")
    if c_p <= 0:
        raise ValueError("specific_heat_capacity must be > 0")

    numerator = ((delta * (Rn - G)) + (rho_a * c_p * (vpd / r_a)))

    denominator = delta + gamma * (1.0 + r_s / r_a)
    if denominator <= 0:
        raise ValueError("Penman-Monteith denominator must be > 0")

    return (1.0 / lambda_) * (numerator / denominator)


def fao_penman_monteith(T, u_2, delta, Rn, G, vpd, gamma):  # pylint: disable=invalid-name
    # type: (float, float, float, float, float, float, float) -> float
    """Compute evapotranspiration rate using the FAO Penman–Monteith equation.

        Equation (symbolic form):

                [ 0.408 Δ (Rₙ - G) + γ 900 / (T + 273)  u2 (eₛ - eₐ)  ]
        ET =    -----------------------------------
                        [ Δ + γ (1 + 0.34 u2) ]

    Where:
        ETo = reference evapotranspiration [mm/day]
        Δ   = slope vapour pressure curve [kPa/°C]
        Rₙ  = net radiation at the crop surface [MJ/m²day]
        G   = soil heat flux density [MJ/m²day]
        T   = mean daily air temperature at 2 m height [°C]
        u2  = wind speed at 2 m height [m/s]
        VPD = vapour pressure deficit (eₛ - eₐ)
            eₛ = Saturation vapor pressure [kPa]
            eₐ = Actual vapor pressure of the air [kPa]
        γ   = psychrometric constant [kPa/°C]

    Args:
        T (float): Mean daily air temperature at 2m height (°C).
        u_2 (float): Wind speed at 2m height (m/s).
        delta (float): Δ, slope of saturation vapour pressure curve (kPa/°C).
        Rn (float): Rₙ, net radiation at surface (MJ/m²day).
        G (float): G, soil heat flux (MJ/m²day).
        vpd (float): VPD = (eₛ - eₐ), Vapor pressure deficit (kPa).
            - eₛ = Saturation vapor pressure (kPa)
            - eₐ = Actual vapor pressure of the air (kPa)
        gamma (float): γ, psychrometric constant (kPa/°C).

    Returns:
        float: ET, evapotranspiration rate in (mm/day).

    Note:
        Temperature conversion (T + 273.0) is used instead of 273.15 to strictly
        comply with the hardcoded empirical constants specified in the
        FAO-56 Penman-Monteith standard.
    """
    if u_2 < 0:
        raise ValueError("Wind speed cannot be negative.")

    numerator = (0.408 * delta * (Rn - G) + gamma *
                 (900.0 / (T + 273.0)) * u_2 * (vpd))

    denominator = delta + gamma * (1.0 + 0.34 * u_2)
    if denominator <= 0:
        raise ValueError("Penman-Monteith denominator must be > 0")

    return numerator / denominator


def calculate_soil_evaporation(t_air, baro, RH,
                               wind_spd, solar_rad,
                               vwc, t_surface=None,
                               albedo=0.23, z_u=2.0, z_h=2.0,
                               theta_fc=0.35, theta_evap_min=0.10,
                               rs_min=50.0, k_s=4.0,
                               soil_heat_flux=0.0):
    # type: (float, float, float, float, float, float, float|None, float, float, float, float, float, float, float, float) -> float  # pylint: disable=line-too-long
    """Calculate soil evaporation flux using the Penman–Monteith equation for a soil surface.

    The calculation combines net radiation, vapour pressure deficit,
    psychrometric properties of air, aerodynamic resistance, and
    soil-surface resistance to estimate the actual evaporation
    flux from the soil surface.

    The calculation uses:

    - :func:`net_radiation` to calculate net radiation from incoming
      shortwave radiation, surface albedo, air temperature, and surface
      temperature.
    - :func:`saturation_vapor_pressure_derivative` to calculate the
      slope of the saturation vapour pressure curve.
    - :func:`soil_surface_vapor_pressure_deficit` to calculate the
      vapour pressure deficit at the soil surface.
    - :func:`psychrometric_constant` to calculate the psychrometric
      constant from atmospheric pressure and air temperature.
    - :func:`latent_heat_of_vaporisation_water` to calculate the
      temperature-dependent latent heat of vaporisation.
    - :func:`dry_air_density` to calculate dry-air density from air
      temperature and atmospheric pressure.
    - :func:`specific_heat_capacity_air` to calculate the specific heat
      capacity of air.
    - :func:`aerodynamic_resistance` to calculate aerodynamic resistance
      from wind speed and measurement heights.
    - :func:`estimate_soil_surface_resistance` to estimate soil-surface
      resistance from volumetric water content.
    - :func:`penman_monteith` to calculate the final evapotranspiration
      flux using the derived terms.

    The resulting evapotranspiration rate is a mass flux:

        ET = kg m⁻² s⁻¹

    which is numerically equivalent to mm/s for water.

    Args:
        t_air (float): Air temperature in degrees Celsius (°C).
        baro (float): Atmospheric pressure in Pascals (Pa).
        RH (float): Relative humidity as a percentage [0-100] (%).
        wind_spd (float): Wind speed at ``z_u`` in metres per second (m/s).
            Must be greater than zero.
        solar_rad (float): Incoming shortwave solar radiation in W/m².
            Must be non-negative.
        vwc (float): Volumetric water content (m³/m³) as a fraction [0-1].
        t_surface (float, optional): Soil-surface temperature in degrees
            Celsius (°C). If ``None``, ``t_air`` is used. Defaults to ``None``.
        albedo (float, optional): Surface albedo, dimensionless and in the
            range [0, 1]. Passed to :func:`net_radiation`. Defaults to 0.23.
        z_u (float, optional): Height of the wind-speed measurement above the
            surface in metres (m). Passed to :func:`aerodynamic_resistance`.
            Defaults to 2.0.
        z_h (float, optional): Height of the air temperature and humidity
            measurements above the surface in metres (m). Passed to
            :func:`aerodynamic_resistance`. Defaults to 2.0.
        theta_fc (float, optional): Volumetric water content at field
            capacity (m³/m³).
            Passed to :func:`estimate_soil_surface_resistance`.
            Defaults to 0.35.
        theta_evap_min (float, optional): Minimum volumetric water content
            represented by the soil-surface resistance model (m³/m³).
            Passed to :func:`estimate_soil_surface_resistance`. Defaults to
            0.10.
        rs_min (float, optional): Minimum soil-surface resistance (s/m).
            Passed to :func:`estimate_soil_surface_resistance`. Defaults to
            50.0.
        k_s (float, optional): Soil-drying sensitivity parameter. Passed to
            :func:`estimate_soil_surface_resistance`. Defaults to 4.0.
        soil_heat_flux (float, optional): Soil heat flux in W/m². Positive
            values represent energy transferred into the soil. Defaults to 0.0.

    Returns:
        float: Actual evapotranspiration flux in kg m⁻² s⁻¹, numerically
            equivalent to mm/s of water. The result is an instantaneous
            flux and is not accumulated over a time interval.

    Raises:
        ValueError: If any input violates the physical or mathematical
            constraints enforced by the underlying calculations.

    Notes:
        If ``t_surface`` is ``None``, ``t_air`` is used as the surface
        temperature.

        ``t_surface`` is used by :func:`net_radiation`,
        :func:`saturation_vapor_pressure_derivative`, and
        :func:`soil_surface_vapor_pressure_deficit`. ``t_air`` is used
        for :func:`specific_heat_capacity_air`,
        :func:`psychrometric_constant`,
        :func:`latent_heat_of_vaporisation_water`, and
        :func:`dry_air_density`.

        ``solar_rad`` and ``soil_heat_flux`` are supplied as energy fluxes
        in W/m². Consequently, :func:`net_radiation` and
        :func:`penman_monteith` operate on an instantaneous flux basis.

        Negative values are possible and represent a negative latent-water
        flux under the sign convention used by :func:`penman_monteith`.
    """
    # pylint: disable=invalid-name
    if t_surface is None:
        t_surface = t_air

    c_p = specific_heat_capacity_air(T=t_air, RH=RH, P=baro)

    delta = saturation_vapor_pressure_derivative(t_surface)
    net_solar = net_radiation_flux(R_s=solar_rad,
                                   T_a_C=t_air,
                                   T_s_C=t_surface,
                                   albedo=albedo)

    # Soil heat flux is supplied as an instantaneous energy flux.
    G = soil_heat_flux
    vpd = soil_surface_vapor_pressure_deficit(
        T_air=t_air,
        RH=RH,
        T_surface=t_surface
    )

    # Use air temperature for latent heat, gamma and air density as they are coupled
    # due to psychrometric constant
    gamma = psychrometric_constant(P=baro, temp=t_air, RH=RH)
    latent_heat = latent_heat_of_vaporisation_water(temp=t_air)
    air_density = total_air_density(RH=RH, T=t_air, Pa=baro)

    res_aero = aerodynamic_resistance(u=wind_spd, z_u=z_u, z_h=z_h)
    res_surface = estimate_soil_surface_resistance(vwc=vwc,
                                                   theta_fc=theta_fc,
                                                   theta_evap_min=theta_evap_min,
                                                   rs_min=rs_min,
                                                   k_s=k_s)

    return penman_monteith(delta=delta,
                           Rn=net_solar,
                           G=G,
                           vpd=vpd,
                           r_a=res_aero,
                           r_s=res_surface,
                           gamma=gamma,
                           lambda_=latent_heat,
                           rho_a=air_density,
                           c_p=c_p)
