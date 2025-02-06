<!-- markdownlint-disable -->

# API Overview

## Modules

- [`postprocess.extern`](./postprocess.extern.md#module-postprocessextern): This is a subpackage of postprocess containing repackaged modules from external sources.
- [`postprocess.file_matching`](./postprocess.file_matching.md#module-postprocessfile_matching): Utilities for matching files to external data records.
- [`postprocess.interpolation`](./postprocess.interpolation.md#module-postprocessinterpolation): Post processing interpolation module.
- [`postprocess.pandas_utils`](./postprocess.pandas_utils.md#module-postprocesspandas_utils): This module contains helper and wrapper functions to work with pandas dataframe objects.
- [`postprocess.transformation`](./postprocess.transformation.md#module-postprocesstransformation): Common data transformation utilities.

## Classes

- [`file_matching.FileCorrelation`](./postprocess.file_matching.md#class-filecorrelation): Represents an image correlation object.
- [`file_matching.FileInfo`](./postprocess.file_matching.md#dataclass-fileinfo): Represents a file detail used in storing file/image correlation info.
- [`file_matching.FileMapXRef`](./postprocess.file_matching.md#dataclass-filemapxref): Cross Reference Object between files and mapped values.
- [`file_matching.MapValue`](./postprocess.file_matching.md#dataclass-mapvalue): Represents a pair of matched/mapped value.
- [`file_matching.XRefRecord`](./postprocess.file_matching.md#dataclass-xrefrecord): Cross Reference Record Object.
- [`interpolation.Interpolation`](./postprocess.interpolation.md#class-interpolation): Represents an interpolation object.

## Functions

- [`pandas_utils.add_multindex_level`](./postprocess.pandas_utils.md#function-add_multindex_level): Add extra levels to index.
- [`pandas_utils.swap_index`](./postprocess.pandas_utils.md#function-swap_index): Inplace swap of DataFrame index with existing given keys.
- [`pandas_utils.unique_index_levels_only`](./postprocess.pandas_utils.md#function-unique_index_levels_only): Remove column heading rows which are not unique from DataFrame.
- [`transformation.calculate_delta`](./postprocess.transformation.md#function-calculate_delta): Calculates the difference (delta) between a single reference value from a set of values.
- [`transformation.normalise`](./postprocess.transformation.md#function-normalise): Map a value to between 0 and 1.
