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
- [`Account`](./thingsboard_api.tb_rest_api.md#class-account): Account class to authenticate with thingsboard server.
	- [`Account.__init__`](./thingsboard_api.tb_rest_api.md#constructor-account__init__): Constructs all the necessary attributes for the user object.
	- [`Account.authenticate`](./thingsboard_api.tb_rest_api.md#method-accountauthenticate): Authenticate with thingsboard server to obtain JWT token for the user.
	- [`Account.set_url`](./thingsboard_api.tb_rest_api.md#method-accountset_url): Modify url used by Thingsboard account.
	- [`Account.update_token`](./thingsboard_api.tb_rest_api.md#method-accountupdate_token): Obtain new token using existing refresh token.
- [`Device`](./thingsboard_api.tb_rest_api.md#class-device): A class to represent the thingsboard device for Thingsboard REST API.
	- [`Device.__init__`](./thingsboard_api.tb_rest_api.md#constructor-device__init__): Constructs all the necessary attributes for the device object.
	- [`Device.delete_timeseries`](./thingsboard_api.tb_rest_api.md#method-devicedelete_timeseries): Delete timeseries data from device.
	- [`Device.get_keys_timeseries`](./thingsboard_api.tb_rest_api.md#method-deviceget_keys_timeseries): Retrieve timeseries keys belonging to device.
	- [`Device.get_timeseries`](./thingsboard_api.tb_rest_api.md#method-deviceget_timeseries): Retrieves timeseries data from device.
	- [`Device.update_timeseries`](./thingsboard_api.tb_rest_api.md#method-deviceupdate_timeseries): Update thingsboard timeseries telemetry (time-series) data.
- [`group_timeseries_by_ts`](./thingsboard_api.tb_rest_api.md#function-group_timeseries_by_ts): Groups timestamped key-value readings into a list of records by timestamp.



---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L612"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `group_timeseries_by_ts`

```python
group_timeseries_by_ts(data)
```

Groups timestamped key-value readings into a list of records by timestamp.

This function takes a dictionary where each key maps to a list of readings
with timestamps. Readings with the same timestamp across different keys
are merged into a single record.

Missing keys for a timestamp are omitted. The resulting list is sorted by timestamp.


**Args:**

- <b>`data`</b> (dict): A dictionary of the form:
    ```python
    {
        key1: [{"ts": int, "value": str}, ...],
        key2: [{"ts": int, "value": str}, ...],
        ...
    }
    ```


**Returns:**

- <b>`list[dict]`</b>: A list of records, each with the structure:
    ```python
    {
        "ts": <timestamp>,
        "values": {
            key1: <value>,
            key2: <value>,
            ...
        }
    }
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



---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `Account`
Account class to authenticate with thingsboard server.

General usage flow is as follows:  
- Create account object with url path to thingsboard server
- Authenticate account with username and password

Methods:  
- `set_url(url)`: Modify url used by account thingsboard account.
- `authenticate(username, password)`: Authenticate user account to get JWT token.
- `update_token()`: Renews token.
- `token_expired()`: Checks if token is expired.


<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L86"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `Account.__init__`

```python
Account(url)
```

Constructs all the necessary attributes for the user object.


**Args:**

- <b>`url`</b> (str): Full URL path to connect to thingsboard, including port,
    must included http(s). i.e. http(s)://host:port



---

#### <kbd>property</kbd> Account.refreshToken

Returns the JWT refreshToken for the user (`str`, read-only)


---

#### <kbd>property</kbd> Account.token

Returns the main JWT token for the user (`str`, read-only).


---

#### <kbd>property</kbd> Account.url

Thingsboard url, including port if provided (`str`, read-only).




---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Account.authenticate`

```python
authenticate(username, password, timeout=3)
```

Authenticate with thingsboard server to obtain JWT token for the user.


**Args:**

- <b>`username`</b> (str): Username of user for authentication.
- <b>`password`</b> (str): Password of user for authentication.
- <b>`timeout`</b> (int | float, Optional): How many seconds to wait for the
    server to send data before giving up. Defaults to 3.


**Returns:**

- <b>`bool`</b>: True on successfull authentication, False otherwise.


---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L119"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Account.set_url`

```python
set_url(url)
```

Modify url used by Thingsboard account.


**Args:**

- <b>`url`</b> (str): URL to Thingsboard server including port number.


**Raises:**

- <b>`ValueError`</b>: URL does not include http(s).
- <b>`gaierror`</b>: Socket error.


---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L163"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Account.update_token`

```python
update_token(timeout=3)
```

Obtain new token using existing refresh token.


**Args:**

- <b>`timeout`</b> (int | float, optional): How many seconds to wait for the
    server to send data before giving up. Defaults to 3.


**Returns:**

- <b>`bool`</b>: True on successfull update, False otherwise.


**References:**

- https://github.com/thingsboard/thingsboard/issues/840



---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L220"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `Device`
A class to represent the thingsboard device for Thingsboard REST API.


**Attributes:**

- <b>`account`</b> (Account): Account used for device telemetry.
- <b>`device_id`</b> (str): Device ID of the as used by application.
- <b>`name`</b> (str): Name of device (User given), unrelated to name on thingsboard.
- <b>`keys_ts`</b> (list): List of keys from timeseries telemetry used by device.

Methods:  
- `get_keys_timeseries()`: Get device keys from thingsboard device timeseries.
- `get_timeseries()`: Get data from thingsboard device telemetry as per REST API.


<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L235"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `Device.__init__`

```python
Device(account, device_id, name)
```

Constructs all the necessary attributes for the device object.


**Args:**

- <b>`account`</b> (thingsboard_api.Account): Account used for device telemetry.
- <b>`device_id`</b> (str): Device ID as used by thingsboard.
- <b>`name`</b> (str): Name of device (user given).





---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L514"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

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
    timeout=10
)
```

Delete timeseries data from device.

Timestamp `ts` used by thingsboard is UTC time, and the retrieved `ts`
is the same as `ts` sent with payload during upload if included.

Time sample window is exclusive of `startTs` and inclusive of `endTs`
at millisecond resolution. `(startTs, endTs]`

`startTs` date object `2024-05-01` will be parsed as `2024-05-01 00:00:00.00`
and will values with exact same timestamp is exclude from the result.


**Args:**

- <b>`keys`</b> (tuple|list|str): Limit data to specified telemetry keys only.
        None, will use instance stored `Device().keys` if available.
        Defaults to None or Device.
- <b>`startTs`</b> (datetime|date|int|float, optional): Interval start time.
        Accepts date object, datetime object or Unix timestamp in milliseconds.
        Not inclusive at millisecond resolution.
        If `startTs` is `date` type object, time will be set to `00:00:00`.
- <b>`endTs`</b> (datetime|date|int|float, optional): Interval end time.
        Accepts date object, datetime object or Unix timestamp in milliseconds.
        Inclusive at millisecond resolution.
        If `endTs` is `date` type object, time will be set to `23:59:59.999999`.
- <b>`deleteLatest`</b> (bool, optional): Latest telemetry can be removed, otherwise latest
        value will not be removed. Defaults to False.
- <b>`rewriteLatestIfDeleted`</b> (bool, optional): Latest telemetry table will be rewritten
        in case that current latest value was removed. Defaults to True.
- <b>`deleteAllDataForKeys`</b> (bool, optional): Flag to specificy if all data should
        be deleted for selected keys or only data within specified time range.
        Defaults to False.
- <b>`tz_offset`</b> (int|float|timedelta, optional): Time offset in hours to apply to
        `startTs` and `endTs`, if the time provided was NOT UTC time.
        i.e. for AEST time of +10 from UTC. `tzoffset=10`,
        Also accepts timedelta object. Defaults to 0.
- <b>`timeout`</b> (int | float, optional): How many seconds to wait for the
        server to send data before giving up. Defaults to 10.


**Returns:**

- <b>`bool`</b>: Returns true if delete was successfull, false otherwise.

API Endpoint:  
> DELETE /api/plugins/telemetry/{entityType}/{entityId}/timeseries/delete{?keys,deleteAllDataForKeys,startTs,endTs,deleteLatest,rewriteLatestIfDeleted}


---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L255"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Device.get_keys_timeseries`

```python
get_keys_timeseries(copy=False, timeout=3)
```

Retrieve timeseries keys belonging to device.


**Args:**

- <b>`copy`</b> (bool, optional): Returns shallow copy of keys.
- <b>`timeout`</b> (int | float, optional): How many seconds to wait for the
    server to send data before giving up. Defaults to 3.


**Returns:**

- <b>`list[str]|False|None`</b>: On successfull key retrieval, will return
    None if `copy=False` or a shallow copy list of keys
    if `copy=True`. Returns False if retrieval failed.

API Endpoint:  
> GET /api/plugins/telemetry/{entityType}/{entityId}/keys/timeseries


---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L291"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Device.get_timeseries`

```python
get_timeseries(
    startTs=None,
    endTs=None,
    keys=None,
    limit=50000,
    interval=None,
    agg=None,
    tz_offset=0,
    useStrictDataTypes=True,
    timeout=30
)
```

Retrieves timeseries data from device.

Timestamp `ts` used by thingsboard is UTC time, and the retrieved `ts`
is the same as `ts` sent with payload during upload if included.

Time sample window is exclusive of `startTs` and inclusive of `endTs`
at millisecond resolution. `(startTs, endTs]`

`startTs` date object `2024-05-01` will be parsed as `2024-05-01 00:00:00.00`
and will values with exact same timestamp is exclude from the result.

If no aggregation or time interval given, will return latest timseries values.


**Args:**

- <b>`startTs`</b> (datetime|date|int|float): Interval start time.
        Accepts date object, datetime object or Unix timestamp in milliseconds.
        Not inclusive at millisecond resolution.
        If `startTs` is `date` type object, time will be set to `00:00:00`.
- <b>`endTs`</b> (datetime|date|int|float): Interval end time.
        Accepts date object, datetime object or Unix timestamp in milliseconds.
        Inclusive at millisecond resolution.
        If `endTs` is `date` type object, time will be set to `23:59:59.999999`.
- <b>`keys`</b> (tuple|list|str, optional): Limit data to specified telemetry keys only.
        None, will use instance stored `Device().keys_ts` if available.
        Defaults to None or Device.
- <b>`limit`</b> (int, optional): Last (max) number of records to return or
        intervals to process, zero and non-positive limit will
        use default limit. Used only when `agg` parameter is set to 'NONE'.
        Defaults to 50000.
- <b>`interval`</b> (timedelta|int, optional): Aggregation interval in milliseconds.
        Also accept timedelta object. Defaults to None.
- <b>`agg`</b> (str, optional): Aggregation function.
        Accepts (MIN, MAX, AVG, SUM, COUNT, NONE). Defaults to None.
- <b>`tz_offset`</b> (int|float|timedelta, optional): Time offset in hours to apply to
        `startTs` and `endTs`, if the time provided was NOT UTC time.
        i.e. for AEST time of +10 from UTC. `tzoffset=10`,
        Also accepts timedelta object. Defaults to 0.
- <b>`timeout`</b> (int | float, optional): How many seconds to wait for the
        server to send data before giving up. Defaults to 30.
- <b>`useStrictDataTypes`</b> (bool, optional): Enables/disables conversion of telemetry
        values to strings. Set `useStrictDataTypes=true` to disable value
        conversion to string. Defaults to True.


**Raises:**

- <b>`ValueError`</b>: Invalid `agg` value, Only Accepts one of MIN, MAX, AVG, SUM, COUNT.
- <b>`TypeError`</b>: Invalid `interval` value.
- <b>`ValueError`</b>: Invalid `limit` value.
- <b>`RuntimeError`</b>: Aggrigation request requires `agg`, `interval`, `startTs` and `endTs`.


**Returns:**

- <b>`dict|None`</b>: Returns telemetry data with with the format
    dict{key: list[dict{ts: value}]} telemetry key as dictionary key
    and value consisting of a list of timeseries and value. None otherwise.


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


---

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/tb_rest_api.py#L461"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `Device.update_timeseries`

```python
update_timeseries(data, timeout=10)
```

Update thingsboard timeseries telemetry (time-series) data.

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
- <b>`timeout`</b> (int | float, optional): How many seconds to wait for the
        server to send data before giving up. Defaults to 10.


**Returns:**

- <b>`bool`</b>: Returns true if update was successfull, false otherwise.

API Endpoint:  
> POST /api/plugins/telemetry/DEVICE/{deviceId}/timeseries/{scope}



