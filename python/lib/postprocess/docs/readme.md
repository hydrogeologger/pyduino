<!-- markdownlint-disable -->

# API Overview

## Modules

- [`postprocess.climate`](./postprocess.climate.md#module-postprocessclimate): postprocess climate subpackage
- [`postprocess.climate.evapotranspiration`](./postprocess.climate.evapotranspiration.md#module-postprocessclimateevapotranspiration): postprocess climate evapotranspiration module
- [`postprocess.climate.openmeteo_api`](./postprocess.climate.openmeteo_api.md#module-postprocessclimateopenmeteo_api): Open Meteo API module
- [`postprocess.common`](./postprocess.common.md#module-postprocesscommon): This module contain simple and common methods used in postprocess package.
- [`postprocess.extern`](./postprocess.extern.md#module-postprocessextern): This is a subpackage of postprocess containing repackaged modules from external sources.
- [`postprocess.filehandler`](./postprocess.filehandler.md#module-postprocessfilehandler): This module assist with working with files/images for post processing.
- [`postprocess.interpolation`](./postprocess.interpolation.md#module-postprocessinterpolation): Post processing interpolation module.
- [`postprocess.pandas_utils`](./postprocess.pandas_utils.md#module-postprocesspandas_utils): This module contains helper and wrapper functions to work with pandas dataframe objects.

## Classes

- [`filehandler.FileCorrelation`](./postprocess.filehandler.md#class-filecorrelation): Represents an image correlation object.
- [`filehandler.FileInfo`](./postprocess.filehandler.md#dataclass-fileinfo): Represents a file detail used in storing file/image correlation info.
- [`filehandler.FileMapXRef`](./postprocess.filehandler.md#dataclass-filemapxref): Cross Reference Object between files and mapped values.
- [`filehandler.MapValue`](./postprocess.filehandler.md#dataclass-mapvalue): Represents a pair of matched/mapped value.
- [`filehandler.XRefRecord`](./postprocess.filehandler.md#dataclass-xrefrecord): Cross Reference Record Object.
- [`interpolation.Interpolation`](./postprocess.interpolation.md#class-interpolation): Represents an interpolation object.

## Functions

- [`evapotranspiration.aerodynamic_resistance`](./postprocess.climate.evapotranspiration.md#function-aerodynamic_resistance): Calculate the aerodynamic resistance (r_a) using the logarithmic wind profile equation.
- [`evapotranspiration.air_specific_heat_capacity`](./postprocess.climate.evapotranspiration.md#function-air_specific_heat_capacity): Calculate the specific heat capacity of dry air at constant pressure (C_p)  as a function of temperature in Celsius using an empirical equation.
- [`evapotranspiration.calculate_actual_evapotranspiration`](./postprocess.climate.evapotranspiration.md#function-calculate_actual_evapotranspiration)
- [`evapotranspiration.calculate_kondo_surface_resistance`](./postprocess.climate.evapotranspiration.md#function-calculate_kondo_surface_resistance): Calculate the surface resistance (r_s) for a given soil type using the Kondo and Saigusa (1990) model.
- [`evapotranspiration.celsius_to_kelvin`](./postprocess.climate.evapotranspiration.md#function-celsius_to_kelvin): Convert temperature from Celsius to Kelvin
- [`evapotranspiration.dry_air_density`](./postprocess.climate.evapotranspiration.md#function-dry_air_density): Calculate dry air density
- [`evapotranspiration.fao_penman_monteith`](./postprocess.climate.evapotranspiration.md#function-fao_penman_monteith): Compute evapotranspiration rate using the FAO Penman–Monteith equation.
- [`evapotranspiration.kelvin_to_celsius`](./postprocess.climate.evapotranspiration.md#function-kelvin_to_celsius): Convert temperature from Kelvin to Celsius
- [`evapotranspiration.latent_heat_of_vaporisation_water`](./postprocess.climate.evapotranspiration.md#function-latent_heat_of_vaporisation_water): Calculate latent heat of vaporisation for water.
- [`evapotranspiration.net_solar_radiation`](./postprocess.climate.evapotranspiration.md#function-net_solar_radiation): Calculate the net radiation (R_n) using solar and longwave radiation components.
- [`evapotranspiration.partial_vapor_pressure`](./postprocess.climate.evapotranspiration.md#function-partial_vapor_pressure): Calculate the actual vapor pressure (E_a) of air.
- [`evapotranspiration.penman_monteith`](./postprocess.climate.evapotranspiration.md#function-penman_monteith): Compute evapotranspiration rate using the Penman–Monteith equation (resistance form).
- [`evapotranspiration.psychrometric_constant`](./postprocess.climate.evapotranspiration.md#function-psychrometric_constant): Calculate the psychrometric constant (gamma)
- [`evapotranspiration.saturation_vapor_pressure`](./postprocess.climate.evapotranspiration.md#function-saturation_vapor_pressure): Calculate the saturation vapor pressure (E_s) at a given temperature.
- [`evapotranspiration.saturation_vapor_pressure_derivative`](./postprocess.climate.evapotranspiration.md#function-saturation_vapor_pressure_derivative): Calculate the slope of the saturation vapor pressure curve (Δ) at a given temperature.
- [`evapotranspiration.total_air_density`](./postprocess.climate.evapotranspiration.md#function-total_air_density): Calculate total air density
- [`evapotranspiration.vapor_pressure_deficit`](./postprocess.climate.evapotranspiration.md#function-vapor_pressure_deficit): Calculate vapor pressure deficit at soil surface.
- [`openmeteo_api.extract_daily_dataframe`](./postprocess.climate.openmeteo_api.md#function-extract_daily_dataframe): Extract daily timeseries data from Open-Meteo API JSON into DataFrame.
- [`openmeteo_api.extract_hourly_dataframe`](./postprocess.climate.openmeteo_api.md#function-extract_hourly_dataframe): Extract hourly timeseries data from Open-Meteo API JSON into DataFrame.
- [`openmeteo_api.get_historical`](./postprocess.climate.openmeteo_api.md#function-get_historical): Fetch historical weather data for one or more coordinates.
- [`common.calculate_delta`](./postprocess.common.md#function-calculate_delta): Calculates the difference (delta) between a single reference value from a set of values.
- [`common.normalise`](./postprocess.common.md#function-normalise): Map a value to between 0 and 1.
- [`pandas_utils.add_multindex_level`](./postprocess.pandas_utils.md#function-add_multindex_level): Add extra levels to index.
- [`pandas_utils.swap_index`](./postprocess.pandas_utils.md#function-swap_index): Inplace swap of DataFrame index with existing given keys.
- [`pandas_utils.unique_index_levels_only`](./postprocess.pandas_utils.md#function-unique_index_levels_only): Remove column heading rows which are not unique from DataFrame.
