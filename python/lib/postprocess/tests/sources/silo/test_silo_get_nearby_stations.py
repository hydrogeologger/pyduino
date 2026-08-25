"""Tests for the SILO ``get_nearby_stations`` function.

HTTP requests are mocked so that the tests do not make network requests
to the SILO API.
"""

# pylint: disable=redefined-outer-name

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


def test_returns_nearby_stations(mocked_response):
    """Parse nearby station records from the SILO response."""
    mocked_response.text = (
        "\n"
        "Number|Station name|Latitude|Longitud|Stat|Elevat.|Distance (km)\n"
        "\n"
        "15526|FINKE POST OFFICE|-25.5833|134.5667|NT|267.0|0.0\n"
        "15527|ANOTHER STATION|-25.6000|134.5000|NT|300.0|5.2\n"
    )

    result = silo.get_nearby_stations(15526)

    assert result == [
        {
            "number": 15526,
            "name": "FINKE POST OFFICE",
            "latitude": -25.5833,
            "longitude": 134.5667,
            "elevation": 267.0,
            "state": "NT",
            "distance_km": 0.0,
        },
        {
            "number": 15527,
            "name": "ANOTHER STATION",
            "latitude": -25.6,
            "longitude": 134.5,
            "elevation": 300.0,
            "state": "NT",
            "distance_km": 5.2,
        },
    ]


def test_empty_response_returns_empty_list(mocked_response):
    """Return an empty list when no stations are returned."""
    mocked_response.text = ""

    assert silo.get_nearby_stations(15526) == []


@pytest.mark.parametrize(
    ("sortby", "expected_params"),
    [
        (
            None,
            {
                "format": "near",
                "station": 15526,
                "radius": 100,
            },
        ),
        (
            "name",
            {
                "format": "near",
                "station": 15526,
                "radius": 100,
                "sortby": "name",
            },
        ),
    ],
)
def test_request_parameters(mocked_get, sortby, expected_params):
    """Send the expected parameters to the SILO API."""
    silo.get_nearby_stations(
        station_id=15526,
        radius=100,
        sortby=sortby,
    )

    mocked_get.assert_called_once_with(
        "https://www.longpaddock.qld.gov.au/cgi-bin/silo/"
        "PatchedPointDataset.php",
        params=expected_params,
        headers={"Accept": "text/plain"},
        timeout=(5, 30),
    )


@pytest.mark.parametrize(
    "timeout",
    [
        10,
        (2, 60),
    ],
)
def test_custom_timeout(mocked_get, timeout):
    """Pass a custom timeout to the request."""
    silo.get_nearby_stations(
        station_id=15526,
        timeout=timeout,
    )

    assert mocked_get.call_args.kwargs["timeout"] == timeout


@pytest.mark.parametrize("radius", [0, -1, -100])
def test_invalid_radius_raises_value_error(radius):
    """Raise ValueError when radius is not positive."""
    with pytest.raises(ValueError, match="radius must be greater than zero"):
        silo.get_nearby_stations(
            station_id=15526,
            radius=radius,
        )


@pytest.mark.parametrize(
    "response_text",
    [
        "15526|FINKE POST OFFICE|-25.5833|134.5667|NT|267.0\n",
        "15526|FINKE POST OFFICE|-25.5833|134.5667|NT|267.0|0.0|extra\n",
    ],
)
def test_invalid_response_format_raises_value_error(
    mocked_response,
    response_text,
):
    """Raise ValueError when a station record has the wrong number of fields."""
    mocked_response.text = response_text

    with pytest.raises(
        ValueError,
        match="Unexpected SILO station response",
    ):
        silo.get_nearby_stations(15526)


@pytest.mark.parametrize(
    "response_text",
    [
        "not-a-number|FINKE POST OFFICE|-25.5833|134.5667|NT|267.0|0.0\n",
        "15526|FINKE POST OFFICE|not-a-latitude|134.5667|NT|267.0|0.0\n",
        "15526|FINKE POST OFFICE|-25.5833|not-a-longitude|NT|267.0|0.0\n",
        "15526|FINKE POST OFFICE|-25.5833|134.5667|NT|not-an-elevation|0.0\n",
        "15526|FINKE POST OFFICE|-25.5833|134.5667|NT|267.0|not-a-distance\n",
    ],
)
def test_invalid_station_data_raises_value_error(
    mocked_response,
    response_text,
):
    """Raise ValueError when station fields cannot be converted."""
    mocked_response.text = response_text

    with pytest.raises(
        ValueError,
        match="Invalid SILO station response",
    ):
        silo.get_nearby_stations(15526)


def test_http_error_is_propagated(mocked_response):
    """Propagate HTTP errors from the SILO API."""
    error = requests.HTTPError("500 Server Error")
    mocked_response.raise_for_status.side_effect = error

    with pytest.raises(requests.HTTPError, match="500 Server Error"):
        silo.get_nearby_stations(15526)

    mocked_response.raise_for_status.assert_called_once_with()
