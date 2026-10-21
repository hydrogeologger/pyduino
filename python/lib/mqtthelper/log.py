"""Logging configuration for the package.

This module provides the internal logging configuration used by this library.
Applications can configure or disable the library's default output through
the public functions exposed by the package.
"""

import logging
import sys
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TextIO

# Safely get the top-level package logger name to avoid root logger pollution
_package_logger = logging.getLogger(__package__ or __name__.split(".", 1)[0])

# Add a NullHandler by default to prevent "No handlers found" warnings
# when the library is used without explicit configuration.
_package_logger.addHandler(logging.NullHandler())

# Thread lock for safe concurrent configuration changes
_lock = threading.Lock()

# pylint: disable-next=invalid-name
_output_handler = None  # type: logging.Handler|None


def configure(level=logging.INFO, stream=None, propagate=False):
    # type: (int|str, TextIO|None, bool) -> None
    """Configure the default logging behavior and stream for the library.

    This function attaches a default stream handler to the package logger,
    sets its verbosity level, and configures event propagation. Subsequent
    calls can update the level or propagation preference safely.

    Args:
        level (int or str, optional): The logging level threshold (e.g., 
            ``logging.DEBUG``, ``"INFO"``). Defaults to ``logging.INFO``.
        stream (TextIO, optional): The text stream to write log output to 
            (e.g., ``sys.stdout``, a file object, or a string stream). 
            Defaults to ``None``, which automatically targets ``sys.stderr``.
        propagate (bool, optional): Whether to allow log events to bubble up 
            to parent or root loggers. Defaults to ``False`` to prevent 
            duplicate console output.
    """
    global _output_handler

    with _lock:
        if _output_handler is None:
            # Remove the NullHandler once a real output handler is attached
            for handler in _package_logger.handlers[:]:
                if isinstance(handler, logging.NullHandler):
                    _package_logger.removeHandler(handler)

            _output_handler = logging.StreamHandler(
                stream if stream is not None else sys.stderr
            )
            _output_handler.setLevel(logging.NOTSET)  # Transparent pipe

            _package_logger.addHandler(_output_handler)
            _package_logger.setLevel(level)
        else:
            # Check the local logger level (not effective level, to avoid inheritance bugs)
            current_level = _package_logger.level

            # If not explicitly set (NOTSET = 0) or requested level is more detailed
            if current_level == logging.NOTSET or level < current_level:
                _package_logger.setLevel(level)

        # Always ensure propagation matches the latest call request
        _package_logger.propagate = propagate


def disable():
    # type: () -> None
    """Disable the default output handler for the library.

    Removes the output handler installed by :func:`configure`.
    Other handlers configured by the application are not affected.
    """
    global _output_handler

    with _lock:
        if _output_handler is None:
            return

        _package_logger.removeHandler(_output_handler)
        _output_handler.close()
        _output_handler = None

        # Restore NullHandler to prevent warnings if output is completely disabled
        if not any(isinstance(h, logging.NullHandler) for h in _package_logger.handlers):
            _package_logger.addHandler(logging.NullHandler())


def get_logger():
    # type: () -> logging.Logger
    """Return the primary package logger.

    Returns:
        logging.Logger: The top-level :class:`logging.Logger` instance for this library.
    """
    return _package_logger


def get_level():
    # type: () -> int
    """Return the current logging level of the package logger.

    Returns:
        int: The current logging level integer (e.g., ``logging.DEBUG``, ``logging.INFO``).
    """
    return _package_logger.level


def set_level(level):
    # type: (int|str) -> None
    """Directly set the logging level for the package.

    Args:
        level (int or str): The new logging level (e.g., ``logging.DEBUG``, ``logging.WARNING``).
    """
    _package_logger.setLevel(level)
