<!-- markdownlint-disable -->

# API Overview

## Modules

- [`thingsboard_api.tb_pandas`](./thingsboard_api.tb_pandas.md#module-thingsboard_apitb_pandas): Module provides pandas.DataFrame wrapper function inclusive of tb_rest_api module.
- [`thingsboard_api.tb_rest_api`](./thingsboard_api.tb_rest_api.md#module-thingsboard_apitb_rest_api): Base module providing partial support for thingsboard client-side REST API calls.

## Classes

- [`tb_rest_api.Account`](./thingsboard_api.tb_rest_api.md#class-account): Account class to authenticate with thingsboard server.
- [`tb_rest_api.Device`](./thingsboard_api.tb_rest_api.md#class-device): A class to represent the thingsboard device for Thingsboard REST API.

## Functions

- [`tb_pandas.add_multindex_level`](./thingsboard_api.tb_pandas.md#function-add_multindex_level): Add extra levels to index.
- [`tb_pandas.concat_dataframes`](./thingsboard_api.tb_pandas.md#function-concat_dataframes): Concatenate a dictionary collection of dataframes to a single DataFrame.
- [`tb_pandas.convert_to_dataframe`](./thingsboard_api.tb_pandas.md#function-convert_to_dataframe): Converts ThingsBoard telemetry JSON into a single pandas DataFrame with aligned timestamps across all telemetry keys.
- [`tb_pandas.convert_to_dataframes`](./thingsboard_api.tb_pandas.md#function-convert_to_dataframes): Converts ThingsBoard telemetry JSON into a dictionary of pandas DataFrames, where each telemetry key is mapped to its own DataFrame.
- [`tb_pandas.dataframe_to_tb_timeseries`](./thingsboard_api.tb_pandas.md#function-dataframe_to_tb_timeseries): Convert telemetry data to the ThingsBoard timeseries response format.
- [`tb_pandas.split_dataframe`](./thingsboard_api.tb_pandas.md#function-split_dataframe): Split a DataFrame into a dictionary of DataFrames grouped by column name.
- [`tb_pandas.unique_column_headings_only`](./thingsboard_api.tb_pandas.md#function-unique_column_headings_only): Remove column heading rows which are not unique from DataFrame.
- [`tb_rest_api.count_records_per_field`](./thingsboard_api.tb_rest_api.md#function-count_records_per_field): Calculate the number of records per field for a Thingsboard telemetry object.
- [`tb_rest_api.filter_by_limit`](./thingsboard_api.tb_rest_api.md#function-filter_by_limit): Filters field names based on an explicit comparison operator and limit.
- [`tb_rest_api.group_timeseries_by_ts`](./thingsboard_api.tb_rest_api.md#function-group_timeseries_by_ts): Groups timestamped key-value readings into a list of records by timestamp.
- [`tb_rest_api.telemetry_limit_hit`](./thingsboard_api.tb_rest_api.md#function-telemetry_limit_hit): Check if any fields/keys in a timeseries telemetry meets or exceeds the given limit.
