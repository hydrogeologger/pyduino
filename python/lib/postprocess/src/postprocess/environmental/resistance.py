"""Aerodynamic and surface resistance calculations for environmental models.

Provides functions for estimating resistance to heat and water-vapour
transfer between a surface and the atmosphere.
"""

import math as _math

def aerodynamic_resistance(u, z_u=2.0, z_h=None, z_om=0.001, z_oh=0.001, d=1e-4):
    # type: (float, float, float|None, float, float, float) -> float
    """Calculate the aerodynamic resistance (r_a) using the logarithmic wind profile equation.

    The aerodynamic resistance is used to model the resistance to the movement of water vapor from 
    the surface to the atmosphere due to wind friction and surface roughness.

    ra = (ln((z_u - d) / z_om) * ln((z_h - d) / z_oh)) / (k^2 * u)

    Args:
        u (float): Wind speed at height `z_m` (m/s).
            Wind speed at a standard reference height (e.g., 2 m or 10 m).
        z_u (float, optional): Height at which the wind speed is measured (m).
            Typically 2 m or 10 m above ground. Defaults to 2.
        z_h (float, optional): Height at which humidity/temperature is measured (m).
            If not defined, `z_h = z_u`. Defaults to None.
        z_om (float, optional): Roughness length governing momentum transfer (m),
            a measure of how wind or air speed is affected by surface roughness.
            Higher value corresponds to greater resistance.
            Defaults to 0.001.

            Typical values:
            - Open water: 0.001 - 0.01 m
            - Grassland/Cropland: 0.01 - 0.1 m
            - Forests: 0.1 - 2.0 m
            - Desert or bare rock: 0.001 - 0.1 m
            - 0.123 * vegetation height

        z_oh (float, optional): Roughness length governing transfer of heat and vapor (m),
            a measure of how temperature is exchanged between the surface and air.
            Higher value corresponds to greater resistance.
            Defaults to 0.001.

            Typical Values:
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
    if u <= 0:
        raise ValueError("wind speed must be greater than zero.")
    if z_u <= d:
        raise ValueError(
            "``z_m`` must be greater than ``d`` wind profile zero plane displacement")
    if z_om <= 0:
        raise ValueError("``z_om`` must be greater than zero.")

    if z_h is None:
        z_h = z_u

    if z_h <= d:
        raise ValueError(
            "``z_h`` must be greater than ``d`` wind profile zero plane displacement")
    if z_oh <= 0:
        raise ValueError("``z_oh`` must be greater than zero.")

    if z_om >= z_u - d:
        raise ValueError("z_om must be less than z_m - d")
    if z_oh >= z_h - d:
        raise ValueError("z_oh must be less than z_h - d")

    # von Kármán constant (dimensionless)
    k = 0.41

    # Calculate the aerodynamic resistance using the logarithmic wind profile equation
    r_a = (_math.log((z_u - d) / z_om) *
           _math.log((z_h - d) / z_oh)) / (k**2 * u)

    return r_a


def estimate_soil_surface_resistance(vwc, theta_fc=0.35, theta_evap_min=0.10, rs_min=50.0, k_s=4.0):
    # type: (float, float, float, float, float) -> float
    """Estimate soil surface resistance from volumetric water content.

    Soil surface resistance is estimated using an exponential soil-drying
    relationship:

        rs = rs_min * exp(
            k_s * (theta_fc - vwc) / (theta_fc - theta_evap_min)
        )

    Volumetric water content is constrained to the range between the
    minimum water content for evaporation and field capacity. This prevents
    the model from producing resistance values below rs_min under very wet
    conditions or extrapolating beyond the defined dry-soil range.

    Args:
        vwc (float): Volumetric water content (m3/m3).

        theta_fc (float, optional): Volumetric water content at field capacity (m3/m3).
            Defaults to 0.35.

            Ideally obtained from measured soil hydraulic properties or a
            soil-specific water retention curve. If these data are not
            available, typical starting ranges by soil texture are:
                - Sandy soils: 0.10-0.25
                - Loamy soils: 0.25-0.40
                - Clayey soils: 0.35-0.50

        theta_evap_min (float, optional): Minimum volumetric water content
            at which soil evaporation is represented by the model (m3/m3).
            Defaults to 0.10.

            This is an evaporation-specific lower boundary and should not
            necessarily be interpreted as the permanent wilting point.
            Ideally determined from soil hydraulic properties, a
            soil-specific water retention curve, or calibrated from observed
            soil evaporation. If observations are unavailable, typical
            starting ranges by soil texture are:
                - Sandy soils: 0.03-0.10
                - Loamy soils: 0.10-0.20
                - Clayey soils: 0.20-0.30

        rs_min (float, optional): Minimum soil surface resistance when the
            soil is wet (s/m). Lower values mean water can evaporate more
            easily; higher values mean evaporation is more restricted.
            Defaults to 50 s/m.

            Ideally calibrated using observed evaporation or latent heat
            flux under wet-soil conditions. Suggested starting ranges by
            surface condition are:
                - Very wet / freely evaporating: 20-40 s/m
                - Wet / relatively permeable: 40-70 s/m
                - Typical moist soil: 50-100 s/m
                - Fine-textured / less permeable: 75-150 s/m
                - Crusted / compacted surface: 100-250 s/m

        k_s (float, optional): Soil drying sensitivity (dimensionless).
            Controls how quickly evaporation becomes restricted as the soil
            dries. Defaults to 4.0.

            Ideally calibrated against observed evaporation or latent heat
            flux over a soil drying period. Suggested starting ranges are:
                - 0.5–2: Wet soil remains relatively easy to evaporate from,
                    such as frequently irrigated or shallow, moist soil.
                - 2–3: Evaporation decreases gradually as the soil dries,
                    typical of relatively sandy or well-drained soil.
                - 3–6: Evaporation decreases noticeably as the soil dries,
                    typical of loam or moderately drying soil.
                - 6–10: Evaporation decreases rapidly once the surface dries,
                    such as fine-textured soil or soil with limited water supply.
                - 10–15: Evaporation becomes very strongly restricted as the
                    soil dries, such as a strongly drying or crusted surface.

    Returns:
        float: Estimated soil surface resistance (s/m).

    Raises:
        ValueError: If vwc is not finite or is outside the physical range
            of 0-1 m3/m3.
        ValueError: If theta_fc is less than or equal to theta_evap_min.
        ValueError: If rs_min is negative.
        ValueError: If k_s is negative.

    Notes:
        The parameterisation is intended for soil evaporation within a
        Penman-Monteith framework.

        theta_fc should preferably be obtained from measured soil hydraulic
        properties or a soil-specific soil-water retention curve.

        theta_evap_min represents the lower moisture limit of the
        evaporation model rather than permanent wilting point. It should
        preferably be determined from observed soil evaporation or inferred
        from soil hydraulic properties.

        rs_min and k_s are empirical model parameters. They should ideally
        be calibrated against observed evaporation, latent heat flux, or
        equivalent measurements. The suggested ranges are intended as
        initial values for calibration rather than universal constants.

        The estimated resistance can be passed directly as the surface
        resistance (rs) term in a Penman-Monteith evaporation model.

    References:
        Monteith, J. L. (1965). Evaporation and environment.
            Symposia of the Society for Experimental Biology, 19, 205-234.

        Sellers, P. J., et al. (1992). Canopy reflectance, photosynthesis,
            and transpiration. Agricultural and Forest Meteorology, 60,
            1-18.

        Allen, R. G., Pereira, L. S., Raes, D., & Smith, M. (1998).
            Crop evapotranspiration: Guidelines for computing crop water
            requirements. FAO Irrigation and Drainage Paper 56.

        USDA NRCS. National Engineering Handbook, Part 623:
            Irrigation Water Requirements.
    """
    if not _math.isfinite(vwc):
        raise ValueError("vwc must be a finite number.")
    if not 0.0 <= vwc <= 1.0:
        raise ValueError("vwc must be between 0 and 1 m3/m3.")
    if not 0.0 <= theta_fc <= 1.0:
        raise ValueError("theta_fc must be between 0 and 1 m3/m3.")
    if not 0.0 <= theta_evap_min <= 1.0:
        raise ValueError("theta_evap_min must be between 0 and 1 m3/m3.")
    if theta_fc <= theta_evap_min:
        raise ValueError("theta_fc must be greater than theta_evap_min.")
    if rs_min < 0:
        raise ValueError("rs_min must be non-negative.")
    if k_s < 0:
        raise ValueError("k_s must be non-negative.")

    # Constrain VWC to the defined soil-moisture range.
    vwc = max(theta_evap_min, min(vwc, theta_fc))

    # Normalised soil dryness:
    # 0 at field capacity and 1 at the minimum moisture
    # represented by the evaporation model.
    dryness = (theta_fc - vwc) / (theta_fc - theta_evap_min)

    # Exponential increase in resistance as soil dries.
    rs = rs_min * _math.exp(k_s * dryness)

    return rs
