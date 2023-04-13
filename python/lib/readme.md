# UQGEC Hydrogeologger Custom Python Helper Modules
Place all custom support modules in this directory.

## Notes
Please refer to the specific modules to determine the python packages that they depend on.
Generally the modules should be built with python 2/3 compatiblity in mind, if there are any import `__future__` or `builtins` errors, try to install the latest python `future` module package.
```python
# Show installed python future package
pip show future
# Install python future package
pip install future
```

## How to use
In python script, require to import `sys` module and add the path of the python library directory to `sys.path`

Example for linux:
```python
import sys
# Append private python library directory to system path
sys.path.append("/home/pi/pyduino/python/lib")
import mqtthelper # MQTT helper module for publishing archive
```