<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.environmental.atmospheric`
Atmospheric thermodynamic calculations used by environmental models.

Provides functions for calculating water-vapour properties, air density,
specific heat capacity, latent heat, and psychrometric properties required
by evapotranspiration models.


## Table of Contents
- [`calculate_specific_humidity`](./postprocess.environmental.atmospheric.md#function-calculate_specific_humidity): Calculate specific humidity from relative humidity.
- [`dry_air_density`](./postprocess.environmental.atmospheric.md#function-dry_air_density): Calculate dry air density
- [`latent_heat_of_vaporisation_water`](./postprocess.environmental.atmospheric.md#function-latent_heat_of_vaporisation_water): Calculate latent heat of vaporisation for water.
- [`partial_vapor_pressure`](./postprocess.environmental.atmospheric.md#function-partial_vapor_pressure): Calculate the actual vapor pressure (e_a) of air.
- [`psychrometric_constant`](./postprocess.environmental.atmospheric.md#function-psychrometric_constant): Calculate the psychrometric constant (gamma)
- [`saturation_vapor_pressure`](./postprocess.environmental.atmospheric.md#function-saturation_vapor_pressure): Calculate the saturation vapor pressure (e_s) at a given temperature.
- [`saturation_vapor_pressure_derivative`](./postprocess.environmental.atmospheric.md#function-saturation_vapor_pressure_derivative): Calculate the slope of the saturation vapor pressure curve (Δ) at a given temperature.
- [`soil_surface_vapor_pressure_deficit`](./postprocess.environmental.atmospheric.md#function-soil_surface_vapor_pressure_deficit): Calculate vapor pressure deficit at the soil surface.
- [`specific_heat_capacity_air`](./postprocess.environmental.atmospheric.md#function-specific_heat_capacity_air): Calculate the specific heat capacity of air (c_p).
- [`total_air_density`](./postprocess.environmental.atmospheric.md#function-total_air_density): Calculate moist-air density using the ideal gas law.
- [`vapor_pressure_deficit`](./postprocess.environmental.atmospheric.md#function-vapor_pressure_deficit): Atmospheric VPD at air temperature.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `saturation_vapor_pressure`

```python
saturation_vapor_pressure(T)
```

Calculate the saturation vapor pressure (e_s) at a given temperature.

Uses Tetens/Magnus-style equation.

e_s(T) = 0.6108 * exp( (17.27 * T) / (T + 237.3) )

Where:  
- e_s = Saturation Vapor Pressure (kPa)
- T = Temperature (°C)


**Args:**

- <b>`T`</b> (float): Temperature in degrees Celsius (°C)


**Returns:**

- <b>`float`</b>: Saturation vapor pressure in Pascal (Pa)



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `partial_vapor_pressure`

```python
partial_vapor_pressure(T, RH)
```

Calculate the actual vapor pressure (e_a) of air.

e_a = (RH / 100) * e_s

Where
- e_s = Saturation Vapor Pressure (Pa)
- RH = Relative Humidity [0-100] (%)
- e_a = Actual vapor pressure (Pa)


**Args:**

- T (float): Temperature of air in degrees Celsius.
- RH (float): Relative Humidity as a percentage.


**Returns:**

- <b>`float`</b>: Actual vapor pressure in Pascals.


**Raises:**

- <b>`ValueError`</b>: If RH is outside the range [0, 100].



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `vapor_pressure_deficit`

```python
vapor_pressure_deficit(T_air, RH)
```

Atmospheric VPD at air temperature.


**Args:**

- <b>`T_air`</b> (float): Air Temperature in degrees Celsius (°C)
- <b>`RH`</b> (float): Relative Humidity [0-100] (%)


**Returns:**

- <b>`float`</b>: Vapour pressure deficit (Pa).



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `soil_surface_vapor_pressure_deficit`

```python
soil_surface_vapor_pressure_deficit(T_air, RH, T_surface=None)
```

Calculate vapor pressure deficit at the soil surface.

The actual vapour pressure is calculated from air temperature and
relative humidity, while saturation vapour pressure is calculated
at the soil surface temperature.


**Args:**

- <b>`T_air`</b> (float): Air Temperature in degrees Celsius (°C)
- <b>`RH`</b> (float): Relative Humidity [0-100] (%)
- <b>`T_gnd`</b> (float, optional): Soil/surface temperature in degrees Celsius (°C).
    If None, air temperature is used. Defaults to None.


**Returns:**

- <b>`float`</b>: Soil-surface vapour pressure deficit (Pa).

> [!NOTE] 
> The calculation is:  
> 
> VPD_surface = e_s(T_surface) - e_a(T_air, RH)
> 
> where:  
> 
> e_s(T_surface) = saturation vapour pressure at the surface
> e_a(T_air, RH) = actual atmospheric vapour pressure



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L119"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `saturation_vapor_pressure_derivative`

```python
saturation_vapor_pressure_derivative(temp)
```

Calculate the slope of the saturation vapor pressure curve (Δ) at a given temperature.

The slope is the rate of change of saturation vapor pressure with respect to temperature.

delta = (4098 * e_s) / (T + 237.3)^2

Where:  
- e_s = Saturation Vapor Pressure (kPa)
- T = Temperature (°C)

This is used in the Penman-Monteith equation for evapotranspiration.


**Args:**

- <b>`temp`</b> (float): Temperature in degrees Celsius (°C).


**Returns:**

- <b>`float`</b>: Slope of the saturation vapor pressure curve in Pa/°C,
    dimensionally equivalent to Pa K⁻¹.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L148"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `dry_air_density`

```python
dry_air_density(T=20, Pa=101325.0)
```

Calculate dry air density

Uses Ideal Gas Law.


**Args:**

- <b>`T`</b> (float, optional): Air Temperature in degrees Celsius (°C). Defaults to 20 °C
- <b>`Pa`</b> (float, optional): Air pressure in Pascals (Pa). Defaults to 101325 Pa.


**Returns:**

- <b>`float`</b>: Dry air density (kg/m³).



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L166"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `total_air_density`

```python
total_air_density(RH, T, Pa=101325.0)
```

Calculate moist-air density using the ideal gas law.

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


**Args:**

- <b>`RH`</b> (float): Relative humidity [0-100] (%).
- <b>`T`</b> (float): Air Temperature in degrees Celsius (°C).
- <b>`Pa`</b> (float, optional): Air pressure in Pascals (Pa). Defaults to 101325 Pa.


**Returns:**

- <b>`float`</b>: Moist-air density (kg/m³).


**Raises:**

- <b>`ValueError`</b>: If atmospheric pressure is not positive or relative
    humidity is outside the range [0, 100].



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L210"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `calculate_specific_humidity`

```python
calculate_specific_humidity(RH, T, P)
```

Calculate specific humidity from relative humidity.

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


**Args:**

- <b>`RH`</b> (float): Relative humidity [%], from 0 to 100.
- <b>`T`</b> (float): Air temperature [°C].
- <b>`P`</b> (float): Atmospheric pressure [Pa].


**Returns:**

- <b>`float`</b>: Specific humidity [kg/kg].


**Raises:**

- <b>`ValueError`</b>: If ``P`` is not positive.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L252"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `specific_heat_capacity_air`

```python
specific_heat_capacity_air(T, RH=None, P=101325.0)
```

Calculate the specific heat capacity of air (c_p).

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


**Args:**

- <b>`T`</b> (float): Temperature of air in degrees Celsius (°C).
- <b>`RH`</b> (float, optional): Relative Humidity as a percentage [0-100] (%).
                      Defaults to None (dry air).
- <b>`P`</b> (float, optional): Atmospheric pressure in Pascals (Pa). 
                     Defaults to standard sea-level pressure (101325.0 Pa).


**Returns:**

- <b>`float`</b>: Specific heat capacity of air in Joules per kilogram 
       per degree Celsius (J kg^-1 °C^-1).


**Raises:**

- <b>`ValueError`</b>: If relative humidity is outside the range [0, 100],
    atmospheric pressure is less than or equal to zero, or actual
    vapor pressure is greater than or equal to atmospheric pressure.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L319"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `latent_heat_of_vaporisation_water`

```python
latent_heat_of_vaporisation_water(temp)
```

Calculate latent heat of vaporisation for water.


**Args:**

- <b>`temp`</b> (float): Temperature in degrees Celsius (°C)


**Returns:**

- <b>`float`</b>: Latent heat of vaporisation (J/kg)



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L333"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `psychrometric_constant`

```python
psychrometric_constant(P, temp=15, RH=None)
```

Calculate the psychrometric constant (gamma)

The psychrometric constant is given by the equation:  

γ = (c_p × P) / (λ × MW_ratio)

Where:  
- γ is the psychrometric constant in Pa/°C,
- c_p is the specific heat of dry air at constant pressure typically 1005 (J/(kg·K)),
- P is the atmospheric pressure in Pa (e.g., 101325 Pa at sea level),
- λ is the latent heat of vaporization of water in J/kg (e.g., 2.45 × 10⁶ J/kg),
- MW_ratio is molecular weight ratio of water vapor/dry air = 0.622


**Args:**

- <b>`P`</b> (float): Atmospheric pressure in pascal (Pa)
- <b>`temp`</b> (float, optional): Temperature in degrees Celsius (°C)
    Defaults to 15 °C.
- <b>`RH`</b> (float, optional): Relative Humidity as a percentage [0-100] (%).
    Defaults to None (uses dry air c_p baseline).


**Returns:**

- <b>`float`</b>: Psychometric constant in Pa/°C



