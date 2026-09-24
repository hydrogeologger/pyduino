"""Shared test fixtures."""

# pylint: disable=redefined-outer-name

from unittest.mock import Mock

import pytest


@pytest.fixture
def mocked_response():
    """Return a generic mocked HTTP response."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {}
    response.text = ""
    return response
