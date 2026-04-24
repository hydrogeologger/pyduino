<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.climate.evapotranspiration`
postprocess climate evapotranspiration module


## Table of Contents
- [`aerodynamic_resistance`](./postprocess.climate.evapotranspiration.md#function-aerodynamic_resistance): Calculate the aerodynamic resistance (r_a) using the logarithmic wind profile equation.
- [`air_specific_heat_capacity`](./postprocess.climate.evapotranspiration.md#function-air_specific_heat_capacity): Calculate the specific heat capacity of dry air at constant pressure (C_p)  as a function of temperature in Celsius using an empirical equation.
- [`calculate_actual_evapotranspiration`](./postprocess.climate.evapotranspiration.md#function-calculate_actual_evapotranspiration)
- [`calculate_kondo_surface_resistance`](./postprocess.climate.evapotranspiration.md#function-calculate_kondo_surface_resistance): Calculate the surface resistance (r_s) for a given soil type using the Kondo and Saigusa (1990) model.
- [`celsius_to_kelvin`](./postprocess.climate.evapotranspiration.md#function-celsius_to_kelvin): Convert temperature from Celsius to Kelvin
- [`dry_air_density`](./postprocess.climate.evapotranspiration.md#function-dry_air_density): Calculate dry air density
- [`fao_penman_monteith`](./postprocess.climate.evapotranspiration.md#function-fao_penman_monteith): Compute evapotranspiration rate using the FAO Penman–Monteith equation.
- [`kelvin_to_celsius`](./postprocess.climate.evapotranspiration.md#function-kelvin_to_celsius): Convert temperature from Kelvin to Celsius
- [`latent_heat_of_vaporisation_water`](./postprocess.climate.evapotranspiration.md#function-latent_heat_of_vaporisation_water): Calculate latent heat of vaporisation for water.
- [`net_solar_radiation`](./postprocess.climate.evapotranspiration.md#function-net_solar_radiation): Calculate the net radiation (R_n) using solar and longwave radiation components.
- [`partial_vapor_pressure`](./postprocess.climate.evapotranspiration.md#function-partial_vapor_pressure): Calculate the actual vapor pressure (E_a) of air.
- [`penman_monteith`](./postprocess.climate.evapotranspiration.md#function-penman_monteith): Compute evapotranspiration rate using the Penman–Monteith equation (resistance form).
- [`psychrometric_constant`](./postprocess.climate.evapotranspiration.md#function-psychrometric_constant): Calculate the psychrometric constant (gamma)
- [`saturation_vapor_pressure`](./postprocess.climate.evapotranspiration.md#function-saturation_vapor_pressure): Calculate the saturation vapor pressure (E_s) at a given temperature.
- [`saturation_vapor_pressure_derivative`](./postprocess.climate.evapotranspiration.md#function-saturation_vapor_pressure_derivative): Calculate the slope of the saturation vapor pressure curve (Δ) at a given temperature.
- [`total_air_density`](./postprocess.climate.evapotranspiration.md#function-total_air_density): Calculate total air density
- [`vapor_pressure_deficit`](./postprocess.climate.evapotranspiration.md#function-vapor_pressure_deficit): Calculate vapor pressure deficit at soil surface.



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `kelvin_to_celsius`

```python
kelvin_to_celsius(val)
```

Convert temperature from Kelvin to Celsius



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `celsius_to_kelvin`

```python
celsius_to_kelvin(val)
```

Convert temperature from Celsius to Kelvin



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `dry_air_density`

```python
dry_air_density(Ta=20, Pa=101325)
```

Calculate dry air density

Uses Ideal Gas Law.


**Args:**

- <b>`Ta`</b> (float, optional): Air Temperature in degrees Celsius (°C). Defaults to 20 °C
- <b>`Pa`</b> (float, optional): Air pressure in Pascals (Pa). Defaults to 101325 Pa.


**Returns:**

- <b>`float`</b>: Dry air density (kg/m³).



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `total_air_density`

```python
total_air_density(Ta, Pa, RH)
```

Calculate total air density

Uses Ideal Gas Law.


**Args:**

- <b>`Ta`</b> (float, optional): Air Temperature in degrees Celsius (°C).
- <b>`Pa`</b> (float, optional): Air pressure in Pascals (Pa).
- <b>`RH`</b> (float, optional): Relative humidity [0-100] (%).


**Returns:**

- <b>`float`</b>: Dry air density (kg/m³).



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `latent_heat_of_vaporisation_water`

```python
latent_heat_of_vaporisation_water(temp)
```

Calculate latent heat of vaporisation for water.


**Args:**

- <b>`temp`</b> (float): Temperature in degrees Celsius (°C)


**Returns:**

- <b>`float`</b>: Latent heat of vaporisation (J/kg)



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `air_specific_heat_capacity`

```python
air_specific_heat_capacity(Ta)
```

Calculate the specific heat capacity of dry air at constant pressure (C_p) 
as a function of temperature in Celsius using an empirical equation.

The specific heat capacity is given by the equation:  
C_p(T) = 1005 + 0.1 * (T - 25)


**Args:**

- <b>`Ta`</b> (float): The temperature in Celsius (°C).


**Returns:**

- <b>`float`</b>: The specific heat capacity of air in J/kg·K at the given temperature.


**Example:**

```python
>>> calculate_specific_heat(30)
1005.5
```



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `penman_monteith`

```python
penman_monteith(delta, Rn, G, vpd, R_a, R_s, gamma, _lambda, rho_a=1.204)
```

Compute evapotranspiration rate using the Penman–Monteith equation (resistance form).

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


**Args:**

- <b>`delta`</b> (float): Δ, slope of saturation vapour pressure curve (Pa/°C).
- <b>`Rn`</b> (float): Rₙ, net radiation (W/m²).
- <b>`G`</b> (float): G, soil heat flux (W/m²).
- <b>`vpd`</b> (float): VPD = (eₛ - eₐ), Vapor pressure deficit (Pa).
    - eₛ = Saturation vapor pressure
    - eₐ = Actual vapor pressure of the air
- <b>`R_a`</b> (float): rₐ, aerodynamic resistance (s/m).
- <b>`R_s`</b> (float): rₛ, surface (canopy) resistance (s/m).
- <b>`gamma`</b> (float): γ, psychrometric constant (Pa/°C).
- <b>`_lambda`</b> (float): λ, latent heat of vaporisation (J/kg).
- <b>`rho_a`</b> (float, optional): ρₐ, dry air density (kg/m³).


**Returns:**

- <b>`float`</b>: ET, evapotranspiration rate in kg m⁻² s⁻¹ (equivalently mm/s).



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L202"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `fao_penman_monteith`

```python
fao_penman_monteith(Ta, u_2, delta, Rn, G, vpd, gamma)
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

- <b>`Ta`</b> (float): Mean daily air temperature at 2m height (°C).
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



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L244"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `saturation_vapor_pressure`

```python
saturation_vapor_pressure(temp)
```

Calculate the saturation vapor pressure (E_s) at a given temperature.

E_s(T) = 0.6108 * exp( (17.27 * T) / (T + 237.3) )

Where:  
- E_s = Saturation Vapor Pressure (kPa)
- T = Temperature (°C)


**Args:**

- <b>`temp`</b> (float): Temperature in degrees Celsius (°C)


**Returns:**

- <b>`float`</b>: Saturation vapor pressure in Pascal (Pa)



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L265"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `partial_vapor_pressure`

```python
partial_vapor_pressure(Ta, RH)
```

Calculate the actual vapor pressure (E_a) of air.

E_a = (RH / 100) * E_s

Where
- E_s = Saturation Vapor Pressure (kPa)
- RH = Relative Humidity [0-100] (%)
- E_a = Actual vapor pressure (kPa)


**Args:**

- Ta (float): Temperature of air in degrees Celsius.
- RH (float): Relative Humidity as a percentage.


**Returns:**

- <b>`float`</b>: Actual vapor pressure in Pascals.



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L290"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `psychrometric_constant`

```python
psychrometric_constant(Pa, temp=15)
```

Calculate the psychrometric constant (gamma)


The psychrometric constant is given by the equation:  

γ = (C_p × P) / (λ × MW_ratio)

Where:  
- γ is the psychrometric constant in Pa/°C,
- C_p is the specific heat of dry air at constant pressure typically 1005 (J/(kg·K)),
- P is the atmospheric pressure in Pa (e.g., 101325 Pa at sea level),
- λ is the latent heat of vaporization of water in J/kg (e.g., 2.45 × 10⁶ J/kg),
- MW_ratio is molecular weight ratio of water vapor/dry air = 0.622


**Args:**

- <b>`Pa`</b> (float): Atmospheric pressure in pascal (Pa)
- <b>`temp`</b> (float): Temperature in degrees Celsius (°C)


**Returns:**

- <b>`float`</b>: Psychometric constant in Pa/°C



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L322"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `aerodynamic_resistance`

```python
aerodynamic_resistance(u, z_m=2, z_h=None, z_om=0.001, z_oh=None, d=0.0001)
```

Calculate the aerodynamic resistance (r_a) using the logarithmic wind profile equation.

The aerodynamic resistance is used to model the resistance to the movement of water vapor from 
the surface to the atmosphere due to wind friction and surface roughness.

ra = (ln((z_u - d) / z_om) * ln((z_h - d) / z_oh)) / (k^2 * u)


**Args:**

- <b>`u`</b> (float): Wind speed at height `z_m` (m/s).
    Wind speed at a standard reference height (e.g., 2 m or 10 m).
- <b>`z_m`</b> (float, optional): Height at which the wind speed is measured (m).
    Typically 2 m or 10 m above ground. Defaults to 2.
- <b>`z_h`</b> (float, optional): Height at which humidity/temperature is measured (m).
    If not defined, `z_h = z_u`. Defaults to None.
- <b>`z_om`</b> (float, optional): Roughness length governing momentum transfer (m),
    a measure of how wind or air speed is affected by surface roughness.
    Higher value corresponds to greater resistance.
    Defaults to 1e-3. Common values:
    - Open water: 0.001 - 0.01 m
    - Grassland/Cropland: 0.01 - 0.1 m
    - Forests: 0.1 - 2.0 m
    - Desert or bare rock: 0.001 - 0.1 m
    - 0.123 * vegetation height
- <b>`z_oh`</b> (float, optional): Roughness length governing transfer of heat and vapor (m),
    a measure of how temperature is exchanged between the surface and air.
    Higher value corresponds to greater resistance.
    Defaults to None. Cmmon Values:
    - Open water: 0.001 - 0.01 m (very smooth, little or no resistance)
    - Grassland/Cropland: 0.01 - 0.1 m
    - Forests: 0.1 - 1.0 m
    - Desert or bare rock: 0.001 - 0.1 m
    - 0.1 * vegetation height
- <b>`d`</b> (float, optional): Zero plane displacement of the wind profile (m),
    accounts for obstacles like trees or buildings.
    Typically 2/3 * vegetation height for forests/crops, or average
    building height for urban areas. Defaults to 1e-4.


**Returns:**

- <b>`float`</b>: Aerodynamic resistance (r_a) in seconds per meter (s/m).


**Reference:**

https://swatplus.gitbook.io/io-docs/theoretical-documentation/section-2-hydrology/chapter-2-2-evapotranspiration/2-2.2-potential-evapotranspiration/2-2.2.1-penman-monteith-method/2-2.2.1.2-aerodynamic-resistance



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L382"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `saturation_vapor_pressure_derivative`

```python
saturation_vapor_pressure_derivative(temp)
```

Calculate the slope of the saturation vapor pressure curve (Δ) at a given temperature.

The slope is the rate of change of saturation vapor pressure with respect to temperature.

delta = (4098 * E_s) / (T + 237.3)^2

Where:  
- E_s = Saturation Vapor Pressure (kPa)
- T = Temperature (°C)

This is used in the Penman-Monteith equation for evapotranspiration.


**Args:**

- <b>`temp`</b> (float): Temperature in degrees Celsius (°C).


**Returns:**

- <b>`float`</b>: Slope of the saturation vapor pressure curve in Pa/°C.



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L410"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `vapor_pressure_deficit`

```python
vapor_pressure_deficit(T_air, RH, T_surface=None)
```

Calculate vapor pressure deficit at soil surface.


**Args:**

- <b>`T_air`</b> (float): Air Temperature in degrees Celsius (°C)
- <b>`RH`</b> (float): Relative Humidity [0-100] (%)
- <b>`T_gnd`</b> (float, optional): Air temperature at soil surface in degrees Celsius (°C).
    If None, will fall back to air temperature. Defaults to None.


**Returns:**

- <b>`_float`</b>: Vapor pressure deficit in pascal (Pa).



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L428"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `net_solar_radiation`

```python
net_solar_radiation(R_s, T_a_C, T_s_C=None, albedo=0.2, epsilon=0.875)
```

Calculate the net radiation (R_n) using solar and longwave radiation components.

Temperature values are provided in Celsius, but they are converted to Kelvin for calculations.


**Args:**

- <b>`R_s`</b> (float): Solar radiation (in J/m²/unit time).
    Solar radiation is the total **shortwave radiation** that reaches
    the Earth's surface, which includes:
        - **Ultraviolet (UV) radiation**: Wavelengths from ~100 nm to 400 nm.
        - **Visible light**: Wavelengths from ~400 nm to 700 nm
            (the range visible to the human eye).
        - **Near-infrared (NIR) radiation**: Wavelengths from ~700 nm to 1400 nm.

    This total shortwave radiation (R_s) is partially reflected by the
    surface (depending on its albedo) and absorbed, contributing to surface heating.
- <b>`T_a_C`</b> (float): Air temperature in Celsius (°C).
- <b>`T_s_C`</b> (float, optional): Surface temperature in Celsius (°C). Default is None.
    If not defined, surface temperature treated to be equal to air temperature.
- <b>`albedo`</b> (float, optional): Albedo (α) of the surface (dimensionless, between 0 and 1).
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

- <b>`epsilon`</b> (float, optional): ε, Emissivity of the surface and atmosphere,
    dimensionless value ranges from 0 to 1 (default is 0.875).
    - ε = 1, surface is perfect black body, meaning it emits maximum
        possible radiation for its temperature.
    - ε = 0, means the surface does not emit any radiation
        (ideal reflector, not an emitter).
    - ε of Soil (dry), typical 0.8 to 0.95


**Returns:**

- <b>`float`</b>: Net radiation (R_n) in J/m²/unit time. Unit time dependent on input
    solar radiation `R_s`, if `R_s` was (J/m²/day), Net radiation `R_n`
    will be (J/m²/day).



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L493"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `calculate_kondo_surface_resistance`

```python
calculate_kondo_surface_resistance(vwc, A, B)
```

Calculate the surface resistance (r_s) for a given soil type using
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


**Args:**

- <b>`vwc`</b> (float): Volumetric water content in fraction form (theta), where 0 <= theta <= 1.
- <b>`A`</b> (float): The reference surface resistance constant (s/m).
    - Typical range for **sandy soils**: 100 to 150 s/m
    - Typical range for **loamy soils**: 150 to 170 s/m
    - Typical range for **clayey soils**: 180 to 220 s/m
    - Typical range for **gravelly rocky soils**: 90 to 120 s/m
- <b>`B`</b> (float): The decay constant for the soil (1/m³).
    - Typical range for **sandy soils**: 0.05 to 0.07 1/m³
    - Typical range for **loamy soils**: 0.06 to 0.08 1/m³
    - Typical range for **clayey soils**: 0.08 to 0.1 1/m³
    - Typical range for **gravelly rocky soils**: 0.04 to 0.06 1/m³


**Returns:**

- <b>`float`</b>: The surface resistance (r_s) for the given soil type and water content.


**Raises:**

- <b>`ValueError`</b>: If theta is outside the valid range (0 <= theta <= 1).

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



---

<a href="../../../../python/lib/postprocess/src/postprocess/climate/evapotranspiration.py#L556"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `calculate_actual_evapotranspiration`

```python
calculate_actual_evapotranspiration(
    t_air,
    baro,
    RH,
    wind_spd,
    solar_rad,
    t_surface,
    vwc,
    albedo=0.2,
    z_u=1.6,
    z_h=2,
    A=120,
    B=0.05
)
```

*No documentation found.*


