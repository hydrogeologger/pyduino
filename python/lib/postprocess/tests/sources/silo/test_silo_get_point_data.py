"""Tests for the SILO ``get_point_data`` function.

HTTP requests are mocked so that the tests do not make network requests
to the SILO API.
"""

# pylint: disable=redefined-outer-name

from datetime import date
from unittest.mock import Mock

import pytest
import requests

from postprocess.sources import silo


REQUESTS_GET = "postprocess.sources.silo._requests.get"


@pytest.fixture(autouse=True)
def mocked_get(monkeypatch, mocked_response):
    """Mock the SILO HTTP GET request."""
    get = Mock(return_value=mocked_response)
    monkeypatch.setattr(REQUESTS_GET, get)
    return get


@pytest.mark.parametrize(
    ("location", "expected_url", "location_params"),
    [
        (
            40004,
            "https://www.longpaddock.qld.gov.au/cgi-bin/silo/PatchedPointDataset.php",
            {"station": 40004},
        ),
        (
            (-27.47, 153.02),
            "https://www.longpaddock.qld.gov.au/cgi-bin/silo/DataDrillDataset.php",
            {"lat": -27.45, "lon": 153.0},
        ),
    ],
)
def test_location_type(
    mocked_get,
    mocked_response,
    location,
    expected_url,
    location_params,
):
    """Use the correct SILO endpoint for each location type."""
    mocked_response.json.return_value = {"data": "test"}

    result = silo.get_point_data(
        location=location,
        start="20200101",
        finish="20200131",
    )

    assert result == {"data": "test"}

    mocked_get.assert_called_once_with(
        expected_url,
        params={
            "format": "json",
            "start": "20200101",
            "finish": "20200131",
            "comment": "R",
            "username": "noemail@net.com",
            **location_params,
        },
        headers={"Accept": "application/json"},
        timeout=(5, 30),
    )

    mocked_response.raise_for_status.assert_called_once_with()
    mocked_response.json.assert_called_once_with()


@pytest.mark.parametrize(
    ("start", "finish"),
    [
        (date(2020, 1, 1), date(2020, 1, 31)),
        ("20200101", "20200131"),
    ],
)
def test_date_formats(mocked_get, start, finish):
    """Accept date objects and SILO-formatted date strings."""
    silo.get_point_data(
        location=40004,
        start=start,
        finish=finish,
    )

    params = mocked_get.call_args.kwargs["params"]

    assert params["start"] == "20200101"
    assert params["finish"] == "20200131"


@pytest.mark.parametrize(
    ("comment", "username"),
    [
        ("RXN", "test@example.com"),
        ("R", "another@example.com"),
    ],
)
def test_custom_parameters(mocked_get, comment, username):
    """Pass custom climate variables and username to the API."""
    silo.get_point_data(
        location=40004,
        start="20200101",
        finish="20200131",
        comment=comment,
        username=username,
    )

    params = mocked_get.call_args.kwargs["params"]

    assert params["comment"] == comment
    assert params["username"] == username


@pytest.mark.parametrize(
    "timeout",
    [
        10,
        (2, 60),
    ],
)
def test_custom_timeout(mocked_get, timeout):
    """Pass custom timeout values to requests.get."""
    silo.get_point_data(
        location=40004,
        start="20200101",
        finish="20200131",
        timeout=timeout,
    )

    assert mocked_get.call_args.kwargs["timeout"] == timeout


def test_coordinates_are_rounded(mocked_get):
    """Round coordinates to the nearest 0.05 before sending them."""
    silo.get_point_data(
        location=(-27.473, 153.027),
        start="20200101",
        finish="20200131",
    )

    params = mocked_get.call_args.kwargs["params"]

    assert params["lat"] == -27.45
    assert params["lon"] == 153.05


@pytest.mark.parametrize(
    "location",
    [
        (100.0, 153.02),
        (-27.47, 200.0),
    ],
)
def test_invalid_coordinates(location):
    """Reject coordinates outside valid decimal-degree bounds."""
    with pytest.raises(ValueError):
        silo.get_point_data(
            location=location,
            start="20200101",
            finish="20200131",
        )


def test_http_error_is_propagated(mocked_response):
    """Propagate HTTP errors raised by the response."""
    error = requests.HTTPError("500 Server Error")
    mocked_response.raise_for_status.side_effect = error

    with pytest.raises(requests.HTTPError, match="500 Server Error"):
        silo.get_point_data(
            location=40004,
            start="20200101",
            finish="20200131",
        )

    mocked_response.raise_for_status.assert_called_once_with()
    mocked_response.json.assert_not_called()
