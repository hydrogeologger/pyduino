"""Atmospheric thermodynamic calculations used by environmental models.

Provides functions for calculating water-vapour properties, air density,
specific heat capacity, latent heat, and psychrometric properties required
by evapotranspiration models.
"""
import math as _math

# pylint: disable-next=unused-import
from ..conversion import (
    celsius_to_kelvin,
)

# pylint: disable=consider-using-f-string

def saturation_vapor_pressure(T):  # pylint: disable=invalid-name
    # type: (float) -> float
    """Calculate the saturation vapor pressure (e_s) at a given temperature.

    Uses Tetens/Magnus-style equation.

    e_s(T) = 0.6108 * exp( (17.27 * T) / (T + 237.3) )

    Where:
    - e_s = Saturation Vapor Pressure (kPa)
    - T = Temperature (°C)

    Args:
        T (float): Temperature in degrees Celsius (°C)

    Returns:
        float: Saturation vapor pressure in Pascal (Pa)
    """
    # pylint: disable-next=invalid-name
    e_s_kPa = 0.6108 * _math.exp((17.27 * T) / (T + 237.3))
    return e_s_kPa * 1000  # Convert kPa to Pa


def partial_vapor_pressure(T, RH):  # pylint: disable=invalid-name
    # type: (float, float) -> float
    """Calculate the actual vapor pressure (e_a) of air.

    e_a = (RH / 100) * e_s

    Where
    - e_s = Saturation Vapor Pressure (Pa)
    - RH = Relative Humidity [0-100] (%)
    - e_a = Actual vapor pressure (Pa)

    Args:
    - T (float): Temperature of air in degrees Celsius.
    - RH (float): Relative Humidity as a percentage.

    Returns:
        float: Actual vapor pressure in Pascals.

    Raises:
        ValueError: If RH is outside the range [0, 100].
    """
    _validate_relative_humidity(RH)

    # pylint: disable-next=invalid-name
    e_s = saturation_vapor_pressure(T)

    # Actual vapor pressure calculation
    return e_s * (RH / 100.0)


def vapor_pressure_deficit(T_air, RH):  # pylint: disable=invalid-name
    # type: (float, float) -> float
    """Atmospheric VPD at air temperature.

    Args:
        T_air (float): Air Temperature in degrees Celsius (°C)
        RH (float): Relative Humidity [0-100] (%)

    Returns:
        float: Vapour pressure deficit (Pa).
    """
    return (saturation_vapor_pressure(T_air) - partial_vapor_pressure(T_air, RH))


def soil_surface_vapor_pressure_deficit(T_air, RH, T_surface=None):  # pylint: disable=invalid-name
    # type: (float, float, float|None) -> float
    """Calculate vapor pressure deficit at the soil surface.

    The actual vapour pressure is calculated from air temperature and
    relative humidity, while saturation vapour pressure is calculated
    at the soil surface temperature.

    Args:
        T_air (float): Air Temperature in degrees Celsius (°C)
        RH (float): Relative Humidity [0-100] (%)
        T_gnd (float, optional): Soil/surface temperature in degrees Celsius (°C).
            If None, air temperature is used. Defaults to None.

    Returns:
        float: Soil-surface vapour pressure deficit (Pa).

    Notes:
        The calculation is:

            VPD_surface = e_s(T_surface) - e_a(T_air, RH)

        where:

            e_s(T_surface) = saturation vapour pressure at the surface
            e_a(T_air, RH) = actual atmospheric vapour pressure
    """
    if T_surface is None:
        T_surface = T_air

    e_actual = partial_vapor_pressure(T=T_air, RH=RH)
    e_s_surface = saturation_vapor_pressure(T=T_surface)

    return e_s_surface - e_actual


def saturation_vapor_pressure_derivative(temp):
    # type: (float) -> float
    """Calculate the slope of the saturation vapor pressure curve (Δ) at a given temperature.

    The slope is the rate of change of saturation vapor pressure with respect to temperature.

    delta = (4098 * e_s) / (T + 237.3)^2

    Where:
    - e_s = Saturation Vapor Pressure (kPa)
    - T = Temperature (°C)

    This is used in the Penman-Monteith equation for evapotranspiration.

    Args:
        temp (float): Temperature in degrees Celsius (°C).

    Returns:
        float: Slope of the saturation vapor pressure curve in Pa/°C,
            dimensionally equivalent to Pa K⁻¹.
    """
    # pylint: disable-next=invalid-name
    e_s = saturation_vapor_pressure(temp)

    # Slope formula for saturation vapor pressure curve calculation
    delta = (4098 * e_s) / (temp + 237.3)**2
    return delta


def dry_air_density(T=20, Pa=101325.0):  # pylint: disable=invalid-name
    # type: (float, float) -> float
    """Calculate dry air density

    Uses Ideal Gas Law.

    Args:
        T (float, optional): Air Temperature in degrees Celsius (°C). Defaults to 20 °C
        Pa (float, optional): Air pressure in Pascals (Pa). Defaults to 101325 Pa.

    Returns:
        float: Dry air density (kg/m³).
    """
    # pylint: disable=invalid-name
    R_DRYAIR = 287.05  # specific gas constant for dry air (J/kg/K)
    return Pa / (R_DRYAIR * celsius_to_kelvin(T))


def total_air_density(RH, T, Pa=101325.0):  # pylint: disable=invalid-name
    # type: (float, float, float|None) -> float
    """Calculate moist-air density using the ideal gas law.

    The density is calculated from the dry-air density corrected for
    the presence of water vapour:

        rho = P / (R_d T) *
              [1 - (e_a / P) * (1 - R_d / R_v)]

    which is equivalent to:

        rho = (P - e_a) / (R_d T) + e_a / (R_v T)

    where:
        rho = moist-air density [kg/m³]
        P   = total atmospheric pressure [Pa]
        e_a = actual water-vapour partial pressure [Pa]
        T   = air temperature [K]
        R_d = specific gas constant for dry air [J/(kg·K)]
        R_v = specific gas constant for water vapour [J/(kg·K)]

    Args:
        RH (float): Relative humidity [0-100] (%).
        T (float): Air Temperature in degrees Celsius (°C).
        Pa (float, optional): Air pressure in Pascals (Pa). Defaults to 101325 Pa.

    Returns:
        float: Moist-air density (kg/m³).

    Raises:
        ValueError: If atmospheric pressure is not positive or relative
            humidity is outside the range [0, 100].
    """
    # pylint: disable=invalid-name
    _validate_pressure(Pa)

    R_DRYAIR = 287.05  # specific gas constant for dry air (J/kg/K)
    R_VAPOUR = 461.5  # specific gas constant for water vapour (J/kg/K)
    compensation = 1 - (
        partial_vapor_pressure(T, RH) / Pa) * (1 - (R_DRYAIR / R_VAPOUR))
    return dry_air_density(T, Pa) * compensation


def calculate_specific_humidity(RH, T, P):
    """Calculate specific humidity from relative humidity.

    Equations:
        eₐ = (RH / 100) × eₛ

        q = (ε × eₐ) / [P − (1 − ε) × eₐ]

    where:
        RH = relative humidity [%]
        T  = air temperature [°C]
        P  = atmospheric pressure [Pa]
        eₛ = saturation vapor pressure [Pa]
        eₐ = actual water-vapor partial pressure [Pa]
        q  = specific humidity [kg/kg]
        ε  = ratio of molecular weight of water vapor to dry air (= 0.622)

    Args:
        RH (float): Relative humidity [%], from 0 to 100.
        T (float): Air temperature [°C].
        P (float): Atmospheric pressure [Pa].

    Returns:
        float: Specific humidity [kg/kg].

    Raises:
        ValueError: If ``P`` is not positive.
    """
    # pylint: disable=invalid-name
    _validate_pressure(P)

    EPSILON = 0.622  # Ratio of molecular mass of water vapor to dry air

    # Actual water-vapor partial pressure [Pa]
    e_a = partial_vapor_pressure(T=T, RH=RH)

    # Specific humidity [kg/kg]
    q = (EPSILON * e_a) / (P - (1 - EPSILON) * e_a)

    return q


def specific_heat_capacity_air(T, RH=None, P=101325.0):  # pylint: disable=invalid-name
    # type: (float, float|None, float) -> float
    """Calculate the specific heat capacity of air (c_p).

    If RH is provided, calculates moist air specific heat capacity.
        c_p = c_p_dry + 1820 * omega
        omega = 0.622 * e_a / (P - e_a)

    If RH=0, is omitted or None, defaults to dry air specific heat capacity.
        c_p = c_p_dry = 1005 + 0.1 * (T - 25)

    Where:
    - c_p = Specific heat capacity of the air mixture (J/kg·°C)
    - c_p_dry = Dynamic specific heat capacity of dry air (J/kg·°C)
    - omega = Humidity ratio (kg_water / kg_dry_air)
    - e_a = Actual vapor pressure (Pa)
    - P = Total atmospheric pressure (Pa)
    - T = Air temperature (°C)
    - RH = Relative Humidity (%)

    Args:
        T (float): Temperature of air in degrees Celsius (°C).
        RH (float, optional): Relative Humidity as a percentage [0-100] (%).
                              Defaults to None (dry air).
        P (float, optional): Atmospheric pressure in Pascals (Pa). 
                             Defaults to standard sea-level pressure (101325.0 Pa).

    Returns:
        float: Specific heat capacity of air in Joules per kilogram 
               per degree Celsius (J kg^-1 °C^-1).

    Raises:
        ValueError: If relative humidity is outside the range [0, 100],
            atmospheric pressure is less than or equal to zero, or actual
            vapor pressure is greater than or equal to atmospheric pressure.
    """
    # pylint: disable=invalid-name

    _validate_pressure(P)

    # Base value of air specific capacity (dry) at 25°C
    air_base_cp_dry = 1005.0
    # Temperature-dependent change in specific heat
    cp_dry_temperature_adjustment = 0.1 * (T - 25)

    # 1. Calculate the specific heat capacity of dry air (baseline) at  this temperature
    c_p_dry = air_base_cp_dry + cp_dry_temperature_adjustment

    # 2. If no humidity is specified, return the dry air value immediately
    if RH is None or RH == 0.0:
        return c_p_dry

    # 3. Calculate the moist air contribution if RH is provided
    e_a = partial_vapor_pressure(T, RH)

    if e_a >= P:
        raise ValueError(
            "Actual vapor pressure cannot exceed total atmospheric pressure.")

    # Calculate humidity ratio (omega)
    omega = 0.622 * e_a / (P - e_a)

    # Return total specific heat of the moist air mixture
    # 1820.0 J/(kg*°C) is the specific heat capacity of water vapor
    return c_p_dry + (1820.0 * omega)


def latent_heat_of_vaporisation_water(temp):
    # type: (float) -> float
    """Calculate latent heat of vaporisation for water.

    Args:
        temp (float): Temperature in degrees Celsius (°C)

    Returns:
        float: Latent heat of vaporisation (J/kg)
    """
    latent_heat = 2500250 - (2365 * temp)
    return latent_heat


def psychrometric_constant(P, temp=15, RH=None):  # pylint: disable=invalid-name
    # type: (float, float, float|None) -> float
    """Calculate the psychrometric constant (gamma)

    The psychrometric constant is given by the equation:

    γ = (c_p × P) / (λ × MW_ratio)

    Where:
    - γ is the psychrometric constant in Pa/°C,
    - c_p is the specific heat of dry air at constant pressure typically 1005 (J/(kg·K)),
    - P is the atmospheric pressure in Pa (e.g., 101325 Pa at sea level),
    - λ is the latent heat of vaporization of water in J/kg (e.g., 2.45 × 10⁶ J/kg),
    - MW_ratio is molecular weight ratio of water vapor/dry air = 0.622

    Args:
        P (float): Atmospheric pressure in pascal (Pa)
        temp (float, optional): Temperature in degrees Celsius (°C)
            Defaults to 15 °C.
        RH (float, optional): Relative Humidity as a percentage [0-100] (%).
            Defaults to None (uses dry air c_p baseline).

    Returns:
        float: Psychometric constant in Pa/°C
    """
    # pylint: disable=invalid-name

    c_p = specific_heat_capacity_air(temp, RH=RH, P=P)

    water_vapor_dryair_molecular_wt_ratio = 0.622
    latent_heat = latent_heat_of_vaporisation_water(temp)

    gamma = ((c_p * P) /
             (latent_heat * water_vapor_dryair_molecular_wt_ratio))

    return gamma


def _validate_pressure(P, name="Atmospheric pressure"):  # pylint: disable=invalid-name
    """Validate that pressure is greater than zero."""
    if P <= 0:
        raise ValueError("{} must be greater than zero.".format(name))


def _validate_relative_humidity(RH):   # pylint: disable=invalid-name
    """Validate that relative humidity is within 0-100%."""
    if not 0.0 <= RH <= 100.0:
        raise ValueError("RH must be between 0 and 100%")
