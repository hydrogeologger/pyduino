<!-- markdownlint-disable -->

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/log.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `mqtthelper.log`
Logging configuration for the package.

This module provides the internal logging configuration used by this library.
Applications can configure or disable the library's default output through
the public functions exposed by the package.


## Table of Contents
- [`configure`](./mqtthelper.log.md#function-configure): Configure the default logging behavior and stream for the library.
- [`disable`](./mqtthelper.log.md#function-disable): Disable the default output handler for the library.
- [`get_level`](./mqtthelper.log.md#function-get_level): Return the current logging level of the package logger.
- [`get_logger`](./mqtthelper.log.md#function-get_logger): Return the primary package logger.
- [`set_level`](./mqtthelper.log.md#function-set_level): Directly set the logging level for the package.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/log.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `configure`

```python
configure(level=20, stream=None, propagate=False)
```

Configure the default logging behavior and stream for the library.

This function attaches a default stream handler to the package logger,
sets its verbosity level, and configures event propagation. Subsequent
calls can update the level or propagation preference safely.


**Args:**

- <b>`level`</b> (int or str, optional): The logging level threshold (e.g., 
    ``logging.DEBUG``, ``"INFO"``). Defaults to ``logging.INFO``.
- <b>`stream`</b> (TextIO, optional): The text stream to write log output to 
    (e.g., ``sys.stdout``, a file object, or a string stream). 
    Defaults to ``None``, which automatically targets ``sys.stderr``.
- <b>`propagate`</b> (bool, optional): Whether to allow log events to bubble up 
    to parent or root loggers. Defaults to ``False`` to prevent 
    duplicate console output.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/log.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `disable`

```python
disable()
```

Disable the default output handler for the library.

Removes the output handler installed by :func:`configure`.
Other handlers configured by the application are not affected.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/log.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `get_logger`

```python
get_logger()
```

Return the primary package logger.


**Returns:**

- <b>`logging.Logger`</b>: The top-level :class:`logging.Logger` instance for this library.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/log.py#L108"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `get_level`

```python
get_level()
```

Return the current logging level of the package logger.


**Returns:**

- <b>`int`</b>: The current logging level integer (e.g., ``logging.DEBUG``, ``logging.INFO``).



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/log.py#L118"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `set_level`

```python
set_level(level)
```

Directly set the logging level for the package.


**Args:**

- <b>`level`</b> (int or str): The new logging level (e.g., ``logging.DEBUG``, ``logging.WARNING``).



