<!-- markdownlint-disable -->

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `thingsboard_api.tb_rest_api`
Base module providing partial support for thingsboard client-side REST API calls.

Dependencies:  
- requests : For http POST request
- jwt : JWT decoding


**Reference:**

- https://thingsboard.io/docs/api/


## Table of Contents
- [`Account`](./thingsboard_api.tb_rest_api.md#class-account): Represents a ThingsBoard account and serves as the primary interface for interacting with the account, its devices, and other resources.
	- [`Account.__init__`](./thingsboard_api.tb_rest_api.md#constructor-account__init__): Constructs all the necessary attributes for the user object.
	- [`Account.authenticate`](./thingsboard_api.tb_rest_api.md#method-accountauthenticate): Authenticate with thingsboard server to obtain JWT token for the user.
	- [`Account.end`](./thingsboard_api.tb_rest_api.md#method-accountend): Close the account HTTP resources.
	- [`Account.fetch_devices`](./thingsboard_api.tb_rest_api.md#method-accountfetch_devices): Perform query of devices belonging to account from Thingsboard.
	- [`Account.request`](./thingsboard_api.tb_rest_api.md#method-accountrequest): Execute an authenticated API request.
	- [`Account.update_token`](./thingsboard_api.tb_rest_api.md#method-accountupdate_token): Obtain new token using existing refresh token.
- [`Device`](./thingsboard_api.tb_rest_api.md#class-device): Represents a device associated with a ThingsBoard account, providing methods to retrieve and manage its data and configuration.
	- [`Device.__init__`](./thingsboard_api.tb_rest_api.md#constructor-device__init__): Constructs all the necessary attributes for the device object.
	- [`Device.delete_timeseries`](./thingsboard_api.tb_rest_api.md#method-devicedelete_timeseries): Update Thingsboard device timeseries telemetry (time-series) data.
	- [`Device.fetch_timeseries_keys`](./thingsboard_api.tb_rest_api.md#method-devicefetch_timeseries_keys): Retrieve timeseries keys belonging to device from Thingsboard.
	- [`Device.get_timeseries`](./thingsboard_api.tb_rest_api.md#method-deviceget_timeseries): Retrieves timeseries data belonging to device from Thingsboard.
	- [`Device.update_timeseries`](./thingsboard_api.tb_rest_api.md#method-deviceupdate_timeseries): Update/Save Thingsboard device timeseries telemetry (time-series) data.
- [`count_records_per_field`](./thingsboard_api.tb_rest_api.md#function-count_records_per_field): Calculate the number of records per field for a Thingsboard telemetry object.
- [`filter_fields_by_threshold`](./thingsboard_api.tb_rest_api.md#function-filter_fields_by_threshold): Filters field names based on an explicit comparison operator and limit.
- [`group_timeseries_by_ts`](./thingsboard_api.tb_rest_api.md#function-group_timeseries_by_ts): Groups timestamped key-value readings into a list of records by timestamp.
- [`telemetry_limit_hit`](./thingsboard_api.tb_rest_api.md#function-telemetry_limit_hit): Check if any fields/keys in a timeseries telemetry meets or exceeds the given limit.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L870"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `group_timeseries_by_ts`

```python
group_timeseries_by_ts(data, flatten=False)
```

Groups timestamped key-value readings into a list of records by timestamp.

This function takes a dictionary where each key maps to a list of readings
with timestamps. Readings with the same timestamp across different keys
are merged into a single record. The resulting list is sorted chronologically
by timestamp.

Missing keys handling: Only keys present for a timestamp record
are included.


**Args:**

- <b>`data`</b> (dict): A dictionary of the form:
    ```python
    {
        "key1": [{"ts": int, "value": str}, ...],
        "key2": [{"ts": int, "value": str}, ...],
        ...
    }
    ```
- <b>`flatten`</b> (bool, optional): If True, keys are spread to the top level of
    each record with missing keys filled with None. Defaults to False.


**Returns:**

- <b>`list[dict]`</b>: A list of records sorted by timestamp. Missing keys are omitted.
- If `flatten` is False:
    ```python
    [
        {"ts": <timestamp>, "values": {"key1": value1, "key2": value2, ...} },
        ...
    ]
    ```
- If `flatten` is True:
    ```python
    [
        {"ts": <timestamp>, "key1": value1, "key2": value2, ...},
        ...
    ]
    ```


**Example:**

```python
data = {
    "temperature": [{"ts": 1000, "value": "25.5"}, {"ts": 2000, "value": "26.0"}],
    "humidity": [{"ts": 1000, "value": "80"}]
}
group_timeseries_by_ts(data)
[
    {"ts": 1000, "values": {"temperature": 25.5, "humidity": 80.0}},
    {"ts": 2000, "values": {"temperature": 26.0}}
]
```



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L955"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `count_records_per_field`

```python
count_records_per_field(data)
```

Calculate the number of records per field for a Thingsboard telemetry object.


**Args:**

- <b>`data`</b> (dict|list): A Thingsboard telemetry object.

    Accepts one of two shapes:
    - dict: Thingsboard telemetry api request response object.
        ```python
        {
            "key1": [{"ts": int, "value": str}, ...],
            "key2": [{"ts": int, "value": str}, ...],
            ...
        }
        ```
    - list: A list of telemetry entries.
        ```python
        # Entries can be nested, e.g.
        [
            {"ts": 123, "values": {"cpu": 45, "temp": 25}},
            ...
        ]

        # Or flattened, e.g.
        [
            {"ts": 123, "cpu": 45, "temp": 25},
            ...
        ]
        ```

**Raises:**

- <b>`TypeError`</b>: If the input data is neither a dictionary nor a list.


**Returns:**

- <b>`collections.Counter`</b>: A Counter mapping each telemetry field name to its
    total occurrence count across the provided data dataset.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L1015"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `filter_fields_by_threshold`

```python
filter_fields_by_threshold(telemetry_counts, limit, op='>=')
```

Filters field names based on an explicit comparison operator and limit.


**Args:**

- <b>`telemetry_counts`</b> (collector.Counter): A Counter mapping telemetry field names
    to their record counts.
- <b>`limit`</b> (int): The threshold value to test against.
- <b>`op`</b> (str, optional): The comparison operator string.
    Supports `>=`, `>`, `<=` and `<`. Defaults to `>=`.


**Returns:**

- <b>`set`</b>: A set of telemetry field names that satisfy the operator condition.


**Raises:**

- <b>`ValueError`</b>: If an unsupported operator string is provided.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L1050"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `telemetry_limit_hit`

```python
telemetry_limit_hit(data, limit)
```

Check if any fields/keys in a timeseries telemetry meets or exceeds the given limit.


**Args:**

- <b>`data`</b> (dict|list): A Thingsboard telemetry object.

    Accepts one of two shapes:
    - dict: Thingsboard telemetry api request response object.
        ```python
        {
            "key1": [{"ts": int, "value": str}, ...],
            "key2": [{"ts": int, "value": str}, ...],
            ...
        }
        ```
    - list: A list of telemetry entries.
        ```python
        # Entries can be nested, e.g.
        [
            {"ts": 123, "values": {"cpu": 45, "temp": 25}},
            ...
        ]

        # Or flattened, e.g.
        [
            {"ts": 123, "cpu": 45, "temp": 25},
            ...
        ]
        ```
- <b>`limit`</b> (int): Threshold count for a key.


**Returns:**

- <b>`bool`</b>: True if any key reaches the threshold limit, False otherwise.


**Raises:**

- <b>`TypeError`</b>: If `data` is not a dict or list.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `Account`
Represents a ThingsBoard account and serves as the primary interface for
interacting with the account, its devices, and other resources.

General usage flow is as follows:  
1. Create account object with url path to thingsboard server
2. Authenticate account with username and password


**Attributes:**

- <b>`url`</b> (str): Thingsboard url including scheme and port if provided (read-write).
- <b>`token`</b> (str): Account JWT token (read-only).
- <b>`refreshToken`</b> (str): Account JWT refresh token (read-only).
- <b>`devices`</b> (dict[str, Device]): Dictionary of devices registered with account (read-write).


<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L79"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `Account.__init__`

```python
Account(url)
```

Constructs all the necessary attributes for the user object.


**Args:**

- <b>`url`</b> (str): Full URL path to connect to thingsboard, including port,
    must include scheme http(s). i.e. http(s)://host:port



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> Account.refreshToken

Returns the JWT refreshToken for the user (`str`, read-only)


<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> Account.token

Returns the main JWT token for the user (`str`, read-only).


<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> Account.url

Thingsboard url, including port if provided (`str`, read-write).

The setter validates url contains `http` or `https`.


**Raises:**

- <b>`ValueError`</b>: URL does not include http(s).




<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L149"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Account.authenticate`

```python
authenticate(username, password, fetch_info=False, timeout=None)
```

Authenticate with thingsboard server to obtain JWT token for the user.

Will also query account user info.


**Args:**

- <b>`username`</b> (str): Username of user for authentication.
- <b>`password`</b> (str): Password of user for authentication.
- <b>`fetch_info`</b> (bool, optional): Fetch associated account user information
    from Thingsboard. Defaults to False.
- <b>`timeout`</b> (int | float | tuple, optional): Request timeout.
    Seconds to wait before giving up. Accepts a single number to set the 
    same time limit for both connecting and receiving data, or a 
    `(connect, read)` tuple to set them separately.
    Defaults to None, which applies the internal `DEFAULT_TIMEOUT`.


**Returns:**

- <b>`bool`</b>: True on successfull authentication, False otherwise.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L429"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Account.end`

```python
end()
```

Close the account HTTP resources.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L265"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Account.fetch_devices`

```python
fetch_devices(page_size=10, timeout=None)
```

Perform query of devices belonging to account from Thingsboard.

Requires `fetch_info` to be True during Account.authenticate().

Clears existing locally cached devices.

Implements both tenant and customer devices query.
Supports TB 2.x and TB 3.x+ api version.


**Args:**

- <b>`page_size`</b> (int, optional): Thingsboard pagination parameter.
    Affects number requests to for retrieval registered devices. Defaults to 10.
- <b>`timeout`</b> (int | float | tuple, optional): Request timeout.
    Seconds to wait before giving up. Accepts a single number to set the 
    same time limit for both connecting and receiving data, or a 
    `(connect, read)` tuple to set them separately.
    Defaults to None, which applies the internal `DEFAULT_TIMEOUT`.


**Returns:**

- <b>`bool`</b>: True on successfull query of account devices, False otherwise.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L326"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Account.request`

```python
request(
    method,
    endpoint,
    params=None,
    headers=None,
    json=None,
    timeout=(5, 30),
    **kwargs
)
```

Execute an authenticated API request.

The Account instance automatically injects the JWT bearer token
into the Authorization header before passing the request to the
HTTP transport layer.


**Args:**

- <b>`method`</b> (str): HTTP method to execute, such as GET, POST, PUT, or DELETE.
- <b>`endpoint`</b> (str): Relative API path.
- <b>`params`</b> (dict, Optional): Query string parameters.
- <b>`headers`</b> (dict, Optional): Additional HTTP headers.
    > [!NOTE] 
    > The headers argument may be supplied, but the Authorization
    > header managed by Account may be modified or overridden.
- <b>`json`</b> (object, Optional): JSON serialisable request body.
- <b>`timeout`</b> (int | float | tuple, optional): Request timeout.
    Seconds to wait before giving up. Accepts a single number to set the 
    same time limit for both connecting and receiving data, or a 
    `(connect, read)` tuple to set them separately.
    Defaults to None, which applies the internal `DEFAULT_TIMEOUT`.
- <b>`kwargs`</b> (dict): Optional arguments supported by requests.Session.request.

    Supported keyword arguments include:
    - data (dict, bytes, str): Request body data.
    - cookies (dict): Cookies to send with the request.
    - files (dict): Files to upload.
    - auth (tuple, callable): Authentication handler.
    - allow_redirects (bool): Whether redirects should be followed.
    - proxies (dict): Proxy configuration.
    - verify (bool, str): SSL certificate verification option.
    - stream (bool): Whether to stream the response.
    - cert (str, tuple): Client certificate configuration.


**Returns:**

- <b>`requests.Response`</b>: HTTP response object.


**Raises:**

- <b>`APIError`</b>: If the API returns an error response.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L211"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Account.update_token`

```python
update_token(timeout=None)
```

Obtain new token using existing refresh token.


**Args:**

- <b>`timeout`</b> (int | float | tuple, optional): Request timeout.
    Seconds to wait before giving up. Accepts a single number to set the 
    same time limit for both connecting and receiving data, or a 
    `(connect, read)` tuple to set them separately.
    Defaults to None, which applies the internal `DEFAULT_TIMEOUT`.


**Returns:**

- <b>`bool`</b>: True on successfull update, False otherwise.


**References:**

- https://github.com/thingsboard/thingsboard/issues/840



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L435"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `Device`
Represents a device associated with a ThingsBoard account, providing
methods to retrieve and manage its data and configuration.


**Attributes:**

- <b>`account`</b> (Account): Account used for device telemetry.
- <b>`device_id`</b> (str): Device ID of the as used by application.
- <b>`name`</b> (str): Name of device (User given), unrelated to name on thingsboard.
- <b>`keys_ts`</b> (list): List of keys from timeseries telemetry used by device.


<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L446"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `Device.__init__`

```python
Device(account, device_id, name)
```

Constructs all the necessary attributes for the device object.


**Args:**

- <b>`account`</b> (thingsboard_api.Account): Account used for device telemetry.
- <b>`device_id`</b> (str): Device ID as used by thingsboard.
- <b>`name`</b> (str): Name of device (user given).





<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L769"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Device.delete_timeseries`

```python
delete_timeseries(
    keys,
    startTs=None,
    endTs=None,
    deleteLatest=False,
    rewriteLatestIfDeleted=True,
    deleteAllDataForKeys=False,
    tz_offset=0,
    timeout=None
)
```

Update Thingsboard device timeseries telemetry (time-series) data.

The `ts` (timestamp) used by ThingsBoard is in UTC. The retrieved `ts`
matches the value sent with the payload during upload, if included.

The boundary condition is defined by the time interval `[startTs, endTs)` at
millisecond resolution, where telemetry at:  
- `startTs` is inclusive (>= startTs)
- `endTs` is exclusive (< endTs)


**Args:**

- <b>`keys`</b> (tuple|list|str): Telemetry key(s) to delete.
- <b>`startTs`</b> (datetime|date|int|float, optional): Interval start time.
        Accepts date object, datetime object or Unix timestamp in milliseconds.
        Inclusive at millisecond resolution.
        If `date` object is provided, time is set to `00:00:00`.
        Defaults to None.
- <b>`endTs`</b> (datetime|date|int|float, optional): Interval end time.
        Accepts date object, datetime object or Unix timestamp in milliseconds.
        Not inclusive at millisecond resolution.
        If `date` object is provided, time is set to `23:59:59.999999`.
        Defaults to None.
- <b>`deleteLatest`</b> (bool, optional): Latest telemetry can be removed, otherwise latest
        value will not be removed. Defaults to False.
- <b>`rewriteLatestIfDeleted`</b> (bool, optional): If True, rewrites the latest
        telemetry table when the current latest value is removed. Defaults to True.
- <b>`deleteAllDataForKeys`</b> (bool, optional): If True, deletes all data for
        the selected keys. Otherwise, only data within the specified
        time range is deleted. Defaults to False.
- <b>`tz_offset`</b> (int|float|timedelta, optional): Time offset in hours to apply to
        `startTs` and `endTs`, if time provided was NOT UTC time.
        i.e. for AEST time of +10 from UTC. `tzoffset=10`,
        Also accepts `timedelta` object. Defaults to 0.
- <b>`timeout`</b> (int | float | tuple, optional): Request timeout.
        Seconds to wait before giving up. Accepts a single number to set the 
        same time limit for both connecting and receiving data, or a 
        `(connect, read)` tuple to set them separately.
        Defaults to None, which applies the internal `DEFAULT_TIMEOUT`.


**Returns:**

- <b>`bool`</b>: Returns true if delete was successfull, false otherwise.

API Endpoint:  
> DELETE /api/plugins/telemetry/{entityType}/{entityId}/timeseries/delete{?keys,deleteAllDataForKeys,startTs,endTs,deleteLatest,rewriteLatestIfDeleted}


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L479"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Device.fetch_timeseries_keys`

```python
fetch_timeseries_keys(copy=False, timeout=None)
```

Retrieve timeseries keys belonging to device from Thingsboard.


**Args:**

- <b>`copy`</b> (bool, optional): Returns shallow copy of keys.
- <b>`timeout`</b> (int | float | tuple, optional): Request timeout.
    Seconds to wait before giving up. Accepts a single number to set the 
    same time limit for both connecting and receiving data, or a 
    `(connect, read)` tuple to set them separately.
    Defaults to None, which applies the internal `DEFAULT_TIMEOUT`.


**Returns:**

- <b>`list[str]|False|None`</b>: On successfull key retrieval, will return
    None if `copy=False` or a shallow copy list of keys
    if `copy=True`. Returns False if retrieval failed.

API Endpoint:  
> GET /api/plugins/telemetry/{entityType}/{entityId}/keys/timeseries


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L513"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Device.get_timeseries`

```python
get_timeseries(
    startTs=None,
    endTs=None,
    keys=None,
    limit=50000,
    warn_on_limit=True,
    interval=None,
    agg=None,
    tz_offset=0,
    useStrictDataTypes=True,
    timeout=None
)
```

Retrieves timeseries data belonging to device from Thingsboard.

The `ts` (timestamp) used by ThingsBoard is in UTC. The retrieved `ts`
matches the value sent with the payload during upload, if included.

The boundary condition is defined by the time interval `[startTs, endTs)` at
millisecond resolution, where telemetry at:  
- `startTs` is inclusive (>= startTs)
- `endTs` is exclusive (< endTs)

If no aggregation or time interval is provided, the function will return
the latest available time series data.

If the number of data points exceeds the specified `limit`, a warning is
issued to inform the user that the result has been truncated.


**Args:**

- <b>`startTs`</b> (datetime|date|int|float): Interval start time.
        Accepts date object, datetime object or Unix timestamp in milliseconds.
        Inclusive at millisecond resolution.
        If `date` object is provided, time is set to `00:00:00`.
- <b>`endTs`</b> (datetime|date|int|float): Interval end time.
        Accepts date object, datetime object or Unix timestamp in milliseconds.
        Not inclusive at millisecond resolution.
        If `date` object is provided, time is set to `23:59:59.999999`.
- <b>`keys`</b> (tuple|list|str, optional): Telemetry keys to fetch.
        If None, uses the instance's stored `Device().keys_ts` if available.
        Defaults to None.
- <b>`limit`</b> (int, optional): limit (int): Maximum number of data points returned per key. 
        If `agg` is not set, limits raw points; if `agg` is set,
        limits applies to aggregated intervals. Non-positive values use the default.
        Defaults to 50000.
- <b>`warn_on_limit`</b> (bool, optional): If True, emits a UserWarning when field 
    counts reached or exceeds the specified limit. If False, no warning
    is triggered if limit is reached. Defaults to True.
- <b>`interval`</b> (timedelta|int, optional): Aggregation interval in milliseconds.
        Also accepts a `timedelta` object. Required if `agg` is set. Defaults to None.
- <b>`agg`</b> (str, optional): Aggregation function to apply over each interval. 
        Common values include `"AVG"`, `"SUM"`, `"MIN"`, `"MAX"`, `"COUNT"`.
        If not provided, raw telemetry points are returned. Defaults to None.
- <b>`tz_offset`</b> (int|float|timedelta, optional): Timezone offset from UTC for
        `startTs` and `endTs` if they are provided in local time rather than UTC.
        The offset may be specified as hours (e.g. `10` for AEST, UTC+10) or
        as a `timedelta`. Defaults to `0` (UTC).
- <b>`useStrictDataTypes`</b> (bool, optional): If True, disables conversion of
        telemetry values to strings. Defaults to True.
- <b>`timeout`</b> (int | float | tuple, optional): Request timeout.
        Seconds to wait before giving up. Accepts a single number to set the 
        same time limit for both connecting and receiving data, or a 
        `(connect, read)` tuple to set them separately.
        Defaults to None, which applies the internal `DEFAULT_TIMEOUT`.


**Returns:**

- <b>`dict|None`</b>: Returns telemetry data with with the format
    dict{key: list[dict{ts: value}]} telemetry key as dictionary key
    and value consisting of a list of timeseries and value. None otherwise.


**Raises:**

- <b>`ValueError`</b>: Invalid `agg` value, Only Accepts one of MIN, MAX, AVG, SUM, COUNT.
    or if `limit` is invalid.
- <b>`TypeError`</b>: Invalid `interval` or `limit` value.
- <b>`OverflowError`</b>: Invalid `limit` value.
- <b>`RuntimeError`</b>: Aggrigation request requires `agg`, `interval`, `startTs` and `endTs`.


**Examples:**

```python
# returns
{
'key1': [{'ts': 1657907105161, 'value': '300.0'},
         {'ts': 1657906205118, 'value': '303.0'}],
'key2': [{'ts': 1657907105161, 'value': '0.4'},
         {'ts': 1657906205118, 'value': '0.2'}]
}

# NOTE: `ts` when converted to datetime may show an offset from thingsboard web.
# As the website automatically adjust to browser timezone.
```

Limit set to 50000 same as web. As when limit not provided in api request,
it defaults to 100 records. Used when `agg` parameter is `none`.


**References:**

- https://thingsboard.io/docs/user-guide/telemetry/#get-historical-time-series-data-values-for-specific-entity
- https://github.com/thingsboard/thingsboard/issues/10751

API Endpoint:  
> GET /api/plugins/telemetry/{entityType}/{entityId}/values/timeseries{?keys,useStrictDataTypes}

> GET /api/plugins/telemetry/{entityType}/{entityId}/values/timeseries{?keys,startTs,endTs,intervalType,interval,timeZone,limit,agg,orderBy,useStrictDataTypes}

> GET /api/plugins/telemetry/{entityType}/{entityId}/values/timeseries?keys=key1,key2,key3&startTs=1479735870785&endTs=1479735871858&interval=60000&limit=100&agg=AVG


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L721"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Device.update_timeseries`

```python
update_timeseries(data, timeout=None)
```

Update/Save Thingsboard device timeseries telemetry (time-series) data.

> [!WARNING] 
> Does NOT do any data structure validation.

Data in JSON Format (officially supported):  
```json
//# Without timestamps (server assigns current time):
{"temperature": 22.5, "humidity": 58}

//# With explicit timestamps (milliseconds since epoch):
//# Single point:
{"ts": 1730457600000, "values": {"temperature": 22.3, "humidity": 57}}
//# Multiple points (array):
[
    {"ts": 1730457600000, "values": {"temperature": 22.3, "humidity": 57}},
    {"ts": 1730461200000, "values": {"temperature": 22.7, "humidity": 59}}
]
```


**Args:**

- <b>`data`</b> (dict): Telemetry data, either a simple dict of key-value pairs,
    a dict with "ts" and "values", or a list of timestamped dicts.
- <b>`timeout`</b> (int | float | tuple, optional): Request timeout.
    Seconds to wait before giving up. Accepts a single number to set the 
    same time limit for both connecting and receiving data, or a 
    `(connect, read)` tuple to set them separately.
    Defaults to None, which applies the internal `DEFAULT_TIMEOUT`.


**Returns:**

- <b>`bool`</b>: Returns true if update was successfull, false otherwise.

API Endpoint:  
> POST /api/plugins/telemetry/DEVICE/{deviceId}/timeseries/{scope}



