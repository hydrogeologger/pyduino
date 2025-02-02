<!-- markdownlint-disable -->

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_pandas.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `thingsboard_api.tb_pandas`
Module provides pandas.DataFrame wrapper function inclusive of tb_rest_api module.

Consider using the custom `postprocess` library for more comprehensive pandas
DataFrame wrapper functions.

Dependencies:  
- pandas : For data post processing


## Table of Contents
- [`add_multindex_level`](./thingsboard_api.tb_pandas.md#function-add_multindex_level): Add extra levels to index.
- [`convert_to_dataframe`](./thingsboard_api.tb_pandas.md#function-convert_to_dataframe): Construct a single DataFrame containing all telemetry keys, with timeseries as dataframe index from thingsboard timeseries data.
- [`convert_to_dataframes`](./thingsboard_api.tb_pandas.md#function-convert_to_dataframes): Construct a dictionary collection consisting of single Series DataFrame objects from thingsboard timeseries data.
- [`dataframe_to_dataframes`](./thingsboard_api.tb_pandas.md#function-dataframe_to_dataframes): Convert a DataFrame object to a dictionary collection of single Series DataFrame objects.
- [`dataframes_to_dataframe`](./thingsboard_api.tb_pandas.md#function-dataframes_to_dataframe): Concatenate a dictionary collection of dataframes to a single DataFrame.
- [`unique_column_headings_only`](./thingsboard_api.tb_pandas.md#function-unique_column_headings_only): Remove column heading rows which are not unique from DataFrame.



---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_pandas.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `convert_to_dataframes`

```python
convert_to_dataframes(
    data,
    keys=None,
    to_numeric=None,
    drop_ts=True,
    verbose=False
)
```

Construct a dictionary collection consisting of single Series
DataFrame objects from thingsboard timeseries data.

Dataframe constains just a single telemetry key data Series.
With "ts" as "timeseries" index and "value" as column heading.

```
{
    "key1" : DataFrame,
    "key2" : DataFrame,
    ...
}
```


**Args:**

- <b>`data`</b> (JSON Object): Dictionary containing keys of telemetry key and
    list of timeseries and value pairs.
- <b>`keys`</b> (tuple|list|set, optional): Limit data to specified telemetry keys only.
    Defaults to None.
- <b>`to_numeric`</b> (bool|tuple|list|set, optional): Convert values of given keys
    to numeric type. If true will convert all values. Defaults to None.
- <b>`drop_ts`</b> (bool, optional): Drop "ts" column from DataFrame. Defaults to True.
- <b>`verbose`</b> (bool, optional): Verbosity, False only outputs errors. Defaults to False.


**Raises:**

- <b>`ValueError`</b>: Empty dataset for conversion.


**Returns:**

- <b>`dict[str,pandas.DataFrame]`</b>: Dictionary consisting of single pandas.DataFrame objects.
    dict{key: pandas.DataFrame}



---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_pandas.py#L104"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `convert_to_dataframe`

```python
convert_to_dataframe(
    data,
    keys=None,
    to_numeric=None,
    drop_ts=True,
    verbose=False
)
```

Construct a single DataFrame containing all telemetry keys,
with timeseries as dataframe index from thingsboard timeseries data.

Leverages convert_to_dataframes(data, keys).
Data is collated by outer join, with missing data represented as NaN (Not a Number).


**Args:**

- <b>`data`</b> (JSON Object): Dictionary containing keys of telemetry key and
    list of timeseries and value pairs.
- <b>`keys`</b> (tuple|list, optional): Limit data to specified telemetry keys only.
    Defaults to None.
- <b>`to_numeric`</b> (bool|tuple|list|set, optional): Convert values of given keys
    to numeric type. If true will convert all values. Defaults to None.
- <b>`drop_ts`</b> (bool, optional): Drop "ts" column from DataFrame. Defaults to True.
- <b>`verbose`</b> (bool, optional): Verbosity, False only outputs errors. Defaults to False.


**Raises:**

- <b>`ValueError`</b>: Empty dataset for conversion.


**Returns:**

- <b>`pandas.DataFrame`</b>: Single dataframe containing concatenated telemetry data.



---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_pandas.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `dataframes_to_dataframe`

```python
dataframes_to_dataframe(dataframes, clean=True)
```

Concatenate a dictionary collection of dataframes to a single DataFrame.


**Args:**

- <b>`dataframes`</b> (dict[str, DataFrame]): Dictionary of dataframes.
- <b>`clean`</b> (bool, optional): Attempts to clear up memory used by DataFrame.
    Defaults to True.


**Returns:**

- <b>`pandas.DataFrame`</b>: Single dataframe object.



---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_pandas.py#L154"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `dataframe_to_dataframes`

```python
dataframe_to_dataframes(dataframe, clean=True)
```

Convert a DataFrame object to a dictionary collection of single Series
DataFrame objects.


**Args:**

- <b>`dataframe`</b> (_pd.DataFrame): Dataframe object to be converted.
- <b>`clean`</b> (bool, optional): Attempt to clean up memory used
    by dataframe object. Defaults to True.


**Returns:**

- <b>`dict[str,pandas.DataFrame]`</b>: A dictionary containing dataframe object with
key as dataframe column headings



---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_pandas.py#L178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `unique_column_headings_only`

```python
unique_column_headings_only(df)
```

Remove column heading rows which are not unique from DataFrame.


**Args:**

- <b>`df`</b> (DataFrame): DataFrame to be modified.



---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_pandas.py#L197"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `add_multindex_level`

```python
add_multindex_level(
    df,
    keys,
    level=0,
    axis=1,
    name=None,
    na_rep=None,
    inplace=False
)
```

Add extra levels to index.


**Args:**

- <b>`df`</b> (DataFrame | Series): Reference indexed DataFrame or Series.
- <b>`keys`</b> (Iterable | str): Keys to insert into new level.
- <b>`level`</b> (int, optional): Level for key insertion, negative value indexes from tail.
    Defaults to 0.
- <b>`axis`</b> (int, optional): {0: `rows`, `index` or 1: `columns`}. Defaults to 1.
- <b>`name`</b> (str, optional): New index level name. Defaults to None.
- <b>`na_rep`</b> (any, optional): Missing data {None, np.nan or empty string} representation
    for level > 0, if None missing data not replaced. Defaults to None.
- <b>`inplace`</b> (bool, optional): Modifies the object directly,
    instead of creating a new DataFrame. Defaults to False.


**Raises:**

- <b>`ValueError`</b>: Axis option invalid.
- <b>`ValueError`</b>: Top level index contain NaN values.
- <b>`ValueError`</b>: Keys must be a value or array-like matching the length
    of the index to extend.


**Returns:**

- <b>`pandas.MultiIndex|None`</b>: DataFrame with modified MultiIndex or None if `inplace=True`.


**Example:**

```python
> source
a  b  c
0  0  5  0
1  1  6  1
2  0  9  4

> add_multindex_level(source, ['x','y','z'], level=1, axis=1)
a  b  c
x  y  z
0  0  5  0
1  1  6  1
2  0  9  4
```


**Reference:**

https://stackoverflow.com/questions/40225683/how-to-simply-add-a-column-level-to-a-pandas-dataframe



