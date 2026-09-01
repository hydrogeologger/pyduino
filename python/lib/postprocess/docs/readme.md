<!-- markdownlint-disable -->

# API Overview

## Modules

- [`postprocess.conversion`](./postprocess.conversion.md#module-postprocessconversion): Utilities for converting between common units and rates.
- [`postprocess.environmental`](./postprocess.environmental.md#module-postprocessenvironmental): Environmental calculations for meteorological and environmental data.
- [`postprocess.environmental.atmospheric`](./postprocess.environmental.atmospheric.md#module-postprocessenvironmentalatmospheric): Atmospheric thermodynamic calculations used by environmental models.
- [`postprocess.environmental.evapotranspiration`](./postprocess.environmental.evapotranspiration.md#module-postprocessenvironmentalevapotranspiration): Methods for calculating evapotranspiration from meteorological data.
- [`postprocess.environmental.radiation`](./postprocess.environmental.radiation.md#module-postprocessenvironmentalradiation): Radiation calculations used by environmental and evapotranspiration models.
- [`postprocess.environmental.resistance`](./postprocess.environmental.resistance.md#module-postprocessenvironmentalresistance): Aerodynamic and surface resistance calculations for environmental models.
- [`postprocess.extern`](./postprocess.extern.md#module-postprocessextern): This is a subpackage of postprocess containing repackaged modules from external sources.
- [`postprocess.file_matching`](./postprocess.file_matching.md#module-postprocessfile_matching): Utilities for matching files to external data records.
- [`postprocess.interpolation`](./postprocess.interpolation.md#module-postprocessinterpolation): Post processing interpolation module.
- [`postprocess.pandas_utils`](./postprocess.pandas_utils.md#module-postprocesspandas_utils): This module contains helper and wrapper functions to work with pandas dataframe objects.
- [`postprocess.sources`](./postprocess.sources.md#module-postprocesssources): Interfaces for retrieving and handling data from external sources.
- [`postprocess.sources.openmeteo`](./postprocess.sources.openmeteo.md#module-postprocesssourcesopenmeteo): Utilities for retrieving meteorological data from the Open-Meteo API.
- [`postprocess.sources.silo`](./postprocess.sources.silo.md#module-postprocesssourcessilo): Utilities for retrieving historical meteorological data from SILO API.
- [`postprocess.sources.utils`](./postprocess.sources.utils.md#module-postprocesssourcesutils): Common utility and shared resources for the postprocess.sources subpackage.
- [`postprocess.transformation`](./postprocess.transformation.md#module-postprocesstransformation): Common data transformation utilities.

## Classes

- [`file_matching.FileCorrelation`](./postprocess.file_matching.md#class-filecorrelation): Represents an image correlation object.
- [`file_matching.FileInfo`](./postprocess.file_matching.md#dataclass-fileinfo): Represents a file detail used in storing file/image correlation info.
- [`file_matching.FileMapXRef`](./postprocess.file_matching.md#dataclass-filemapxref): Cross Reference Object between files and mapped values.
- [`file_matching.MapValue`](./postprocess.file_matching.md#dataclass-mapvalue): Represents a pair of matched/mapped value.
- [`file_matching.XRefRecord`](./postprocess.file_matching.md#dataclass-xrefrecord): Cross Reference Record Object.
- [`interpolation.Interpolation`](./postprocess.interpolation.md#class-interpolation): Represents an interpolation object.
- [`silo.SILOStationMetadata`](./postprocess.sources.silo.md#class-silostationmetadata): SILO Longpaddock BOM Station Metadata.
- [`utils.LocationMetadata`](./postprocess.sources.utils.md#class-locationmetadata): Stores geographical metadata for general locations.

## Functions

- [`conversion.celsius_to_kelvin`](./postprocess.conversion.md#function-celsius_to_kelvin): Convert a temperature from degrees Celsius to Kelvin.
- [`conversion.kelvin_to_celsius`](./postprocess.conversion.md#function-kelvin_to_celsius): Convert a temperature from Kelvin to degrees Celsius.
- [`conversion.per_second_to_daily`](./postprocess.conversion.md#function-per_second_to_daily): Convert a per-second rate to an equivalent daily rate.
- [`conversion.per_second_to_hourly`](./postprocess.conversion.md#function-per_second_to_hourly): Convert a per-second rate to an equivalent hourly rate.
- [`atmospheric.calculate_specific_humidity`](./postprocess.environmental.atmospheric.md#function-calculate_specific_humidity): Calculate specific humidity from relative humidity.
- [`atmospheric.dry_air_density`](./postprocess.environmental.atmospheric.md#function-dry_air_density): Calculate dry air density
- [`atmospheric.latent_heat_of_vaporisation_water`](./postprocess.environmental.atmospheric.md#function-latent_heat_of_vaporisation_water): Calculate latent heat of vaporisation for water.
- [`atmospheric.partial_vapor_pressure`](./postprocess.environmental.atmospheric.md#function-partial_vapor_pressure): Calculate the actual vapor pressure (e_a) of air.
- [`atmospheric.psychrometric_constant`](./postprocess.environmental.atmospheric.md#function-psychrometric_constant): Calculate the psychrometric constant (gamma)
- [`atmospheric.saturation_vapor_pressure`](./postprocess.environmental.atmospheric.md#function-saturation_vapor_pressure): Calculate the saturation vapor pressure (e_s) at a given temperature.
- [`atmospheric.saturation_vapor_pressure_derivative`](./postprocess.environmental.atmospheric.md#function-saturation_vapor_pressure_derivative): Calculate the slope of the saturation vapor pressure curve (Δ) at a given temperature.
- [`atmospheric.soil_surface_vapor_pressure_deficit`](./postprocess.environmental.atmospheric.md#function-soil_surface_vapor_pressure_deficit): Calculate vapor pressure deficit at the soil surface.
- [`atmospheric.specific_heat_capacity_air`](./postprocess.environmental.atmospheric.md#function-specific_heat_capacity_air): Calculate the specific heat capacity of air (c_p).
- [`atmospheric.total_air_density`](./postprocess.environmental.atmospheric.md#function-total_air_density): Calculate moist-air density using the ideal gas law.
- [`atmospheric.vapor_pressure_deficit`](./postprocess.environmental.atmospheric.md#function-vapor_pressure_deficit): Atmospheric VPD at air temperature.
- [`evapotranspiration.calculate_soil_evaporation`](./postprocess.environmental.evapotranspiration.md#function-calculate_soil_evaporation): Calculate soil evaporation flux using the Penman–Monteith equation for a soil surface.
- [`evapotranspiration.fao_penman_monteith`](./postprocess.environmental.evapotranspiration.md#function-fao_penman_monteith): Compute evapotranspiration rate using the FAO Penman–Monteith equation.
- [`evapotranspiration.penman_monteith`](./postprocess.environmental.evapotranspiration.md#function-penman_monteith): Compute evapotranspiration rate using the Penman–Monteith equation (resistance form).
- [`radiation.net_radiation_energy`](./postprocess.environmental.radiation.md#function-net_radiation_energy): Calculate accumulated net radiation energy over a time interval.
- [`radiation.net_radiation_flux`](./postprocess.environmental.radiation.md#function-net_radiation_flux): Calculate net radiation as an instantaneous energy flux.
- [`resistance.aerodynamic_resistance`](./postprocess.environmental.resistance.md#function-aerodynamic_resistance): Calculate the aerodynamic resistance (r_a) using the logarithmic wind profile equation.
- [`resistance.estimate_soil_surface_resistance`](./postprocess.environmental.resistance.md#function-estimate_soil_surface_resistance): Estimate soil surface resistance from volumetric water content.
- [`pandas_utils.add_multindex_level`](./postprocess.pandas_utils.md#function-add_multindex_level): Add extra levels to index.
- [`pandas_utils.swap_index`](./postprocess.pandas_utils.md#function-swap_index): Inplace swap of DataFrame index with existing given keys.
- [`pandas_utils.unique_index_levels_only`](./postprocess.pandas_utils.md#function-unique_index_levels_only): Remove column heading rows which are not unique from DataFrame.
- [`openmeteo.extract_timeseries_dataframe`](./postprocess.sources.openmeteo.md#function-extract_timeseries_dataframe): Extract timeseries data from Open-Meteo API JSON into DataFrame.
- [`openmeteo.get_historical`](./postprocess.sources.openmeteo.md#function-get_historical): Fetch historical weather data for one or more coordinates.
- [`openmeteo.get_location_meta`](./postprocess.sources.openmeteo.md#function-get_location_meta): Get location info metadata from API response json object.
- [`silo.extract_timeseries_dataframe`](./postprocess.sources.silo.md#function-extract_timeseries_dataframe): Extract timeseries data from SILO API point data response into DataFrame.
- [`silo.find_nearby_stations`](./postprocess.sources.silo.md#function-find_nearby_stations): Return nearby SILO stations relative to a station or coordinates.
- [`silo.get_location_meta`](./postprocess.sources.silo.md#function-get_location_meta): Get station info from retrieved point or drill data.
- [`silo.get_nearby_stations`](./postprocess.sources.silo.md#function-get_nearby_stations): Return SILO stations within a radius of a reference station.
- [`silo.get_point_data`](./postprocess.sources.silo.md#function-get_point_data): Retrieve climate data from the SILO point dataset.
- [`utils.haversine_distance`](./postprocess.sources.utils.md#function-haversine_distance): Computes great-circle distance between two geographic coordinates.
- [`utils.is_valid_coordinates`](./postprocess.sources.utils.md#function-is_valid_coordinates): Check whether a value is a valid (latitude, longitude) coordinate pair.
- [`transformation.calculate_delta`](./postprocess.transformation.md#function-calculate_delta): Calculates the difference (delta) between a single reference value from a set of values.
- [`transformation.normalise`](./postprocess.transformation.md#function-normalise): Map a value to between 0 and 1.
