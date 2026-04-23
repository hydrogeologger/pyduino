"""Radiation calculations used by environmental and evapotranspiration models.

Provides functions for calculating radiation quantities.
"""

# pylint: disable-next=unused-import
from ..conversion import (
    celsius_to_kelvin,
)

# pylint: disable=consider-using-f-string


def net_radiation_flux(
    R_s, T_a_C, T_s_C=None,
    albedo=0.23, epsilon_s=0.95, epsilon_a=0.75
):  # pylint: disable=invalid-name
    # type: (float, float, float|None, float, float, float) -> float
    """Calculate net radiation as an instantaneous energy flux.

    Net radiation is calculated as the sum of net shortwave and net longwave
    radiation:

        R_n = R_ns + R_nl

    where:

        R_ns = (1 - albedo) * R_s

        R_nl = sigma * (epsilon_a * T_a^4 - epsilon_s * T_s^4)

    The sign convention is positive toward the surface:
        - Radiation directed toward the surface is positive.
        - Radiation directed away from the surface is negative.
        - Positive net radiation indicates a net energy gain by the surface.
        - Negative net radiation indicates a net energy loss by the surface.

    Temperature values are provided in Celsius and converted to Kelvin for
    the Stefan-Boltzmann calculation.

    Solar radiation is incoming shortwave radiation reaching the
    Earth's surface, which includes:
    - **Ultraviolet (UV) radiation**: Wavelengths from ~100 nm to 400 nm.
    - **Visible light**: Wavelengths from ~400 nm to 700 nm
        (the range visible to the human eye).
    - **Near-infrared (NIR) radiation**: Wavelengths from ~700 nm to 1400 nm.

    This total shortwave radiation (R_s) is partially reflected by the
    surface (depending on its albedo) and absorbed, contributing to surface heating.

    Args:
        R_s (float): Incoming shortwave solar radiation flux (W/m²), equivalent to J/m²/s.
            The absorbed shortwave component is calculated using the surface albedo.
        T_a_C (float): Air temperature in degrees Celsius (°C).
        T_s_C (float, optional): Surface temperature in degrees Celsius (°C).
            If ``None``, the air temperature is used. Defaults to ``None``.
        albedo (float, optional): Surface albedo [α], dimensionless between 0 and 1.
            Defaults to 0.23 (dry bare soil).

            Example Albedo Values (higher value means more reflective surface):
            - **Dry Soil**: ~0.17 to 0.27 (e.g., sandy soil, clayey soil)
            - **Wet Soil**: ~0.1 to 0.2 (e.g., waterlogged soil, moist soil)
            - **Rocks/Rocky Surfaces**: ~0.2 to 0.4
                (e.g., granite, limestone, basalt, volcanic rock)
            - **Fresh Snow**: ~0.8 to 0.9 (high albedo, highly reflective)
            - **Grass or Vegetation**: ~0.2 to 0.3 (vegetated surfaces)
            - **Water (with high sun angle)**: ~0.05 to 0.1 (water absorbs most solar radiation)
            - **Asphalt**: ~0.05 to 0.1 (dark surface, low albedo, absorbs most radiation)
            - **Concrete**: ~0.1 to 0.2 (lighter than asphalt but still absorbs much radiation)

        epsilon_s (float, optional): Surface emissivity [ε_s], dimensionless and
            between 0 and 1. Defaults to 0.95.

            The range is between 0 and 1, where 1 indicates a perfect blackbody emitter.
            Typical Values:
            - Water: 0.97 (calm surface), 0.92 (wavy surface)
            - Soil (dry): 0.90 - 0.95, (wet): 0.98
            - Vegetation: 0.98
            - Snow (fresh): 0.97 - 0.99, (old): 0.85 - 0.90
            - Asphalt: 0.90 - 0.95
            - Concrete: 0.80 - 0.90
            - Rock (bare): 0.85 - 0.90

        epsilon_a (float, optional): Atmospheric emissivity [ε_a] (sky),
            dimensionless and between 0 and 1. Defaults to 0.75.

            The range is between 0 and 1, where 1 indicates a perfect blackbody emitter.
            Typical Values:
            - Dry atmosphere: 0.60 - 0.70
            - Moderate humidity: 0.75 - 0.80
            - Humid, cloudy atmosphere: 0.80 - 0.90
            - Clear sky, low humidity: 0.60 - 0.70
            - Tropical or monsoon climates: 0.80 - 0.85

    Returns:
        float: Net radiation. Returns W/m², equivalent to J/m²/s.

    Raises:
        ValueError: If ``R_s`` is negative, ``albedo`` is outside [0, 1],
            ``epsilon_s`` is outside [0, 1], ``epsilon_a`` is outside [0, 1].
    """
    # pylint: disable=invalid-name
    if R_s < 0.0:
        raise ValueError("Incoming solar radiation must be >= 0.")
    if not 0 <= albedo <= 1:
        raise ValueError("Albedo value must be between 0 and 1.")
    if not 0.0 <= epsilon_s <= 1.0:
        raise ValueError("Surface emissivity must be between 0 and 1.")
    if not 0.0 <= epsilon_a <= 1.0:
        raise ValueError("Atmospheric emissivity must be between 0 and 1.")

    # Convert temperatures to Kelvin
    T_air_K = celsius_to_kelvin(T_a_C)
    T_surface_K = celsius_to_kelvin(T_s_C) if T_s_C is not None else T_air_K

    # Stefan-Boltzmann constant [sigma] ( W/(m²·K⁴), equivalent to J/(s·m²·K⁴) )
    STEFAN_BOLTZMANN = 5.670374419e-08

    # Calculate net longwave radiation received by the surface.
    R_nl = STEFAN_BOLTZMANN * (
        (epsilon_a * T_air_K**4) - (epsilon_s * T_surface_K**4)
    )

    # Calculate net short wave radiation
    R_ns = (1.0 - albedo) * R_s

    # Net radiation = absorbed shortwave + net longwave.
    # R_n > 0  → surface receives net energy
    # R_n < 0  → surface loses net energy
    R_n = R_ns + R_nl
    return R_n


def net_radiation_energy(
    R_s, T_a_C, time_step_seconds, T_s_C=None,
    albedo=0.23, epsilon_s=0.95, epsilon_a=0.75
):  # pylint: disable=invalid-name
    # type: (float, float, int|float, float|None, float, float, float) -> float
    """Calculate accumulated net radiation energy over a time interval.

    The net radiation flux is calculated using :func:`net_radiation_flux`
    and multiplied by the specified timestep. This assumes that the
    calculated radiation flux is representative of the entire interval.

    Args:
        R_s (float): Incoming shortwave solar radiation flux (W/m²), equivalent to J/m²/s.
        T_a_C (float): Air temperature in degrees Celsius (°C).
        time_step_seconds (int or float): Duration of the time interval in seconds.

            Typical values:
            - ``1``: output is a flux in W/m² (equivalent to J/m²/s).
            - ``3600``: output is accumulated energy over one hour in J/m².
            - ``86400``: output is accumulated energy over one day in J/m².

        T_s_C (float, optional): Surface temperature in degrees Celsius (°C).
            If ``None``, air temperature is used.
        albedo (float, optional): Surface albedo [0, 1].
            Defaults to 0.23.
        epsilon_s (float, optional): Surface emissivity [0, 1].
            Defaults to 0.95.
        epsilon_a (float, optional): Atmospheric emissivity [0, 1].
            Defaults to 0.75.

    Returns:
        float: Accumulated net radiation energy in J/m².

    Raises:
        ValueError: If ``time_step_seconds`` is not a positive value or
            any radiation input violates the constraints of
            :func:`net_radiation_flux`.
    """
    if not isinstance(time_step_seconds, (int, float)) or time_step_seconds <= 0.0:
        raise ValueError("`time_step_seconds` must be a positive value.")

    return net_radiation_flux(
        R_s=R_s,
        T_a_C=T_a_C,
        T_s_C=T_s_C,
        albedo=albedo,
        epsilon_s=epsilon_s,
        epsilon_a=epsilon_a,
    ) * time_step_seconds
