# UQGEC Hydrogeologger Custom Python Helper Modules

Place all custom support python packages/library NOT available from PyPI distributable platform in this directory.

There will be two distinctions of packages described here.

- Installable (distributable)
  - Able to be installed by using `pip install` and not available on PyPI.
- Un-installable (undistributable)
  - NOT able to be installed by `pip`

**NOTE: Unfortunately not all package available here is Installable.**

The following provides a generic guide to the installation and or usage of custom packages.
Please refer to individual packages for available installation and usage methods.

<a id="installation"></a>

# Installation

For installable packages, there are multiple methods to install and use the custom package based on use case. Including the option of not installing.

Installing the custom packages allow the packages to be used normally by python environments offering linting support.

For uninstallable packages. See [No-Installation](#no-installation)

For the purpose of this guide, there are two python installation methods:

- [Regular or Normal](#normal-or-regular-installs)
- [Editable](#editable-installs)

You may target specific python environments or versions. Commands for those not listed.

To install, first traverse to wherever this `pyduino\python\lib` directory is located. And run `pip` command. Please note that installation will be performed to the Python version that pip is associated with.

## Editable Installs

```shell
pip install -e ./PackageName
```

or

```shell
# if you are in the package directory
pip install -e .
```

Editable installs allow you to install the package without copying any files. Instead, the files in the development directory are added to Python's import path. This approach is well suited for development and is also known as a “development installation”.

Installation will break if the path to the package directory is modified (i.e. packaged contents is moved from original directory).

This method allows any changes to the project to be updated in the python environment. Only need to repeat editable installation process if package metadata changes.

## Normal or Regular Installs

```shell
# `pip install PackageName` will not work as the package is not published in PyPi package indexer.
# Need to traverse into directory `pyduino\python\lib` using `cd` prior to running following command.

pip install ./PackageName
```

or

```shell
# if you are in the package directory
pip install .
```

This will install the project into the Python that pip is associated with as how a normal python distributed package is installed.

This method allow you to move the library directory, however any updates to the package requires reinstalled for changes to apply.

## No installation

You may choose to not install. However installation offers benefits such as linting support. See [No-Install Usage](#usage.noinstall) to learn how to use the package in python scripts if the package is not installed.

<a id="usage"></a>

# How to Use

Methods of using the packages depends on the installation status of the package.

- [Installed](#installed-usage)
- [Not Installed](#no-install-usage)

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
pip install -e ./PackageName --config-settings editable_mode=compat
```

or

```shell
# if you are in the package directory
pip install -e . --config-settings editable_mode=compat
```

`compat` editable mode is transitional and may be removed in future versions of `setuptools`.
<https://setuptools.pypa.io/en/latest/userguide/development_mode.html>

## pip editable installation error: option --user not recognized

During installation for python2.7 when setup.py is executed.
The following error could be observed

```shell
error: option --user not recognized
```

Try removing pyproject.toml from the installation package and execute pip installation again.
