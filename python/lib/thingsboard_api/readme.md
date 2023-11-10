# thingsboard_api module
This is a thingsboard REST API library package and contains thingsboard specific post processing methods.

Reference: https://thingsboard.io/docs/api/

# Dependencies
* requests
* pyjwt (Optional)
* pandas (Only if importing tb_pandas, for post processing)

# Usage and API
```python
# Import only any one.
import thingsboard_api # If not planning to use pandas DataFrame
import thingsboard_api.tb_pandas # Planning to use pandas DataFrame
```

## Account
Account class to authenticate with thingsboard server. General usage flow is as follows:
* Create account object with url path to thingsboard server
* Authenticate account with username and password
* Use `token()` to show the token from authentication
* Use `refreshToken()` to show the refreshToken from authentication
* Use `token_expired()` to check if authenticated token has expired
* Use `update_token()` to renew expired token

### Account() - Constructor/reinitialize
```python
Account(url)
```
#### Params
* `url` - the full url path to thingsboard server including http/https and port (if required) number

#### Attributes
Same as [params](#Params)


### authenticate()
```python
authenticate(username, password)
```
Authenticate with thingsboard server to obtain JWT token for the user.

See:

* [token()](#token())
* [refreshToken()](#refreshToken())
* [token_expired()](#token_isexpired())
* [update_token()](#update_token())


#### Params
* `username` - Username to authenticate with server
* `password` - Password to authenticate with server


### token()
```python
token()
```
Returns the token from authentication


### refreshToken()
```python
refreshToken()
```
Returns the refresh token from authentication


### token_expired()
** Function is commented out in code as not trully necessary, requires pyjwt module
```python
token_expired()
```

Checks if main jwt token is expired


### update_token()
```python
update_token()
```
Obtain new token using using jwt refreshToken



## Device
Device class reference thingsboard devices.

### Device() - Constructor/reinitialize
```python
Device(account, name, device_id)
```

#### Params
* `account` - Reference to Account() object
* `name` - Verbose device name (user given)
* `device_id` - Device ID as used by thingsboard

### Attributes
* `account` - Account associated with device
* `name` - Verbose device name
* `device_id` - Device ID as used by thingsboard
* `keys` - Available keys from thingsboard as obtained from [get_keys()](#get_keys())


### get_keys()
```python
get_keys()
```
Retrieve and returns telemetry keys belonging to device.


### get_data()
```python
get_data(startTs, endTs, keys=None, limit=None, interval=None, agg=None)
```
Retrieves timeseries data from device. Returns JSON object with devices keys as
json key and values containing list of timeseries and values.

#### Params
* `startTs` (datetime|int|float) - Start of time interval. \
        Either datetime object or Unix timestamp in milliseconds.
* `endTs` (datetime|int|float) - End of time interval, not inclusive.\
        Either datetime object or Unix timestamp in milliseconds.
* `keys` (tuple|list, optional) - Limit data to specified telemetry keys only. \
        Defaults to None.[get_keys()](#get_keys())
* `limit` (int, optional) - Max amount of data points to return. Defaults to None.
* `interval` (timedelta|int, optional) - Aggregation interval, in milliseconds. \
        Also accept timedelta object. Defaults to None.
* `agg` (str, optional) - Aggregation function. \
        Accepts (MIN, MAX, AVG, SUM, COUNT, NONE). Defaults to None.
* `tz_offset1` (float, optional): Timezone offset in hours. Defaults to 0.

Raises `ValueError` when keys is empty or when `agg` function is not one of allowed types.


# thingsboard_api.tb_pandas module
Extends [thingsboard_api](#thingsboard_api-module) base module, with pandas data processing wrapper functions.

## convert_to_dataframes()
```python
convert_to_dataframes(data, keys=None, debug=False)
```
Convert JSON object of telemetry data into a dictionary collection of pandas.DataFrame objects. Setting timeseries "ts" as dataframe index.
i.e. Each telemetry key in own dataframe. See [convert_to_dataframe()](#convert_to_dataframe()) to convert telemetry data to a single dataframe containing all telemetry keys.

### Params
* `data` - JSON object data to convert
* `keys` - List of keys to limit subset of data converted
* `debug` - Show original "ts". Defaults to False.

See:

* [get_data()](#get_data())
* [convert_to_dataframe()](#convert_to_dataframe())


## convert_to_dataframe()
```python
convert_to_dataframe(data, keys=None, debug=False)
```
Construct a Pandas.DataFrame object telemetry data with all telemetry keys. See [convert_to_dataframes()](#convert_to_dataframes()) to convert each key into it's own dataframe.

### Params
* `data` - JSON object data to convert
* `keys` - List of keys to limit subset of data converted
* `debug` - Show original "ts". Defaults to False

See:

* [get_data()](#get_data())
* [convert_to_dataframes()](#convert_to_dataframes())


# Examples:
```python
import datetime
import thingsboard_api.tb_pandas as tb_pandas

account = tb_pandas.Account(url="http://thingsboard.url")
account.authenticate(username="user@user.com", password="password")

# Normal, without manually requesting keys
device = tb_pandas.Device(account, name="DeviceName", device_id="55f0d405-248d-eb11-8a6b-9b13d3e7fe2e")
device.get_keys()
result = device.get_data(start_time=datetime.datetime(2022,6,1), end_time=datetime.datetime.now(), keys=None, limit=1000, tz_offset=10)

# Normal with requesting for specific keys
device = tb_pandas.Device(account, name="DeviceName", device_id="55f0d405-248d-eb11-8a6b-9b13d3e7fe2e")
result = device.get_data(start_time=datetime.datetime(2022,6,1), end_time=datetime.datetime.now(), keys=['a', 'b'], limit=1000, tz_offset=10)

# With thingsboard_api.tb_pandas, key subset not specified
device = tb_pandas.Device(account, name="DeviceName", device_id="55f0d405-248d-eb11-8a6b-9b13d3e7fe2e")
device.get_keys()
data = device.get_data(start_time=datetime.datetime(2022,6,1), end_time=datetime.datetime.now(), keys=None, limit=1000, tz_offset=10)

# Each telemetry key in own dataframe
data_frames = tb_pandas.convert_to_dataframes(data)
# Collate all telemetry key into single dataframe
data_frame = tb_pandas.convert_to_dataframe(data)
```
