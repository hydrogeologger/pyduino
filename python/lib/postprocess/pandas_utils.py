"""This module contains helper and wrapper functions to work with pandas dataframe objects.

Dependencies:
- pandas
"""
# from typing import Union, List, Any
from typing import Any as _Any
from typing import Iterable as _Iterable
from typing import Optional as _Optional

import pandas as _pd
from pandas._typing import Dtype as _PandasDtype

# python2 compatiblity
# pylint: disable=consider-using-f-string


def _get_axis_arg_num(key):
    # type: (int|str) -> int
    axis = {0: 0, "index": 0, "rows": 0, "columns": 1, 1: 1}.get(key)
    if axis is None:
        raise ValueError("Invalid axis option")
    return axis


def unique_index_levels_only(df, axis=1, remove=None, ignore=None, inplace=False):  # pylint: disable-next=line-too-long
    # type: (_pd.DataFrame, str|int, _Optional[str|_Iterable], _Optional[_Iterable[int]], _Optional[bool]) -> None | _pd.MultiIndex | _pd.Index
    """Remove column heading rows which are not unique from DataFrame.

    Args:
        df (DataFrame): Reference indexed DataFrame.
        axis (int, optional): {0: `rows`, `index` or 1: `columns`}. Defaults to 1.
        remove (str|Iterable, optional): Force remove keys for where index vector
            is of size one like Series, i.e. remove="value" or remove=("key1", "key2").
            Defaults to None.
        ignore (int|Iterable[int], optional): Level or list of level index allowed
            to be non-unique, i.e. (2, 4, 5), level 2, 4 and 5 are not to be removed.
        inplace (bool, optional): Modifies the object directly,
            instead of creating a new DataFrame. Defaults to False.

    Raises:
        ValueError: Axis option invalid.
        ValueError: Keys must be a value or array-like matching the length
            of the index to extend.

    Returns:
        pandas.Index or pandas.MultiIndex: Index or MultiIndex with unique Index.
        None: When `inplace=True`.
    """
    axis = _get_axis_arg_num(axis)
    index_obj = df.columns if axis == 1 else df.index
    if isinstance(index_obj, _pd.MultiIndex):
        column_size = index_obj.size
        if not isinstance(ignore, _Iterable):
            ignore = (ignore,)
        for level in range(index_obj.nlevels - 1, -1, -1):
            if ignore is not None and level in ignore:
                continue
            headers = index_obj.levels[level]
            header_size = len(headers)
            if header_size <= 1 and (column_size != header_size or
                                     ((headers[0] in remove) if remove else False)):
                index_obj = index_obj.droplevel(level)
                if not isinstance(index_obj, _pd.MultiIndex):
                    break  # No longer multiindex, escape

        if not inplace:
            return index_obj
        if axis:
            df.columns = index_obj
        else:
            df.index = index_obj
        return None
    return index_obj


def add_multindex_level(df,  # type: _pd.DataFrame|_pd.Series
                        keys,  # type: _Iterable[_Any]|str
                        level=0,  # type: int
                        axis=1,  # type: int|str
                        name=None,  # type:  _Optional[str]
                        na_rep=None,  # type: _Optional[_Any]
                        dtype=None,  # type: _Optional[_PandasDtype]
                        inplace=False  # type: _Optional[bool]
                        ):  # type: (...) -> None | _pd.MultiIndex
    """Add extra levels to index.

    Args:
        df (DataFrame | Series): Reference indexed DataFrame or Series.
        keys (Iterable | str): Keys to insert into new level.
        level (int, optional): Level for key insertion, negative value indexes from tail.
            Defaults to 0.
        axis (int, optional): {0: `rows`, `index` or 1: `columns`}. Defaults to 1.
        name (str, optional): New index level name. Defaults to None.
        na_rep (any, optional): Missing data {None, np.nan or empty string} representation
            for level > 0, if None missing data not replaced. Defaults to None.
        dtype (str, numpy.dtype, or PandasDtype, optional): Data type for the
            new Index. If not specified, will be inferred from `keys`. Defaults to None.
            See the :ref:`pandas guide <basics.dtypes>`.
        inplace (bool, optional): Modifies the object directly,
            instead of creating a new DataFrame. Defaults to False.

    Raises:
        ValueError: Axis option invalid.
        ValueError: Top level index contain NaN values.
        ValueError: Keys must be a value or array-like matching the length
            of the index to extend.

    Returns:
        pandas.MultiIndex|None: DataFrame with modified MultiIndex or None if `inplace=True`.

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
    # Also implemented in pyduino.thingsboard_api.tb_pandas
    axis = _get_axis_arg_num(axis)
    to_promote = df.columns if axis == 1 else df.index
    to_promote_len = len(to_promote)

    # Allow tail/reverse indexing, keeping within bounds
    if level < 0:
        level += to_promote.nlevels + 1
    level = min(max(0, level), to_promote.nlevels)

    # Check level zero index validity
    if level == 0 and (_pd.isna(na_rep) or
                       (isinstance(na_rep, str) and not na_rep.strip())):
        for val in [keys] if isinstance(keys, str) or not isinstance(keys, _Iterable) else keys:
            if _pd.isna(val) or (isinstance(val, str) and not val.strip()):
                raise ValueError("Top level index contain NaN or Empty values")

    # Process new keys and Process NaN handling
    if isinstance(keys, str) or not isinstance(keys, _Iterable):
        if not _pd.isna(na_rep) and (_pd.isna(keys) or not keys.strip()):
            keys = na_rep
        keys = [keys] * to_promote_len  # Stretch key over whole range
    elif isinstance(keys, _Iterable):
        if len(keys) != to_promote_len:
            raise ValueError(
                "Keys must be a value or array-like matching the length of the index to extend")
        # Process NaN handling
        if not _pd.isna(na_rep):
            keys = [na_rep
                    if _pd.isna(val) or (isinstance(val, str) and not val.strip())
                    else val for val in keys]

    # Extract and preserve all existing levels
    if to_promote.nlevels > 1:
        index_levels = [to_promote.get_level_values(i)
                        for i in range(to_promote.nlevels)]
    else:
        index_levels = [to_promote]

    # Convert new keys into pandas Index
    keys_index = _pd.Index(data=keys, name=name,
                           dtype=dtype, tupleize_cols=False)

    # Inject the new level array cleanly at the specified position
    index_levels.insert(level, keys_index)

    # Build final MultiIndex from arrays
    new_index = _pd.MultiIndex.from_arrays(index_levels)

    if not inplace:
        return new_index

    if axis:
        df.columns = new_index
    else:
        df.index = new_index
    return None


def swap_index(df, keys):
    # type: (_pd.DataFrame, str|list) -> bool
    """Inplace swap of DataFrame index with existing given keys.

    Warning: Index may be reset even if swap failed.

    Returns:
        bool: True - Successfull swap. False otherwise.
    """
    if isinstance(keys, str):
        keys = [keys]

    if any(key not in df.columns for key in keys):
        return False

    df.reset_index(inplace=True, drop=False)
    df.set_index(keys=keys, inplace=True, drop=True)
    return True
