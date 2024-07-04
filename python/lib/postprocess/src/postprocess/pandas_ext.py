"""This module contains helper and wrapper functions to work with pandas dataframe objects.

Dependencies:
- pandas
"""
# from typing import Union, List, Any
from typing import Iterable as _iterable

import numpy as _np
import pandas as _pd

# python2 compatiblity
# pylint: disable=consider-using-f-string


def _get_axis_arg_num(key):
    # type: (int|str) -> int
    axis = {0: 0, "index": 0, "rows": 0, "columns": 1, 1: 1}.get(key)
    if axis is None:
        raise ValueError("Invalid axis option")
    return axis


def unique_index_levels_only(df, axis=1, remove=None, inplace=False):
    # type: (_pd.DataFrame, int|str, str|_iterable, bool) -> None|_pd.DataFrame
    """Remove column heading rows which are not unique from DataFrame.

    Args:
        df (DataFrame): Reference indexed DataFrame.
        axis (int, optional): {0: `rows`, `index` or 1: `columns`}. Defaults to 1.
        remove (str|Iterable, optional): Force remove keys for where index vector \
            is of size one like Series, i.e. remove="value" or remove=("key1", "key2"). \
            Defaults to None.
        inplace (bool, optional): Modifies the object directly, \
            instead of creating a new DataFrame. Defaults to False.

    Raises:
        ValueError: Axis option invalid.
        ValueError: Keys must be a value or array-like matching the length \
            of the index to extend.

    Returns:
        DataFrame: The same as `df` or None if `inplace=True`.
    """
    axis = _get_axis_arg_num(axis)
    index_obj = df.columns if axis == 1 else df.index
    if isinstance(index_obj, _pd.MultiIndex):
        column_size = index_obj.size
        for level in range(index_obj.nlevels - 1, -1, -1):
            headers = index_obj.levels[level]
            header_size = len(headers)
            print(level, header_size, header_size, column_size,
                  header_size <= 1, column_size != header_size, headers)
            if header_size <= 1 and (column_size != header_size or
                                     (headers[0] in remove) if remove else False):
                print(level)
                index_obj = index_obj.droplevel(level)
                if not isinstance(index_obj, _pd.MultiIndex):
                    break  # No longer multiindex, escape

        data_ = df if inplace else df.copy(deep=True)
        if axis:
            data_.columns = index_obj
        else:
            data_.index = index_obj
        return None if inplace else data_


# def add_multindex_level(data, keys, level=0, axis=1, name=None, na_rep=None, inplace=False):  # pylint: disable-next=line-too-long
def add_multindex_level(df, keys, level=0, axis=1, name=None, na_rep=None, inplace=False):  # pylint: disable-next=line-too-long
    # type: (_pd.DataFrame, (any|list[any]), int|None, int|None, str|None, any|None, bool|None) -> _pd.DataFrame
    """Add extra levels to index.

    Args:
        data (DataFrame): Reference indexed DataFrame.
        keys (Union[Any, List[Any]]): Keys to insert into new level.
        level (int, optional): Level for key insertion. Defaults to 0.
        axis (int, optional): {0: `rows`, `index` or 1: `columns`}. Defaults to 1.
        name (str, optional): New index level name. Defaults to None.
        na_rep (any, optional): Missing data {None or np.nan} representation \
            for level > 0, if None missing data not replaced. Defaults to None.
        inplace (bool, optional): Modifies the object directly, \
            instead of creating a new DataFrame. Defaults to False.

    Raises:
        ValueError: Axis option invalid.
        ValueError: Keys must be a value or array-like matching the length \
            of the index to extend.

    Returns:
        DataFrame: The same as `data` or None if `inplace=True`.

    Example:
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

    Reference:
    https://stackoverflow.com/questions/40225683/how-to-simply-add-a-column-level-to-a-pandas-dataframe
    """
    axis = _get_axis_arg_num(axis)
    to_promote = df.columns if axis == 1 else df.index

    # Process new keys
    if isinstance(keys, _iterable) and na_rep is not None and level:
        # Process NaN handling
        keys = [na_rep if val in (None, _np.nan) else val for val in keys]
    elif isinstance(keys, str):
        keys = [keys] * len(to_promote)  # Stretch key over whole range

    if len(keys) != len(to_promote):
        raise ValueError(
            "Keys must be a value or array-like matching the length of the index to extend")

    # Create new index level
    new_keys = []  # Reference for index level keys
    for existing_key, insert_key in zip(to_promote, keys):
        if isinstance(existing_key, tuple):
            # py2 support
            new_key = list(existing_key)
            new_key.insert(level, insert_key)
            # py3 version
            # new_key = (*existing_key[:level], insert_key, *existing_key[level:])
        else:
            new_key = (existing_key, insert_key) if level else (
                insert_key, existing_key)
        new_keys.append(new_key)
    new_index = _pd.MultiIndex.from_tuples(new_keys)

    # Update index level names
    new_names = []  # Reference index level names
    for l in range(new_index.nlevels):
        if l == level:
            n = name
        else:
            n = to_promote.names[l - (1 if l >= level else 0)]
        new_names.append(n)
    new_index.names = new_names

    data_ = df if inplace else df.copy(deep=True)
    if axis:
        data_.columns = new_index
    else:
        data_.index = new_index

    return None if inplace else data_
