# thingsboard_api module
This is a thingsboard REST API library package and contains thingsboard specific post processing methods.

Reference: https://thingsboard.io/docs/api/

# Dependencies
* requests
* pyjwt (Optional)
* pandas (Only if importing tb_pandas, for post processing)

# Usage and API
```python
import thingsboard_api
import thingsboard_api.tb_pandas # Include only if require dataframe
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
* `url` - the full url path to thingsboard server including http/https and port number

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
* `name` - Verbose device name
* `device_id` - ID of device as from thingsboard

### Attributes
* `name` - Verbose device name
* `device_id` - ID of device as from thingsboard
* `keys` - Available keys from thingsboard as obtained from [get_keys()](#get_keys())


### get_keys()
```python
get_keys()
```
Retrieves and returns the keys used by the thingsboard device


### get_data()
```python
get_data(startTs, endTs, keys=None, limit=100000, interval=None, agg=None)
```
Sends a post request to thingsboard telemetry to extract device data. Returns dictionary of
timeseries telemetry data.

#### Params
* `startTs` - Unix timestamp that identifies the start of the interval in milliseconds
* `endTs` - Unix timestamp that identifies the end of the interval in milliseconds
* `keys` - List of telemetry keys to fetch, If not provided, must have called [get_keys()](#get_keys())
* `limit` - Max amount of data points to return or intervals to process, default=100000
* `interval` - Aggregation interval, in milliseconds
* `agg` - Aggregation function, one of MIN, MAX, AVG, SUM, COUNT

Raises `ValueError` when keys is empty.


### get_data2()
```python
get_data2(self, start_time, end_time, keys=None, limit=100000, interval=None, agg=None, tz_offset=10):
```
Alternate to [get_data()](#get_data), get_data2() requires a datetime time interval and allows
time zone hour offset calculation, returns dictionary of timeseries telemetry data.

#### Params
* `start_time` - Date and time that identifies the start of the interval
* `end_time` - Date and time that identifies the end of the interval
* `keys` - List of telemetry keys to fetch, if ommited must have called [get_keys()](#get_keys())
* `limit` - Max amount of data points to return or intervals to process, default=100000
* `interval` - Aggregation interval, in milliseconds
* `agg` - Aggregation function, one of MIN, MAX, AVG, SUM, COUNT
* `tz_offset` - Timezone hour offset for thingsboard server, defaults to +10 hours

Raises `ValueError` when keys is empty.


## tb_pandas.Device
Child class of thingsboard_api.Device class object. Extends [Device Class](#Device),
with pandas data processing wrapper functions.
Use as per `Device` class object, will store device data telemetry in object.

### get_data (Override)
Overrides [get_data()](#get_data()) to store timeseries telemetry data in object.


### get_dataframe()
```python
get_dataframe(keys=None, tz_offset=10)
```
Construct a Pandas.DataFrame object from device timeseries telemetry

#### Params
* `keys` - List of telemetry keys to limit for data frame
* `tz_offset` - Timezone hour offset for thingsboard server, defaults to +10 hours


# Examples:
```python
import thingsboard_api
import thingsboard_api.tb_pandas as tb_pandas

account = thingsboard_api.Account(url="http://thingsboard.url")
account.authenticate(username="user@user.com", password="password")

# Normal, without manually requesting keys
device = thingsboard_api.Device(account, name="DeviceName", device_id="55f0d405-248d-eb11-8a6b-9b13d3e7fe2e")
device.get_keys()
result = device.get_data2(start_time=datetime.datetime(2022,6,1), end_time=datetime.datetime.now(), keys=None, limit=1000, tz_offset=10)

# Normal with requesting for specific keys
device = thingsboard_api.Device(account, name="DeviceName", device_id="55f0d405-248d-eb11-8a6b-9b13d3e7fe2e")
result = device.get_data2(start_time=datetime.datetime(2022,6,1), end_time=datetime.datetime.now(), keys=['a', 'b'], limit=1000, tz_offset=10)

# With thingsboard_api.tb_pandas, specific keys for data frame
device = tb_pandas.Device(account, name="DeviceName", device_id="55f0d405-248d-eb11-8a6b-9b13d3e7fe2e")
device.get_keys()
result = device.get_data2(start_time=datetime.datetime(2022,6,1), end_time=datetime.datetime.now(), keys=None, limit=1000, tz_offset=10)

result_df = device.get_dataframe(keys=['a','b'], tz_offset=10)
```
