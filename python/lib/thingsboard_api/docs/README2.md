# Table of Contents

* [thingsboard\_api](#thingsboard_api)
* [thingsboard\_api.tb\_pandas](#thingsboard_api.tb_pandas)
  * [convert\_to\_dataframes](#thingsboard_api.tb_pandas.convert_to_dataframes)
  * [dataframes\_to\_dataframe](#thingsboard_api.tb_pandas.dataframes_to_dataframe)
  * [convert\_to\_dataframe](#thingsboard_api.tb_pandas.convert_to_dataframe)
  * [dataframe\_to\_dataframes](#thingsboard_api.tb_pandas.dataframe_to_dataframes)
  * [unique\_column\_headings\_only](#thingsboard_api.tb_pandas.unique_column_headings_only)
* [thingsboard\_api.tb\_rest\_api](#thingsboard_api.tb_rest_api)
  * [Account](#thingsboard_api.tb_rest_api.Account)
    * [\_\_init\_\_](#thingsboard_api.tb_rest_api.Account.__init__)
    * [token](#thingsboard_api.tb_rest_api.Account.token)
    * [refreshToken](#thingsboard_api.tb_rest_api.Account.refreshToken)
    * [authenticate](#thingsboard_api.tb_rest_api.Account.authenticate)
    * [update\_token](#thingsboard_api.tb_rest_api.Account.update_token)
  * [Device](#thingsboard_api.tb_rest_api.Device)
    * [\_\_init\_\_](#thingsboard_api.tb_rest_api.Device.__init__)
    * [get\_keys](#thingsboard_api.tb_rest_api.Device.get_keys)
    * [get\_data](#thingsboard_api.tb_rest_api.Device.get_data)

<a id="thingsboard_api"></a>

# thingsboard\_api

This package provides modules for thingsboard REST calls and data extraction.

Dependencies:
- requests : For http POST request
- jwt : JWT decoding
- pandas : pandas dataframe and series

<a id="thingsboard_api.tb_pandas"></a>

# thingsboard\_api.tb\_pandas

Module provides pandas wrapper function to support thingsboard_api.

Dependencies:
- thingsboard_api : REST API for thingsboard
- pandas : For data post processing

<a id="thingsboard_api.tb_pandas.convert_to_dataframes"></a>

#### convert\_to\_dataframes

```python
def convert_to_dataframes(data, keys=None, drop_ts=True)
```

Construct a dictionary collection consisting of single Series         DataFrame objects from thingsboard timeseries data.

Dataframe constains just a single telemetry key data Series. With "ts" as         "timeseries" index and "value" as column heading.


```
{
    "key1" : DataFrame,
    "key2" : DataFrame,
    ...
}
```

**Arguments**:

- `data` _JSON Object_ - Dictionary containing keys of telemetry key and                 list of timeseries and value pairs.
- `keys` _tuple|list, optional_ - Limit data to specified telemetry keys only.                 Defaults to None.
- `drop_ts` _bool, optional_ - Drop "ts" column from DataFrame. Defaults to True.
  

**Returns**:

- `dict` - Dictionary consisting of single pandas.DataFrame objects.             dict{key: pandas.DataFrame}

<a id="thingsboard_api.tb_pandas.dataframes_to_dataframe"></a>

#### dataframes\_to\_dataframe

```python
def dataframes_to_dataframe(dataframes, clean=True)
```

Concatenate a dictionary collection of dataframes to a single DataFrame.

**Arguments**:

- `dataframes` _dict[str, DataFrame]_ - Dictionary of dataframes.
- `copy` _bool, optional_ - Attempts to clear up memory used by DataFrame.             Defaults to True.
  

**Returns**:

- `DataFrame` - Single dataframe object.

<a id="thingsboard_api.tb_pandas.convert_to_dataframe"></a>

#### convert\_to\_dataframe

```python
def convert_to_dataframe(data, keys=None, drop_ts=True)
```

Construct a single DataFrame containing all telemetry keys,     with timeseries as dataframe index from thingsboard timeseries data.

Leverages convert_to_dataframes(data, keys).
Data is collated by outer join, with missing data represented as NaN (Not a Number).

**Arguments**:

- `data` _JSON Object_ - Dictionary containing keys of telemetry key and                 list of timeseries and value pairs.
- `keys` _tuple|list, optional_ - Limit data to specified telemetry keys only.                 Defaults to None.
- `drop_ts` _bool, optional_ - Drop "ts" column from DataFrame. Defaults to True.
  

**Returns**:

- `pandas.DataFrame` - Single dataframe containing concatenated telemetry data.

<a id="thingsboard_api.tb_pandas.dataframe_to_dataframes"></a>

#### dataframe\_to\_dataframes

```python
def dataframe_to_dataframes(dataframe, clean=True)
```

Convert a DataFrame object to a dictionary collection of single Series     DataFrame objects.

**Arguments**:

- `dataframe` _pd.DataFrame_ - Dataframe object to be converted.
- `clean` _bool, optional_ - Attempt to clean up memory used             by dataframe object. Defaults to True.
  

**Returns**:

  dict(str : DataFrame): A dictionary containing dataframe object with         key as dataframe column headings

<a id="thingsboard_api.tb_pandas.unique_column_headings_only"></a>

#### unique\_column\_headings\_only

```python
def unique_column_headings_only(dataframe)
```

Remove column heading rows which are not unique from DataFrame.

**Arguments**:

- `dataframe` _DataFrame_ - DataFrame to be modified.

<a id="thingsboard_api.tb_rest_api"></a>

# thingsboard\_api.tb\_rest\_api

This module provides partial support for thingsboard client-side REST API calls     using requests calls.

Reference: https://thingsboard.io/docs/api/

Dependencies:
- requests : For http POST request
- jwt : JWT decoding

<a id="thingsboard_api.tb_rest_api.Account"></a>

## Account Objects

```python
class Account()
```

Account class to authenticate with thingsboard server.

General usage flow is as follows:
- Create account object with url path to thingsboard server
- Authenticate account with username and password

**Attributes**:

- `url` _str_ - URL for thingsboard
  
  Properties:
- `token` _str_ - Thingsboard JWT token
- `refreshToken` _str_ - Thingsboard JWT refresh Token
  

**Methods**:

  - `authenticate(username, password)`:             Authenticate user account to get JWT token.
  - `update_token()`:             Renews token.
  - `token_expired()`:             Checks if token is expired.

<a id="thingsboard_api.tb_rest_api.Account.__init__"></a>

#### \_\_init\_\_

```python
def __init__(url)
```

Constructs all the necessary attributes for the user object.

**Arguments**:

- `url` _str_ - Full URL path to connect to thingsboard, must included http/https

<a id="thingsboard_api.tb_rest_api.Account.token"></a>

#### token

```python
@property
def token()
```

Returns the main JWT token for the user

<a id="thingsboard_api.tb_rest_api.Account.refreshToken"></a>

#### refreshToken

```python
@property
def refreshToken()
```

Returns the JWT refreshToken for the user

<a id="thingsboard_api.tb_rest_api.Account.authenticate"></a>

#### authenticate

```python
def authenticate(username, password)
```

Authenticate with thingsboard server to obtain JWT token for the user.

**Arguments**:

- `username` _str_ - Username of user for authentication
- `password` _str_ - Password of user for authentication

<a id="thingsboard_api.tb_rest_api.Account.update_token"></a>

#### update\_token

```python
def update_token()
```

Obtain new token using existing refresh token
https://github.com/thingsboard/thingsboard/issues/840

<a id="thingsboard_api.tb_rest_api.Device"></a>

## Device Objects

```python
class Device()
```

A class to represent the thingsboard device for Thingsboard REST API.

**Attributes**:

- `account` _Account_ - Account used for device telemetry
- `name` _str_ - Name of device (User given)
- `device_id` _str_ - Device ID of the device
- `keys` _list_ - List of keys from thingsboard telemetry
  

**Methods**:

  - `get_keys()`:             Get device keys from thingsboard device telemetry
  - `get_data()`:             Get data from thingsboard device telemetry as per REST API

<a id="thingsboard_api.tb_rest_api.Device.__init__"></a>

#### \_\_init\_\_

```python
def __init__(account, name, device_id)
```

Constructs all the necessary attributes for the device object.

**Arguments**:

- `account` _thingsboard_api.Account_ - Account used for device telemetry
- `name` _str_ - Name of device (user given)
- `device_id` _str_ - Device ID as used by thingsboard

<a id="thingsboard_api.tb_rest_api.Device.get_keys"></a>

#### get\_keys

```python
def get_keys()
```

Retrieve and returns telemetry keys belonging to device.

<a id="thingsboard_api.tb_rest_api.Device.get_data"></a>

#### get\_data

```python
def get_data(startTs,
             endTs,
             keys=None,
             limit=None,
             interval=None,
             agg=None,
             tz_offset=0)
```

Retrieves timeseries data from device.
https://thingsboard.io/docs/user-guide/telemetry#data-query-api

**Arguments**:

- `startTs` _datetime|int|float_ - Start of time interval.                     Either datetime object or Unix timestamp in milliseconds.
- `endTs` _datetime|int|float_ - End of time interval, not inclusive.                    Either datetime object or Unix timestamp in milliseconds.
- `keys` _tuple|list|str, optional_ - Limit data to specified telemetry keys only.                     Defaults to None.
- `limit` _int, optional_ - Max amount of data points to return. Defaults to None.
- `interval` _timedelta|int, optional_ - Aggregation interval in milliseconds.                    Also accept timedelta object. Defaults to None.
- `agg` _str, optional_ - Aggregation function.                     Accepts (MIN, MAX, AVG, SUM, COUNT, NONE). Defaults to None.
- `tz_offset` _float, optional_ - Timezone offset in hours. Defaults to 0.
  

**Raises**:

- `ValueError` - List of keys not specified.
- `ValueError` - AGG function not one of MIN, MAX, AVG, SUM, COUNT
  

**Returns**:

  json object: Dictionary of telemetry data with telemetry key as dictionary                     key and value consisting list of timeseries and value.                     dict{key : list[ts, value]}

