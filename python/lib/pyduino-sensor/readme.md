# pyduino-sensor

Hydrogeologger/Pyduino sensor hardware and post processing helper package.

NOTE: Package is currently not distributed on PyPi package indexer!

## Dependencies

- gpiozero (Optional) : Required only if interfacing with GPIO.

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
pip install -e ./pyduino-sensor
```

or

```shell
# if you are in the package directory
# ...\pyduino\python\lib\pyduino-sensor
pip install -e .
```

#### Regular Installation

Will install the package normally such that any modifications to the package
files is not reflected in the python environment.

Any changes to the packages need to be reinstalled to take effect.

```shell
# `pip install PackageName` will not work as the package is not published in PyPi package indexer.
# Need to traverse into `...\pyduino\python\lib` directory prior to running following command.
pip install ./pyduino-sensor
```

or

```shell
# if you are in the package directory
# ...\pyduino\python\lib\pyduino-sensor
pip install -e .
```

##### Installation from Git Repository

This method requires git to be installed on the system and performs a [*regular package installation*](#regular-installation)
directly from the repository without copying all the pyduino files.\
It is NOT recommended to perform an editable mode install from the remote git repo.

```shell
pip install "git+https://github.com/hydrogeologger/pyduino.git#egg=pyduino-sensor&subdirectory=python/lib/pyduino-sensor"
```

### No installation

You may choose to not install. However installation offers IntelliSense support.\
See [No-Install Usage](#no-installation-example) to learn how to use the package in python scripts if the package is not installed.

### Example

```python
import pyduino_sensor.davis as davis

rain_tip_bucket = davis.Rain(name="rain", pin=8, debounce=0.001, resolution=0.2, debug=False)
wind_speed = davis.WindSpeed(name="wind_speed", pin=18, debounce=None, debug=False)

rain_tip_bucket.begin()
wind_speed.begin()
while True:
    average_wind = wind_speed.get_average()
    rain_period_cumulative = rain_tip_bucket.get_cumulative()
    time.sleep(900) # 15 min interval
```

#### No-Installation Example

Note this method does not provide IntelliSense support! For IntelliSense please use one of the [installation](#initial-setup) methods.

```python
# Need to add path to package module files before importing
sys.path.append("/path/to/pyduino/python/lib/pyduino-sensor/src")
import pyduino_sensor.davis as davis
```

## API

See documentation [here](<./docs/readme.md>)
