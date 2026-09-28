"""Tests for :meth"`StationFinder.find_matching_locations`."""

from unittest.mock import Mock

import pytest

from postprocess.sources.bom.cdio import _random  # Monkeypatch and Mocking
from postprocess.sources.bom.cdio import _requests  # Monkeypatch and Mocking
from postprocess.sources.bom.cdio import (
    StationFinder,
)

# pylint: disable=redefined-outer-name


@pytest.fixture
def mock_get(monkeypatch):
    """Mock get requests"""
    get_mock = Mock()
    monkeypatch.setattr(_requests, "get", get_mock)
    return get_mock


@pytest.mark.parametrize(
    "response_text, expected_locations",
    [
        (
            "Melbourne, VIC, 37.84°S, 144.98°E",
            [
                ("Melbourne", "VIC", -37.84, 144.98),
            ],
        ),
        (
            (
                "Melbourne, VIC, 37.84°S, 144.98°E||"
                "Brisbane, QLD, 27.47°S, 153.03°E"
            ),
            [
                ("Melbourne", "VIC", -37.84, 144.98),
                ("Brisbane", "QLD", -27.47, 153.03),
            ],
        ),
    ],
)
def test_returns_matching_locations(
    mock_get,
    response_text,
    expected_locations,
):
    """Return locations parsed from the BOM gazetteer response."""
    response = Mock(
        status_code=200,
        text=response_text,
    )
    response.raise_for_status.return_value = None
    mock_get.return_value = response

    locations = StationFinder.find_matching_locations("Melbourne")

    assert len(locations) == len(expected_locations)

    for location, expected in zip(locations, expected_locations):
        name, state, latitude, longitude = expected

        assert location.name == name
        assert location.state == state
        assert location.latitude == pytest.approx(latitude)
        assert location.longitude == pytest.approx(longitude)


@pytest.mark.parametrize(
    "response_text",
    [
        "Empty resultset",
        "<!DOCTYPE html><html></html>",
    ],
)
def test_returns_empty_list_when_no_locations_match(
    mock_get,
    response_text,
):
    """Return an empty list when no locations are found."""
    response = Mock(
        status_code=200,
        text=response_text,
    )
    response.raise_for_status.return_value = None
    mock_get.return_value = response

    result = StationFinder.find_matching_locations("Unknown")

    assert result == []


def test_sends_expected_request(monkeypatch, mock_get):
    """Send the expected request to the BOM gazetteer."""
    response = Mock(
        status_code=200,
        text="Melbourne, VIC, 37.84°S, 144.98°E",
    )
    response.raise_for_status.return_value = None
    mock_get.return_value = response

    monkeypatch.setattr(
        _random,
        "random",
        Mock(return_value=0.123),
    )

    StationFinder.find_matching_locations(
        "Melbourne",
        timeout=(10, 60),
    )

    mock_get.assert_called_once_with(
        url="https://reg.bom.gov.au/jsp/ncc/cdio/weatherData/av",
        params={
            "p_stn_num": 86071,
            "p_display_type": "gazetteer",
            "p_nccObsCode": 139,
            "p_locSearch": "Melbourne",
            "p_state": "ALL",
            "sid": 0.123,
        },
        headers={
            "Accept": "text/html; charset=ISO-8859-1",
        },
        timeout=(10, 60),
    )


def test_propagates_http_error(mock_get):
    """Propagate an exception raised by the HTTP response."""
    response = Mock(
        status_code=500,
        text="Internal Server Error",
    )
    response.raise_for_status.side_effect = RuntimeError("HTTP error")
    mock_get.return_value = response

    with pytest.raises(RuntimeError, match="HTTP error"):
        StationFinder.find_matching_locations("Melbourne")
