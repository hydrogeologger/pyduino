"""Environmental calculations for meteorological and environmental data.

Provides utilities and models for atmospheric thermodynamics, radiation,
surface and aerodynamic resistance, and evapotranspiration.
"""

from .evapotranspiration import (
    # --- Evapotranspiration & Soil Surface Fluxes ---
    penman_monteith,
    fao_penman_monteith,
    calculate_soil_evaporation,

    # --- Temporal Conversions & Aggregations ---
    per_second_to_daily,
    per_second_to_hourly,
)

from .radiation import (
    # --- Required Radiation Arguments ---
    net_radiation_flux,
)

from .resistance import (
    # --- Required Resistance Arguments ---
    aerodynamic_resistance,
    estimate_soil_surface_resistance,
)

from .atmospheric import (
    # --- Required Psychrometric & Vapor Pressure Arguments ---
    vapor_pressure_deficit,
    psychrometric_constant,
    saturation_vapor_pressure_slope_tetens,
    wind_speed_at_2m,
)
