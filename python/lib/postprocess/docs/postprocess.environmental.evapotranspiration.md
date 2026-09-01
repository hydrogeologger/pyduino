<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/evapotranspiration.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.environmental.evapotranspiration`
Methods for calculating evapotranspiration from meteorological data.

Provides implementations of evapotranspiration estimation approaches
using commonly available weather variables.

This module contains the high-level evapotranspiration models and composes
atmospheric, radiation, and resistance calculations provided by the
corresponding environmental modules.


## Table of Contents
- [`calculate_soil_evaporation`](./postprocess.environmental.evapotranspiration.md#function-calculate_soil_evaporation): Calculate soil evaporation flux using the Penman–Monteith equation for a soil surface.
- [`fao_penman_monteith`](./postprocess.environmental.evapotranspiration.md#function-fao_penman_monteith): Compute evapotranspiration rate using the FAO Penman–Monteith equation.
- [`penman_monteith`](./postprocess.environmental.evapotranspiration.md#function-penman_monteith): Compute evapotranspiration rate using the Penman–Monteith equation (resistance form).



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/evapotranspiration.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `penman_monteith`

```python
penman_monteith(
    delta,
    Rn,
    G,
    vpd,
    r_a,
    r_s,
    gamma,
    lambda_=2450000.0,
    rho_a=1.204,
    c_p=1013.0
)
```

Compute evapotranspiration rate using the Penman–Monteith equation (resistance form).

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


**Args:**

- <b>`delta`</b> (float): Δ, slope of saturation vapour pressure curve (Pa/°C).
- <b>`Rn`</b> (float): Rₙ, net radiation (W/m²).
- <b>`G`</b> (float): G, soil heat flux (W/m²).
- <b>`vpd`</b> (float): VPD = (eₛ - eₐ), Vapor pressure deficit (Pa).
    - eₛ = Saturation vapor pressure
    - eₐ = Actual vapor pressure of the air
- <b>`r_a`</b> (float): rₐ, aerodynamic resistance (s/m).
- <b>`r_s`</b> (float): rₛ, surface (canopy) resistance (s/m).
- <b>`gamma`</b> (float): γ, psychrometric constant (Pa/°C).
- <b>`lambda_`</b> (float, optional): λ, latent heat of vaporisation (J/kg).
    Defaults to 2.45 x 10^6 J/kg.
- <b>`rho_a`</b> (float, optional): ρₐ, Air density (kg/m³).
    Defaults to (dry air) 1.204 kg/m³.
- <b>`c_p`</b> (float, optional): cₚ, specific heat capacity of air (J/kg/°C).
    Defaults to dry air 1013 J/kg/°C.


**Returns:**

- <b>`float`</b>: ET, evapotranspiration rate in kg m⁻² s⁻¹ (equivalently mm/s).



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/evapotranspiration.py#L157"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `fao_penman_monteith`

```python
fao_penman_monteith(T, u_2, delta, Rn, G, vpd, gamma)
```

Compute evapotranspiration rate using the FAO Penman–Monteith equation.

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


**Args:**

- <b>`T`</b> (float): Mean daily air temperature at 2m height (°C).
- <b>`u_2`</b> (float): Wind speed at 2m height (m/s).
- <b>`delta`</b> (float): Δ, slope of saturation vapour pressure curve (kPa/°C).
- <b>`Rn`</b> (float): Rₙ, net radiation at surface (MJ/m²day).
- <b>`G`</b> (float): G, soil heat flux (MJ/m²day).
- <b>`vpd`</b> (float): VPD = (eₛ - eₐ), Vapor pressure deficit (kPa).
    - eₛ = Saturation vapor pressure (kPa)
    - eₐ = Actual vapor pressure of the air (kPa)
- <b>`gamma`</b> (float): γ, psychrometric constant (kPa/°C).


**Returns:**

- <b>`float`</b>: ET, evapotranspiration rate in (mm/day).

> [!NOTE] 
> Temperature conversion (T + 273.0) is used instead of 273.15 to strictly
> comply with the hardcoded empirical constants specified in the
> FAO-56 Penman-Monteith standard.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/evapotranspiration.py#L211"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `calculate_soil_evaporation`

```python
calculate_soil_evaporation(
    t_air,
    baro,
    RH,
    wind_spd,
    solar_rad,
    vwc,
    t_surface=None,
    albedo=0.23,
    z_u=2.0,
    z_h=2.0,
    theta_fc=0.35,
    theta_evap_min=0.1,
    rs_min=50.0,
    k_s=4.0,
    soil_heat_flux=0.0
)
```

Calculate soil evaporation flux using the Penman–Monteith equation for a soil surface.

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


**Args:**

- <b>`t_air`</b> (float): Air temperature in degrees Celsius (°C).
- <b>`baro`</b> (float): Atmospheric pressure in Pascals (Pa).
- <b>`RH`</b> (float): Relative humidity as a percentage [0-100] (%).
- <b>`wind_spd`</b> (float): Wind speed at ``z_u`` in metres per second (m/s).
    Must be greater than zero.
- <b>`solar_rad`</b> (float): Incoming shortwave solar radiation in W/m².
    Must be non-negative.
- <b>`vwc`</b> (float): Volumetric water content (m³/m³) as a fraction [0-1].
- <b>`t_surface`</b> (float, optional): Soil-surface temperature in degrees
    Celsius (°C). If ``None``, ``t_air`` is used. Defaults to ``None``.
- <b>`albedo`</b> (float, optional): Surface albedo, dimensionless and in the
    range [0, 1]. Passed to :func:`net_radiation`. Defaults to 0.23.
- <b>`z_u`</b> (float, optional): Height of the wind-speed measurement above the
    surface in metres (m). Passed to :func:`aerodynamic_resistance`.
    Defaults to 2.0.
- <b>`z_h`</b> (float, optional): Height of the air temperature and humidity
    measurements above the surface in metres (m). Passed to
    :func:`aerodynamic_resistance`. Defaults to 2.0.
- <b>`theta_fc`</b> (float, optional): Volumetric water content at field
    capacity (m³/m³).
    Passed to :func:`estimate_soil_surface_resistance`.
    Defaults to 0.35.
- <b>`theta_evap_min`</b> (float, optional): Minimum volumetric water content
    represented by the soil-surface resistance model (m³/m³).
    Passed to :func:`estimate_soil_surface_resistance`. Defaults to
    0.10.
- <b>`rs_min`</b> (float, optional): Minimum soil-surface resistance (s/m).
    Passed to :func:`estimate_soil_surface_resistance`. Defaults to
    50.0.
- <b>`k_s`</b> (float, optional): Soil-drying sensitivity parameter. Passed to
    :func:`estimate_soil_surface_resistance`. Defaults to 4.0.
- <b>`soil_heat_flux`</b> (float, optional): Soil heat flux in W/m². Positive
    values represent energy transferred into the soil. Defaults to 0.0.


**Returns:**

- <b>`float`</b>: Actual evapotranspiration flux in kg m⁻² s⁻¹, numerically
    equivalent to mm/s of water. The result is an instantaneous
    flux and is not accumulated over a time interval.


**Raises:**

- <b>`ValueError`</b>: If any input violates the physical or mathematical
    constraints enforced by the underlying calculations.

> [!NOTE] 
> If ``t_surface`` is ``None``, ``t_air`` is used as the surface
> temperature.
> 
> ``t_surface`` is used by :func:`net_radiation`,
> :func:`saturation_vapor_pressure_derivative`, and
> :func:`soil_surface_vapor_pressure_deficit`. ``t_air`` is used
> for :func:`specific_heat_capacity_air`,
> :func:`psychrometric_constant`,
> :func:`latent_heat_of_vaporisation_water`, and
> :func:`dry_air_density`.
> 
> ``solar_rad`` and ``soil_heat_flux`` are supplied as energy fluxes
> in W/m². Consequently, :func:`net_radiation` and
> :func:`penman_monteith` operate on an instantaneous flux basis.
> 
> Negative values are possible and represent a negative latent-water
> flux under the sign convention used by :func:`penman_monteith`.



