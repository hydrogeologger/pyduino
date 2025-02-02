<!-- markdownlint-disable -->

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/error_handler.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `thingsboard_api.error_handler`
Exception handling utilities for thingsboard_api.

This module provides an optional exception handler that suppresses internal library 
tracebacks for uncaught exceptions derived from ``ThingsBoardAPIError``, displaying 
only the traceback frames from the end-user's application implementation.

The handler affects only the current Python process and is not installed
automatically.

Applications can enable friendly error output by calling:  
```python
import thingsboard_api

thingsboard_api.enable_friendly_exceptions()
```


## Table of Contents
- [`disable_friendly_exceptions`](./thingsboard_api.error_handler.md#function-disable_friendly_exceptions): Disable friendly ThingsBoard API exception output.
- [`enable_friendly_exceptions`](./thingsboard_api.error_handler.md#function-enable_friendly_exceptions): Enable friendly ThingsBoard API exception output.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/error_handler.py#L207"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `enable_friendly_exceptions`

```python
enable_friendly_exceptions()
```

Enable friendly ThingsBoard API exception output.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/error_handler.py#L213"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `disable_friendly_exceptions`

```python
disable_friendly_exceptions()
```

Disable friendly ThingsBoard API exception output.



