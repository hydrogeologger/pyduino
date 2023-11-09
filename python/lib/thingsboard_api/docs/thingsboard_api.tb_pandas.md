<!-- markdownlint-disable -->

<a href="..\..\..\..\python\lib\thingsboard_api\thingsboard_api\tb_pandas.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `thingsboard_api.tb_pandas`
Module provides pandas wrapper function to support thingsboard_api. 

Dependencies: 
- thingsboard_api : REST API for thingsboard 
- pandas : For data post processing 


---

<a href="..\..\..\..\python\lib\thingsboard_api\thingsboard_api\tb_pandas.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `convert_to_dataframes`

```python
convert_to_dataframes(data, keys=None, drop_ts=True)
```

Construct a dictionary collection consisting of single Series         DataFrame objects from thingsboard timeseries data. 

Dataframe constains just a single telemetry key data Series. With "ts" as         "timeseries" index and "value" as column heading. 

```
{
     "key1" : DataFrame,
     "key2" : DataFrame,
     ...
}
``` 



**Args:**
 
 - <b>`data`</b> (JSON Object):  Dictionary containing keys of telemetry key and                 list of timeseries and value pairs. 
 - <b>`keys`</b> (tuple|list, optional):  Limit data to specified telemetry keys only.                 Defaults to None. 
 - <b>`drop_ts`</b> (bool, optional):  Drop "ts" column from DataFrame. Defaults to True. 



**Returns:**
 
 - <b>`dict`</b>:  Dictionary consisting of single pandas.DataFrame objects.             dict{key: pandas.DataFrame} 


---

<a href="..\..\..\..\python\lib\thingsboard_api\thingsboard_api\tb_pandas.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `dataframes_to_dataframe`

```python
dataframes_to_dataframe(dataframes, clean=True)
```

Concatenate a dictionary collection of dataframes to a single DataFrame. 



**Args:**
 
 - <b>`dataframes`</b> (dict[str, DataFrame]):  Dictionary of dataframes. 
 - <b>`copy`</b> (bool, optional):  Attempts to clear up memory used by DataFrame.             Defaults to True. 



**Returns:**
 
 - <b>`DataFrame`</b>:  Single dataframe object. 


---

<a href="..\..\..\..\python\lib\thingsboard_api\thingsboard_api\tb_pandas.py#L92"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `convert_to_dataframe`

```python
convert_to_dataframe(data, keys=None, drop_ts=True)
```

Construct a single DataFrame containing all telemetry keys,     with timeseries as dataframe index from thingsboard timeseries data. 

Leverages convert_to_dataframes(data, keys). Data is collated by outer join, with missing data represented as NaN (Not a Number). 



**Args:**
 
 - <b>`data`</b> (JSON Object):  Dictionary containing keys of telemetry key and                 list of timeseries and value pairs. 
 - <b>`keys`</b> (tuple|list, optional):  Limit data to specified telemetry keys only.                 Defaults to None. 
 - <b>`drop_ts`</b> (bool, optional):  Drop "ts" column from DataFrame. Defaults to True. 



**Returns:**
 
 - <b>`pandas.DataFrame`</b>:  Single dataframe containing concatenated telemetry data. 


---

<a href="..\..\..\..\python\lib\thingsboard_api\thingsboard_api\tb_pandas.py#L113"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `dataframe_to_dataframes`

```python
dataframe_to_dataframes(dataframe, clean=True)
```

Convert a DataFrame object to a dictionary collection of single Series     DataFrame objects. 



**Args:**
 
 - <b>`dataframe`</b> (pd.DataFrame):  Dataframe object to be converted. 
 - <b>`clean`</b> (bool, optional):  Attempt to clean up memory used             by dataframe object. Defaults to True. 



**Returns:**
 
 - <b>`dict`</b> (str : DataFrame):  A dictionary containing dataframe object with         key as dataframe column headings 


---

<a href="..\..\..\..\python\lib\thingsboard_api\thingsboard_api\tb_pandas.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `unique_column_headings_only`

```python
unique_column_headings_only(dataframe)
```

Remove column heading rows which are not unique from DataFrame. 



**Args:**
 
 - <b>`dataframe`</b> (DataFrame):  DataFrame to be modified. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
