<!-- markdownlint-disable -->

# API Overview

## Modules

- [`thingsboard_api.error_handler`](./thingsboard_api.error_handler.md#module-thingsboard_apierror_handler): Exception handling utilities for thingsboard_api.
- [`thingsboard_api.exceptions`](./thingsboard_api.exceptions.md#module-thingsboard_apiexceptions): Exception hierarchy for the thingsboard_api package.
- [`thingsboard_api.tb_pandas`](./thingsboard_api.tb_pandas.md#module-thingsboard_apitb_pandas): An alternate single entry point for all core `thingsboard_api` functions and Pandas DataFrame helpers.
- [`thingsboard_api.tb_rest_api`](./thingsboard_api.tb_rest_api.md#module-thingsboard_apitb_rest_api): Base module providing partial support for thingsboard client-side REST API calls.

## Classes

- [`exceptions.APIError`](./thingsboard_api.exceptions.md#exception-apierror): Base exception for API response failures.
- [`exceptions.AuthenticationError`](./thingsboard_api.exceptions.md#exception-authenticationerror): Raised when authentication fails.
- [`exceptions.BadRequestError`](./thingsboard_api.exceptions.md#exception-badrequesterror): Raised when the API rejects a malformed request.
- [`exceptions.ConflictError`](./thingsboard_api.exceptions.md#exception-conflicterror): Raised when the request conflicts with the current resource state.
- [`exceptions.MethodNotAllowedError`](./thingsboard_api.exceptions.md#exception-methodnotallowederror): Raised when the requested HTTP method is not supported.
- [`exceptions.NotFoundError`](./thingsboard_api.exceptions.md#exception-notfounderror): Raised when the requested resource does not exist.
- [`exceptions.PermissionDeniedError`](./thingsboard_api.exceptions.md#exception-permissiondeniederror): Raised when the authenticated user lacks permission.
- [`exceptions.PreconditionFailedError`](./thingsboard_api.exceptions.md#exception-preconditionfailederror): Raised when a request precondition is not satisfied.
- [`exceptions.RateLimitError`](./thingsboard_api.exceptions.md#exception-ratelimiterror): Raised when the API rate limit has been exceeded.
- [`exceptions.ServerError`](./thingsboard_api.exceptions.md#exception-servererror): Raised when the ThingsBoard server reports an internal failure.
- [`exceptions.ThingsBoardAPIError`](./thingsboard_api.exceptions.md#exception-thingsboardapierror): Base exception for all thingsboard_api errors.
- [`exceptions.TransportConnectTimeoutError`](./thingsboard_api.exceptions.md#exception-transportconnecttimeouterror): Raised when the initial TCP handshake/connection setup to the server times out.
- [`exceptions.TransportConnectionError`](./thingsboard_api.exceptions.md#exception-transportconnectionerror): Base exception raised when a connection to the server cannot be established.
- [`exceptions.TransportError`](./thingsboard_api.exceptions.md#exception-transporterror): Base exception for HTTP transport failures.
- [`exceptions.TransportReadTimeoutError`](./thingsboard_api.exceptions.md#exception-transportreadtimeouterror): Raised when the connection is established but the server fails to send data mid-stream.
- [`exceptions.TransportSSLError`](./thingsboard_api.exceptions.md#exception-transportsslerror): Raised when SSL verification or negotiation fails.
- [`exceptions.TransportTimeoutError`](./thingsboard_api.exceptions.md#exception-transporttimeouterror): Raised when an HTTP request exceeds a configured connection or read timeout.
- [`tb_rest_api.Account`](./thingsboard_api.tb_rest_api.md#class-account): Represents a ThingsBoard account and serves as the primary interface for interacting with the account, its devices, and other resources.
- [`tb_rest_api.Device`](./thingsboard_api.tb_rest_api.md#class-device): Represents a device associated with a ThingsBoard account, providing methods to retrieve and manage its data and configuration.

## Functions

- [`error_handler.disable_friendly_exceptions`](./thingsboard_api.error_handler.md#function-disable_friendly_exceptions): Disable friendly ThingsBoard API exception output.
- [`error_handler.enable_friendly_exceptions`](./thingsboard_api.error_handler.md#function-enable_friendly_exceptions): Enable friendly ThingsBoard API exception output.
- [`tb_pandas.add_multindex_level`](./thingsboard_api.tb_pandas.md#function-add_multindex_level): Add extra levels to index.
- [`tb_pandas.concat_dataframes`](./thingsboard_api.tb_pandas.md#function-concat_dataframes): Concatenate a dictionary collection of dataframes to a single DataFrame.
- [`tb_pandas.convert_to_dataframe`](./thingsboard_api.tb_pandas.md#function-convert_to_dataframe): Converts ThingsBoard telemetry JSON into a single pandas DataFrame with aligned timestamps across all telemetry keys.
- [`tb_pandas.convert_to_dataframes`](./thingsboard_api.tb_pandas.md#function-convert_to_dataframes): Converts ThingsBoard telemetry JSON into a dictionary of pandas DataFrames, where each telemetry key is mapped to its own DataFrame.
- [`tb_pandas.dataframe_to_tb_timeseries`](./thingsboard_api.tb_pandas.md#function-dataframe_to_tb_timeseries): Convert telemetry data to the ThingsBoard timeseries response format.
- [`tb_pandas.split_dataframe`](./thingsboard_api.tb_pandas.md#function-split_dataframe): Split a DataFrame into a dictionary of DataFrames grouped by column name.
- [`tb_pandas.unique_column_headings_only`](./thingsboard_api.tb_pandas.md#function-unique_column_headings_only): Remove column heading rows which are not unique from DataFrame.
- [`tb_rest_api.count_records_per_field`](./thingsboard_api.tb_rest_api.md#function-count_records_per_field): Calculate the number of records per field for a Thingsboard telemetry object.
- [`tb_rest_api.filter_fields_by_threshold`](./thingsboard_api.tb_rest_api.md#function-filter_fields_by_threshold): Filters field names based on an explicit comparison operator and limit.
- [`tb_rest_api.group_timeseries_by_ts`](./thingsboard_api.tb_rest_api.md#function-group_timeseries_by_ts): Groups timestamped key-value readings into a list of records by timestamp.
- [`tb_rest_api.telemetry_limit_hit`](./thingsboard_api.tb_rest_api.md#function-telemetry_limit_hit): Check if any fields/keys in a timeseries telemetry meets or exceeds the given limit.
