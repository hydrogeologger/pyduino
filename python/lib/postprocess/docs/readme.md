<!-- markdownlint-disable -->

# API Overview

## Modules

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
