<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/postprocess/pandas_ext#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.pandas_ext`
This module contains helper and wrapper functions to work with pandas dataframe objects.

Dependencies:
- pandas


## Table of Contents
- [`add_multindex_level`](./postprocess.pandas_ext.md#function-add_multindex_level): Add extra levels to index.
- [`swap_index`](./postprocess.pandas_ext.md#function-swap_index): Inplace swap of DataFrame index with existing given keys.
- [`unique_index_levels_only`](./postprocess.pandas_ext.md#function-unique_index_levels_only): Remove column heading rows which are not unique from DataFrame.



---

<a href="../../../../python/lib/postprocess/postprocess/pandas_ext/unique_index_levels_only#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

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

- <b>`Index or MultiIndex or None`</b>: DataFrame with unique Index or None if `inplace=True`.



---

<a href="../../../../python/lib/postprocess/postprocess/pandas_ext/add_multindex_level#L74"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

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

- <b>`df`</b> (DataFrame|Series): Reference indexed DataFrame or Series.
- <b>`keys`</b> (Union[Any, List[Any]]): Keys to insert into new level.
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

- <b>`MultiIndex or None`</b>: DataFrame with modified MultiIndex or None if `inplace=True`.


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



---

<a href="../../../../python/lib/postprocess/postprocess/pandas_ext/swap_index#L184"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `swap_index`

```python
swap_index(df, keys)
```

Inplace swap of DataFrame index with existing given keys.

> [!WARNING] Index may be reset even if swap failed.


**Returns:**

- <b>`bool`</b>: True - Successfull swap. False otherwise.



