<!-- markdownlint-disable -->

# API Overview

## Modules

- [`postprocess.conversion`](./postprocess.conversion.md#module-postprocessconversion): Utilities for converting between common units and rates.
- [`postprocess.extern`](./postprocess.extern.md#module-postprocessextern): This is a subpackage of postprocess containing repackaged modules from external sources.
- [`postprocess.file_matching`](./postprocess.file_matching.md#module-postprocessfile_matching): Utilities for matching files to external data records.
- [`postprocess.interpolation`](./postprocess.interpolation.md#module-postprocessinterpolation): Post processing interpolation module.
- [`postprocess.pandas_utils`](./postprocess.pandas_utils.md#module-postprocesspandas_utils): This module contains helper and wrapper functions to work with pandas dataframe objects.
- [`postprocess.sources`](./postprocess.sources.md#module-postprocesssources): Interfaces for retrieving and handling data from external sources.
- [`postprocess.sources.bom`](./postprocess.sources.bom.md#module-postprocesssourcesbom): Access historical climate and weather observations from Australian Bureau of Meteorology data services.
- [`postprocess.sources.bom.cdio`](./postprocess.sources.bom.cdio.md#module-postprocesssourcesbomcdio): Client for accessing historical climate and weather observations from the Australian Bureau of Meteorology's Climate Data Online service.
- [`postprocess.sources.bom.ftp`](./postprocess.sources.bom.ftp.md#module-postprocesssourcesbomftp): Access historical climate and weather observation data from the Australian Bureau of Meteorology's anonymous FTP service.
- [`postprocess.sources.bom.types`](./postprocess.sources.bom.types.md#module-postprocesssourcesbomtypes): Shared type definitions for the postprocess.sources.bom subpackage.
- [`postprocess.sources.openmeteo`](./postprocess.sources.openmeteo.md#module-postprocesssourcesopenmeteo): Utilities for retrieving meteorological data from the Open-Meteo API.
- [`postprocess.sources.silo`](./postprocess.sources.silo.md#module-postprocesssourcessilo): Utilities for retrieving historical meteorological data from SILO API.
- [`postprocess.sources.types`](./postprocess.sources.types.md#module-postprocesssourcestypes): Shared type definitions for the postprocess.sources subpackage.
- [`postprocess.sources.utils`](./postprocess.sources.utils.md#module-postprocesssourcesutils): Common utility and shared resources for the postprocess.sources subpackage.
- [`postprocess.transformation`](./postprocess.transformation.md#module-postprocesstransformation): Common data transformation utilities.

## Classes

- [`file_matching.FileCorrelator`](./postprocess.file_matching.md#class-filecorrelator): Represents a file correlation and metadata parsing manager.
- [`file_matching.FileInfo`](./postprocess.file_matching.md#dataclass-fileinfo): Represents a file detail used in storing file/image correlation info.
- [`file_matching.FileMapping`](./postprocess.file_matching.md#dataclass-filemapping): Manages cross-reference links between parsed files and matched data values.
- [`file_matching.MappingRecord`](./postprocess.file_matching.md#dataclass-mappingrecord): Represents a single cross-reference linking a file index to a matched value.
- [`file_matching.MatchPair`](./postprocess.file_matching.md#dataclass-matchpair): Represents a pair of matched/mapped value.
- [`interpolation.Interpolation`](./postprocess.interpolation.md#class-interpolation): Represents an interpolation object.
- [`cdio.DWOStation`](./postprocess.sources.bom.cdio.md#class-dwostation): DWOStation(dwo_id, station_id, name, state, distance_km, is_open)
- [`cdio.Location`](./postprocess.sources.bom.cdio.md#class-location): Represents a geographic location returned from BOM gazetteer.
- [`cdio.StationFinder`](./postprocess.sources.bom.cdio.md#class-stationfinder): An execution system mirroring the BOM Climate Data Online Text Tool Guide.
- [`cdio.WeatherObservationsClient`](./postprocess.sources.bom.cdio.md#class-weatherobservationsclient): Client for finding stations and retrieving BOM daily weather observations.
- [`ftp.BOMStationDistanceRecord`](./postprocess.sources.bom.ftp.md#class-bomstationdistancerecord): BOMStationDistanceRecord(distance_km, station)
- [`ftp.DailyWeatherObservations`](./postprocess.sources.bom.ftp.md#class-dailyweatherobservations): Client for accessing daily weather observations via FTP.
- [`types.BOMStationBase`](./postprocess.sources.bom.types.md#class-bomstationbase): Base Bureau of Meteorology Station Metadata.
- [`types.BOMStationRecord`](./postprocess.sources.bom.types.md#class-bomstationrecord): BOMStationRecord(station_id, region, name, start_date, end_date, latitude, longitude, source, state, elevation_m, barometer_height_m, wmo_id)
- [`silo.SILOStation`](./postprocess.sources.silo.md#class-silostation): SILO Longpaddock BOM Station Metadata.
- [`silo.SILOStationRecord`](./postprocess.sources.silo.md#class-silostationrecord): SILOStationRecord(station_id, name, latitude, longitude, state, elevation_m, distance_km)
- [`types.Coordinates`](./postprocess.sources.types.md#class-coordinates): Represents a geographic point on Earth using coordinate geometry.
- [`types.LocationBase`](./postprocess.sources.types.md#class-locationbase): Stores geographical metadata for general locations.
- [`utils.URLBuilder`](./postprocess.sources.utils.md#class-urlbuilder): A fluent builder for incrementally constructing well-formed web URLs.

## Functions

- [`conversion.celsius_to_kelvin`](./postprocess.conversion.md#function-celsius_to_kelvin): Convert a temperature from degrees Celsius to Kelvin.
- [`conversion.kelvin_to_celsius`](./postprocess.conversion.md#function-kelvin_to_celsius): Convert a temperature from Kelvin to degrees Celsius.
- [`conversion.per_second_to_daily`](./postprocess.conversion.md#function-per_second_to_daily): Convert a per-second rate to an equivalent daily rate.
- [`conversion.per_second_to_hourly`](./postprocess.conversion.md#function-per_second_to_hourly): Convert a per-second rate to an equivalent hourly rate.
- [`pandas_utils.flatten_column_headers`](./postprocess.pandas_utils.md#function-flatten_column_headers): Flatten a MultiIndex of column headers into a list of strings.
- [`pandas_utils.insert_index_level`](./postprocess.pandas_utils.md#function-insert_index_level): Add extra levels to index.
- [`pandas_utils.swap_index`](./postprocess.pandas_utils.md#function-swap_index): Inplace swap of DataFrame index with existing given keys.
- [`pandas_utils.unique_index_levels_only`](./postprocess.pandas_utils.md#function-unique_index_levels_only): Remove column heading rows which are not unique from DataFrame.
- [`ftp.slugify_bom_ftp_segment`](./postprocess.sources.bom.ftp.md#function-slugify_bom_ftp_segment): Converts a raw BOM data string into a lowercase, filesystem-safe slug.
- [`openmeteo.dataframe_from_data`](./postprocess.sources.openmeteo.md#function-dataframe_from_data): Extract timeseries data from Open-Meteo API JSON into DataFrame.
- [`openmeteo.get_historical_data`](./postprocess.sources.openmeteo.md#function-get_historical_data): Fetch historical weather data for one or more coordinates.
- [`openmeteo.location_meta_from_data`](./postprocess.sources.openmeteo.md#function-location_meta_from_data): Get location info metadata from API response json object.
- [`silo.dataframe_from_data`](./postprocess.sources.silo.md#function-dataframe_from_data): Extract timeseries data from SILO API point data response into DataFrame.
- [`silo.find_nearby_stations`](./postprocess.sources.silo.md#function-find_nearby_stations): Return nearby SILO stations relative to a station or coordinates.
- [`silo.get_nearby_stations`](./postprocess.sources.silo.md#function-get_nearby_stations): Return SILO stations within a radius of a reference station.
- [`silo.get_point_data`](./postprocess.sources.silo.md#function-get_point_data): Retrieve climate data from the SILO point dataset.
- [`silo.location_meta_from_data`](./postprocess.sources.silo.md#function-location_meta_from_data): Get station info from retrieved point or drill data.
- [`utils.advance_one_month`](./postprocess.sources.utils.md#function-advance_one_month): Advance a date or datetime by one calendar month, clamping to month end.
- [`utils.generate_monthly_dates`](./postprocess.sources.utils.md#function-generate_monthly_dates): Generate monthly dates while they are less than or equal to end date, preserving the start date's day when possible.
- [`utils.haversine_distance`](./postprocess.sources.utils.md#function-haversine_distance): Computes great-circle distance between two geographic coordinates.
- [`utils.round_to_nearest_05`](./postprocess.sources.utils.md#function-round_to_nearest_05): Round value to nearest 0.05.
- [`transformation.calculate_delta`](./postprocess.transformation.md#function-calculate_delta): Calculates the difference (delta) between a single reference value from a set of values.
- [`transformation.normalise`](./postprocess.transformation.md#function-normalise): Map a value to between 0 and 1.
