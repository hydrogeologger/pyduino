"""
Module provides pandas.DataFrame wrapper function inclusive of tb_rest_api module.

Consider using the custom `postprocess` library for more comprehensive pandas \
DataFrame wrapper functions.

Dependencies:
- pandas : For data post processing
"""
# from typing import Union, List, Any
from typing import Iterable as _Iterable

import numpy as _np
import pandas as _pd

# Package imports
# Expose tb_rest_api to namespace
from .tb_rest_api import *  # pylint: disable=wildcard-import,unused-wildcard-import

# python2 compatiblity
# pylint: disable=consider-using-f-string


def convert_to_dataframes(data, keys=None, drop_ts=True, verbose=False):
    # type: (dict[str, list[dict[str, any]]], tuple|list|None, bool|None, bool|None) -> dict[str, _pd.DataFrame] # pylint: disable=line-too-long
    """Construct a dictionary collection consisting of single Series \
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

    Args:
        data (JSON Object): Dictionary containing keys of telemetry key and \
                list of timeseries and value pairs.
        keys (tuple|list, optional): Limit data to specified telemetry keys only. \
                Defaults to None.
        drop_ts (bool, optional): Drop "ts" column from DataFrame. Defaults to True.
        verbose (bool, optional): Verbosity, False only outputs errors. Defaults to False.

    Raises:
        ValueError: Empty dataset for conversion.

    Returns:
        dict: Dictionary consisting of single pandas.DataFrame objects. \
            dict{key: pandas.DataFrame}
    """
    if keys is None:
        keys = data

    # Do nothing if dataset empty
    if not data:
        raise ValueError("Dataset is empty.")

    dataframes = {}
    if verbose:
        print("Converting timeseries keys to Dataframe:")
    for key in keys:
        # pdb.set_trace()
        try:
            dataframes[key] = _pd.DataFrame(data[key])
            # result_df[key]['ts'] = _pd.to_datetime(result_df[key]['ts'], unit='ms') + \
            #         datetime.timedelta(hours=tz_offset)  # due to UTC time
            dataframes[key]["timestamp"] = _pd.to_datetime(dataframes[key]["ts"].values,
                                                           unit="ms")
            # https://stackoverflow.com/questions/42196337/dataframe-set-index-not-setting/42196399
            dataframes[key].set_index(keys=["timestamp", "ts"],
                                      inplace=True,
                                      drop=True)
            if drop_ts:
                dataframes[key].reset_index(level=1, inplace=True, drop=True)
            dataframes[key].sort_index(axis="index",
                                       ascending=True,
                                       inplace=True)
            # Convert values from string to numeric
            dataframes[key]["value"] = _pd.to_numeric(
                dataframes[key]["value"], errors="coerce"
            )
            # Rename column headings from value to key name
            # result_df[key].rename(columns={'value': key}, inplace=True)
        except KeyError:
            print("Failed: {}. {}".format(key, "Key not found."))
        except Exception as err:  # pylint: disable=broad-exception-caught
            print("Failed: {}. {}".format(key, type(err)))
        else:
            if verbose:
                print("Success: {}".format(key))
    return dataframes


def dataframes_to_dataframe(dataframes, clean=True):
    # type: (dict[str, _pd.DataFrame], bool|None) -> _pd.DataFrame
    """Concatenate a dictionary collection of dataframes to a single DataFrame.

    Args:
        dataframes (dict[str, DataFrame]): Dictionary of dataframes.
        clean (bool, optional): Attempts to clear up memory used by DataFrame. \
            Defaults to True.

    Returns:
        DataFrame: Single dataframe object.
    """
    result_df = _pd.concat(dataframes, axis="columns", join="outer")
    unique_column_headings_only(result_df)
    if clean:
        for dataframe in dataframes:
            del dataframe
    return result_df


def convert_to_dataframe(data, keys=None, drop_ts=True, verbose=False):
    # type: (dict[str, list[dict[str, any]]], tuple|list|None, bool|None, bool|None) -> _pd.DataFrame # pylint: disable=line-too-long
    """Construct a single DataFrame containing all telemetry keys, \
    with timeseries as dataframe index from thingsboard timeseries data.

    Leverages convert_to_dataframes(data, keys).
    Data is collated by outer join, with missing data represented as NaN (Not a Number).

    Args:
        data (JSON Object): Dictionary containing keys of telemetry key and \
            list of timeseries and value pairs.
        keys (tuple|list, optional): Limit data to specified telemetry keys only. \
            Defaults to None.
        drop_ts (bool, optional): Drop "ts" column from DataFrame. Defaults to True.
        verbose (bool, optional): Verbosity, False only outputs errors. Defaults to False.

    Raises:
        ValueError: Empty dataset for conversion.

    Returns:
        pandas.DataFrame: Single dataframe containing concatenated telemetry data.
    """
    return dataframes_to_dataframe(convert_to_dataframes(data, keys, drop_ts, verbose))


def dataframe_to_dataframes(dataframe, clean=True):
    # type: (_pd.DataFrame, bool|None) -> dict[str, _pd.DataFrame]
    """
    Convert a DataFrame object to a dictionary collection of single Series \
    DataFrame objects.

    Args:
        dataframe (_pd.DataFrame): Dataframe object to be converted.
        clean (bool, optional): Attempt to clean up memory used \
            by dataframe object. Defaults to True.

    Returns:
        dict(str : DataFrame): A dictionary containing dataframe object with \
        key as dataframe column headings
    """
    dataframes = {}
    for column in dataframe.columns:
        dataframes[column] = _pd.DataFrame(dataframe[column])
        dataframes[column].rename(columns={column: "value"}, inplace=True)
    if clean:
        del dataframe
    return dataframes


def unique_column_headings_only(df):
    # type: (_pd.DataFrame) -> None
    """Remove column heading rows which are not unique from DataFrame.

    Args:
        df (DataFrame): DataFrame to be modified.
    """
    if isinstance(df.columns, _pd.MultiIndex):
        column_size = df.columns.size
        for level in range(df.columns.nlevels - 1, -1, -1):
            headers = df.columns.levels[level]
            header_size = len(headers)
            if header_size <= 1 and (column_size != header_size or
                                     headers[0] in ("value")):
                df.columns = df.columns.droplevel(level)
                if not isinstance(df.columns, _pd.MultiIndex):
                    break  # No longer multiindex, escape


def add_multindex_level(df, keys, level=0, axis=1, name=None, na_rep=None, inplace=False):  # pylint: disable-next=line-too-long
    # type: (_pd.DataFrame|_pd.Series, (any|list[any]), int|None, int|None, str|None, any|None, bool|None) -> None | _pd.MultiIndex
    """Add extra levels to index.

    Args:
        df (DataFrame|Series): Reference indexed DataFrame or Series.
        keys (Union[Any, List[Any]]): Keys to insert into new level.
        level (int, optional): Level for key insertion, negative level indexes from tail. Defaults to 0.
        axis (int, optional): {0: `rows`, `index` or 1: `columns`}. Defaults to 1.
        name (str, optional): New index level name. Defaults to None.
        na_rep (any, optional): Missing data {None or np.nan} representation \
            for level > 0, if None missing data not replaced. Defaults to None.
        inplace (bool, optional): Modifies the object directly, \
            instead of creating a new DataFrame. Defaults to False.

    Raises:
        ValueError: Axis option invalid.
        ValueError: Top level index contain NaN values.
        ValueError: Keys must be a value or array-like matching the length \
            of the index to extend.

    Returns:
        MultiIndex or None: DataFrame with modified MultiIndex or None if `inplace=True`.

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
    # Copy of pyduino.postprocess.pandas_ext.add_multindex_level()
    axis = {0: 0, "index": 0, "rows": 0, "columns": 1, 1: 1}.get(axis)
    if axis is None:
        raise ValueError("Invalid axis option")
    to_promote = df.columns if axis == 1 else df.index

    # Check for index validity
    if na_rep is None and level == 0 and \
            (len(keys.strip()) == 0 if isinstance(keys, str)
                else (isinstance(keys, _Iterable) and _pd.isna(keys).any())
             or _pd.isna(keys)):
        raise ValueError("Top level index contain NaN values")

    # Process new keys and Process NaN handling
    if isinstance(keys, str):
        if not keys.strip() and na_rep:
            keys = na_rep
        keys = [keys] * len(to_promote)  # Stretch key over whole range
    elif isinstance(keys, _Iterable) and na_rep:
        # Process NaN handling
        keys = [na_rep if val in (None, _np.nan) else val for val in keys]

    if len(keys) != len(to_promote):
        raise ValueError(
            "Keys must be a value or array-like matching the length of the index to extend")

    # Allow tail/reverse indexing
    if level < 0:
        level += to_promote.nlevels + 1
    level = min(level, to_promote.nlevels)

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

    if not inplace:
        return new_index
    if axis:
        df.columns = new_index
    else:
        df.index = new_index
    return None
