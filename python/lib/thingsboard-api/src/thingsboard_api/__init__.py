"""
This package provides modules for thingsboard REST API calls and data extraction.

Dependencies:
- requests : For http POST request
- jwt : JWT decoding
- pandas : pandas dataframe and series
"""

# Module Info
__version__ = "0.1.0"

# Import base modules
from .error_handler import (
    disable_friendly_exceptions,
    enable_friendly_exceptions,
)
from .exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    MethodNotAllowedError,
    NotFoundError,
    PermissionDeniedError,
    PreconditionFailedError,
    RateLimitError,
    ServerError,
)
from .tb_rest_api import *
