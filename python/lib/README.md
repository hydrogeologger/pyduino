# UQGEC Hydrogeologger Custom Python Helper Modules
Place all custom support python packages/library NOT available from PyPI distributable platform in this directory.

There will be two distinctions of packages described here.
- Installable (distributable)
    - Able to be installed by using `pip install` and not available on PyPI.
- Un-installable (undistributable)
    - NOT able to be installed by `pip`

**NOTE: Unfortunately not all package available here is Installable.**


<a id="installation"></a>
# Installation
For installable packages, there are multiple methods to install and use the custom package based on use case. Including the option of not installing.

However installing the custom packages allow the packages to be used normally by python environments offering linting support.

Read further for methods on how to use uninstallable packages.

For the purpose of this guide, there are two python installation methods:
- Regular or Normal
- Editable

You may target specific python environments or versions. Commands for those not listed.

To install, first traverse to wherever this `pyduino\python\lib` directory is located. And run `pip` command. Please note that installation will be performed to the Python version that pip is associated with.


## Editable Installs
```shell
pip install -e PackageName
or
pip install -e . # if you are in the package directory
```
Editable installs allow you to install the package without copying any files. Instead, the files in the development directory are added to Python’s import path. This approach is well suited for development and is also known as a “development installation”.

This method allows any changes to the project to be updated in the python environment. Only need to run `pip install -e` again if package metadata changes.


## Normal or Regular Installs
```shell
# `pip install PackageName` will not work as the package is not published in PyPi package indexer.
# Need to traverse into package directory using `cd` prior to running following command.
pip install .
```
This will install the project into the Python that pip is associated with as how a normal python distributed package is installed.

This method allow you to move the library directory, however any changes to the packages need to be reinstalled with the `pip install .` command.

## No installation
You may choose to not install. However installation offers support such as linting. See [No-Install Usage](#usage.noinstall) to learn how to use the package in python scripts if the package is not installed.




<a id="usage"></a>
# How to Use
Using the packages depends if the package is installed or not installed.

## Installed Usage
Import the package as normal
```python
import PackageName
# Example:
import postprocess
```

<a id="usage.noinstall"></a>
## No-Install usage
To use the package if the package is not installed. you will need to manually add the package path to system `PATH` environment `sys.path`.

One method to do this in your script is as follows. Note this does not offer linting support, only allows your script to execute.
```python
# first you need to import sys to append path
import sys
```
```python
# If you add the python lib path to PATH
sys.path.append("/path/to/python/lib")
import packagename.packagename
# Or with module aliasing
import packagename.packagename as alias

# Example:
sys.path.append("/path/to/python/lib")
import postprocess.postprocess as postprocess
```
or
```python
# If you add the path to the specific package
sys.path.append("/path/to/python/lib/packagename")
import packagename
# With aliasing
import packagename as alias

# Example:
sys.path.append("/path/to/python/lib/postprocess")
import postprocess
```




<a id="faq"></a>
# FAQ
## `__future__` or `builtins` error
Please refer to the specific modules to determine the python packages that they depend on.
Generally the modules should be built with python 2/3 compatiblity in mind, if there are any import `__future__` or `builtins` errors, try to install the latest python `future` module package.
```python
# Show installed python future package
pip show future
# Install python future package
pip install future
```

## pylance, linting reportMissingImports
This appears to be an issue with setuptools prepending `__editable__` to module path.
It does not seem to affect importing and running the package, only linting.

Try adding `--config-settings editable_mode=compat` argument to pip install when
executing pip install from `pyduino\python\lib` directory.
```shell
pip install -e PackageName --config-settings editable_mode=compat
# or
pip install -e . --config-settings editable_mode=compat
```
`compat` editable mode is transitional and may be removed in future versions of `setuptools`.
https://setuptools.pypa.io/en/latest/userguide/development_mode.html
