<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.file_matching`
Utilities for matching files to external data records.

This module provides classes for parsing file metadata, storing file
information, and correlating files with data values based on matching
criteria such as timestamps or nearest numerical values.

The module is intended for workflows where files (e.g. images, rasters,
or other time-indexed datasets) need to be associated with observations
or processed data records.

Dependencies:  
- numpy


## Table of Contents
- [`FileCorrelator`](./postprocess.file_matching.md#class-filecorrelator): Represents a file correlation and metadata parsing manager.
	- [`FileCorrelator.__init__`](./postprocess.file_matching.md#constructor-filecorrelator__init__): Initialize a FileCorrelator object.
	- [`FileCorrelator.map_by_datetime`](./postprocess.file_matching.md#method-filecorrelatormap_by_datetime): Correlate external values and reference timestamps with parsed file timestamps.
	- [`FileCorrelator.parse_files`](./postprocess.file_matching.md#method-filecorrelatorparse_files): Parses date time string from filenames in directory for correlation.
	- [`FileCorrelator.reset`](./postprocess.file_matching.md#method-filecorrelatorreset): Reset list of parsed files.
	- [`FileCorrelator.values`](./postprocess.file_matching.md#method-filecorrelatorvalues): Getter for list for all values for parsed files.
- [`FileInfo`](./postprocess.file_matching.md#dataclass-fileinfo): Represents a file detail used in storing file/image correlation info.
	- [`FileInfo.__init__`](./postprocess.file_matching.md#constructor-fileinfo__init__): Initialize a FileInfo object.
	- [`FileInfo.reset`](./postprocess.file_matching.md#method-fileinforeset): Resets value associated with file.
- [`FileMapping`](./postprocess.file_matching.md#dataclass-filemapping): Manages cross-reference links between parsed files and matched data values.
	- [`FileMapping.__init__`](./postprocess.file_matching.md#constructor-filemapping__init__): Initialize a FileMapping object.
	- [`FileMapping.append`](./postprocess.file_matching.md#method-filemappingappend): Add a cross reference link mapping file to data.
	- [`FileMapping.reset`](./postprocess.file_matching.md#method-filemappingreset): Resets all mapped cross reference links.
- [`MappingRecord`](./postprocess.file_matching.md#dataclass-mappingrecord): Represents a single cross-reference linking a file index to a matched value.
	- [`MappingRecord.__init__`](./postprocess.file_matching.md#constructor-mappingrecord__init__): Initialize a MappingRecord object.
- [`MatchPair`](./postprocess.file_matching.md#dataclass-matchpair): Represents a pair of matched/mapped value.
	- [`MatchPair.__init__`](./postprocess.file_matching.md#constructor-matchpair__init__): Initialize a MatchPair object.
	- [`MatchPair.delta`](./postprocess.file_matching.md#method-matchpairdelta): Calculates the mathematical difference (delta) between the left and right values.
	- [`MatchPair.swap`](./postprocess.file_matching.md#method-matchpairswap): Performs in place left and right value swap.




<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>dataclass</kbd> `MatchPair`
Represents a pair of matched/mapped value.


**Attributes:**

- <b>`left`</b> (Any): The left-side value of the matched pair.
- <b>`right`</b> (Any): The right-side value of the matched pair.


<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `MatchPair.__init__`

```python
MatchPair(left, right)
```

Initialize a MatchPair object.


**Args:**

- <b>`left`</b> (any): Left value.
- <b>`right`</b> (any): Right value.



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> MatchPair.left

Getter for left match value (`any`, read-only).


<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> MatchPair.right

Getter for right match value (`any`, read-only).




<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L108"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `MatchPair.delta`

```python
delta(inverted=False)
```

Calculates the mathematical difference (delta) between the left and right values.

By default, calculates the difference moving left-to-right (Right minus Left).


**Args:**

- <b>`inverted`</b> (bool, optional): If True, calculates Left minus Right 
    instead. Defaults to False.


**Returns:**

- <b>`Any`</b>: Difference between the matched/mapped values.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L103"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `MatchPair.swap`

```python
swap()
```

Performs in place left and right value swap.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>dataclass</kbd> `FileInfo`
Represents a file detail used in storing file/image correlation info.


**Attributes:**

- <b>`name`</b> (str): Name of file including extension.
- <b>`filepath`</b> (str): Full file path, includes filename and extension.
- <b>`date_time`</b> (datetime): Parsed timestamp of corresponding file.
- <b>`value`</b> (any): Value reference for any matching data corresponding with file.


<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L140"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `FileInfo.__init__`

```python
FileInfo(name, filepath, date_time=None, value=None)
```

Initialize a FileInfo object.


**Args:**

- <b>`name`</b> (str): Name of file including extension.
- <b>`filepath`</b> (str): Full file path, includes filename and extension.
- <b>`date_time`</b> (datetime, optional): Timestamp. Defaults to None.
- <b>`value`</b> (any, optional): Value that file is matched on. Defaults to None.





<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `FileInfo.reset`

```python
reset()
```

Resets value associated with file.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L199"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>dataclass</kbd> `MappingRecord`
Represents a single cross-reference linking a file index to a matched value.


**Attributes:**

- <b>`index`</b> (int): Index of the mapped file.
- <b>`value`</b> (any): Value linked to the file index.


<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L208"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `MappingRecord.__init__`

```python
MappingRecord(index, value)
```

Initialize a MappingRecord object.


**Args:**

- <b>`index`</b> (int): Index of the mapped file.
- <b>`value`</b> (any): Value linked by the index.






<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L238"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>dataclass</kbd> `FileMapping`
Manages cross-reference links between parsed files and matched data values.


<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L242"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `FileMapping.__init__`

```python
FileMapping(files)
```

Initialize a FileMapping object.



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> FileMapping.filenames

List of deciphered cross referenced file names (`list[str]`, read-only).



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> FileMapping.filepaths

List of deciphered cross referenced file paths (`list[str]`, read-only).



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> FileMapping.files

List of deciphered cross referenced files with mapped values
(`list[FileInfo]`, read-only).


<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> FileMapping.indexes

List of undeciphered cross referenced file index (`list[int]`, read-only).



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> FileMapping.values

List of values that was used for cross referencing (`list[Any]`, read-only).



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> FileMapping.xref

List of undeciphered file index mapped value cross references
(`list[MappingRecord[int, any]]`, read-only).




<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L316"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `FileMapping.append`

```python
append(index, data)
```

Add a cross reference link mapping file to data.


**Args:**

- <b>`index`</b> (int): Index of mapped file.
- <b>`data`</b> (any): Value of mapped data corresponding to file.


**Raises:**

- <b>`IndexError`</b>: Index is out of range of parsed files.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L331"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `FileMapping.reset`

```python
reset()
```

Resets all mapped cross reference links.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L337"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `FileCorrelator`
Represents a file correlation and metadata parsing manager.


**Attributes:**

- <b>`mapped`</b> (list): Reference to list of file map records.


<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L344"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `FileCorrelator.__init__`

```python
FileCorrelator(path, format_=None)
```

Initialize a FileCorrelator object.


**Args:**

- <b>`path`</b> (str): Directory path containing files to parse.
- <b>`format_`</b> (str, optional): Format of filename containing datetime string like
    `time.strptime()` and `datetime.datetime.strptime()`.
    Format exclude file extension. .i.e "2023-05-03_1030_filename.jpg"
    is "%Y-%m-%d_%H%M_filename".  Defaults to None.


**Raises:**

- <b>`FileNotFoundError`</b>: Directory path does not exist.



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> FileCorrelator.date_times

List of datetime as matched from currently parsed filenames
(`list[datetime | None]`, read-only).


<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> FileCorrelator.filenames

List of currently parsed filenames (`list[str]`, read-only).


<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> FileCorrelator.filepaths

List of currently parsed full file paths (`list[str]`, read-only).


<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> FileCorrelator.files

List of currently parsed files (`list[FileInfo]`, read-only).


<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> FileCorrelator.matched

List of parsed files that currently have matched values (`list[FileInfo]`, read-only).


<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> FileCorrelator.path

Reference to path of directory used for file parsing (`str`).


**Raises:**

- <b>`FileNotFoundError`</b>: Directory path does not exist.




<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L493"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `FileCorrelator.map_by_datetime`

```python
map_by_datetime(map_values, ref_date_time, data, direction=0)
```

Correlate external values and reference timestamps with parsed file timestamps.

Links datasets through a shared timestamp chain:  
``map_values`` <-> ``ref_date_time`` <-> ``Parsed File Timestamps``


**Args:**

- <b>`map_values`</b> (Iterable): External values to map (e.g., sensor readings).
- <b>`ref_date_time`</b> (Iterable): Timestamps corresponding to ``map_values`` 
    used to bridge the dataset to the files.
- <b>`data`</b> (Iterable): Data values to correlate with ``map_values``.
- <b>`direction`</b> (int, optional): Search direction preference for closest datetime.
    Future: 1, Past: -1, No preference: 0. Defaults to 0.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L447"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `FileCorrelator.parse_files`

```python
parse_files(format_=None, ext='.jpg')
```

Parses date time string from filenames in directory for correlation.


**Args:**

- <b>`format_`</b> (str, optional): Format of filename containing datetime string like
    ``time.strptime()`` or ``datetime.datetime.strptime()``.  
    Required if not declared during initialization. Defaults to None.  
    Format excludes file extension.
    e.g., ``"2023-05-03_1030_filename.jpg"`` uses ``"%Y-%m-%d_%H%M_filename"``.
- <b>`ext`</b> (tuple | str, optional): File extension to include
    i.e (".jpg", ".png") or ".jpg" . Defaults to ".jpg".


**Raises:**

- <b>`RuntimeError`</b>: No filename datetime string format provided during
    initialization and calling this method.
- <b>`RuntimeError`</b>: No file extension provided during method call.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L548"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `FileCorrelator.reset`

```python
reset(reload=False)
```

Reset list of parsed files.


**Args:**

- <b>`reload`</b> (bool, optional): Forces reparsing of files from directory.
    Defaults to False.


**Warns:**

- <b>`UserWarning`</b>: Unable to reload files. Need to call :meth:`parse_files` first.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/file_matching.py#L430"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `FileCorrelator.values`

```python
values(flat=False)
```

Getter for list for all values for parsed files.


**Args:**

- <b>`flat`</b> (bool, optional): Flatten output. Defaults to False.


**Returns:**

- <b>`list`</b>: List of values matched to file.



