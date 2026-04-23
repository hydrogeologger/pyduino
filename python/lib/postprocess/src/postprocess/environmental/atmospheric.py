"""Atmospheric thermodynamic calculations used by environmental models.

Provides functions for calculating water-vapor properties, air density,
specific heat capacity, latent heat, and psychrometric properties required
by evapotranspiration models.
"""

__all__ = [
    # --- Vapor Pressure & Humidity ---
    "saturation_vapor_pressure_buck",
    "saturation_vapor_pressure_tetens",
    "saturation_vapor_pressure_mean_tetens",
    "actual_vapor_pressure",
    "actual_vapor_pressure_from_extremes",
    "vapor_pressure_deficit",
    "saturation_vapor_pressure_slope_tetens",
    "calculate_specific_humidity",

    # --- Air Density & Psychrometrics ---
    "dry_air_density",
    "total_air_density",
    "specific_heat_capacity_air",
    "latent_heat_of_vaporisation_water",
    "psychrometric_constant",

    # --- Atmospheric & Profile Calculations ---
    "estimate_atmospheric_pressure",
    "calculate_temperature_lapse_rate",
    "wind_speed_at_2m",
]


import math as _math

# pylint: disable-next=unused-import
from ..conversion import (
    celsius_to_kelvin,
)

# pylint: disable=consider-using-f-string


def saturation_vapor_pressure_buck(T):
    # type: (float) -> float
    # pylint: disable=invalid-name
    """Calculate saturation vapor pressure (e_s) at a given temperature using the Buck equation.

    The Buck equation is an empirical approximation of saturation vapor
    pressure over water. It provides a highly accurate approximation for
    temperatures above 0 °C and is more accurate than the Tetens equation,
    particularly at higher temperatures.

    e_s(T) = 0.61121 * exp((18.678 - T / 234.5) * T / (257.14 + T))

    Where:
    - e_s = Saturation Vapor Pressure (kPa)
    - T = Temperature (°C)

    Args:
        T (float): Temperature in degrees Celsius (°C).

    Returns:
        float: Saturation Vapor Pressure in Pascal (Pa).

    Raises:
        ValueError: If ``T`` is not finite.

    See Also:
        :func:`saturation_vapor_pressure_tetens`

    References:
        - https://en.wikipedia.org/wiki/Vapour_pressure_of_water
    """
    if not _math.isfinite(T):
        raise ValueError("temperature must be finite.")
    e_s_kPa = 0.61121 * _math.exp((18.678 - (T/234.5)) * (T/(257.14+T)))
    return e_s_kPa * 1000.0  # Convert kPa to Pa


def saturation_vapor_pressure_tetens(T):
    # type: (float) -> float
    """Calculate the saturation vapor pressure (e_s) at a given temperature using
        the Tetens equation.

    Uses the Tetens equation, which provides a good approximation of
    saturation vapor pressure over liquid water, particularly for
    temperatures between 0 and 50 °C.

    e_s(T) = 0.6108 * exp( (17.27 * T) / (T + 237.3) )

    Where:
    - e_s = Saturation Vapor Pressure (kPa)
    - T = Temperature (°C)

    Args:
        T (float): Temperature in degrees Celsius (°C)

    Returns:
        float: Saturation Vapor Pressure in Pascal (Pa)

    Raises:
        ValueError: If ``T`` is not finite.

    Note:
        Due to the non-linearity of the equation, mean saturation vapor
        pressure over a period should be calculated as the mean of the
        saturation vapor pressures at the period's mean minimum and
        maximum air temperatures. See :func:`saturation_vapor_pressure_mean`.

    See Also:
        :func:`saturation_vapor_pressure_buck`

    References:
        - https://www.fao.org/4/X0490E/x0490e07.htm#measurement
        - https://en.wikipedia.org/wiki/Vapour_pressure_of_water
    """
    # pylint: disable=invalid-name
    if not _math.isfinite(T):
        raise ValueError("temperature must be finite.")
    e_s_kPa = 0.6108 * _math.exp((17.27 * T) / (T + 237.3))
    return e_s_kPa * 1000.0  # Convert kPa to Pa


def saturation_vapor_pressure_mean_tetens(tmin, tmax):
    # type: (float, float) -> float
    """Calculate the mean saturation vapor pressure using the Tetens equation.

    Mean saturation vapor pressure is calculated from the saturation vapor
    pressures at the daily minimum and maximum air temperatures. Using mean
    air temperature directly can underestimate the mean saturation vapor
    pressure due to the non-linearity of the saturation vapor pressure
    equation.

    e_s = (e_s[T_max] + e_s[T_min]) / 2

    Where:
    - e_s[T_max] = Saturation Vapor Pressure at maximum temperature.
    - e_s[T_min] = Saturation Vapor Pressure at minimum temperature.

    Args:
        tmin (float): Minimum temperature in degrees Celsius (°C)
        tmax (float): Maximum temperature in degrees Celsius (°C)

    Returns:
        float: Mean saturation vapor pressure in Pascal (Pa)

    See Also:
        :func:`saturation_vapor_pressure_tetens`
    """
    e_s_mean_pa = (
        saturation_vapor_pressure_tetens(tmax)
        + saturation_vapor_pressure_tetens(tmin)
    ) / 2.0
    return e_s_mean_pa


def actual_vapor_pressure(T, RH):
    # type: (float, float) -> float
    """Calculate actual vapor pressure (e_a), also known as
    partial vapor pressure of water vapor.

    e_a = (RH / 100) * e_s

    Where
    - e_s = Saturation Vapor Pressure (Pa)
    - RH = Relative Humidity [0-100] (%)
    - e_a = Actual vapor pressure (Pa)

    Args:
        T (float): Temperature of air in degrees Celsius. Typical minimum temperature.
        RH (float): Relative Humidity as a percentage (0-100). Typical RH max.

    Returns:
        float: Actual vapor pressure in Pascals.

    Raises:
        ValueError: If RH is outside the range [0, 100].

    Note:
        For daily estimates of actual vapor pressure, this function can be
        evaluated at the daily minimum temperature and maximum relative
        humidity when only RH_max is available. See
        :func:`actual_vapor_pressure_from_extremes`.
    """
    # pylint: disable=invalid-name
    _validate_relative_humidity(RH)

    e_s = saturation_vapor_pressure_tetens(T)

    # Actual vapor pressure calculation
    return e_s * (RH / 100.0)


def actual_vapor_pressure_from_extremes(temperature, relative_humidity):
    # type: (tuple[float, float], tuple[float, float]) -> float
    """Calculate actual vapor pressure (e_a) from temperature and RH extremes

    This function implements the standard FAO-56 Equation 17. It pairs the maximum 
    relative humidity with the minimum temperature (when the air is closest to saturation), 
    and the minimum relative humidity with the maximum temperature.

    e_a = (e_a[T_min, RH_max] + e_a[T_max, RH_min]) / 2

    Where
    - e_a[T_min, RH_max] = Actual vapor pressure (Pa) at daily minimum temperature,
        maximum relative humidity (0-100%).
    - e_a[T_max, RH_min]) = Actual vapor pressure (Pa) at daily maximum temperature,
        minimum relative humidity (0-100%).

    Args:
        temperature: Minimum and maximum air temperature in degrees Celsius (°C),
            as ``(tmin, tmax)``.
        relative_humidity: Minimum and maximum relative humidity in percent (0-100%),
            as ``(rh_min, rh_max)``.

    Returns:
        float: Actual vapor pressure in Pascals.

    Raises:
        ValueError: If maximum values are less than minimum values, 
            or if relative humidity values fall outside.

    Notes:
        FAO-56 provides several methods for estimating daily actual vapor
        pressure depending on the available relative humidity data:

        - When both RH_min and RH_max are available, Equation 17 is used:

            ``e_a = (e_a[T_min, RH_max] + e_a[T_max, RH_min]) / 2``

        - When RH_min is unavailable or its estimate is unreliable, Equation 18
            uses only RH_max:

            ``e_a = e_a[T_min, RH_max]``

            See :func:`actual_vapor_pressure`.

        - When only mean relative humidity is available, Equation 19 can be used:

            ``e_a = (RH_mean / 100) * e_s_mean``

            where ``e_s_mean`` is the mean saturation vapor pressure calculated
            from the daily minimum and maximum air temperatures. See
            :func:`saturation_vapor_pressure_mean_tetens`.

    References:
        - https://www.fao.org/4/X0490E/x0490e07.htm#measurement
    """
    # pylint: disable=invalid-name
    if len(temperature) != 2:
        raise ValueError("temperature must contain (tmin, tmax).")

    if len(relative_humidity) != 2:
        raise ValueError("relative_humidity must contain (rh_min, rh_max).")

    tmin, tmax = temperature
    rh_min, rh_max = relative_humidity

    if tmax < tmin:
        raise ValueError("tmax ({tmax}°C) cannot be less than tmin ({tmin}°C).".format(
            tmax=tmax,
            tmin=tmin,
        ))

    if rh_max < rh_min:
        raise ValueError("rh_max ({rh_max}%) cannot be less than rh_min ({rh_min}%).".format(
            rh_max=rh_max,
            rh_min=rh_min,
        ))

    e_a_tmin = actual_vapor_pressure(T=tmin, RH=rh_max)
    e_a_tmax = actual_vapor_pressure(T=tmax, RH=rh_min)

    # Actual vapor pressure calculation
    return (e_a_tmin + e_a_tmax) / 2.0


def vapor_pressure_deficit(temperature, RH):
    # type: (float|tuple[float,float], float|tuple[float,float]) -> float
    """Calculate vapor pressure deficit (VPD).

    VPD is the difference between saturation and actual vapor pressure:

        VPD = e_s - e_a

    For a single air temperature and relative humidity, VPD is calculated
    at that temperature.

    For period minimum and maximum air temperatures, ``temperature`` may
    be provided as ``(tmin, tmax)``. The method used to estimate actual
    vapor pressure depends on the available relative humidity data:

    - With minimum and maximum relative humidity, FAO-56 Equation 17 is
      used to estimate actual vapor pressure. See
      :func:`actual_vapor_pressure_from_extremes`.

    - With maximum relative humidity only, FAO-56 Equation 18 is used to
      estimate actual vapor pressure. In this case, scalar
      ``RH`` is interpreted as RH_max, and actual vapor
      pressure is calculated at the period minimum temperature. See
      :func:`actual_vapor_pressure`.

    Args:
        temperature (float or tuple): Air temperature in degrees Celsius (°C), or period
            minimum and maximum air temperatures as ``(tmin, tmax)``.
        RH (float or tuple): Relative humidity as a percentage (0-100%), or
            minimum and maximum relative humidity as ``(rh_min, rh_max)``.
            When ``temperature`` contains minimum and maximum values and
            this is scalar, it is interpreted as maximum relative humidity
            (RH_max).

    Returns:
        float: Vapor pressure deficit in Pascal (Pa).

    Raises:
        ValueError: If temperature or relative humidity inputs are invalid.

    References:
        FAO-56, Equations 17 and 18.
        - https://www.fao.org/4/X0490E/x0490e07.htm#air%20humidity
        - https://www.fao.org/4/X0490E/x0490e07.htm#calculation%20procedures
    """
    # pylint: disable=invalid-name
    temperature_is_extremes = isinstance(temperature, (tuple, list))
    relative_humidity_is_extremes = isinstance(
        RH, (tuple, list)
    )

    if not temperature_is_extremes:
        if relative_humidity_is_extremes:
            raise ValueError(
                "relative_humidity must be scalar when temperature is scalar."
            )

        return (
            saturation_vapor_pressure_tetens(temperature)
            - actual_vapor_pressure(temperature, RH)
        )

    if len(temperature) != 2:
        raise ValueError("temperature must contain (tmin, tmax).")

    tmin, tmax = temperature
    if tmax < tmin:
        raise ValueError(
            "tmax ({tmax}°C) cannot be less than tmin ({tmin}°C).".format(
                tmax=tmax,
                tmin=tmin,
            )
        )

    e_s_mean = saturation_vapor_pressure_mean_tetens(tmin, tmax)

    if relative_humidity_is_extremes:
        if len(RH) != 2:
            raise ValueError(
                "relative_humidity must contain (rh_min, rh_max)."
            )
        e_a = actual_vapor_pressure_from_extremes(
            temperature,
            RH,
        )
    else:
        e_a = actual_vapor_pressure(T=tmin, RH=RH)

    return e_s_mean - e_a


def saturation_vapor_pressure_slope_tetens(temperature):
    # type: (float|tuple[float, float]) -> float
    """Calculate the slope of the saturation vapor pressure curve (Δ) with respect
    to temperature using the Tetens equation.

    The slope is the derivative of saturation vapor pressure with
    respect to temperature:

        de_s/dT = 4098 * e_s(T) / (T + 237.3)^2

    For a single temperature, the derivative is evaluated at that
    temperature.

    For minimum and maximum temperatures, the slope is evaluated
    at the mean temperature:

        T_mean = (T_min + T_max) / 2

    Where:
    - e_s(T) = Saturation Vapor Pressure at temperature T (Pa)
    - T = Temperature (°C)
    - de_s/dT or Δ = Slope of the saturation vapor pressure curve (Pa/°C)

    This is used in the Penman-Monteith equation for evapotranspiration.

    Args:
        temperature (float or tuple): Temperature in degrees Celsius (°C),
            or minimum and maximum temperatures as ``(tmin, tmax)``.

    Returns:
        float: Slope of the saturation vapor pressure curve in Pa/°C,
            dimensionally equivalent to Pa K⁻¹.

    Raises:
        ValueError: If ``temperature`` is a tuple or list that does not
            contain exactly two values.

    References:
        - https://www.fao.org/4/X0490E/x0490e07.htm#calculation%20procedures
    """
    # pylint: disable=invalid-name
    if isinstance(temperature, (tuple, list)):
        if len(temperature) != 2:
            raise ValueError("temperature must contain (tmin, tmax).")

        T = sum(temperature) / 2.0
    else:
        T = temperature

    e_s = saturation_vapor_pressure_tetens(T=T)

    # Slope formula for saturation vapor pressure curve calculation
    delta = (4098.0 * e_s) / ((T + 237.3)**2)
    return delta


def dry_air_density(T=20, Pa=101325.0):
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


def total_air_density(RH, T, Pa=101325.0):
    # type: (float, float, float|None) -> float
    """Calculate moist-air density using the ideal gas law.

    The density is calculated from the dry-air density corrected for
    the presence of water vapor:

        rho = P / (R_d T) *
              [1 - (e_a / P) * (1 - R_d / R_v)]

    which is equivalent to:

        rho = (P - e_a) / (R_d T) + e_a / (R_v T)

    where:
        rho = moist-air density [kg/m³]
        P   = total atmospheric pressure [Pa]
        e_a = actual water-vapor partial pressure [Pa]
        T   = air temperature [K]
        R_d = specific gas constant for dry air [J/(kg·K)]
        R_v = specific gas constant for water vapor [J/(kg·K)]

    Args:
        RH (float): Relative humidity [0-100] (%).
        T (float): Air Temperature in degrees Celsius (°C).
        Pa (float, optional): Air pressure in Pascals (Pa). Defaults to 101325 Pa.

    Returns:
        float: Moist-air density (kg/m³).

    Raises:
        ValueError: If atmospheric pressure is not finite or positive, or if
            relative humidity is not finite or is outside the range 0-100%.
    """
    # pylint: disable=invalid-name
    _validate_pressure(Pa)

    R_DRYAIR = 287.05  # specific gas constant for dry air (J/kg/K)
    R_VAPOR = 461.5  # specific gas constant for water vapor (J/kg/K)
    compensation = 1 - (
        actual_vapor_pressure(T, RH) / Pa) * (1 - (R_DRYAIR / R_VAPOR))
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
        ValueError: ValueError: If atmospheric pressure is not finite or positive, or if
            relative humidity is not finite or is outside the range 0-100%.
    """
    # pylint: disable=invalid-name
    _validate_pressure(P)

    EPSILON = 0.622  # Ratio of molecular mass of water vapor to dry air

    # Actual water-vapor partial pressure [Pa]
    e_a = actual_vapor_pressure(T=T, RH=RH)

    # Specific humidity [kg/kg]
    q = (EPSILON * e_a) / (P - (1 - EPSILON) * e_a)

    return q


def specific_heat_capacity_air(T, RH=None, P=101325.0):
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
        ValueError:
            - If relative humidity is not finite or is outside the range
                0-100%.
            - If atmospheric pressure is not finite or is not positive.
            - If actual vapor pressure is greater than or equal to atmospheric
                pressure.
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
    e_a = actual_vapor_pressure(T, RH)

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


def psychrometric_constant(P, temp=15, RH=None):
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
             (water_vapor_dryair_molecular_wt_ratio * latent_heat))

    return gamma


def calculate_temperature_lapse_rate(T_2, z_2, T_1=15, z_1=0):
    # type: (float, float, float, float) -> float
    """Calculate the atmospheric temperature lapse rate.

    The temperature lapse rate L describes the rate at which atmospheric
    temperature changes with altitude.

    The equation is:

        L = (T_1 - T_2) / (z_2 - z_1)

    Default starting conditions as defined by International Standard Atmosphere (ISA).

    Args:
        T_2 (float): Temperature at the second measurement point in degrees Celsius.
        z_2 (float): Altitude of the second measurement point in meters.
        T_1 (float, optional): Temperature at the first measurement point
            in degrees Celsius. Defaults to 15 K.
        z_1 (float, optional): Altitude of the first measurement point in meters.
            Defaults to 0 m (Sea Level).

    Returns:
        Temperature lapse rate `L` in Celsius per meter.
    """
    # pylint: disable=invalid-name
    T_1 = celsius_to_kelvin(T_1)
    T_2 = celsius_to_kelvin(T_2)

    if z_1 == z_2:
        raise ValueError("z_1 and z_2 must be different.")

    return (T_1 - T_2) / (z_2 - z_1)


def wind_speed_at_2m(wind_speed, measurement_height):
    # type: (float, float) -> float
    """Convert wind speed measured at a given height to wind speed at 2 m.

    Uses the FAO-56 wind profile relationship:

        u_2 = u_z * 4.87 / ln(67.8z - 5.42)

    Where:
    - u_2 = Wind speed at 2 m above ground (m/s)
    - u_z = Wind speed measured at height z (m/s)
    - z = Height of wind measurement above ground (m)

    Args:
        wind_speed (float): Wind speed measured at the specified height,
            in metres per second (m/s).
        measurement_height (float): Height of the wind speed measurement
            above ground, in metres (m).

    Returns:
        float: Wind speed at 2 m above ground, in metres per second (m/s).

    Raises:
        ValueError: If ``wind_speed`` or ``measurement_height`` is not
            finite, or if ``measurement_height`` is not valid for the
            wind profile relationship.

    References:
        - https://www.fao.org/4/X0490E/x0490e07.htm#wind%20profile%20relationship
    """
    if not _math.isfinite(wind_speed):
        raise ValueError("wind speed must be finite.")

    if not _math.isfinite(measurement_height):
        raise ValueError("measurement height must be finite.")

    if measurement_height <= 0:
        raise ValueError("measurement height must be greater than zero.")

    log_argument = 67.8 * measurement_height - 5.42

    if log_argument <= 0:
        raise ValueError(
            "measurement height is too low for the wind profile relationship."
        )

    return (
        wind_speed * 4.87
        / _math.log(log_argument)
    )


def estimate_atmospheric_pressure(z, P_0=101325.0, T_0=15, L=0.0065):
    # type: (float, float, float, float) -> float
    """Estimate atmospheric pressure at altitude z.

    Uses the barometric equation derived from the ideal gas law and
    hydrostatic equilibrium, assuming a constant temperature lapse rate.

    The equation is:

        P(z) = P_0 * ((T_0 - L * z) / T_0) ** (M * g / R * L)

    Where:
        (M * g / R * L) is approximately: 5.256
        - M — molar mass of dry air, approximately 0.0289644 kg/mol
        - g — gravitational acceleration, approximately 9.80665 m/s²
        - R — universal gas constant, 8.31446 J/(mol·K)
        - L — temperature lapse rate, typically 0.0065 K/m (6.5 K/km) in the standard atmosphere

    Args:
        z: Altitude z above sea level in meters.
        P_0: Sea-level atmospheric pressure P_0 in pascals.
        T_0: Sea-level temperature T_0 in degrees Celsius.
        L: Temperature lapse rate L in degrees Celsius per meter.

    Returns:
        Estimated atmospheric pressure P(z) in pascals.

    Raises:
        ValueError: If the calculated temperature is less than or equal
            to zero Kelvin.
    """
    # pylint: disable=invalid-name
    T_0 = celsius_to_kelvin(T_0)

    T = T_0 - L * z
    if T <= 0:
        raise ValueError("Calculated temperature must be greater than zero.")

    M = 0.0289644  # Molar mass of dry air, (kg/mol)
    g = 9.80665  # gravitational acceleration, (m/s²)
    R = 8.31446  # universal gas constant, (J/(mol·K))

    return P_0 * (T / T_0) ** ((M * g) / (R * L))


def _validate_pressure(P, name="Atmospheric pressure"):
    """Validate that pressure is finite and greater than zero."""
    # pylint: disable=invalid-name
    if not _math.isfinite(P):
        raise ValueError("{} must be finite.".format(name))
    if P <= 0:
        raise ValueError("{} must be greater than zero.".format(name))


def _validate_relative_humidity(RH):
    """Validate that relative humidity is finite and within 0-100%."""
    # pylint: disable=invalid-name
    if not _math.isfinite(RH):
        raise ValueError("relative humidity must be finite.")
    if not 0.0 <= RH <= 100.0:
        raise ValueError("relative humidity must be between 0 and 100%")
