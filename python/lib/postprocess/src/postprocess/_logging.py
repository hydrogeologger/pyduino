"""Logging configuration for the yourlib package.

This module provides the internal logging configuration used by yourlib.
Applications can configure or disable the library's default output through
the public functions exposed by the package.
"""

import logging
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TextIO


_package_logger = logging.getLogger(__package__)
_package_logger.setLevel(logging.INFO)

_output_handler = None  # type: logging.Handler | None


def configure_output(level=logging.INFO, stream=None):
        # type: (int, TextIO | None) -> None
    """Configure the default output handler for yourlib.

    Args:
        level: Logging level to use for the default output handler.
        stream: Text stream to write output to. Defaults to ``sys.stderr``.
    """
    global _output_handler

    if _output_handler is None:
        _output_handler = logging.StreamHandler(
            stream if stream is not None else sys.stderr
        )

        # _output_handler.setFormatter(
        #     logging.Formatter(
        #         "%(levelname)s [%(name)s]: %(message)s"
        #     )
        # )

        _package_logger.addHandler(_output_handler)

    _output_handler.setLevel(level)


def disable_output():
    """Disable the default output handler for yourlib.

    Removes the output handler installed by :func:`configure_output`.
    Other handlers configured by the application are not affected.
    """
    global _output_handler

    if _output_handler is None:
        return

    _package_logger.removeHandler(_output_handler)
    _output_handler.close()
    _output_handler = None
