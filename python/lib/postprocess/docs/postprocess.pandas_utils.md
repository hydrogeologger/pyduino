<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/pandas_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.pandas_utils`
This module contains helper and wrapper functions to work with pandas dataframe objects.

Dependencies:  
- pandas


## Table of Contents
- [`add_multindex_level`](./postprocess.pandas_utils.md#function-add_multindex_level): Add extra levels to index.
- [`swap_index`](./postprocess.pandas_utils.md#function-swap_index): Inplace swap of DataFrame index with existing given keys.
- [`unique_index_levels_only`](./postprocess.pandas_utils.md#function-unique_index_levels_only): Remove column heading rows which are not unique from DataFrame.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/pandas_utils.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `unique_index_levels_only`

```python
unique_index_levels_only(df, axis=1, remove=None, ignore=None, inplace=False)
```

Remove column heading rows which are not unique from DataFrame.


**Args:**

- <b>`df`</b> (DataFrame): Reference indexed DataFrame.
- <b>`axis`</b> (int, optional): {0: `rows`, `index` or 1: `columns`}. Defaults to 1.
- <b>`remove`</b> (str|Iterable, optional): Force remove keys for where index vector
    is of size one like Series, i.e. remove="value" or remove=("key1", "key2").
    Defaults to None.
- <b>`ignore`</b> (int|Iterable[int], optional): Level or list of level index allowed
    to be non-unique, i.e. (2, 4, 5), level 2, 4 and 5 are not to be removed.
- <b>`inplace`</b> (bool, optional): Modifies the object directly,
    instead of creating a new DataFrame. Defaults to False.


**Raises:**

- <b>`ValueError`</b>: Axis option invalid.
- <b>`ValueError`</b>: Keys must be a value or array-like matching the length
    of the index to extend.


**Returns:**

- <b>`pandas.Index or pandas.MultiIndex`</b>: Index or MultiIndex with unique Index.
- <b>`None`</b>: When `inplace=True`.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/pandas_utils.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

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

<a href="../../../../python/lib/postprocess/src/postprocess/pandas_utils.py#L190"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `swap_index`

```python
swap_index(df, keys)
```

Inplace swap of DataFrame index with existing given keys.

> [!WARNING] Index may be reset even if swap failed.


**Returns:**

- <b>`bool`</b>: True - Successfull swap. False otherwise.



