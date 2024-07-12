# postprocess

Postprocessing support library including interpolation and file mapping correlation support.

NOTE: Package is currently not distributed on PyPi package indexer!

## Dependencies

- numpy
- pandas
- scipy
- matplotlib (Optional) : Use for visual debugging interpolation plots.

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
pip install -e ./postprocess
```

or

```shell
# if you are in the package directory
# ...\pyduino\python\lib\postprocess
pip install -e .
```

#### Regular Installation

Will install the package normally such that any modifications to the package
files is not reflected in the python environment.

Any changes to the packages need to be reinstalled to take effect.

```shell
# `pip install PackageName` will not work as the package is not published in PyPi package indexer.
# Need to traverse into `...\pyduino\python\lib` directory prior to running following command.
pip install ./postprocess
```

or

```shell
# if you are in the package directory
# ...\pyduino\python\lib\postprocess
pip install -e .
```

##### Installation from Git Repository

This method requires git to be installed on the system and performs a [*regular package installation*](#regular-installation)
directly from the repository without copying all the pyduino files.\
It is NOT recommended to perform an editable mode install from the remote git repo.

```shell
pip install "git+https://github.com/hydrogeologger/pyduino.git#egg=postprocess&subdirectory=python/lib/postprocess"
```

### No installation

You may choose to not install. However installation offers IntelliSense support.\
See [No-Install Usage](#no-installation-example) to learn how to use the package in python scripts if the package is not installed.

### Example

```python
from datetime import timedelta, datetime

import numpy as np
import pandas as pd
import postprocess
from postprocess.filehandler import FileCorrelation

START_TIME = datetime(2024, 6, 1)  # Start of period
END_TIME = datetime(2024, 6, 30)  # End of Period

# Generate example dummy DataFrame data
example_data = pd.DataFrame(np.random.randint(0, 30, size=10),
                            columns=["value"],
                            index=pd.date_range(START_TIME, END_TIME, freq="3D"))

# Create interpolation object with interval window within start and end period
interpolated = postprocess.Interpolation(
    start_time=START_TIME + timedelta(days=1),
    end_time=END_TIME - timedelta(days=1),
    interval=timedelta(days=1),
    data=example_data
)
# Perform smooth interpolation on "value" dataset
interpolated.interpolate_smooth(key_name="value")


# Create file correlation mapping object
image_files = FileCorrelation(path="full/path/to/directory")

# Map files to datetime value
image_files.parse_files(format_="%Y-%m-%d_%H%M_filename", ext=(".jpg"))

# Dummy map values data to focus on a map date range with parsed date-time stamp with filenames
map_values = pd.date_range(START_TIME + timedelta(days=1),
                           end=END_TIME - timedelta(days=1),
                           freq=timedelta(days=1)).tolist()

image_files.map_to_filename_datetime(map_values=map_values,
                                     ref_date_time=image_files.date_times,
                                     data=image_files.date_times)
```

#### No-Installation Example

Note this method does not provide IntelliSense support! For IntelliSense please use one of the [installation](#initial-setup) methods.

```python
# Need to add path to package module files before importing
sys.path.append("/path/to/pyduino/python/lib/postprocess/src")
import postprocess
from postprocess.filehandler import FileCorrelation
```

## API

See documentation [here](<./docs/readme.md>)
