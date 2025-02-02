<!-- markdownlint-disable -->

<a href="..\..\..\..\python\lib\thingsboard-api\src\thingsboard_api\tb_rest_api.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `thingsboard_api.tb_rest_api`
Base module providing partial support for thingsboard client-side REST API calls. 

Dependencies: 
- requests : For http POST request 
- jwt : JWT decoding 

Reference: 
- https://thingsboard.io/docs/api/ 



---

<a href="..\..\..\..\python\lib\thingsboard-api\src\thingsboard_api\tb_rest_api.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="..\..\..\..\python\lib\thingsboard-api\src\thingsboard_api\tb_rest_api.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(url)
```

Constructs all the necessary attributes for the user object. 



**Args:**
 
 - <b>`url`</b> (str):  Full URL path to connect to thingsboard, including port,                 must included http(s). i.e. http(s)://host:port 


---

#### <kbd>property</kbd> refreshToken

Returns the JWT refreshToken for the user (`str`, read-only) 

---

#### <kbd>property</kbd> token

Returns the main JWT token for the user (`str`, read-only). 

---

#### <kbd>property</kbd> url

Thingsboard url, including port if provided (`str`, read-only). 



---

<a href="..\..\..\..\python\lib\thingsboard-api\src\thingsboard_api\tb_rest_api.py#L103"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `authenticate`

```python
authenticate(username, password, timeout=3)
```

Authenticate with thingsboard server to obtain JWT token for the user. 



**Args:**
 
 - <b>`username`</b> (str):  Username of user for authentication. 
 - <b>`password`</b> (str):  Password of user for authentication. 
 - <b>`timeout`</b> (int | float, Optional):  How many seconds to wait for the                 server to send data before giving up. Defaults to 3. 



**Returns:**
 
 - <b>`bool`</b>:  True on successfull authentication, False otherwise. 

---

<a href="..\..\..\..\python\lib\thingsboard-api\src\thingsboard_api\tb_rest_api.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `set_url`

```python
set_url(url)
```

Modify url used by Thingsboard account. 



**Args:**
 
 - <b>`url`</b> (str):  URL to Thingsboard server including port number. 



**Raises:**
 
 - <b>`ValueError`</b>:  URL does not include http(s). 
 - <b>`gaierror`</b>:  Socket error. 

---

<a href="..\..\..\..\python\lib\thingsboard-api\src\thingsboard_api\tb_rest_api.py#L129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_token`

```python
update_token(timeout=3)
```

Obtain new token using existing refresh token. 



**Args:**
 
 - <b>`timeout`</b> (int | float, optional):  How many seconds to wait for the                 server to send data before giving up. Defaults to 3. 



**Returns:**
 
 - <b>`bool`</b>:  True on successfull update, False otherwise. 

References: 
- https://github.com/thingsboard/thingsboard/issues/840 


---

<a href="..\..\..\..\python\lib\thingsboard-api\src\thingsboard_api\tb_rest_api.py#L186"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Device`
A class to represent the thingsboard device for Thingsboard REST API. 



**Attributes:**
 
 - <b>`account`</b> (Account):  Account used for device telemetry. 
 - <b>`name`</b> (str):  Name of device (User given), unrelated to name on thingsboard. 
 - <b>`device_id`</b> (str):  Device ID of the as used by application. 
 - <b>`keys_ts`</b> (list):  List of keys from timeseries telemetry used by device. 

Methods: 
- `get_keys_timeseries()`: Get device keys from thingsboard device timeseries. 
- `get_timeseries()`: Get data from thingsboard device telemetry as per REST API. 

<a href="..\..\..\..\python\lib\thingsboard-api\src\thingsboard_api\tb_rest_api.py#L201"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(account, name, device_id)
```

Constructs all the necessary attributes for the device object. 



**Args:**
 
 - <b>`account`</b> (thingsboard_api.Account):  Account used for device telemetry. 
 - <b>`name`</b> (str):  Name of device (user given). 
 - <b>`device_id`</b> (str):  Device ID as used by thingsboard. 




---

<a href="..\..\..\..\python\lib\thingsboard-api\src\thingsboard_api\tb_rest_api.py#L221"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_keys_timeseries`

```python
get_keys_timeseries(copy=False, timeout=3)
```

Retrieve timeseries keys belonging to device. 



**Args:**
 
 - <b>`copy`</b> (bool, optional):  Returns shallow copy of keys. 
 - <b>`timeout`</b> (int | float, optional):  How many seconds to wait for the                 server to send data before giving up. Defaults to 3. 



**Returns:**
 
 - <b>`list[str] or False`</b>:  Timeseries keys if `copy` requested and Successfull. 
 - <b>`False`</b>:  Request failed. None otherwise. 

---

<a href="..\..\..\..\python\lib\thingsboard-api\src\thingsboard_api\tb_rest_api.py#L251"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_timeseries`

```python
get_timeseries(
    startTs,
    endTs,
    keys=None,
    limit=50000,
    interval=None,
    agg=None,
    tz_offset=0,
    timeout=10
)
```

Retrieves timeseries data from device. 

Timestamp `ts` used by thingsboard is UTC time, and the retrieved `ts` is the same as `ts` sent with payload during upload if included. 

Time sample window is exclusive of `startTs` and inclusive of `endTs` at millisecond resolution. `(startTs, endTs]` 

`startTs` date object `2024-05-01` will be parsed as `2024-05-01 00:00:00.00` and will exclude the timestamp from the result. 





**Args:**
 
 - <b>`startTs`</b> (datetime|date|int|float):  Interval start time.                     Accepts date object, datetime object or Unix timestamp in milliseconds.                     Not inclusive at millisecond resolution.                     If `startTs` is `date` type object, time will be set to `00:00:00`. 
 - <b>`endTs`</b> (datetime|date|int|float):  Interval end time.                     Accepts date object, datetime object or Unix timestamp in milliseconds.                     Inclusive at millisecond resolution.                    If `endTs` is `date` type object, time will be set to `23:59:59.999999`. 
 - <b>`keys`</b> (tuple|list|str, optional):  Limit data to specified telemetry keys only.                     None, will use instance stored `Device().keys` if available.                     Defaults to None or Device. 
 - <b>`limit`</b> (int, optional):  Last (max) number of records to return or                     intervals to process, zero and non-positive limit will                     use default limit. Defaults to 50000. 
 - <b>`interval`</b> (timedelta|int, optional):  Aggregation interval in milliseconds.                    Also accept timedelta object. Defaults to None. 
 - <b>`agg`</b> (str, optional):  Aggregation function.                     Accepts (MIN, MAX, AVG, SUM, COUNT, NONE). Defaults to None. 
 - <b>`tz_offset`</b> (int|float|timedelta, optional):  Time offset in hours to apply to                     `startTs` and `endTs`, if the time provided was NOT UTC time.                     i.e. for AEST time of +10 from UTC. `tzoffset=10`,                     Also accepts timedelta object. Defaults to 0. 
 - <b>`timeout`</b> (int | float, optional):  How many seconds to wait for the                     server to send data before giving up. Defaults to 10. 





**Raises:**
 
 - <b>`ValueError`</b>:  Invalid "agg" value, Only Accepts one of MIN, MAX, AVG, SUM, COUNT. 
 - <b>`TypeError`</b>:  Invalid "interval" value. 
 - <b>`ValueError`</b>:  Invalid "limit" value. 
 - <b>`RuntimeError`</b>:  "agg" or "interval argument required, if either is used. 



**Returns:**
 
 - <b>`dict{key`</b>:  list[dict{ts: value}]}: Telemetry data with                     telemetry key as dictionary key and value consisting of list                     of timeseries and value. None otherwise. 





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

http(s)://host:port/api/plugins/telemetry/{entityType}/{entityId}/values/timeseries        ?keys=key1,key2,key3&startTs=1479735870785&endTs=1479735871858        &interval=60000&limit=100&agg=AVG 

limit set to 50000 same as web. As when limit not provided in api request,            it defaults to 100 records. 

References: 
- https://thingsboard.io/docs/user-guide/telemetry/#get-historical-time-series-data-values-for-specific-entity 
- https://github.com/thingsboard/thingsboard/issues/10751 


