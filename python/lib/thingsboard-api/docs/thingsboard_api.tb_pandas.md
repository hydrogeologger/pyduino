<!-- markdownlint-disable -->

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_pandas.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `thingsboard_api.tb_pandas`
An alternate single entry point for all core `thingsboard_api` functions and
Pandas DataFrame helpers.

This module combines everything from `thingsboard_api` core with extra Pandas wrapper 
functions. Import this module to access the package's full functionality 
without needing to import multiple files.

Consider using the custom `postprocess` library for more comprehensive pandas
DataFrame wrapper functions.

Dependencies:  
- pandas : For data post processing

Usage:  
```python
import thingsboard_api.tb_pandas as tb
# Following is not a functional code snippet!
tb.Account(url)                 # From thingsboard_api core
tb.convert_to_dataframe(data)   # From tb.py
```


## Table of Contents
- [`add_multindex_level`](./thingsboard_api.tb_pandas.md#function-add_multindex_level): Add extra levels to index.
- [`concat_dataframes`](./thingsboard_api.tb_pandas.md#function-concat_dataframes): Concatenate a dictionary collection of dataframes to a single DataFrame.
- [`convert_to_dataframe`](./thingsboard_api.tb_pandas.md#function-convert_to_dataframe): Converts ThingsBoard telemetry JSON into a single pandas DataFrame with aligned timestamps across all telemetry keys.
- [`convert_to_dataframes`](./thingsboard_api.tb_pandas.md#function-convert_to_dataframes): Converts ThingsBoard telemetry JSON into a dictionary of pandas DataFrames, where each telemetry key is mapped to its own DataFrame.
- [`dataframe_to_tb_timeseries`](./thingsboard_api.tb_pandas.md#function-dataframe_to_tb_timeseries): Convert telemetry data to the ThingsBoard timeseries response format.
- [`split_dataframe`](./thingsboard_api.tb_pandas.md#function-split_dataframe): Split a DataFrame into a dictionary of DataFrames grouped by column name.
- [`unique_column_headings_only`](./thingsboard_api.tb_pandas.md#function-unique_column_headings_only): Remove column heading rows which are not unique from DataFrame.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_pandas.py#L46"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `convert_to_dataframes`

```python
convert_to_dataframes(
    data,
    type_conversion,
    keys=None,
    drop_ts=True,
    verbose=False
)
```

Converts ThingsBoard telemetry JSON into a dictionary of pandas DataFrames,
where each telemetry key is mapped to its own DataFrame.

```python
{
    "key1" : DataFrame,
    "key2" : DataFrame,
    ...
}
```
Each Dataframe object contains raw time-series points for a single telemetry key.
With "ts" as "timeseries" index and "value" as column heading.


**Args:**

- <b>`data`</b> (JSON Object): Dictionary containing keys of telemetry key and
    list of timeseries and value pairs.

    Where data has the form:
    ```python
    {
        'key1': [{'ts': 1657907105161, 'value': '300.0'},
                {'ts': 1657906205118, 'value': '303.0'}],
        'key2': [{'ts': 1657907105161, 'value': '0.4'},
                {'ts': 1657906205118, 'value': '0.2'}],
        ...
    }
    ```
- <b>`type_conversion`</b> (bool, list or dict): Controls the conversion behavior.
    - True: Convert all keys to numeric type where possible.
    - False: Do not perform any conversion.
    - list: Convert only specified keys to numeric.
    - dict: Column-to-type schema mapping for explicit conversion.

        Accepts the following schema string:
        - Numeric: numeric, number, float, int
        - Date/Time: datetime, date, timestamp
        - Boolean: bool, boolean, logical
        - Category: category, categorical
        - String: string, str

        Dict schema example:
        ```python
        {
            "name": "string",
            "gender": "category",
            "age": "numeric",
            "date": "datetime",
            "active": "bool",
        }
        ```
- <b>`keys`</b> (tuple|list|set, optional): Limit dataframe creation to specified
    telemetry keys only. Defaults to None.
- <b>`drop_ts`</b> (bool, optional): Drop "ts" column from DataFrame. Defaults to True.
- <b>`verbose`</b> (bool, optional): Verbosity, False only outputs errors. Defaults to False.


**Raises:**

- <b>`ValueError`</b>: Empty dataset for conversion.


**Returns:**

- <b>`dict[str,pandas.DataFrame]`</b>: Dictionary consisting of single pandas.DataFrame objects.
    dict{key: pandas.DataFrame}

See Also:  
    :func:`convert_to_dataframe`



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_pandas.py#L179"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `convert_to_dataframe`

```python
convert_to_dataframe(
    data,
    type_conversion,
    keys=None,
    drop_ts=True,
    verbose=False
)
```

Converts ThingsBoard telemetry JSON into a single pandas DataFrame
with aligned timestamps across all telemetry keys.

Data is collated by outer join with each telemetry key becomes a column,
and rows are indexed by timestamp ('ts').
Missing values are filled with NaN (Not a Number) where a key does not have
a value for a given timestamp.


**Args:**

- <b>`data`</b> (JSON Object): Dictionary containing keys of telemetry key and
    list of timeseries and value pairs.

    Where data has the form:
    ```python
    {
        'key1': [{'ts': 1657907105161, 'value': '300.0'},
                {'ts': 1657906205118, 'value': '303.0'}],
        'key2': [{'ts': 1657907105161, 'value': '0.4'},
                {'ts': 1657906205118, 'value': '0.2'}],
        ...
    }
    ```
- <b>`type_conversion`</b> (bool, list or dict): Controls the conversion behavior.
    - True: Convert all keys to numeric type where possible.
    - False: Do not perform any conversion.
    - list: Convert only specified keys to numeric.
    - dict: Column-to-type schema mapping for explicit conversion.

        Accepts the following schema string:
        - Numeric: numeric, number, float, int
        - Date/Time: datetime, date, timestamp
        - Boolean: bool, boolean, logical
        - Category: category, categorical
        - String: string, str

        Dict schema example:
        ```python
        {
            "name": "string",
            "gender": "category",
            "age": "numeric",
            "date": "datetime",
            "active": "bool",
        }
        ```
- <b>`keys`</b> (tuple|list, optional): Limit columns to specified telemetry keys only.
    Defaults to None.
- <b>`drop_ts`</b> (bool, optional): Drop "ts" column from DataFrame. Defaults to True.
- <b>`verbose`</b> (bool, optional): Verbosity, False only outputs errors. Defaults to False.


**Raises:**

- <b>`ValueError`</b>: Empty dataset for conversion.


**Returns:**

- <b>`pandas.DataFrame`</b>: Single dataframe containing concatenated telemetry data.

See Also:  
    :func:`convert_to_dataframes`



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_pandas.py#L249"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `concat_dataframes`

```python
concat_dataframes(dataframes, sort=False, clean=True)
```

Concatenate a dictionary collection of dataframes to a single DataFrame.


**Args:**

- <b>`dataframes`</b> (dict[str, DataFrame]): Dictionary of dataframes.
- <b>`sort`</b> (bool, optional): Sort index if it is not already aligned.
    One exception to this is when the index is a DatetimeIndex.
    In that case, index is sorted lexicographically. Defaults to False.
- <b>`clean`</b> (bool, optional): Attempts to clear up memory used by DataFrame.
    Defaults to True.


**Returns:**

- <b>`pandas.DataFrame`</b>: Single dataframe object.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_pandas.py#L272"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `split_dataframe`

```python
split_dataframe(dataframe, dropna=False, clean=True)
```

Split a DataFrame into a dictionary of DataFrames grouped by column name.


**Args:**

- <b>`dataframe`</b> (_pd.DataFrame): Dataframe object to be converted.
- <b>`dropna`</b> (bool, optional): If True, removes rows containing missing values (NaN)
    from the result. If False, missing values are retained. Default is False.
- <b>`clean`</b> (bool, optional): Attempt to clean up memory used
    by dataframe object. Defaults to True.


**Returns:**

- <b>`dict[str, pandas.DataFrame]`</b>: Dictionary where each key is an original
    DataFrame column name and each value is a DataFrame with the original
    column renamed to `"value"`.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_pandas.py#L300"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `unique_column_headings_only`

```python
unique_column_headings_only(df)
```

Remove column heading rows which are not unique from DataFrame.


**Args:**

- <b>`df`</b> (DataFrame): DataFrame to be modified.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_pandas.py#L321"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `add_multindex_level`

```python
add_multindex_level(
    df,
    keys,
    level=0,
    axis=1,
    name=None,
    na_rep=None,
    dtype=None,
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
- <b>`dtype`</b> (str, numpy.dtype, or PandasDtype, optional): Data type for the
    new Index. If not specified, will be inferred from `keys`. Defaults to None.
    See the :ref:`pandas guide <basics.dtypes>`.
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



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_pandas.py#L437"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `dataframe_to_tb_timeseries`

```python
dataframe_to_tb_timeseries(data, ts_level='ts')
```

Convert telemetry data to the ThingsBoard timeseries response format.


**Args:**

- <b>`data`</b> (pd.DataFrame | dict[str, pd.DataFrame]): Telemetry data to convert.
    Accepted formats are:
    - `pd.DataFrame`: each column is a telemetry key and the index
        contains the timestamps.
    - `dict[str, pd.DataFrame]`: keys are telemetry field and values are DataFrames
        with a `"value"` column containing the timeseries records.

- <b>`ts_level`</b> (str | int, optional): Index level containing timestamps. Defaults to `"ts"`.
    - int: MultiIndex level position.
    - str: MultiIndex level name.


**Returns:**

- <b>`dict[str, list[dict[str, Any]]]`</b>: Dictionary in the same format as the ThingsBoard timeseries
    telemetry response.


**Raises:**

- <b>`TypeError`</b>: 
    - If `data` is not a pandas DataFrame or a dict of pandas DataFrames.
    - If `data` is a dict and any value is not a pandas DataFrame.
- <b>`ValueError`</b>: 
    - If MultiIndex `ts_level` name is not found in the DataFrame index.
    - If dictionary DataFrame does not contain a "value" column.



