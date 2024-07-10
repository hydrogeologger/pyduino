"""
Module provides pandas.DataFrame wrapper function inclusive of tb_rest_api module.

Consider using the custom `postprocess` library for more comprehensive pandas
DataFrame wrapper functions.

Dependencies:
- pandas : For data post processing
"""
# from typing import Union, List, Any
from typing import Any as _Any
from typing import Iterable as _Iterable
from typing import KeysView as _KeysView
from typing import Optional as _Optional

import pandas as _pd
from pandas._typing import Dtype as _PandasDtype

# Package imports
# Expose tb_rest_api to namespace
from .tb_rest_api import *  # pylint: disable=wildcard-import,unused-wildcard-import

# python2 compatiblity
# pylint: disable=consider-using-f-string


def convert_to_dataframes(data, type_conversion, keys=None, drop_ts=True, verbose=False):  # pylint: disable-next=line-too-long
    # type: (dict[str, list[dict[str, _Any]]], bool|list|tuple|set|dict, _Optional[_KeysView|list|tuple|set], _Optional[bool], _Optional[bool]) -> dict[str, _pd.DataFrame]
    """Converts ThingsBoard telemetry JSON into a dictionary of pandas DataFrames,
    where each telemetry key is mapped to its own DataFrame.

    ```
    {
        "key1" : DataFrame,
        "key2" : DataFrame,
        ...
    }
    ```
    Each Dataframe object contains raw time-series points for a single telemetry key.
    With "ts" as "timeseries" index and "value" as column heading.

    Args:
        data (JSON Object): Dictionary containing keys of telemetry key and
            list of timeseries and value pairs. Where data has the form:
            ```python
                {
                    'key1': [{'ts': 1657907105161, 'value': '300.0'},
                            {'ts': 1657906205118, 'value': '303.0'}],
                    'key2': [{'ts': 1657907105161, 'value': '0.4'},
                            {'ts': 1657906205118, 'value': '0.2'}],
                    ...
                }
            ```
        type_conversion (bool, list or dict): Controls the conversion behavior.
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
            ```
            {
                "name": "string"
                "gender": "category",
                "age": "numeric",
                "date": "datetime",
                "active": "bool",
            }
            ```
        keys (tuple|list|set, optional): Limit dataframe creation to specified
            telemetry keys only. Defaults to None.
        drop_ts (bool, optional): Drop "ts" column from DataFrame. Defaults to True.
        verbose (bool, optional): Verbosity, False only outputs errors. Defaults to False.

    Raises:
        ValueError: Empty dataset for conversion.

    Returns:
        dict[str,pandas.DataFrame]: Dictionary consisting of single pandas.DataFrame objects.
            dict{key: pandas.DataFrame}

    See Also:
        :func:`convert_to_dataframe`
    """
    # Do nothing if dataset empty
    if not data:
        raise ValueError("Dataset is empty.")

    if keys is None:
        keys = data.keys()

    dataframes = {}  # type: dict[str, _pd.DataFrame]
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
        except KeyError:
            print("Failed: {}. {}".format(key, "Key not found."))
        except Exception as err:  # pylint: disable=broad-exception-caught
            print("Failed: {}. {}".format(key, type(err)))
        else:
            dataframes[key].sort_index(axis="index",
                                       ascending=True,
                                       inplace=True)

            # Convert values from string to numeric
            target_type = None
            if type_conversion is True or \
                    (isinstance(type_conversion, _Iterable) and
                     not isinstance(type_conversion, (str, dict)) and key in type_conversion):
                target_type = "numeric"
            elif isinstance(type_conversion, dict):
                target_type = type_conversion.get(key)
                target_type = target_type.lower() if target_type else None

            series = dataframes[key]["value"]
            if target_type in ('numeric', 'float', 'int', 'number'):
                dataframes[key]["value"] = _pd.to_numeric(
                    series, errors="coerce")
            elif target_type in ('datetime', 'date', 'timestamp'):
                dataframes[key]["value"] = _pd.to_datetime(series,
                                                           errors="coerce",
                                                           infer_datetime_format=True
                                                           )
            elif target_type in ('bool', 'boolean', 'logical'):
                dataframes[key]["value"] = series.astype('boolean')
            elif target_type in ('category', 'categorical'):
                dataframes[key]["value"] = series.astype('category')
            elif target_type in ('string', 'str'):
                dataframes[key]["value"] = series.astype('string')

            # Rename column headings from value to key name
            # result_df[key].rename(columns={'value': key}, inplace=True)
            if verbose:
                print("Success: {}".format(key))
    return dataframes


def convert_to_dataframe(data, type_conversion, keys=None, drop_ts=True, verbose=False):  # pylint: disable-next=line-too-long
    # type: (dict[str, list[dict[str, _Any]]], bool|list|tuple|set|dict, _Optional[_KeysView|list|tuple|set], _Optional[bool], _Optional[bool]) -> _pd.DataFrame
    """Converts ThingsBoard telemetry JSON into a single pandas DataFrame
    with aligned timestamps across all telemetry keys.

    Data is collated by outer join with each telemetry key becomes a column,
    and rows are indexed by timestamp ('ts').
    Missing values are filled with NaN (Not a Number) where a key does not have
    a value for a given timestamp.

    Args:
        data (JSON Object): Dictionary containing keys of telemetry key and
            list of timeseries and value pairs. Where data has the form:
            ```python
                {
                    'key1': [{'ts': 1657907105161, 'value': '300.0'},
                            {'ts': 1657906205118, 'value': '303.0'}],
                    'key2': [{'ts': 1657907105161, 'value': '0.4'},
                            {'ts': 1657906205118, 'value': '0.2'}],
                    ...
                }
            ```
        type_conversion (bool, list or dict): Controls the conversion behavior.
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
            ```
            {
                "name": "string"
                "gender": "category",
                "age": "numeric",
                "date": "datetime",
                "active": "bool",
            }
            ```
        keys (tuple|list, optional): Limit columns to specified telemetry keys only.
            Defaults to None.
        drop_ts (bool, optional): Drop "ts" column from DataFrame. Defaults to True.
        verbose (bool, optional): Verbosity, False only outputs errors. Defaults to False.

    Raises:
        ValueError: Empty dataset for conversion.

    Returns:
        pandas.DataFrame: Single dataframe containing concatenated telemetry data.

    See Also:
        :func:`convert_to_dataframes`
    """
    return concat_dataframes(convert_to_dataframes(data=data,
                                                   type_conversion=type_conversion,
                                                   keys=keys,
                                                   drop_ts=drop_ts,
                                                   verbose=verbose),
                             sort=not drop_ts,
                             clean=True)


def concat_dataframes(dataframes, sort=False, clean=True):
    # type: (dict[str, _pd.DataFrame], bool, _Optional[bool]) -> _pd.DataFrame
    """Concatenate a dictionary collection of dataframes to a single DataFrame.

    Args:
        dataframes (dict[str, DataFrame]): Dictionary of dataframes.
        sort (bool, optional): Sort index if it is not already aligned.
            One exception to this is when the index is a DatetimeIndex.
            In that case, index is sorted lexicographically. Defaults to False.
        clean (bool, optional): Attempts to clear up memory used by DataFrame.
            Defaults to True.

    Returns:
        pandas.DataFrame: Single dataframe object.
    """
    result_df = _pd.concat(dataframes, axis="columns", join="outer",
                           ignore_index=False, sort=sort)
    unique_column_headings_only(result_df)
    if clean:
        dataframes.clear()
    return result_df


def split_dataframe(dataframe, dropna=False, clean=True):
    # type: (_pd.DataFrame, _Optional[bool], _Optional[bool]) -> dict[str, _pd.DataFrame]
    """Split a DataFrame into a dictionary of DataFrames grouped by column name.

    Args:
        dataframe (_pd.DataFrame): Dataframe object to be converted.
        dropna (bool, optional): If True, removes rows containing missing values (NaN)
            from the result. If False, missing values are retained. Default is False.
        clean (bool, optional): Attempt to clean up memory used
            by dataframe object. Defaults to True.

    Returns:
        dict[str, pandas.DataFrame]: Dictionary where each key is an original
            DataFrame column name and each value is a DataFrame with the original
            column renamed to `"value"`.
    """
    dataframes = {}  # type: dict[_Any, _pd.DataFrame]
    for column in dataframe.columns:
        dataframes[column] = _pd.DataFrame(dataframe[column])
        dataframes[column].rename(columns={column: "value"}, inplace=True)
        if dropna:
            dataframes[column].dropna(axis="index", subset=["value"],
                                      inplace=True, ignore_index=False)
    if clean:
        del dataframe
    return dataframes


def unique_column_headings_only(df):
    # type: (_pd.DataFrame) -> None
    """Remove column heading rows which are not unique from DataFrame.

    Args:
        df (DataFrame): DataFrame to be modified.
    """
    columns = df.columns
    if isinstance(columns, _pd.MultiIndex):
        column_size = columns.size
        for level in range(columns.nlevels - 1, -1, -1):
            headers = columns.levels[level]
            header_size = len(headers)
            if header_size <= 1 and (column_size != header_size or
                                     headers[0] in ("value")):
                columns = columns.droplevel(level)
                if not isinstance(columns, _pd.MultiIndex):
                    break  # No longer multiindex, escape
        df.columns = columns  # Update df.columns outside the loop


def add_multindex_level(df,  # type: _pd.DataFrame|_pd.Series
                        keys,  # type: _Iterable[_Any]|str
                        level=0,  # type: int
                        axis=1,  # type: int|str
                        name=None,  # type:  _Optional[str]
                        na_rep=None,  # type: _Optional[_Any]
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
    # Copy of pyduino.postprocess.pandas_ext.add_multindex_level()
    axis = {0: 0, "index": 0, "rows": 0,
            "columns": 1, 1: 1}.get(axis)  # type: ignore
    if axis is None:
        raise ValueError("Invalid axis option")
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


def dataframe_to_tb_timeseries(data, ts_level="ts"):
    # type: (_pd.DataFrame|dict[str,_pd.DataFrame], str|int) -> dict[str, list[dict]]
    """Convert telemetry data to the ThingsBoard timeseries response format.

    Args:
        data (pd.DataFrame | dict[str, pd.DataFrame]): Telemetry data to convert.
            Accepted formats are:
            - `pd.DataFrame`: each column is a telemetry key and the index
                contains the timestamps.
            - `dict[str, pd.DataFrame]`: keys are telemetry field and values are DataFrames
                with a `"value"` column containing the timeseries records.

        ts_level (str | int, optional): Index level containing timestamps. Defaults to `"ts"`.
            - int: MultiIndex level position.
            - str: MultiIndex level name.

    Returns:
        dict[str, list[dict]]: Dictionary in the same format as the ThingsBoard timeseries
            telemetry response.

    Raises:
        TypeError:
            - If `data` is not a pandas DataFrame or a dict of pandas DataFrames.
            - If `data` is a dict and any value is not a pandas DataFrame.
        ValueError:
            - If MultiIndex `ts_level` name is not found in the DataFrame index.
            - If dictionary DataFrame does not contain a "value" column.
    """

    def extract_ts(index, ts_level):
        if isinstance(index, _pd.MultiIndex):
            ts_idx = ts_level
            if isinstance(ts_idx, str):
                if ts_idx not in index.names:
                    raise ValueError("Invalid ts_level: {}".format(ts_idx))
                ts_idx = index.names.index(ts_idx)
            return index.get_level_values(ts_idx)
        return index

    def build(series, ts):
        mask = series.notna()
        return [
            {"ts": t, "value": v}
            for t, v in zip(ts[mask], series[mask])
        ]

    response = {}
    if isinstance(data, _pd.DataFrame):
        ts = extract_ts(index=data.index, ts_level=ts_level)

        for key, series in data.items():
            values = build(series, ts)
            if values:
                response[key] = values
        return response

    if isinstance(data, dict):
        for key, df in data.items():
            if not isinstance(df, _pd.DataFrame):
                raise TypeError(
                    "{} value must be a pandas DataFrame.".format(key))

            if "value" not in df.columns:
                raise ValueError(
                    "DataFrame for key {} must contain a \"value\" column.".format(key))
            series = df["value"]
            ts = extract_ts(index=series.index, ts_level=ts_level)
            values = build(series, ts)
            if values:
                response[key] = values
        return response

    raise TypeError(
        "data must be a pandas DataFrame or a dict[str, pandas.DataFrame], "
        "got {}".format(type(data).__name__)
    )
