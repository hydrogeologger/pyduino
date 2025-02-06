<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/postprocess/filehandler#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.filehandler`
This module assist with working with files/images for post processing.

Dependencies:
- numpy


## Table of Contents
- [`FileCorrelation`](./postprocess.filehandler.md#class-filecorrelation): Represents an image correlation object.
	- [`FileCorrelation.__init__`](./postprocess.filehandler.md#constructor-filecorrelation__init__): Generator for FileCorrelation object.
	- [`FileCorrelation.map_to_filename_datetime`](./postprocess.filehandler.md#method-filecorrelationmap_to_filename_datetime): Process mapping of values and date time to parsed date time in filenames.
	- [`FileCorrelation.parse_files`](./postprocess.filehandler.md#method-filecorrelationparse_files): Parses date time string from filenames in directory for correlation.
	- [`FileCorrelation.reset`](./postprocess.filehandler.md#method-filecorrelationreset): Reset list of parsed files.
	- [`FileCorrelation.values`](./postprocess.filehandler.md#method-filecorrelationvalues): Getter for list for all values for parsed files.
- [`FileInfo`](./postprocess.filehandler.md#dataclass-fileinfo): Represents a file detail used in storing file/image correlation info.
	- [`FileInfo.__init__`](./postprocess.filehandler.md#constructor-fileinfo__init__): Generator for FileInfo object.
	- [`FileInfo.reset`](./postprocess.filehandler.md#method-fileinforeset): Resets value associated with file.
- [`FileMapXRef`](./postprocess.filehandler.md#dataclass-filemapxref): Cross Reference Object between files and mapped values.
	- [`FileMapXRef.__init__`](./postprocess.filehandler.md#constructor-filemapxref__init__)
	- [`FileMapXRef.append`](./postprocess.filehandler.md#method-filemapxrefappend): Add a cross reference link mapping file to data.
	- [`FileMapXRef.reset`](./postprocess.filehandler.md#method-filemapxrefreset): Resets all mapped cross reference links.
- [`MapValue`](./postprocess.filehandler.md#dataclass-mapvalue): Represents a pair of matched/mapped value.
	- [`MapValue.__init__`](./postprocess.filehandler.md#constructor-mapvalue__init__): Generator for MatchInfo object.
	- [`MapValue.delta`](./postprocess.filehandler.md#method-mapvaluedelta): Calculates the difference between left and right value.
- [`XRefRecord`](./postprocess.filehandler.md#dataclass-xrefrecord): Cross Reference Record Object.
	- [`XRefRecord.__init__`](./postprocess.filehandler.md#constructor-xrefrecord__init__): Generator for Cross Reference Record.




---

<a href="../../../../python/lib/postprocess/postprocess/filehandler/MapValue#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>dataclass</kbd> `MapValue`
Represents a pair of matched/mapped value.


**Attributes:**

- <b>`left`</b> (any): Value of left orientated matched/mapped pair.
- <b>`right`</b> (any): Value of right orientated matched/mapped pair.


<a href="../../../../python/lib/postprocess/postprocess/filehandler/__init__#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `MapValue.__init__`

```python
MapValue(left, right)
```

Generator for MatchInfo object.


**Args:**

- <b>`left`</b> (any): Left value.
- <b>`right`</b> (any): Right value.


**Raises:**

- <b>`TypeError`</b>: Left and Right not of same type.



---

#### <kbd>property</kbd> MapValue.left

Getter for left match value (`any`, read-only).


---

#### <kbd>property</kbd> MapValue.right

Getter for right match value (`any`, read-only).




---

<a href="../../../../python/lib/postprocess/postprocess/filehandler/delta#L92"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `MapValue.delta`

```python
delta(reverse=False)
```

Calculates the difference between left and right value.


**Args:**

- <b>`reverse`</b> (bool, optional): Subtract Left from Right.
    Defaults to False (Right from Left).


**Returns:**

- <b>`any`</b>: Difference between matched/mapped value



---

<a href="../../../../python/lib/postprocess/postprocess/filehandler/FileInfo#L108"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>dataclass</kbd> `FileInfo`
Represents a file detail used in storing file/image correlation info.


**Attributes:**

- <b>`name`</b> (str): Name of file including extension.
- <b>`filepath`</b> (str): Full file path, includes filename and extension.
- <b>`date_time`</b> (datetime): Parsed timestamp of corresponding file.
- <b>`value`</b> (any): Value reference for any matching data corresponding with file.


<a href="../../../../python/lib/postprocess/postprocess/filehandler/__init__#L119"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `FileInfo.__init__`

```python
FileInfo(name, filepath, date_time=None, value=None)
```

Generator for FileInfo object.


**Args:**

- <b>`name`</b> (str): Name of file including extension.
- <b>`filepath`</b> (str): Full file path, includes filename and extension.
- <b>`date_time`</b> (datetime, optional): Timestamp. Defaults to None.
- <b>`value`</b> (any, optional): Value that file is matched on. Defaults to None.





---

<a href="../../../../python/lib/postprocess/postprocess/filehandler/reset#L173"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `FileInfo.reset`

```python
reset()
```

Resets value associated with file.



---

<a href="../../../../python/lib/postprocess/postprocess/filehandler/XRefRecord#L178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>dataclass</kbd> `XRefRecord`
Cross Reference Record Object.


**Attributes:**

- <b>`index`</b> (int): Index info of mapped object crossed reference value
    maps to.
- <b>`value`</b> (any): Value that is linked by cross referenced index.


<a href="../../../../python/lib/postprocess/postprocess/filehandler/__init__#L188"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `XRefRecord.__init__`

```python
XRefRecord(index, value)
```

Generator for Cross Reference Record.


**Args:**

- <b>`index`</b> (int): Index info of mapped object crossed reference value
    maps to.
- <b>`value`</b> (any): Value that is linked by cross referenced index.






---

<a href="../../../../python/lib/postprocess/postprocess/filehandler/FileMapXRef#L219"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>dataclass</kbd> `FileMapXRef`
Cross Reference Object between files and mapped values.


<a href="../../../../python/lib/postprocess/postprocess/filehandler/__init__#L223"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `FileMapXRef.__init__`

```python
FileMapXRef(files)
```





---

#### <kbd>property</kbd> FileMapXRef.filenames

List of deciphered cross referenced file names (`list[str]`, read-only).



---

#### <kbd>property</kbd> FileMapXRef.filepaths

List of deciphered cross referenced file paths (`list[str]`, read-only).



---

#### <kbd>property</kbd> FileMapXRef.files

List of deciphered cross referenced files with mapped values
(`list[FileInfo]`, read-only).


---

#### <kbd>property</kbd> FileMapXRef.indexes

List of undeciphered cross referenced file index (`list[int]`, read-only).



---

#### <kbd>property</kbd> FileMapXRef.values

List of values that was used for cross referencing (`list[any]`, read-only).



---

#### <kbd>property</kbd> FileMapXRef.xref

List of undeciphered file index mapped value cross references
(`list[XRefRecord[int,any]]`, read-only).




---

<a href="../../../../python/lib/postprocess/postprocess/filehandler/append#L294"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `FileMapXRef.append`

```python
append(index, data)
```

Add a cross reference link mapping file to data.


**Args:**

- <b>`index`</b> (int): Index of mapped file.
- <b>`data`</b> (any): Value of mapped data corresponding to file.


**Raises:**

- <b>`IndexError`</b>: Index is out of range of parsed files.


---

<a href="../../../../python/lib/postprocess/postprocess/filehandler/reset#L309"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `FileMapXRef.reset`

```python
reset()
```

Resets all mapped cross reference links.



---

<a href="../../../../python/lib/postprocess/postprocess/filehandler/FileCorrelation#L315"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `FileCorrelation`
Represents an image correlation object.


**Attributes:**

- <b>`mapped`</b> (list): Reference to list of file map records.


<a href="../../../../python/lib/postprocess/postprocess/filehandler/__init__#L322"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `FileCorrelation.__init__`

```python
FileCorrelation(path, format_=None)
```

Generator for FileCorrelation object.


**Args:**

- <b>`path`</b> (str): Directory path containing files to parse.
- <b>`format_`</b> (str, optional): Format of filename containing datetime string like
    `time.strptime()` and `datetime.datetime.strptime()`.
    Format exclude file extension. .i.e "2023-05-03_1030_filename.jpg"
    is "%Y-%m-%d_%H%M_filename".  Defaults to None.


**Raises:**

- <b>`FileNotFoundError`</b>: Directory path does not exist.



---

#### <kbd>property</kbd> FileCorrelation.date_times

List of datetime as matched from currently parsed filenames
(`list[datetime, None]`, read-only).


---

#### <kbd>property</kbd> FileCorrelation.filenames

List of currently parsed filenames (`list[str]`, read-only).


---

#### <kbd>property</kbd> FileCorrelation.filepaths

List of currently parsed full file paths (`list[str]`, read-only).


---

#### <kbd>property</kbd> FileCorrelation.files

List of currently parsed files (`list[FileInfo]`, read-only).


---

#### <kbd>property</kbd> FileCorrelation.matched

List for values currently parsed files has matched on only (`list[any`], read-only).


---

#### <kbd>property</kbd> FileCorrelation.path

Reference to path of directory used for file parsing (`str`).


**Raises:**

- <b>`FileNotFoundError`</b>: Directory path does not exist.




---

<a href="../../../../python/lib/postprocess/postprocess/filehandler/map_to_filename_datetime#L471"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `FileCorrelation.map_to_filename_datetime`

```python
map_to_filename_datetime(map_values, ref_date_time, data, dir_=0)
```

Process mapping of values and date time to parsed date time in filenames.

map_values <-> ref_date_time <-> data


**Args:**

- <b>`map_values`</b> (Iterable): Values to map on.
- <b>`ref_date_time`</b> (Iterable): Common reference between values to be mapped
    and dataset. Allow correlation between map_values and data.
- <b>`data`</b> (Iterable): Data or Values to corellate map_values with.
- <b>`dir_`</b> (int, optional): Direction preference for closest date_time.
    Future: 1, Past: -1, No preference: 0. Defaults to 0.


---

<a href="../../../../python/lib/postprocess/postprocess/filehandler/parse_files#L425"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `FileCorrelation.parse_files`

```python
parse_files(format_=None, ext='.jpg')
```

Parses date time string from filenames in directory for correlation.


**Args:**

- <b>`format_`</b> (str, optional): Format of filename containing datetime
    string like `time.strptime()` or `datetime.datetime.strptime()`.  
    Required if not declared during initialization. Defaults to None.  
    Format exclude file extension.
    i.e "2023-05-03_1030_filename.jpg" is "%Y-%m-%d_%H%M_filename".
- <b>`ext`</b> (tuple | str, optional): File extension to include
    i.e (".jpg", ".png") or ".jpg" . Defaults to ".jpg".


**Raises:**

- <b>`RuntimeError`</b>: No filename datetime string format provided during
    initialization and calling this method.
- <b>`RuntimeError`</b>: No file extension provided during method call.


---

<a href="../../../../python/lib/postprocess/postprocess/filehandler/reset#L525"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `FileCorrelation.reset`

```python
reset(reload=False)
```

Reset list of parsed files.


**Args:**

- <b>`reload`</b> (bool, optional): Forces reparsing of files from directory.
    Defaults to False.


**Raises:**

- <b>`RuntimeWarning`</b>: Unable to reload. Need to call parse_files() first.


---

<a href="../../../../python/lib/postprocess/postprocess/filehandler/values#L408"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `FileCorrelation.values`

```python
values(flat=False)
```

Getter for list for all values for parsed files.


**Args:**

- <b>`flat`</b> (bool, optional): Flatten output. Defaults to False.


**Returns:**

- <b>`list`</b>: List of values matched to file.



