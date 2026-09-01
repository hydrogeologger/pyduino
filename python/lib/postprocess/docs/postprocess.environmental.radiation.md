<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/radiation.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.environmental.radiation`
Radiation calculations used by environmental and evapotranspiration models.

Provides functions for calculating radiation quantities.


## Table of Contents
- [`net_radiation_energy`](./postprocess.environmental.radiation.md#function-net_radiation_energy): Calculate accumulated net radiation energy over a time interval.
- [`net_radiation_flux`](./postprocess.environmental.radiation.md#function-net_radiation_flux): Calculate net radiation as an instantaneous energy flux.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/radiation.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `net_radiation_flux`

```python
net_radiation_flux(
    R_s,
    T_a_C,
    T_s_C=None,
    albedo=0.23,
    epsilon_s=0.95,
    epsilon_a=0.75
)
```

Calculate net radiation as an instantaneous energy flux.

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


**Args:**

- <b>`R_s`</b> (float): Incoming shortwave solar radiation flux (W/m²), equivalent to J/m²/s.
    The absorbed shortwave component is calculated using the surface albedo.
- <b>`T_a_C`</b> (float): Air temperature in degrees Celsius (°C).
- <b>`T_s_C`</b> (float, optional): Surface temperature in degrees Celsius (°C).
    If ``None``, the air temperature is used. Defaults to ``None``.
- <b>`albedo`</b> (float, optional): Surface albedo [α], dimensionless between 0 and 1.
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

- <b>`epsilon_s`</b> (float, optional): Surface emissivity [ε_s], dimensionless and
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

- <b>`epsilon_a`</b> (float, optional): Atmospheric emissivity [ε_a] (sky),
    dimensionless and between 0 and 1. Defaults to 0.75.

    The range is between 0 and 1, where 1 indicates a perfect blackbody emitter.
    Typical Values:
    - Dry atmosphere: 0.60 - 0.70
    - Moderate humidity: 0.75 - 0.80
    - Humid, cloudy atmosphere: 0.80 - 0.90
    - Clear sky, low humidity: 0.60 - 0.70
    - Tropical or monsoon climates: 0.80 - 0.85


**Returns:**

- <b>`float`</b>: Net radiation. Returns W/m², equivalent to J/m²/s.


**Raises:**

- <b>`ValueError`</b>: If ``R_s`` is negative, ``albedo`` is outside [0, 1],
    ``epsilon_s`` is outside [0, 1], ``epsilon_a`` is outside [0, 1].



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/environmental/radiation.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `net_radiation_energy`

```python
net_radiation_energy(
    R_s,
    T_a_C,
    time_step_seconds,
    T_s_C=None,
    albedo=0.23,
    epsilon_s=0.95,
    epsilon_a=0.75
)
```

Calculate accumulated net radiation energy over a time interval.

The net radiation flux is calculated using :func:`net_radiation_flux`
and multiplied by the specified timestep. This assumes that the
calculated radiation flux is representative of the entire interval.


**Args:**

- <b>`R_s`</b> (float): Incoming shortwave solar radiation flux (W/m²), equivalent to J/m²/s.
- <b>`T_a_C`</b> (float): Air temperature in degrees Celsius (°C).
- <b>`time_step_seconds`</b> (int or float): Duration of the time interval in seconds.

    Typical values:
    - ``1``: output is a flux in W/m² (equivalent to J/m²/s).
    - ``3600``: output is accumulated energy over one hour in J/m².
    - ``86400``: output is accumulated energy over one day in J/m².

- <b>`T_s_C`</b> (float, optional): Surface temperature in degrees Celsius (°C).
    If ``None``, air temperature is used.
- <b>`albedo`</b> (float, optional): Surface albedo [0, 1].
    Defaults to 0.23.
- <b>`epsilon_s`</b> (float, optional): Surface emissivity [0, 1].
    Defaults to 0.95.
- <b>`epsilon_a`</b> (float, optional): Atmospheric emissivity [0, 1].
    Defaults to 0.75.


**Returns:**

- <b>`float`</b>: Accumulated net radiation energy in J/m².


**Raises:**

- <b>`ValueError`</b>: If ``time_step_seconds`` is not a positive value or
    any radiation input violates the constraints of
    :func:`net_radiation_flux`.



