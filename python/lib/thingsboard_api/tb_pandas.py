"""
Module provides pandas wrapper function to support thingsboard_api.

Dependencies:
- thingsboard_api : REST API for thingsboard
- pandas : For data post processing
"""
import pandas as pd

# Package imports
# Expose Account and Device from base package
from .tb_rest_api import Account, Device  # pylint: disable=unused-import


def convert_to_dataframes(data, keys=None, drop_ts=True):
    # type: (dict[str, dict[str,any]], tuple|list, bool) -> dict[str, pd.DataFrame]
    """Construct a dictionary collection consisting of single Series \
        DataFrame objects from thingsboard timeseries data.

    Dataframe constains just a single telemetry key data Series. With "ts" as \
        "timeseries" index and "value" as column heading.

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

    Returns:
        dict: Dictionary consisting of single pandas.DataFrame objects. \
            dict{key: pandas.DataFrame}
    """
    dataframes = {}
    if keys is None:
        keys = data

    for key in keys:
        # pdb.set_trace()
        try:
            dataframes[key] = pd.DataFrame(data[key])
            # result_df[key]['ts'] = pd.to_datetime(result_df[key]['ts'], unit='ms') + \
            #         datetime.timedelta(hours=tz_offset)  # due to UTC time
            dataframes[key]["timestamp"] = pd.to_datetime(dataframes[key]["ts"].values,
                                                          unit="ms")
            # https://stackoverflow.com/questions/42196337/dataframe-set-index-not-setting/42196399
            dataframes[key].set_index(keys=["timestamp", "ts"], inplace=True, drop=True)
            if drop_ts:
                dataframes[key].reset_index(level=1, inplace=True, drop=True)
            dataframes[key].sort_index(axis="index", ascending=True, inplace=True)
            # Convert values from string to numeric
            dataframes[key]["value"] = pd.to_numeric(
                dataframes[key]["value"], errors="coerce"
            )
            # Rename column headings from value to key name
            # result_df[key].rename(columns={'value': key}, inplace=True)
        except KeyError:
            print("FAILED to Convert key: " + key)
        else:
            print("Success to convert key: " + key)
    return dataframes


def dataframes_to_dataframe(dataframes, clean=True):
    # type: (dict[str, pd.DataFrame], bool) -> pd.DataFrame
    """Concatenate a dictionary collection of dataframes to a single DataFrame.

    Args:
        dataframes (dict[str, DataFrame]): Dictionary of dataframes.
        copy (bool, optional): Attempts to clear up memory used by DataFrame. \
            Defaults to True.

    Returns:
        DataFrame: Single dataframe object.
    """
    result_df = pd.concat(dataframes, axis="columns", join="outer")
    unique_column_headings_only(result_df)
    if clean:
        for dataframe in dataframes:
            del dataframe
    return result_df


def convert_to_dataframe(data, keys=None, drop_ts=True):
    # type: (dict[str, dict[str,any]], tuple|list, bool) -> pd.DataFrame
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

    Returns:
        pandas.DataFrame: Single dataframe containing concatenated telemetry data.
    """
    return dataframes_to_dataframe( convert_to_dataframes(data, keys, drop_ts) )


def dataframe_to_dataframes(dataframe, clean=True):
    # type: (pd.DataFrame, bool) -> dict[str, pd.DataFrame]
    """
    Convert a DataFrame object to a dictionary collection of single Series \
    DataFrame objects.

    Args:
        dataframe (pd.DataFrame): Dataframe object to be converted.
        clean (bool, optional): Attempt to clean up memory used \
            by dataframe object. Defaults to True.

    Returns:
        dict(str : DataFrame): A dictionary containing dataframe object with \
        key as dataframe column headings
    """
    dataframes = {}
    for column in dataframe.columns:
        dataframes[column] = pd.DataFrame(dataframe[column])
        dataframes[column].rename(columns={column: "value"}, inplace=True)
    if clean:
        del dataframe
    return dataframes


def unique_column_headings_only(dataframe):
    # type: (pd.DataFrame) -> None
    """Remove column heading rows which are not unique from DataFrame.

    Args:
        dataframe (DataFrame): DataFrame to be modified.
    """
    if isinstance(dataframe.columns, pd.MultiIndex):
        number_of_columns = dataframe.columns.size
        for level, headers in enumerate(dataframe.columns.levels):
            size = len(headers)
            if size == 1 and (size != number_of_columns or
                    headers[0] in ("value")):
                dataframe.columns = dataframe.columns.droplevel(level)
