# tests/test_error_handler.py
# pylint: disable=protected-access, missing-function-docstring, missing-module-docstring

import os
import sys
import threading
import traceback
import types

import pytest

from thingsboard_api.error_handler import _ExceptionHandler
from thingsboard_api.exceptions import ThingsBoardAPIError


class MockLegacyExceptionHandler(_ExceptionHandler):
    """Subclass that safely mimics the legacy Python 3.5 structure under modern Python versions."""
    
    def _filter_traceback(self, exc_traceback):
        extracted_frames = traceback.extract_tb(exc_traceback)
        filtered_frames = []

        for frame in extracted_frames:
            # Check safely to support both 3.5 tuples and 3.10 FrameSummary
            if hasattr(frame, "filename"):
                raw_filename = frame.filename
            else:
                raw_filename = frame

            filepath = os.path.abspath(raw_filename) 
            if not filepath.startswith(self._package_root + os.sep):
                filtered_frames.append(frame)

        if not filtered_frames:
            return extracted_frames

        return filtered_frames


def raise_thingsboard_error():
    raise ThingsBoardAPIError("device not found")


# --- FIXED DISCOVERY: SPLIT PARAMETERIZED FUNCTION INTO TWO FLAT TESTS ---

def test_format_exception_filtering_modern():
    """Verifies exception formatting via standard/modern code paths."""
    handler = _ExceptionHandler()
    if not getattr(handler, "_package_root", None):
        handler._package_root = os.path.dirname(os.path.abspath(__file__))

    message = None
    try:
        raise_thingsboard_error()
    except ThingsBoardAPIError:
        exc_type, exc_value, exc_tb = sys.exc_info()
        message = handler._format_exception(exc_type, exc_value, exc_tb)

    assert "ThingsBoardAPIError: device not found" in message
    assert "Traceback (most recent call last):" in message
    assert "test_error_handler.py" in message
    assert "raise_thingsboard_error" in message


def test_format_exception_filtering_legacy():
    """Verifies exception formatting explicitly forcing the legacy fallback code paths."""
    handler = MockLegacyExceptionHandler()
    if not getattr(handler, "_package_root", None):
        handler._package_root = os.path.dirname(os.path.abspath(__file__))

    message = None
    try:
        raise_thingsboard_error()
    except ThingsBoardAPIError:
        exc_type, exc_value, exc_tb = sys.exc_info()
        message = handler._format_exception(exc_type, exc_value, exc_tb)

    assert "ThingsBoardAPIError: device not found" in message
    assert "Traceback (most recent call last):" in message
    assert "test_error_handler.py" in message
    assert "raise_thingsboard_error" in message


def test_sys_hook_suppresses_traceback_when_fully_filtered(capsys):
    """Verifies fallback behavior if filtering strips away all traceable frames."""
    handler = _ExceptionHandler()
    handler._package_root = os.path.dirname(os.path.abspath(__file__))

    try:
        raise_thingsboard_error()
    except ThingsBoardAPIError:
        handler._sys_exception_hook(*sys.exc_info())

    captured = capsys.readouterr()
    assert "ThingsBoardAPIError: device not found" in captured.err
    assert "Traceback (most recent call last)" in captured.err


def test_sys_hook_delegates_unknown_exception():
    """Verifies fallback hooks trigger properly for unrelated script exceptions."""
    handler = _ExceptionHandler()
    called = {}

    def fake_previous_hook(exc_type, exc_value, _):
        called["type"] = exc_type
        called["value"] = exc_value

    handler._previous_sys_hook = fake_previous_hook
    error = ValueError("bad value")

    try:
        raise error
    except ValueError:
        exc_type, exc_value, exc_tb = sys.exc_info()
        handler._sys_exception_hook(exc_type, exc_value, exc_tb)

    assert called["type"] is ValueError
    assert str(called["value"]) == "bad value"


def test_install_and_uninstall():
    """Confirms installation correctly binds boundaries over system hook parameters."""
    handler = _ExceptionHandler()
    original_hook = sys.excepthook

    try:
        handler.install()
        assert handler._installed is True
        
        if hasattr(sys.excepthook, "__self__"):
            assert sys.excepthook.__self__ is handler
            assert sys.excepthook.__func__ is handler._sys_exception_hook.__func__
        else:
            assert sys.excepthook.__code__ == handler._sys_exception_hook.__code__

        handler.uninstall()
        assert handler._installed is False
        assert sys.excepthook == original_hook
    finally:
        handler.uninstall()


@pytest.mark.skipif(
    "not hasattr(sys.modules['threading'], 'excepthook')",
    reason="threading.excepthook unavailable before Python 3.8",
)
def test_thread_hook_suppresses_thingsboard_error(capsys):
    """Verifies thread hook exceptions filter framework directories correctly."""
    handler = _ExceptionHandler()
    error = ThingsBoardAPIError("thread failed")

    try:
        raise error
    except ThingsBoardAPIError:
        exc_type, exc_value, exc_tb = sys.exc_info()
        
        args = types.SimpleNamespace()
        args.exc_type = exc_type
        args.exc_value = exc_value
        args.exc_traceback = exc_tb
        
        handler._thread_exception_hook(args)

    captured = capsys.readouterr()
    assert "ThingsBoardAPIError: thread failed" in captured.err
    assert "Traceback" in captured.err
