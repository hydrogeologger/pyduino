"""Internal HTTP transport implementation.

Provides helpers and abstractions for sending HTTP requests and handling
HTTP communication details.
"""

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3.exceptions import (
    ConnectTimeoutError,
    MaxRetryError,
    ReadTimeoutError,
)
from urllib3.util.retry import Retry

from .exceptions import (
    TransportConnectionError,
    TransportSSLError,
    TransportConnectTimeoutError,
    TransportReadTimeoutError,
)


class _HTTPTransport:
    """HTTP transport layer for executing API requests."""
    DEFAULT_TIMEOUT = (5, 30)  # type: tuple[int, int]
    """Default request timeout, (connect timeout, read timeout)."""

    def __init__(self):
        """Initialise the HTTP transport."""
        self._session = self._create_session()  # type: requests.Session

    def _create_session(self):
        # type: (...) -> requests.Session
        """Create and configure the HTTP session.

        Returns:
            requests.Session: Configured requests session.
        """
        session = requests.Session()

        retry = Retry(
            total=3,
            read=False,  # False: Stops retries on ReadTimeout, True: Allows retries
            backoff_factor=1,
            status_forcelist=[
                429,  # Too many requests
                500,  # Internal Server Error
                502,  # Bad Gateway
                503,  # Service Unavailable
                504,  # Gateway Timeout
            ],
            allowed_methods=[
                "GET",
                "PUT",
                "DELETE",
                "HEAD",
                "OPTIONS",
            ],
            respect_retry_after_header=True,
        )

        adapter = HTTPAdapter(
            max_retries=retry,
            pool_connections=10,
            pool_maxsize=10,
        )

        session.mount("http://", adapter)
        session.mount("https://", adapter)

        session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        return session

    def request(self, method, url,
                params=None,
                headers=None,
                json=None,
                timeout=DEFAULT_TIMEOUT,
                **kwargs):  # pylint: disable-next=line-too-long
        # type: (str, str, dict|bytes|None, dict|None, dict|None, int|float|tuple|None, **object) -> Response
        """Execute an HTTP request.

        Args:
            method (str): HTTP method to execute, such as GET, POST, PUT, or DELETE.
            url (str): Fully qualified URL to send the request to.
            params (dict | bytes, optional): Query string parameters.
            headers (dict, optional): Additional HTTP headers.
                Note:
                    Headers may be modified or overridden by higher-level
                    API clients. Authentication headers managed by Account
                    should not be replaced manually.
            json (dict, optional): JSON serialisable request body.
            timeout (int | float | tuple[float, float], optional):
                Request timeout. A single float specifies the total timeout
                value. A tuple specifies (connect timeout, read timeout).
                Defaults to set `DEFAULT_TIMEOUT`.
            kwargs (dict): Optional arguments supported by requests.Session.request.

                Supported keyword arguments include:
                - data (dict, bytes, str): Request body data.
                - cookies (dict): Cookies to send with the request.
                - files (dict): Dictionary of ``'filename': file-like-objects``
                    for multipart encoding upload.
                - auth (tuple, callable): Authentication handler.
                - allow_redirects (bool): Whether redirects should be followed.
                - proxies (dict): Proxy configuration.
                - verify (bool, str): SSL certificate verification option.
                - stream (bool): Whether to stream the response.
                - cert (str, tuple): Client certificate configuration.

        Returns:
            requests.Response: HTTP response object.

        Raises:
            requests.HTTPError: Raised when the HTTP response status indicates failure.
            requests.RequestException: Raised when the HTTP request fails.
        """
        if (
            timeout is None
            or (isinstance(timeout, (int, float)) and timeout <= 0)
            or (isinstance(timeout, tuple) and any(t <= 0 for t in timeout))
        ):
            timeout = self.DEFAULT_TIMEOUT

        try:
            return self._session.request(
                method, url,
                params=params,
                headers=headers,
                json=json,
                timeout=timeout,
                **kwargs
            )

        except (requests.exceptions.ConnectTimeout, ConnectTimeoutError) as ex:
            raise TransportConnectTimeoutError("Connection timed out.") from ex
        except (requests.exceptions.ReadTimeout, ReadTimeoutError) as ex:
            raise TransportReadTimeoutError("Request read timed out.") from ex

        except requests.exceptions.SSLError as ex:
            raise TransportSSLError("SSL verification failed.") from ex

        except requests.exceptions.ConnectionError as ex:
            # Access the urllib3 exception attached to requests.exceptions.ConnectionError
            underlying_err = getattr(ex, 'reason', None)

            if isinstance(underlying_err, MaxRetryError):
                # Dig into what caused the MaxRetryError to exhaust
                root_cause = underlying_err.reason

                # Check explicitly for connection setup timeouts
                if isinstance(root_cause, ConnectTimeoutError):
                    raise TransportConnectTimeoutError(
                        "Connection timed out after exhausting retry attempts.") from ex
                # Check explicitly for read/data stream timeouts
                if isinstance(root_cause, ReadTimeoutError):
                    raise TransportReadTimeoutError(
                        "Request Read timed out after exhausting retry attempts.") from ex

            # Fallback string check for older urllib3 architectures
            # (For unique OS/socket-level edge cases)
            error_msg = str(ex).lower()
            if "connect timeout" in error_msg or "connection timed out" in error_msg:
                raise TransportConnectTimeoutError(
                    "Connection timed out during handshake.") from ex
            if "read timeout" in error_msg or "time out reading" in error_msg:
                raise TransportReadTimeoutError(
                    "Read timed out mid-stream.") from ex

            # Genuine structural connection drop (e.g., ConnectionRefused, DNS resolution fail)
            raise TransportConnectionError(
                "Unable to connect to the server.") from ex

    def close(self):
        # type: () -> None
        """Close the HTTP session."""
        self._session.close()
