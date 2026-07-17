"""Exception handling utilities for thingsboard_api.

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
"""
import os
import sys
import threading
import traceback
import types

from .exceptions import ThingsBoardAPIError

# Python2/3 Compatibility
# pylint: disable=consider-using-f-string


class _ExceptionHandler(object):
    """Manages friendly exception handling for thingsboard_api."""

    def __init__(self):
        """Initialize the exception handler."""
        self._installed = False
        self._previous_sys_hook = None
        self._previous_threading_excepthook = None
        # Get the absolute normalized path of the package root
        self._package_root = os.path.abspath(os.path.dirname(__file__))

    def install(self):
        """Install the exception handler.

        Uncaught ``ThingsBoardAPIError`` exceptions are displayed without internal
        package tracebacks. Other exceptions are passed to the previously installed
        exception handler.
        """
        if self._installed:
            return

        self._previous_sys_hook = sys.excepthook
        sys.excepthook = self._sys_exception_hook

        # threading.excepthook was added in Python 3.8.
        if hasattr(threading, "excepthook"):
            self._previous_threading_excepthook = threading.excepthook
            threading.excepthook = self._thread_exception_hook

        self._installed = True

    def uninstall(self):
        """Restore the previous exception handlers."""
        if not self._installed:
            return

        sys.excepthook = self._previous_sys_hook

        if self._previous_threading_excepthook is not None:
            threading.excepthook = self._previous_threading_excepthook

        self._installed = False

    def _filter_traceback(self, exc_traceback):  # pylint: disable-next=line-too-long
        # type: (types.TracebackType) -> types.TracebackType|traceback.StackSummary|list[traceback.FrameSummary]
        """Removes traceback frames originating from this package.

        Checks if types.TracebackType can be instantiated at runtime (Python 3.7+).
        If it cannot, it falls back to a structural list-filtering mechanism.

        Args:
            exc_traceback (traceback): The original exception traceback object 
                to filter.

        Returns:
            types.TracebackType or list: A reconstructed, filtered TracebackType 
                object for modern Python, or a list of filtered frame tuples for 
                legacy environments.
        """
        # 1. Check if types.TracebackType supports instantiation
        can_instantiate_tb = False
        try:
            types.TracebackType(None, None, None, None)
            can_instantiate_tb = True
        except TypeError:
            pass

        # --- MODERN APPROACH (Python 3.7+) ---
        if can_instantiate_tb:
            original_traceback = exc_traceback
            frames = []
            while exc_traceback:
                frame = exc_traceback.tb_frame
                filepath = os.path.abspath(frame.f_code.co_filename)

                if not filepath.startswith(self._package_root + os.sep):
                    frames.append(exc_traceback)

                exc_traceback = exc_traceback.tb_next

            if not frames:
                return original_traceback

            filtered_head = None  # type: types.TracebackType
            current_node = None  # type: types.TracebackType

            # Reconstruct the linked list backwards to properly set tb_next attributes
            # using the custom TracebackType instantiation.
            for tb in frames:
                new_segment = types.TracebackType(
                    None,
                    tb.tb_frame,
                    tb.tb_lasti,
                    tb.tb_lineno,
                )
                if filtered_head is None:
                    filtered_head = new_segment
                    current_node = filtered_head
                else:
                    # Leverage standard CPython behavior via descriptor binding
                    current_node.tb_next = new_segment
                    current_node = new_segment
            return filtered_head

        # --- LEGACY FALLBACK APPROACH ---
        else:
            extracted_frames = traceback.extract_tb(exc_traceback)
            filtered_frames = []

            for frame in extracted_frames:
                filepath = os.path.abspath(frame[0])
                if not filepath.startswith(self._package_root + os.sep):
                    filtered_frames.append(frame)

            if not filtered_frames:
                return extracted_frames

            return filtered_frames

    def _format_exception(self, exc_type, exc_value, exc_traceback):
        # type: (type[BaseException], BaseException, types.TracebackType) -> str
        """Format an exception message using the best available strategy."""
        filtered_data = self._filter_traceback(exc_traceback)

        # Check if we successfully built a pure TracebackType object
        if isinstance(filtered_data, types.TracebackType) or filtered_data is None:
            return "".join(
                traceback.format_exception(
                    exc_type,
                    exc_value,
                    filtered_data,
                )
            )
        else:  # Legacy path: custom format structure using raw list extraction
            output_lines = ["Traceback (most recent call last):\n"]
            output_lines.extend(traceback.format_list(filtered_data))
            output_lines.extend(
                traceback.format_exception_only(exc_type, exc_value))
            return "".join(output_lines)

    def _sys_exception_hook(self, exc_type, exc_value, exc_traceback):
        # type: (type[BaseException], BaseException, types.TracebackType) -> None
        """Handle uncaught exceptions in the main thread."""
        if issubclass(exc_type, ThingsBoardAPIError):
            sys.stderr.write(
                self._format_exception(
                    exc_type,
                    exc_value,
                    exc_traceback
                )
            )
            return

        if self._previous_sys_hook:
            self._previous_sys_hook(
                exc_type,
                exc_value,
                exc_traceback
            )

    def _thread_exception_hook(self, args):
        # type: (object) -> None
        """Handle uncaught exceptions in worker threads."""
        if issubclass(args.exc_type, ThingsBoardAPIError):
            sys.stderr.write(
                self._format_exception(
                    args.exc_type,
                    args.exc_value,
                    args.exc_traceback
                )
            )
        elif self._previous_threading_excepthook is not None:
            self._previous_threading_excepthook(args)


_exception_handler = _ExceptionHandler()


def enable_friendly_exceptions():
    # type: () -> None
    """Enable friendly ThingsBoard API exception output."""
    _exception_handler.install()


def disable_friendly_exceptions():
    # type: () -> None
    """Disable friendly ThingsBoard API exception output."""
    _exception_handler.uninstall()
