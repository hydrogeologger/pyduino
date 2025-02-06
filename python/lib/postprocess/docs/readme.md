<!-- markdownlint-disable -->

# API Overview

## Modules

- [`postprocess.common`](./postprocess.common.md#module-postprocesscommon): This module contain simple and common methods used in postprocess package.
- [`postprocess.extern`](./postprocess.extern.md#module-postprocessextern): This is a subpackage of postprocess containing repackaged modules from external sources.
- [`postprocess.filehandler`](./postprocess.filehandler.md#module-postprocessfilehandler): This module assist with working with files/images for post processing.
- [`postprocess.interpolation`](./postprocess.interpolation.md#module-postprocessinterpolation): Post processing interpolation module.
- [`postprocess.pandas_ext`](./postprocess.pandas_ext.md#module-postprocesspandas_ext): This module contains helper and wrapper functions to work with pandas dataframe objects.

## Classes

- [`filehandler.FileCorrelation`](./postprocess.filehandler.md#class-filecorrelation): Represents an image correlation object.
- [`filehandler.FileInfo`](./postprocess.filehandler.md#dataclass-fileinfo): Represents a file detail used in storing file/image correlation info.
- [`filehandler.FileMapXRef`](./postprocess.filehandler.md#dataclass-filemapxref): Cross Reference Object between files and mapped values.
- [`filehandler.MapValue`](./postprocess.filehandler.md#dataclass-mapvalue): Represents a pair of matched/mapped value.
- [`filehandler.XRefRecord`](./postprocess.filehandler.md#dataclass-xrefrecord): Cross Reference Record Object.
- [`interpolation.Interpolation`](./postprocess.interpolation.md#class-interpolation): Represents an interpolation object.

## Functions

- [`common.calculate_delta`](./postprocess.common.md#function-calculate_delta): Calculates the difference (delta) between a single reference value from a set of values.
- [`common.normalise`](./postprocess.common.md#function-normalise): Map a value to between 0 and 1.
- [`pandas_ext.add_multindex_level`](./postprocess.pandas_ext.md#function-add_multindex_level): Add extra levels to index.
- [`pandas_ext.swap_index`](./postprocess.pandas_ext.md#function-swap_index): Inplace swap of DataFrame index with existing given keys.
- [`pandas_ext.unique_index_levels_only`](./postprocess.pandas_ext.md#function-unique_index_levels_only): Remove column heading rows which are not unique from DataFrame.
