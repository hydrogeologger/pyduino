<!-- markdownlint-disable -->

<a href="..\..\..\..\python\lib\thingsboard_api\thingsboard_api\thingsboard_api.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `thingsboard_api.thingsboard_api`
This module provides partial support for thingsboard client-side REST API calls     using requests calls. 

Reference: https://thingsboard.io/docs/api/ 

Dependencies: 
- requests : For http POST request 
- jwt : JWT decoding 



---

<a href="..\..\..\..\python\lib\thingsboard_api\thingsboard_api\thingsboard_api.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Account`
Account class to authenticate with thingsboard server. 

General usage flow is as follows: 
- Create account object with url path to thingsboard server 
- Authenticate account with username and password 



**Attributes:**
 
 - <b>`url`</b> (str):  URL for thingsboard 

Properties: 
 - <b>`token`</b> (str):  Thingsboard JWT token 
 - <b>`refreshToken`</b> (str):  Thingsboard JWT refresh Token 

Methods: 
- `authenticate(username, password)`:         Authenticate user account to get JWT token. 
- `update_token()`:         Renews token. 
- `token_expired()`:         Checks if token is expired. 

<a href="..\..\..\..\python\lib\thingsboard_api\thingsboard_api\thingsboard_api.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(url)
```

Constructs all the necessary attributes for the user object. 



**Args:**
 
 - <b>`url`</b> (str):  Full URL path to connect to thingsboard, must included http/https 


---

#### <kbd>property</kbd> refreshToken

Returns the JWT refreshToken for the user 

---

#### <kbd>property</kbd> token

Returns the main JWT token for the user 



---

<a href="..\..\..\..\python\lib\thingsboard_api\thingsboard_api\thingsboard_api.py#L68"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `authenticate`

```python
authenticate(username, password)
```

Authenticate with thingsboard server to obtain JWT token for the user. 



**Args:**
 
 - <b>`username`</b> (str):  Username of user for authentication 
 - <b>`password`</b> (str):  Password of user for authentication 

---

<a href="..\..\..\..\python\lib\thingsboard_api\thingsboard_api\thingsboard_api.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_token`

```python
update_token()
```

Obtain new token using existing refresh token https://github.com/thingsboard/thingsboard/issues/840 


---

<a href="..\..\..\..\python\lib\thingsboard_api\thingsboard_api\thingsboard_api.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Device`
A class to represent the thingsboard device for Thingsboard REST API. 



**Attributes:**
 
 - <b>`account`</b> (Account):  Account used for device telemetry 
 - <b>`name`</b> (str):  Name of device (User given) 
 - <b>`device_id`</b> (str):  Device ID of the device 
 - <b>`keys`</b> (list):  List of keys from thingsboard telemetry 

Methods: 
 - <b>`get_keys`</b> ():              Get device keys from thingsboard device telemetry 
 - <b>`get_data`</b> ():              Get data from thingsboard device telemetry as per REST API 

<a href="..\..\..\..\python\lib\thingsboard_api\thingsboard_api\thingsboard_api.py#L128"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(account, name, device_id)
```

Constructs all the necessary attributes for the device object. 



**Args:**
 
 - <b>`account`</b> (thingsboard_api.Account):  Account used for device telemetry 
 - <b>`name`</b> (str):  Name of device (user given) 
 - <b>`device_id`</b> (str):  Device ID as used by thingsboard 




---

<a href="..\..\..\..\python\lib\thingsboard_api\thingsboard_api\thingsboard_api.py#L157"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_data`

```python
get_data(
    startTs,
    endTs,
    keys=None,
    limit=None,
    interval=None,
    agg=None,
    tz_offset=0
)
```

Retrieves timeseries data from device. https://thingsboard.io/docs/user-guide/telemetry#data-query-api 



**Args:**
 
 - <b>`startTs`</b> (datetime|int|float):  Start of time interval.                     Either datetime object or Unix timestamp in milliseconds. 
 - <b>`endTs`</b> (datetime|int|float):  End of time interval, not inclusive.                    Either datetime object or Unix timestamp in milliseconds. 
 - <b>`keys`</b> (tuple|list, optional):  Limit data to specified telemetry keys only.                     Defaults to None. 
 - <b>`limit`</b> (int, optional):  Max amount of data points to return. Defaults to None. 
 - <b>`interval`</b> (timedelta|int, optional):  Aggregation interval in milliseconds.                    Also accept timedelta object. Defaults to None. 
 - <b>`agg`</b> (str, optional):  Aggregation function.                     Accepts (MIN, MAX, AVG, SUM, COUNT, NONE). Defaults to None. 
 - <b>`tz_offset`</b> (float, optional):  Timezone offset in hours. Defaults to 0. 



**Raises:**
 
 - <b>`ValueError`</b>:  List of keys not specified. 
 - <b>`ValueError`</b>:  AGG function not one of MIN, MAX, AVG, SUM, COUNT 



**Returns:**
 
 - <b>`json object`</b>:  Dictionary of telemetry data with telemetry key as dictionary                     key and value consisting list of timeseries and value.                     dict{key : list[ts, value]} 

---

<a href="..\..\..\..\python\lib\thingsboard_api\thingsboard_api\thingsboard_api.py#L145"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_keys`

```python
get_keys()
```

Retrieve and returns telemetry keys belonging to device. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
