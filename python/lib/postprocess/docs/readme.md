<!-- markdownlint-disable -->

# API Overview

## Modules

- [`postprocess.extern`](./postprocess.extern.md#module-postprocessextern): This is a subpackage of postprocess containing repackaged modules from external sources.
- [`postprocess.file_matching`](./postprocess.file_matching.md#module-postprocessfile_matching): Utilities for matching files to external data records.
- [`postprocess.interpolation`](./postprocess.interpolation.md#module-postprocessinterpolation): Post processing interpolation module.
- [`postprocess.pandas_utils`](./postprocess.pandas_utils.md#module-postprocesspandas_utils): This module contains helper and wrapper functions to work with pandas dataframe objects.
- [`postprocess.transformation`](./postprocess.transformation.md#module-postprocesstransformation): Common data transformation utilities.

## Classes

- [`file_matching.FileCorrelator`](./postprocess.file_matching.md#class-filecorrelator): Represents a file correlation and metadata parsing manager.
- [`file_matching.FileInfo`](./postprocess.file_matching.md#dataclass-fileinfo): Represents a file detail used in storing file/image correlation info.
- [`file_matching.FileMapping`](./postprocess.file_matching.md#dataclass-filemapping): Manages cross-reference links between parsed files and matched data values.
- [`file_matching.MappingRecord`](./postprocess.file_matching.md#dataclass-mappingrecord): Represents a single cross-reference linking a file index to a matched value.
- [`file_matching.MatchPair`](./postprocess.file_matching.md#dataclass-matchpair): Represents a pair of matched/mapped value.
- [`interpolation.Interpolation`](./postprocess.interpolation.md#class-interpolation): Represents an interpolation object.

## Functions

- [`pandas_utils.flatten_column_headers`](./postprocess.pandas_utils.md#function-flatten_column_headers): Flatten a MultiIndex of column headers into a list of strings.
- [`pandas_utils.insert_index_level`](./postprocess.pandas_utils.md#function-insert_index_level): Add extra levels to index.
- [`pandas_utils.swap_index`](./postprocess.pandas_utils.md#function-swap_index): Inplace swap of DataFrame index with existing given keys.
- [`pandas_utils.unique_index_levels_only`](./postprocess.pandas_utils.md#function-unique_index_levels_only): Remove column heading rows which are not unique from DataFrame.
- [`transformation.calculate_delta`](./postprocess.transformation.md#function-calculate_delta): Calculates the difference (delta) between a single reference value from a set of values.
- [`transformation.normalise`](./postprocess.transformation.md#function-normalise): Map a value to between 0 and 1.
