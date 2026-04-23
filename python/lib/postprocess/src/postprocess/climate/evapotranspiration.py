"""postprocess climate evapotranspiration module"""

import math as _math


def kelvin_to_celsius(val):
    """Convert temperature from Kelvin to Celsius"""
    return val - 273.15


def celsius_to_kelvin(val):
    """Convert temperature from Celsius to Kelvin"""
    return val + 273.15


def dry_air_density(Ta=20, Pa=101325):  # pylint: disable=invalid-name
    # type: (float, float) -> float
    """Calculate dry air density

    Uses Ideal Gas Law.

    Args:
        Ta (float, optional): Air Temperature in degrees Celsius (°C). Defaults to 20 °C
        Pa (float, optional): Air pressure in Pascals (Pa). Defaults to 101325 Pa.

    Returns:
        float: Dry air density (kg/m³).
    """
    # pylint: disable=invalid-name
    R_dryair = 287.05  # specific gas constant for dry air (J/kg/K)
    return Pa / (R_dryair * celsius_to_kelvin(Ta))


def total_air_density(Ta, Pa, RH):  # pylint: disable=invalid-name
    # type: (float, float, float|None) -> float
    """Calculate total air density

    Uses Ideal Gas Law.

    Args:
        Ta (float, optional): Air Temperature in degrees Celsius (°C).
        Pa (float, optional): Air pressure in Pascals (Pa).
        RH (float, optional): Relative humidity [0-100] (%).

    Returns:
        float: Dry air density (kg/m³).
    """
    # pylint: disable=invalid-name
    R_dryair = 287.05  # specific gas constant for dry air (J/kg/K)
    R_vapour = 461.5  # specific gas constant for water vapour (R_dryairJ/kg/K)
    compensation = 1 - (
        partial_vapor_pressure(Ta, RH) / Pa) * (R_dryair / R_vapour)
    return dry_air_density(Ta, Pa) * compensation


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


def air_specific_heat_capacity(Ta):  # pylint: disable=invalid-name
    # type: (float) -> float
    """Calculate the specific heat capacity of dry air at constant pressure (C_p) 
    as a function of temperature in Celsius using an empirical equation.

    The specific heat capacity is given by the equation:
    C_p(T) = 1005 + 0.1 * (T - 25)

    Args:
        Ta (float): The temperature in Celsius (°C).

    Returns:
        float: The specific heat capacity of air in J/kg·K at the given temperature.

    Example:
        >>> calculate_specific_heat(30)
        1005.5
    """
    # Base value of C_p at 25°C
    base_cp = 1005

    # Temperature-dependent change in specific heat
    temperature_adjustment = 0.1 * (Ta - 25)

    # Calculate and return the specific heat at temperature T
    return base_cp + temperature_adjustment


def penman_monteith(delta, Rn, G, vpd, R_a, R_s, gamma, _lambda, rho_a=1.204):  # pylint: disable=invalid-name
    # type: (float, float, float, float, float, float, float, float, float) -> float
    """Compute evapotranspiration rate using the Penman–Monteith equation (resistance form).

    High level Structure:

        ET=(energy term)+(aerodynamic term)

    Penman–Monteith equation (explicit factorised form)

        ET = (1 / λ) * [
            ((Rₙ - G) * Δ) / (Δ + γ * (1 + rₛ / rₐ))
            + (ρₐ * cₚ * (VPD / rₐ)) / (Δ + γ * (1 + rₛ / rₐ)
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
        ρₐ  = dry air density (kg/m³) (≈ 1.204 kg/m³ at 20°C at sea level)
        cₚ  = specific heat of air (J/kg/°C) (≈ 1013 J/kg/°C)
        VPD = vapour pressure deficit (eₛ - eₐ)
            eₛ = Saturation vapor pressure
            eₐ = Actual vapor pressure of the air
        rₐ  = aerodynamic resistance
        rₛ  = surface (canopy) resistance
        γ   = psychrometric constant

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
        R_a (float): rₐ, aerodynamic resistance (s/m).
        R_s (float): rₛ, surface (canopy) resistance (s/m).
        gamma (float): γ, psychrometric constant (Pa/°C).
        _lambda (float): λ, latent heat of vaporisation (J/kg).
        rho_a (float, optional): ρₐ, dry air density (kg/m³).

    Returns:
        float: ET, evapotranspiration rate in kg m⁻² s⁻¹ (equivalently mm/s).
    """
    if R_a <= 0:
        raise ValueError("aerodynamic_resistance must be > 0")

    if _lambda <= 0:
        raise ValueError("latent_heat_vaporisation must be > 0")

    rho_a = 1.27  # mean air density (kg/m³)

    # pylint: disable-next=invalid-name
    Cp = 1013  # specific heat capacity of dry air (J/kg/°C)

    numerator = ((delta * (Rn - G)) + (rho_a * Cp * (vpd / R_a)))

    denominator = delta + gamma * (1.0 + R_s / R_a)

    return (1.0 / _lambda) * (numerator / denominator)


def fao_penman_monteith(Ta, u_2, delta, Rn, G, vpd, gamma):  # pylint: disable=invalid-name
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
        Ta (float): Mean daily air temperature at 2m height (°C).
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
    """
    numerator = (0.408 * delta * (Rn - G) + gamma *
                 (900 / (Ta + 273)) * u_2 * (vpd))
    denominator = delta + gamma * (1 + 0.34 * u_2)
    return numerator / denominator


def saturation_vapor_pressure(temp):
    # type: (float) -> float
    """Calculate the saturation vapor pressure (E_s) at a given temperature.

    E_s(T) = 0.6108 * exp( (17.27 * T) / (T + 237.3) )

    Where:
    - E_s = Saturation Vapor Pressure (kPa)
    - T = Temperature (°C)

    Args:
        temp (float): Temperature in degrees Celsius (°C)

    Returns:
        float: Saturation vapor pressure in Pascal (Pa)
    """
    # pylint: disable-next=invalid-name
    E_s_kPa = 0.6108 * _math.exp((17.27 * temp) / (temp + 237.3))
    return E_s_kPa * 1000  # Convert kPa to Pa


def partial_vapor_pressure(Ta, RH):  # pylint: disable=invalid-name
    # type: (float, float) -> float
    """Calculate the actual vapor pressure (E_a) of air.

    E_a = (RH / 100) * E_s

    Where
    - E_s = Saturation Vapor Pressure (kPa)
    - RH = Relative Humidity [0-100] (%)
    - E_a = Actual vapor pressure (kPa)

    Args:
    - Ta (float): Temperature of air in degrees Celsius.
    - RH (float): Relative Humidity as a percentage.

    Returns:
        float: Actual vapor pressure in Pascals.
    """
    # pylint: disable-next=invalid-name
    E_s = saturation_vapor_pressure(Ta)

    # Actual vapor pressure calculation
    return (RH / 100.0) * E_s


def psychrometric_constant(Pa, temp=15):  # pylint: disable=invalid-name
    # type: (float, float) -> float
    """Calculate the psychrometric constant (gamma)


    The psychrometric constant is given by the equation:

    γ = (C_p × P) / (λ × MW_ratio)

    Where:
    - γ is the psychrometric constant in Pa/°C,
    - C_p is the specific heat of dry air at constant pressure typically 1005 (J/(kg·K)),
    - P is the atmospheric pressure in Pa (e.g., 101325 Pa at sea level),
    - λ is the latent heat of vaporization of water in J/kg (e.g., 2.45 × 10⁶ J/kg),
    - MW_ratio is molecular weight ratio of water vapor/dry air = 0.622

    Args:
        Pa (float): Atmospheric pressure in pascal (Pa)
        temp (float): Temperature in degrees Celsius (°C)

    Returns:
        float: Psychometric constant in Pa/°C
    """
    water_vapor_dryair_molecular_wt_ratio = 0.622
    latent_heat = latent_heat_of_vaporisation_water(temp)
    dry_air_specific_heat = 1005

    gamma = (dry_air_specific_heat * Pa) / (latent_heat *
                                            water_vapor_dryair_molecular_wt_ratio)
    return gamma


def aerodynamic_resistance(u, z_m=2, z_h=None, z_om=1e-3, z_oh=None, d=1e-4):
    # type: (float, float, float|None, float, float|None, float) -> float
    """Calculate the aerodynamic resistance (r_a) using the logarithmic wind profile equation.

    The aerodynamic resistance is used to model the resistance to the movement of water vapor from 
    the surface to the atmosphere due to wind friction and surface roughness.

    ra = (ln((z_u - d) / z_om) * ln((z_h - d) / z_oh)) / (k^2 * u)

    Args:
        u (float): Wind speed at height `z_m` (m/s).
            Wind speed at a standard reference height (e.g., 2 m or 10 m).
        z_m (float, optional): Height at which the wind speed is measured (m).
            Typically 2 m or 10 m above ground. Defaults to 2.
        z_h (float, optional): Height at which humidity/temperature is measured (m).
            If not defined, `z_h = z_u`. Defaults to None.
        z_om (float, optional): Roughness length governing momentum transfer (m),
            a measure of how wind or air speed is affected by surface roughness.
            Higher value corresponds to greater resistance.
            Defaults to 1e-3. Common values:
            - Open water: 0.001 - 0.01 m
            - Grassland/Cropland: 0.01 - 0.1 m
            - Forests: 0.1 - 2.0 m
            - Desert or bare rock: 0.001 - 0.1 m
            - 0.123 * vegetation height
        z_oh (float, optional): Roughness length governing transfer of heat and vapor (m),
            a measure of how temperature is exchanged between the surface and air.
            Higher value corresponds to greater resistance.
            Defaults to None. Cmmon Values:
            - Open water: 0.001 - 0.01 m (very smooth, little or no resistance)
            - Grassland/Cropland: 0.01 - 0.1 m
            - Forests: 0.1 - 1.0 m
            - Desert or bare rock: 0.001 - 0.1 m
            - 0.1 * vegetation height
        d (float, optional): Zero plane displacement of the wind profile (m),
            accounts for obstacles like trees or buildings.
            Typically 2/3 * vegetation height for forests/crops, or average
            building height for urban areas. Defaults to 1e-4.

    Returns:
        float: Aerodynamic resistance (r_a) in seconds per meter (s/m).

    Reference:
        https://swatplus.gitbook.io/io-docs/theoretical-documentation/section-2-hydrology/chapter-2-2-evapotranspiration/2-2.2-potential-evapotranspiration/2-2.2.1-penman-monteith-method/2-2.2.1.2-aerodynamic-resistance
    """
    # von Kármán constant (dimensionless)
    k = 0.41

    if z_h is None:
        z_h = z_m
    if z_oh is None:
        z_oh = z_om

    # Calculate the aerodynamic resistance using the logarithmic wind profile equation
    r_a = (_math.log((z_m - d) / z_om) *
           _math.log((z_h - d) / z_oh)) / (k**2 * u)

    return r_a


def saturation_vapor_pressure_derivative(temp):
    # type: (float) -> float
    """Calculate the slope of the saturation vapor pressure curve (Δ) at a given temperature.

    The slope is the rate of change of saturation vapor pressure with respect to temperature.

    delta = (4098 * E_s) / (T + 237.3)^2

    Where:
    - E_s = Saturation Vapor Pressure (kPa)
    - T = Temperature (°C)

    This is used in the Penman-Monteith equation for evapotranspiration.

    Args:
        temp (float): Temperature in degrees Celsius (°C).

    Returns:
        float: Slope of the saturation vapor pressure curve in Pa/°C.
    """
    # pylint: disable-next=invalid-name
    E_s = saturation_vapor_pressure(temp)

    # Slope formula for saturation vapor pressure curve calculation
    delta = (4098 * E_s) / (temp + 237.3)**2
    return delta


def vapor_pressure_deficit(T_air, RH, T_surface=None):  # pylint: disable=invalid-name
    # type: (float, float, float|None) -> float
    """Calculate vapor pressure deficit at soil surface.

    Args:
        T_air (float): Air Temperature in degrees Celsius (°C)
        RH (float): Relative Humidity [0-100] (%)
        T_gnd (float, optional): Air temperature at soil surface in degrees Celsius (°C).
            If None, will fall back to air temperature. Defaults to None.

    Returns:
        _float: Vapor pressure deficit in pascal (Pa).
    """
    if T_surface is None:
        T_surface = T_air
    return (saturation_vapor_pressure(T_surface) - partial_vapor_pressure(T_air, RH))


def net_solar_radiation(R_s, T_a_C, T_s_C=None, albedo=0.2, epsilon=0.875):  # pylint: disable=invalid-name
    # type: (float, float, float|None, float, float) -> float
    """Calculate the net radiation (R_n) using solar and longwave radiation components.

    Temperature values are provided in Celsius, but they are converted to Kelvin for calculations.

    Args:
        R_s (float): Solar radiation (in J/m²/unit time).
            Solar radiation is the total **shortwave radiation** that reaches
            the Earth's surface, which includes:
                - **Ultraviolet (UV) radiation**: Wavelengths from ~100 nm to 400 nm.
                - **Visible light**: Wavelengths from ~400 nm to 700 nm
                    (the range visible to the human eye).
                - **Near-infrared (NIR) radiation**: Wavelengths from ~700 nm to 1400 nm.

            This total shortwave radiation (R_s) is partially reflected by the
            surface (depending on its albedo) and absorbed, contributing to surface heating.
        T_a_C (float): Air temperature in Celsius (°C).
        T_s_C (float, optional): Surface temperature in Celsius (°C). Default is None.
            If not defined, surface temperature treated to be equal to air temperature.
        albedo (float, optional): Albedo (α) of the surface (dimensionless, between 0 and 1).
            Defaults to 0.2 (bare soil). Examples:
                - **Dry Soil**: ~0.17 to 0.27 (e.g., sandy soil, clayey soil)
                - **Wet Soil**: ~0.1 to 0.2 (e.g., waterlogged soil, moist soil)
                - **Rocks/Rocky Surfaces**: ~0.2 to 0.4
                    (e.g., granite, limestone, basalt, volcanic rock)
                - **Fresh Snow**: ~0.8 to 0.9 (high albedo, highly reflective)
                - **Grass or Vegetation**: ~0.2 to 0.3 (vegetated surfaces)
                - **Water (with high sun angle)**: ~0.05 to 0.1 (water absorbs most solar radiation)
                - **Asphalt**: ~0.05 to 0.1 (dark surface, low albedo, absorbs most radiation)
                - **Concrete**: ~0.1 to 0.2 (lighter than asphalt but still absorbs much radiation)

        epsilon (float, optional): ε, Emissivity of the surface and atmosphere,
            dimensionless value ranges from 0 to 1 (default is 0.875).
            - ε = 1, surface is perfect black body, meaning it emits maximum
                possible radiation for its temperature.
            - ε = 0, means the surface does not emit any radiation
                (ideal reflector, not an emitter).
            - ε of Soil (dry), typical 0.8 to 0.95

    Returns:
        float: Net radiation (R_n) in J/m²/unit time. Unit time dependent on input
            solar radiation `R_s`, if `R_s` was (J/m²/day), Net radiation `R_n`
            will be (J/m²/day).
    """
    # pylint: disable=invalid-name
    if not 0 <= albedo <= 1:
        raise ValueError("Albedo value must be between 0 and 1.")

    # Convert temperatures to Kelvin
    T_air_K = celsius_to_kelvin(T_a_C)
    T_surface_K = celsius_to_kelvin(T_s_C) if not T_s_C is None else T_air_K

    # Stefan-Boltzmann constant (W/m²·K⁴)
    sigma = 5.67e-8

    # Estimate net longwave radiation
    R_nl = sigma * epsilon * (T_surface_K**4 - T_air_K**4)

    # Calculate net radiation
    R_n = (1 - albedo) * R_s - R_nl

    return R_n


def calculate_kondo_surface_resistance(vwc, A, B):  # pylint: disable=invalid-name
    # type: (float, float, float) -> float
    """Calculate the surface resistance (r_s) for a given soil type using
    the Kondo and Saigusa (1990) model.

    This function uses the empirical constants A and B provided for the soil
    and calculates the surface resistance based on the volumetric water content (theta).
    The formula used is:

        r_s = A / (1 - B * theta)

    Where:
        - r_s = surface resistance (s/m).
        - A  = reference surface resistance constant (s/m).
        - B = decay rate constant for the soil (1/m³).
        - theta = volumetric water content (fraction) (m³/m³).

    Args:
        vwc (float): Volumetric water content in fraction form (theta), where 0 <= theta <= 1.
        A (float): The reference surface resistance constant (s/m).
            - Typical range for **sandy soils**: 100 to 150 s/m
            - Typical range for **loamy soils**: 150 to 170 s/m
            - Typical range for **clayey soils**: 180 to 220 s/m
            - Typical range for **gravelly rocky soils**: 90 to 120 s/m
        B (float): The decay constant for the soil (1/m³).
            - Typical range for **sandy soils**: 0.05 to 0.07 1/m³
            - Typical range for **loamy soils**: 0.06 to 0.08 1/m³
            - Typical range for **clayey soils**: 0.08 to 0.1 1/m³
            - Typical range for **gravelly rocky soils**: 0.04 to 0.06 1/m³

    Returns:
        float: The surface resistance (r_s) for the given soil type and water content.

    Raises:
        ValueError: If theta is outside the valid range (0 <= theta <= 1).

    **Particle Size Distribution (PSD) Reference**:
    - **Sandy soils**: Particle size typically ranges from **0.05 mm to 2 mm**
        (gravel to fine sand). Coarse-grained, high permeability, low surface area.
    - **Loamy soils**: A mixture of sand, silt, and clay.
        Particle size ranges from **0.002 mm to 2 mm**.
        Typically, **sand (0.05–2 mm)**, **silt (0.002–0.05 mm)**,
        and **clay (< 0.002 mm)**.
    - **Clayey soils**: Very fine particles, mostly < **0.002 mm**.
        High surface area, high water retention, low permeability.
    - **Gravelly rocky soils**: Particle size > **2 mm** (gravel, rocks).
        Very coarse-grained with high permeability, low water retention.

    These ranges represent typical soil textures and are useful for selecting
    the appropriate**A** and **B** values for your model.
    """

    # Check if theta is within the valid range
    if not 0 <= vwc <= 1:
        raise ValueError(
            "Volumetric water content (theta) must be between 0 and 1.")

    # Calculate the surface resistance (r_s) using the Kondo and Saigusa formula
    r_s = A / (1 - B * vwc)

    return r_s


def calculate_actual_evapotranspiration(t_air, baro, RH,  # pylint: disable=invalid-name
                                        wind_spd, solar_rad,
                                        t_surface, vwc,
                                        albedo=0.2, z_u=1.6, z_h=2,
                                        A=120, B=0.05):  # pylint: disable=invalid-name
    delta = saturation_vapor_pressure_derivative(t_air)
    net_solar = net_solar_radiation(R_s=solar_rad,
                                    T_a_C=t_air,
                                    T_s_C=t_surface,
                                    albedo=albedo
                                    )
    G = 0
    vpd = vapor_pressure_deficit(
        T_air=t_air,
        RH=RH,
        T_surface=t_surface
    )

    gamma = psychrometric_constant(Pa=baro, temp=t_air)
    latent_heat = latent_heat_of_vaporisation_water(temp=t_surface)
    air_density_dry = dry_air_density(Ta=t_air, Pa=baro)

    res_aero = aerodynamic_resistance(u=wind_spd, z_m=z_u, z_h=z_h)
    res_surface = calculate_kondo_surface_resistance(vwc=vwc, A=A, B=B)

    return penman_monteith(delta=delta,
                           Rn=net_solar,
                           G=G,
                           vpd=vpd,
                           R_a=res_aero,
                           R_s=res_surface,
                           gamma=gamma,
                           _lambda=latent_heat,
                           rho_a=air_density_dry)
