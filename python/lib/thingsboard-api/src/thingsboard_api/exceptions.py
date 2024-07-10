"""Exception hierarchy for the thingsboard_api package.

This module defines exceptions raised by the ThingsBoard API client.

The hierarchy separates:
- Transport errors: failures communicating with the server.
- API errors: failures returned by the ThingsBoard API.
"""
import requests as _requests


class ThingsBoardAPIError(Exception):
    """Base exception for all thingsboard_api errors.

    All exceptions raised by the ThingsBoard API client inherit from this
    exception.
    """


class TransportError(ThingsBoardAPIError):
    """Base exception for HTTP transport failures.

    Transport errors occur when the client cannot successfully communicate
    with the ThingsBoard server.
    """


class TransportConnectionError(TransportError):
    """Base exception raised when a connection to the server cannot be established."""


class TransportTimeoutError(TransportError):
    """Raised when an HTTP request exceeds a configured connection or read timeout."""


class TransportConnectTimeoutError(TransportConnectionError, TransportTimeoutError):
    """Raised when the initial TCP handshake/connection setup to the server times out."""


class TransportReadTimeoutError(TransportTimeoutError):
    """Raised when the connection is established but the server fails to send data mid-stream."""


class TransportSSLError(TransportError):
    """Raised when SSL verification or negotiation fails."""


class APIError(ThingsBoardAPIError):
    """Base exception for API response failures.

    Raised when the ThingsBoard server receives the request but returns
    an error response.

    Attributes:
        status_code (int): HTTP response status code.
        message (str): Error message returned by the API.
        error_code (int): ThingsBoard error code.
        timestamp (str): Timestamp returned by the API.
        payload (dict): Parsed API error response payload.
        response (requests.Response): Original HTTP response object.
    """

    def __init__(
        self,
        status_code,
        message,
        error_code=None,
        timestamp=None,
        payload=None,
        response=None,
    ):
        # type: (int, str, int, str, dict, _requests.Response) -> None
        """Initialise an API error.

        Args:
            status_code (int): HTTP response status code.
            message (str): Error message.
            error_code (int): ThingsBoard error code.
            timestamp (str): Timestamp returned by the API.
            response (requests.Response): Original HTTP response object.
        """
        super(APIError, self).__init__(message)

        self.status_code = status_code          # type: int
        self.message = message                  # type: str
        self.error_code = error_code            # type: int
        self.timestamp = timestamp              # type: str
        self.payload = payload                  # type: dict
        self.response = response                # type: _requests.Response

    @classmethod
    def from_response(cls, response):
        # type: (_requests.Response) -> APIError
        """Create an API error from an HTTP response.

        Args:
            response (requests.Response): HTTP response object.

        Returns:
            APIError: Initialised API error.
        """
        payload = {}

        try:
            payload.update(response.json())
        except ValueError:
            pass

        message = payload.get("message") or response.text or response.reason
        error_code = payload.get("errorCode", None)
        timestamp = payload.get("timestamp", None)

        return cls(
            status_code=response.status_code,
            message=message,
            error_code=error_code,
            timestamp=timestamp,
            payload=payload,
            response=response,
        )


class BadRequestError(APIError):
    """Raised when the API rejects a malformed request.

    Corresponds to HTTP status code 400.
    """


class AuthenticationError(APIError):
    """Raised when authentication fails.

    Corresponds to HTTP status code 401.
    """


class PermissionDeniedError(APIError):
    """Raised when the authenticated user lacks permission.

    Corresponds to HTTP status code 403.
    """


class NotFoundError(APIError):
    """Raised when the requested resource does not exist.

    Corresponds to HTTP status code 404.
    """


class MethodNotAllowedError(APIError):
    """Raised when the requested HTTP method is not supported.

    Corresponds to HTTP status code 405.
    """


class ConflictError(APIError):
    """Raised when the request conflicts with the current resource state.

    Corresponds to HTTP status code 409.
    """


class PreconditionFailedError(APIError):
    """Raised when a request precondition is not satisfied.

    Corresponds to HTTP status code 412.
    """


class RateLimitError(APIError):
    """Raised when the API rate limit has been exceeded.

    Corresponds to HTTP status code 429.
    """


class ServerError(APIError):
    """Raised when the ThingsBoard server reports an internal failure.

    Corresponds to HTTP status codes 500-599.
    """
