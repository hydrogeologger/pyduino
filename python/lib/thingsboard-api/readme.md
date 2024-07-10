# thingsboard-api python package

This is a Hydrogeologger/Pyduino python package partially implementing thingsboard REST API
and contains thingsboard specific post processing and pandas library helper methods for data extraction.

> [!IMPORTANT]
> **Package is NOT distributed on PyPi package indexer!**

Reference: <https://thingsboard.io/docs/api/>

## Dependencies

- requests : For REST API calls.
- pandas (Optional) : Only if importing tb_pandas, for post processing.
- numpy (Optional) : Pandas dependency, for post processing.

## Usage

For IntelliSense support, it is recommended to use one of the following installation options:

1. [Editable](#editable-installation)
2. [Regular](#regular-installation)

Non-Installation use is also possible but provides no IntelliSense support. See [No-Install Usage](#no-installation-example).

### Initial Setup

1. Obtain copy of pyduino files.\
   If Git is installed and you do not want a copy of pyduino files.
   See [Installation from Git Repository](#installation-from-git-repository)\
   If git repo method is used, you can skip the following methods.
2. Traverse to pyduino, python library directory `...\pyduino\python\lib\`.
3. Install package using [regular](#regular-installation) or [editable](#editable-installation) Installation methods.
    Alternatively can ignore installation see [No Installation](#no-installation).

#### Editable Installation

Allows module changes to be automatically updated in the python environment.\
However any package file directory changes will also affect the python environment.

Note: package version does not update automatically, need to perform reinstallation.

```shell
pip install -e ./thingsboard-api
```

or

```shell
# if you are in the package directory
# ...\pyduino\python\lib\thingsboard-api
pip install -e .
```

#### Regular Installation

Will install the package normally such that any modifications to the package
files is not reflected in the python environment.

Any changes to the packages need to be reinstalled to take effect.

```shell
# `pip install PackageName` will not work as the package is not published in PyPi package indexer.
# Need to traverse into `...\pyduino\python\lib` directory prior to running following command.
pip install ./thingsboard-api
```

or

```shell
# if you are in the package directory
# ...\pyduino\python\lib\thingsboard-api
pip install -e .
```

##### Installation from Git Repository

This method requires git to be installed on the system and performs a [*regular package installation*](#regular-installation)
directly from the repository without copying all the pyduino files.\
It is NOT recommended to perform an editable mode install from the remote git repo.

```shell
pip install "git+https://github.com/hydrogeologger/pyduino.git#egg=thingsboard-api&subdirectory=python/lib/thingsboard-api"
```

### No installation

You may choose to not install. However installation offers IntelliSense support.\
See [No-Install Usage](#no-installation-example) to learn how to use the package in python scripts if the package is not installed.

### Example

```python
import thingsboard_api.tb_pandas as tb_pandas

account = tb_pandas.Account(url="http://thingsboard.url")
account.authenticate(username="user@user.com", password="password")

# Normal, timeseries data for all keys for device is requested
device = tb_pandas.Device(account=account,
                          name="DeviceName",
                          device_id="55f0d405-248d-eb11-8a6b-9b13d3e7fe2e")
device.get_keys_timeseries()  # Retrieve all timeseries keys for device
result = device.get_timeseries(startTs=tb_pandas.datetime(2022, 6, 1),
                         endTs=tb_pandas.datetime.now(),
                         keys=None,
                         limit=1000,
                         tz_offset=0)

# Normal, timeseries data for specific keys only
device = tb_pandas.Device(account=account,
                          name="DeviceName",
                          device_id="55f0d405-248d-eb11-8a6b-9b13d3e7fe2e")
result = device.get_timeseries(startTs=tb_pandas.datetime(2022, 6, 1),
                         endTs=tb_pandas.datetime.now(),
                         keys=['key_a', 'key_b'],
                         limit=1000,
                         tz_offset=0)

# With thingsboard_api.tb_pandas, key subset not specified
device = tb_pandas.Device(account=account,
                          name="DeviceName",
                          device_id="55f0d405-248d-eb11-8a6b-9b13d3e7fe2e")
device.get_keys_timeseries()
data = device.get_timeseries(startTs=tb_pandas.datetime(2022, 6, 1),
                       endTs=tb_pandas.datetime.now(),
                       keys=None,
                       limit=1000,
                       tz_offset=0)

# Collate each telemetry key in own dataframe (one dataframe per key)
data_frames = tb_pandas.convert_to_dataframes(data)
# Collate all telemetry key into single dataframe (multiple key per dataframe)
data_frame = tb_pandas.convert_to_dataframe(data)
```

#### No-Installation Example

Note this method does not provide IntelliSense support! For IntelliSense please use one of the [installation](#initial-setup) methods.

```python
# Need to add path to package module files before importing
sys.path.append("/path/to/pyduino/python/lib/thingsboard-api/src")
import thingsboard_api
```

## API

See documentation [here](<./docs/readme.md>)
