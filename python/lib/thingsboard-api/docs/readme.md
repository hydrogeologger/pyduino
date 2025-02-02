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
- [`tb_pandas.convert_to_dataframe`](./thingsboard_api.tb_pandas.md#function-convert_to_dataframe): Construct a single DataFrame containing all telemetry keys,     with timeseries as dataframe index from thingsboard timeseries data.
- [`tb_pandas.convert_to_dataframes`](./thingsboard_api.tb_pandas.md#function-convert_to_dataframes): Construct a dictionary collection consisting of single Series     DataFrame objects from thingsboard timeseries data.
- [`tb_pandas.dataframe_to_dataframes`](./thingsboard_api.tb_pandas.md#function-dataframe_to_dataframes): Convert a DataFrame object to a dictionary collection of single Series     DataFrame objects.
- [`tb_pandas.dataframes_to_dataframe`](./thingsboard_api.tb_pandas.md#function-dataframes_to_dataframe): Concatenate a dictionary collection of dataframes to a single DataFrame.
- [`tb_pandas.unique_column_headings_only`](./thingsboard_api.tb_pandas.md#function-unique_column_headings_only): Remove column heading rows which are not unique from DataFrame.
