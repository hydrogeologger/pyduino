<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.environmental.atmospheric`
Atmospheric thermodynamic calculations used by environmental models.

Provides functions for calculating water-vapor properties, air density,
specific heat capacity, latent heat, and psychrometric properties required
by evapotranspiration models.


## Table of Contents
- [`actual_vapor_pressure`](./postprocess.environmental.atmospheric.md#function-actual_vapor_pressure): Calculate actual vapor pressure (e_a), also known as partial vapor pressure of water vapor.
- [`actual_vapor_pressure_from_extremes`](./postprocess.environmental.atmospheric.md#function-actual_vapor_pressure_from_extremes): Calculate actual vapor pressure (e_a) from temperature and RH extremes
- [`calculate_specific_humidity`](./postprocess.environmental.atmospheric.md#function-calculate_specific_humidity): Calculate specific humidity from relative humidity.
- [`calculate_temperature_lapse_rate`](./postprocess.environmental.atmospheric.md#function-calculate_temperature_lapse_rate): Calculate the atmospheric temperature lapse rate.
- [`dry_air_density`](./postprocess.environmental.atmospheric.md#function-dry_air_density): Calculate dry air density
- [`estimate_atmospheric_pressure`](./postprocess.environmental.atmospheric.md#function-estimate_atmospheric_pressure): Estimate atmospheric pressure at altitude z.
- [`latent_heat_of_vaporisation_water`](./postprocess.environmental.atmospheric.md#function-latent_heat_of_vaporisation_water): Calculate latent heat of vaporisation for water.
- [`psychrometric_constant`](./postprocess.environmental.atmospheric.md#function-psychrometric_constant): Calculate the psychrometric constant (gamma)
- [`saturation_vapor_pressure_buck`](./postprocess.environmental.atmospheric.md#function-saturation_vapor_pressure_buck): Calculate saturation vapor pressure (e_s) at a given temperature using the Buck equation.
- [`saturation_vapor_pressure_mean_tetens`](./postprocess.environmental.atmospheric.md#function-saturation_vapor_pressure_mean_tetens): Calculate the mean saturation vapor pressure using the Tetens equation.
- [`saturation_vapor_pressure_slope_tetens`](./postprocess.environmental.atmospheric.md#function-saturation_vapor_pressure_slope_tetens): Calculate the slope of the saturation vapor pressure curve (Δ) with respect to temperature using the Tetens equation.
- [`saturation_vapor_pressure_tetens`](./postprocess.environmental.atmospheric.md#function-saturation_vapor_pressure_tetens): Calculate the saturation vapor pressure (e_s) at a given temperature using the Tetens equation.
- [`specific_heat_capacity_air`](./postprocess.environmental.atmospheric.md#function-specific_heat_capacity_air): Calculate the specific heat capacity of air (c_p).
- [`total_air_density`](./postprocess.environmental.atmospheric.md#function-total_air_density): Calculate moist-air density using the ideal gas law.
- [`vapor_pressure_deficit`](./postprocess.environmental.atmospheric.md#function-vapor_pressure_deficit): Calculate vapor pressure deficit (VPD).
- [`wind_speed_at_2m`](./postprocess.environmental.atmospheric.md#function-wind_speed_at_2m): Convert wind speed measured at a given height to wind speed at 2 m.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `saturation_vapor_pressure_buck`

```python
saturation_vapor_pressure_buck(T)
```

Calculate saturation vapor pressure (e_s) at a given temperature using the Buck equation.

The Buck equation is an empirical approximation of saturation vapor
pressure over water. It provides a highly accurate approximation for
temperatures above 0 °C and is more accurate than the Tetens equation,
particularly at higher temperatures.

e_s(T) = 0.61121 * exp((18.678 - T / 234.5) * T / (257.14 + T))

Where:  
- e_s = Saturation Vapor Pressure (kPa)
- T = Temperature (°C)


**Args:**

- <b>`T`</b> (float): Temperature in degrees Celsius (°C).


**Returns:**

- <b>`float`</b>: Saturation Vapor Pressure in Pascal (Pa).


**Raises:**

- <b>`ValueError`</b>: If ``T`` is not finite.


**See Also:**

:func:`saturation_vapor_pressure_tetens`


**References:**

- https://en.wikipedia.org/wiki/Vapour_pressure_of_water



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L80"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `saturation_vapor_pressure_tetens`

```python
saturation_vapor_pressure_tetens(T)
```

Calculate the saturation vapor pressure (e_s) at a given temperature using
    the Tetens equation.

Uses the Tetens equation, which provides a good approximation of
saturation vapor pressure over liquid water, particularly for
temperatures between 0 and 50 °C.

e_s(T) = 0.6108 * exp( (17.27 * T) / (T + 237.3) )

Where:  
- e_s = Saturation Vapor Pressure (kPa)
- T = Temperature (°C)


**Args:**

- <b>`T`</b> (float): Temperature in degrees Celsius (°C)


**Returns:**

- <b>`float`</b>: Saturation Vapor Pressure in Pascal (Pa)


**Raises:**

- <b>`ValueError`</b>: If ``T`` is not finite.

> [!NOTE] 
> Due to the non-linearity of the equation, mean saturation vapor
> pressure over a period should be calculated as the mean of the
> saturation vapor pressures at the period's mean minimum and
> maximum air temperatures. See :func:`saturation_vapor_pressure_mean`.


**See Also:**

:func:`saturation_vapor_pressure_buck`


**References:**

- https://www.fao.org/4/X0490E/x0490e07.htm#measurement
- https://en.wikipedia.org/wiki/Vapour_pressure_of_water



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L124"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `saturation_vapor_pressure_mean_tetens`

```python
saturation_vapor_pressure_mean_tetens(tmin, tmax)
```

Calculate the mean saturation vapor pressure using the Tetens equation.

Mean saturation vapor pressure is calculated from the saturation vapor
pressures at the daily minimum and maximum air temperatures. Using mean
air temperature directly can underestimate the mean saturation vapor
pressure due to the non-linearity of the saturation vapor pressure
equation.

e_s = (e_s[T_max] + e_s[T_min]) / 2

Where:  
- e_s[T_max] = Saturation Vapor Pressure at maximum temperature.
- e_s[T_min] = Saturation Vapor Pressure at minimum temperature.


**Args:**

- <b>`tmin`</b> (float): Minimum temperature in degrees Celsius (°C)
- <b>`tmax`</b> (float): Maximum temperature in degrees Celsius (°C)


**Returns:**

- <b>`float`</b>: Mean saturation vapor pressure in Pascal (Pa)


**See Also:**

:func:`saturation_vapor_pressure_tetens`



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L157"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `actual_vapor_pressure`

```python
actual_vapor_pressure(T, RH)
```

Calculate actual vapor pressure (e_a), also known as
partial vapor pressure of water vapor.

e_a = (RH / 100) * e_s

Where
- e_s = Saturation Vapor Pressure (Pa)
- RH = Relative Humidity [0-100] (%)
- e_a = Actual vapor pressure (Pa)


**Args:**

- <b>`T`</b> (float): Temperature of air in degrees Celsius. Typical minimum temperature.
- <b>`RH`</b> (float): Relative Humidity as a percentage (0-100). Typical RH max.


**Returns:**

- <b>`float`</b>: Actual vapor pressure in Pascals.


**Raises:**

- <b>`ValueError`</b>: If RH is outside the range [0, 100].

> [!NOTE] 
> For daily estimates of actual vapor pressure, this function can be
> evaluated at the daily minimum temperature and maximum relative
> humidity when only RH_max is available. See
> :func:`actual_vapor_pressure_from_extremes`.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `actual_vapor_pressure_from_extremes`

```python
actual_vapor_pressure_from_extremes(temperature, relative_humidity)
```

Calculate actual vapor pressure (e_a) from temperature and RH extremes

This function implements the standard FAO-56 Equation 17. It pairs the maximum 
relative humidity with the minimum temperature (when the air is closest to saturation), 
and the minimum relative humidity with the maximum temperature.

e_a = (e_a[T_min, RH_max] + e_a[T_max, RH_min]) / 2

Where
- e_a[T_min, RH_max] = Actual vapor pressure (Pa) at daily minimum temperature,
    maximum relative humidity (0-100%).
- e_a[T_max, RH_min]) = Actual vapor pressure (Pa) at daily maximum temperature,
    minimum relative humidity (0-100%).


**Args:**

- <b>`temperature`</b>: Minimum and maximum air temperature in degrees Celsius (°C),
    as ``(tmin, tmax)``.
- <b>`relative_humidity`</b>: Minimum and maximum relative humidity in percent (0-100%),
    as ``(rh_min, rh_max)``.


**Returns:**

- <b>`float`</b>: Actual vapor pressure in Pascals.


**Raises:**

- <b>`ValueError`</b>: If maximum values are less than minimum values, 
    or if relative humidity values fall outside.


**Notes:**

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


**References:**

- https://www.fao.org/4/X0490E/x0490e07.htm#measurement



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L278"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `vapor_pressure_deficit`

```python
vapor_pressure_deficit(temperature, RH)
```

Calculate vapor pressure deficit (VPD).

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


**Args:**

- <b>`temperature`</b> (float or tuple): Air temperature in degrees Celsius (°C), or period
    minimum and maximum air temperatures as ``(tmin, tmax)``.
- <b>`RH`</b> (float or tuple): Relative humidity as a percentage (0-100%), or
    minimum and maximum relative humidity as ``(rh_min, rh_max)``.
    When ``temperature`` contains minimum and maximum values and
    this is scalar, it is interpreted as maximum relative humidity
    (RH_max).


**Returns:**

- <b>`float`</b>: Vapor pressure deficit in Pascal (Pa).


**Raises:**

- <b>`ValueError`</b>: If temperature or relative humidity inputs are invalid.


**References:**

FAO-56, Equations 17 and 18.
- https://www.fao.org/4/X0490E/x0490e07.htm#air%20humidity
- https://www.fao.org/4/X0490E/x0490e07.htm#calculation%20procedures



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L369"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `saturation_vapor_pressure_slope_tetens`

```python
saturation_vapor_pressure_slope_tetens(temperature)
```

Calculate the slope of the saturation vapor pressure curve (Δ) with respect
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


**Args:**

- <b>`temperature`</b> (float or tuple): Temperature in degrees Celsius (°C),
    or minimum and maximum temperatures as ``(tmin, tmax)``.


**Returns:**

- <b>`float`</b>: Slope of the saturation vapor pressure curve in Pa/°C,
    dimensionally equivalent to Pa K⁻¹.


**Raises:**

- <b>`ValueError`</b>: If ``temperature`` is a tuple or list that does not
    contain exactly two values.


**References:**

- https://www.fao.org/4/X0490E/x0490e07.htm#calculation%20procedures



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L425"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

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

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L443"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `total_air_density`

```python
total_air_density(RH, T, Pa=101325.0)
```

Calculate moist-air density using the ideal gas law.

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


**Args:**

- <b>`RH`</b> (float): Relative humidity [0-100] (%).
- <b>`T`</b> (float): Air Temperature in degrees Celsius (°C).
- <b>`Pa`</b> (float, optional): Air pressure in Pascals (Pa). Defaults to 101325 Pa.


**Returns:**

- <b>`float`</b>: Moist-air density (kg/m³).


**Raises:**

- <b>`ValueError`</b>: If atmospheric pressure is not finite or positive, or if
    relative humidity is not finite or is outside the range 0-100%.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L487"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

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

- <b>`ValueError`</b>: ValueError: If atmospheric pressure is not finite or positive, or if
    relative humidity is not finite or is outside the range 0-100%.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L530"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

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
ValueError:
    - If relative humidity is not finite or is outside the range
        0-100%.
    - If atmospheric pressure is not finite or is not positive.
    - If actual vapor pressure is greater than or equal to atmospheric
        pressure.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L603"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

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

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L617"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

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



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L655"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `calculate_temperature_lapse_rate`

```python
calculate_temperature_lapse_rate(T_2, z_2, T_1=15, z_1=0)
```

Calculate the atmospheric temperature lapse rate.

The temperature lapse rate L describes the rate at which atmospheric
temperature changes with altitude.

The equation is:  

    L = (T_1 - T_2) / (z_2 - z_1)

Default starting conditions as defined by International Standard Atmosphere (ISA).


**Args:**

- <b>`T_2`</b> (float): Temperature at the second measurement point in degrees Celsius.
- <b>`z_2`</b> (float): Altitude of the second measurement point in meters.
- <b>`T_1`</b> (float, optional): Temperature at the first measurement point
    in degrees Celsius. Defaults to 15 K.
- <b>`z_1`</b> (float, optional): Altitude of the first measurement point in meters.
    Defaults to 0 m (Sea Level).


**Returns:**

Temperature lapse rate `L` in Celsius per meter.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L689"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `wind_speed_at_2m`

```python
wind_speed_at_2m(wind_speed, measurement_height)
```

Convert wind speed measured at a given height to wind speed at 2 m.

Uses the FAO-56 wind profile relationship:  

    u_2 = u_z * 4.87 / ln(67.8z - 5.42)

Where:  
- u_2 = Wind speed at 2 m above ground (m/s)
- u_z = Wind speed measured at height z (m/s)
- z = Height of wind measurement above ground (m)


**Args:**

- <b>`wind_speed`</b> (float): Wind speed measured at the specified height,
    in metres per second (m/s).
- <b>`measurement_height`</b> (float): Height of the wind speed measurement
    above ground, in metres (m).


**Returns:**

- <b>`float`</b>: Wind speed at 2 m above ground, in metres per second (m/s).


**Raises:**

- <b>`ValueError`</b>: If ``wind_speed`` or ``measurement_height`` is not
    finite, or if ``measurement_height`` is not valid for the
    wind profile relationship.


**References:**

- https://www.fao.org/4/X0490E/x0490e07.htm#wind%20profile%20relationship



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/atmospheric.py#L741"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `estimate_atmospheric_pressure`

```python
estimate_atmospheric_pressure(z, P_0=101325.0, T_0=15, L=0.0065)
```

Estimate atmospheric pressure at altitude z.

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


**Args:**

- <b>`z`</b>: Altitude z above sea level in meters.
- <b>`P_0`</b>: Sea-level atmospheric pressure P_0 in pascals.
- <b>`T_0`</b>: Sea-level temperature T_0 in degrees Celsius.
- <b>`L`</b>: Temperature lapse rate L in degrees Celsius per meter.


**Returns:**

Estimated atmospheric pressure P(z) in pascals.


**Raises:**

- <b>`ValueError`</b>: If the calculated temperature is less than or equal
    to zero Kelvin.



