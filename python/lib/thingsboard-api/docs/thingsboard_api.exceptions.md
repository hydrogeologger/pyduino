<!-- markdownlint-disable -->

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `thingsboard_api.exceptions`
Exception hierarchy for the thingsboard_api package.

This module defines exceptions raised by the ThingsBoard API client.

The hierarchy separates:  
- Transport errors: failures communicating with the server.
- API errors: failures returned by the ThingsBoard API.


## Table of Contents
- [`APIError`](./thingsboard_api.exceptions.md#exception-apierror): Base exception for API response failures.
	- [`APIError.__init__`](./thingsboard_api.exceptions.md#constructor-apierror__init__): Initialise an API error.
	- [`APIError.from_response`](./thingsboard_api.exceptions.md#classmethod-apierrorfrom_response): Create an API error from an HTTP response.
- [`AuthenticationError`](./thingsboard_api.exceptions.md#exception-authenticationerror): Raised when authentication fails.
	- [`AuthenticationError.__init__`](./thingsboard_api.exceptions.md#constructor-authenticationerror__init__): Initialise an API error.
	- [`AuthenticationError.from_response`](./thingsboard_api.exceptions.md#classmethod-authenticationerrorfrom_response): Create an API error from an HTTP response.
- [`BadRequestError`](./thingsboard_api.exceptions.md#exception-badrequesterror): Raised when the API rejects a malformed request.
	- [`BadRequestError.__init__`](./thingsboard_api.exceptions.md#constructor-badrequesterror__init__): Initialise an API error.
	- [`BadRequestError.from_response`](./thingsboard_api.exceptions.md#classmethod-badrequesterrorfrom_response): Create an API error from an HTTP response.
- [`ConflictError`](./thingsboard_api.exceptions.md#exception-conflicterror): Raised when the request conflicts with the current resource state.
	- [`ConflictError.__init__`](./thingsboard_api.exceptions.md#constructor-conflicterror__init__): Initialise an API error.
	- [`ConflictError.from_response`](./thingsboard_api.exceptions.md#classmethod-conflicterrorfrom_response): Create an API error from an HTTP response.
- [`MethodNotAllowedError`](./thingsboard_api.exceptions.md#exception-methodnotallowederror): Raised when the requested HTTP method is not supported.
	- [`MethodNotAllowedError.__init__`](./thingsboard_api.exceptions.md#constructor-methodnotallowederror__init__): Initialise an API error.
	- [`MethodNotAllowedError.from_response`](./thingsboard_api.exceptions.md#classmethod-methodnotallowederrorfrom_response): Create an API error from an HTTP response.
- [`NotFoundError`](./thingsboard_api.exceptions.md#exception-notfounderror): Raised when the requested resource does not exist.
	- [`NotFoundError.__init__`](./thingsboard_api.exceptions.md#constructor-notfounderror__init__): Initialise an API error.
	- [`NotFoundError.from_response`](./thingsboard_api.exceptions.md#classmethod-notfounderrorfrom_response): Create an API error from an HTTP response.
- [`PermissionDeniedError`](./thingsboard_api.exceptions.md#exception-permissiondeniederror): Raised when the authenticated user lacks permission.
	- [`PermissionDeniedError.__init__`](./thingsboard_api.exceptions.md#constructor-permissiondeniederror__init__): Initialise an API error.
	- [`PermissionDeniedError.from_response`](./thingsboard_api.exceptions.md#classmethod-permissiondeniederrorfrom_response): Create an API error from an HTTP response.
- [`PreconditionFailedError`](./thingsboard_api.exceptions.md#exception-preconditionfailederror): Raised when a request precondition is not satisfied.
	- [`PreconditionFailedError.__init__`](./thingsboard_api.exceptions.md#constructor-preconditionfailederror__init__): Initialise an API error.
	- [`PreconditionFailedError.from_response`](./thingsboard_api.exceptions.md#classmethod-preconditionfailederrorfrom_response): Create an API error from an HTTP response.
- [`RateLimitError`](./thingsboard_api.exceptions.md#exception-ratelimiterror): Raised when the API rate limit has been exceeded.
	- [`RateLimitError.__init__`](./thingsboard_api.exceptions.md#constructor-ratelimiterror__init__): Initialise an API error.
	- [`RateLimitError.from_response`](./thingsboard_api.exceptions.md#classmethod-ratelimiterrorfrom_response): Create an API error from an HTTP response.
- [`ServerError`](./thingsboard_api.exceptions.md#exception-servererror): Raised when the ThingsBoard server reports an internal failure.
	- [`ServerError.__init__`](./thingsboard_api.exceptions.md#constructor-servererror__init__): Initialise an API error.
	- [`ServerError.from_response`](./thingsboard_api.exceptions.md#classmethod-servererrorfrom_response): Create an API error from an HTTP response.
- [`ThingsBoardAPIError`](./thingsboard_api.exceptions.md#exception-thingsboardapierror): Base exception for all thingsboard_api errors.
- [`TransportConnectTimeoutError`](./thingsboard_api.exceptions.md#exception-transportconnecttimeouterror): Raised when the initial TCP handshake/connection setup to the server times out.
- [`TransportConnectionError`](./thingsboard_api.exceptions.md#exception-transportconnectionerror): Base exception raised when a connection to the server cannot be established.
- [`TransportError`](./thingsboard_api.exceptions.md#exception-transporterror): Base exception for HTTP transport failures.
- [`TransportReadTimeoutError`](./thingsboard_api.exceptions.md#exception-transportreadtimeouterror): Raised when the connection is established but the server fails to send data mid-stream.
- [`TransportSSLError`](./thingsboard_api.exceptions.md#exception-transportsslerror): Raised when SSL verification or negotiation fails.
- [`TransportTimeoutError`](./thingsboard_api.exceptions.md#exception-transporttimeouterror): Raised when an HTTP request exceeds a configured connection or read timeout.




<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L12"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `ThingsBoardAPIError`
Base exception for all thingsboard_api errors.

All exceptions raised by the ThingsBoard API client inherit from this
exception.






<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `TransportError`
Base exception for HTTP transport failures.

Transport errors occur when the client cannot successfully communicate
with the ThingsBoard server.






<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `TransportConnectionError`
Base exception raised when a connection to the server cannot be established.






<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `TransportTimeoutError`
Raised when an HTTP request exceeds a configured connection or read timeout.






<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `TransportConnectTimeoutError`
Raised when the initial TCP handshake/connection setup to the server times out.






<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `TransportReadTimeoutError`
Raised when the connection is established but the server fails to send data mid-stream.






<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L44"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `TransportSSLError`
Raised when SSL verification or negotiation fails.






<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `APIError`
Base exception for API response failures.

Raised when the ThingsBoard server receives the request but returns
an error response.


**Attributes:**

- <b>`status_code`</b> (int): HTTP response status code.
- <b>`message`</b> (str): Error message returned by the API.
- <b>`error_code`</b> (int): ThingsBoard error code.
- <b>`timestamp`</b> (str): Timestamp returned by the API.
- <b>`payload`</b> (dict): Parsed API error response payload.
- <b>`response`</b> (requests.Response): Original HTTP response object.


<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `APIError.__init__`

```python
APIError(
    status_code,
    message,
    error_code=None,
    timestamp=None,
    payload=None,
    response=None
)
```

Initialise an API error.


**Args:**

- <b>`status_code`</b> (int): HTTP response status code.
- <b>`message`</b> (str): Error message.
- <b>`error_code`</b> (int): ThingsBoard error code.
- <b>`timestamp`</b> (str): Timestamp returned by the API.
- <b>`response`</b> (requests.Response): Original HTTP response object.





<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>classmethod</kbd> `APIError.from_response`

```python
from_response(response)
```

Create an API error from an HTTP response.


**Args:**

- <b>`response`</b> (requests.Response): HTTP response object.


**Returns:**

- <b>`APIError`</b>: Initialised API error.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L123"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `BadRequestError`
Raised when the API rejects a malformed request.

Corresponds to HTTP status code 400.


<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `BadRequestError.__init__`

```python
APIError(
    status_code,
    message,
    error_code=None,
    timestamp=None,
    payload=None,
    response=None
)
```

Initialise an API error.


**Args:**

- <b>`status_code`</b> (int): HTTP response status code.
- <b>`message`</b> (str): Error message.
- <b>`error_code`</b> (int): ThingsBoard error code.
- <b>`timestamp`</b> (str): Timestamp returned by the API.
- <b>`response`</b> (requests.Response): Original HTTP response object.





<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>classmethod</kbd> `BadRequestError.from_response`

```python
from_response(response)
```

Create an API error from an HTTP response.


**Args:**

- <b>`response`</b> (requests.Response): HTTP response object.


**Returns:**

- <b>`APIError`</b>: Initialised API error.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L130"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `AuthenticationError`
Raised when authentication fails.

Corresponds to HTTP status code 401.


<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `AuthenticationError.__init__`

```python
APIError(
    status_code,
    message,
    error_code=None,
    timestamp=None,
    payload=None,
    response=None
)
```

Initialise an API error.


**Args:**

- <b>`status_code`</b> (int): HTTP response status code.
- <b>`message`</b> (str): Error message.
- <b>`error_code`</b> (int): ThingsBoard error code.
- <b>`timestamp`</b> (str): Timestamp returned by the API.
- <b>`response`</b> (requests.Response): Original HTTP response object.





<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>classmethod</kbd> `AuthenticationError.from_response`

```python
from_response(response)
```

Create an API error from an HTTP response.


**Args:**

- <b>`response`</b> (requests.Response): HTTP response object.


**Returns:**

- <b>`APIError`</b>: Initialised API error.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `PermissionDeniedError`
Raised when the authenticated user lacks permission.

Corresponds to HTTP status code 403.


<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `PermissionDeniedError.__init__`

```python
APIError(
    status_code,
    message,
    error_code=None,
    timestamp=None,
    payload=None,
    response=None
)
```

Initialise an API error.


**Args:**

- <b>`status_code`</b> (int): HTTP response status code.
- <b>`message`</b> (str): Error message.
- <b>`error_code`</b> (int): ThingsBoard error code.
- <b>`timestamp`</b> (str): Timestamp returned by the API.
- <b>`response`</b> (requests.Response): Original HTTP response object.





<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>classmethod</kbd> `PermissionDeniedError.from_response`

```python
from_response(response)
```

Create an API error from an HTTP response.


**Args:**

- <b>`response`</b> (requests.Response): HTTP response object.


**Returns:**

- <b>`APIError`</b>: Initialised API error.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L144"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `NotFoundError`
Raised when the requested resource does not exist.

Corresponds to HTTP status code 404.


<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `NotFoundError.__init__`

```python
APIError(
    status_code,
    message,
    error_code=None,
    timestamp=None,
    payload=None,
    response=None
)
```

Initialise an API error.


**Args:**

- <b>`status_code`</b> (int): HTTP response status code.
- <b>`message`</b> (str): Error message.
- <b>`error_code`</b> (int): ThingsBoard error code.
- <b>`timestamp`</b> (str): Timestamp returned by the API.
- <b>`response`</b> (requests.Response): Original HTTP response object.





<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>classmethod</kbd> `NotFoundError.from_response`

```python
from_response(response)
```

Create an API error from an HTTP response.


**Args:**

- <b>`response`</b> (requests.Response): HTTP response object.


**Returns:**

- <b>`APIError`</b>: Initialised API error.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L151"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `MethodNotAllowedError`
Raised when the requested HTTP method is not supported.

Corresponds to HTTP status code 405.


<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `MethodNotAllowedError.__init__`

```python
APIError(
    status_code,
    message,
    error_code=None,
    timestamp=None,
    payload=None,
    response=None
)
```

Initialise an API error.


**Args:**

- <b>`status_code`</b> (int): HTTP response status code.
- <b>`message`</b> (str): Error message.
- <b>`error_code`</b> (int): ThingsBoard error code.
- <b>`timestamp`</b> (str): Timestamp returned by the API.
- <b>`response`</b> (requests.Response): Original HTTP response object.





<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>classmethod</kbd> `MethodNotAllowedError.from_response`

```python
from_response(response)
```

Create an API error from an HTTP response.


**Args:**

- <b>`response`</b> (requests.Response): HTTP response object.


**Returns:**

- <b>`APIError`</b>: Initialised API error.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L158"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `ConflictError`
Raised when the request conflicts with the current resource state.

Corresponds to HTTP status code 409.


<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `ConflictError.__init__`

```python
APIError(
    status_code,
    message,
    error_code=None,
    timestamp=None,
    payload=None,
    response=None
)
```

Initialise an API error.


**Args:**

- <b>`status_code`</b> (int): HTTP response status code.
- <b>`message`</b> (str): Error message.
- <b>`error_code`</b> (int): ThingsBoard error code.
- <b>`timestamp`</b> (str): Timestamp returned by the API.
- <b>`response`</b> (requests.Response): Original HTTP response object.





<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>classmethod</kbd> `ConflictError.from_response`

```python
from_response(response)
```

Create an API error from an HTTP response.


**Args:**

- <b>`response`</b> (requests.Response): HTTP response object.


**Returns:**

- <b>`APIError`</b>: Initialised API error.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L165"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `PreconditionFailedError`
Raised when a request precondition is not satisfied.

Corresponds to HTTP status code 412.


<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `PreconditionFailedError.__init__`

```python
APIError(
    status_code,
    message,
    error_code=None,
    timestamp=None,
    payload=None,
    response=None
)
```

Initialise an API error.


**Args:**

- <b>`status_code`</b> (int): HTTP response status code.
- <b>`message`</b> (str): Error message.
- <b>`error_code`</b> (int): ThingsBoard error code.
- <b>`timestamp`</b> (str): Timestamp returned by the API.
- <b>`response`</b> (requests.Response): Original HTTP response object.





<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>classmethod</kbd> `PreconditionFailedError.from_response`

```python
from_response(response)
```

Create an API error from an HTTP response.


**Args:**

- <b>`response`</b> (requests.Response): HTTP response object.


**Returns:**

- <b>`APIError`</b>: Initialised API error.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L172"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `RateLimitError`
Raised when the API rate limit has been exceeded.

Corresponds to HTTP status code 429.


<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `RateLimitError.__init__`

```python
APIError(
    status_code,
    message,
    error_code=None,
    timestamp=None,
    payload=None,
    response=None
)
```

Initialise an API error.


**Args:**

- <b>`status_code`</b> (int): HTTP response status code.
- <b>`message`</b> (str): Error message.
- <b>`error_code`</b> (int): ThingsBoard error code.
- <b>`timestamp`</b> (str): Timestamp returned by the API.
- <b>`response`</b> (requests.Response): Original HTTP response object.





<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>classmethod</kbd> `RateLimitError.from_response`

```python
from_response(response)
```

Create an API error from an HTTP response.


**Args:**

- <b>`response`</b> (requests.Response): HTTP response object.


**Returns:**

- <b>`APIError`</b>: Initialised API error.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L179"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>exception</kbd> `ServerError`
Raised when the ThingsBoard server reports an internal failure.

Corresponds to HTTP status codes 500-599.


<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `ServerError.__init__`

```python
APIError(
    status_code,
    message,
    error_code=None,
    timestamp=None,
    payload=None,
    response=None
)
```

Initialise an API error.


**Args:**

- <b>`status_code`</b> (int): HTTP response status code.
- <b>`message`</b> (str): Error message.
- <b>`error_code`</b> (int): ThingsBoard error code.
- <b>`timestamp`</b> (str): Timestamp returned by the API.
- <b>`response`</b> (requests.Response): Original HTTP response object.





<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/thingsboard-api/src/thingsboard_api/exceptions.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>classmethod</kbd> `ServerError.from_response`

```python
from_response(response)
```

Create an API error from an HTTP response.


**Args:**

- <b>`response`</b> (requests.Response): HTTP response object.


**Returns:**

- <b>`APIError`</b>: Initialised API error.



