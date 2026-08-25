"""Tests for the SILO ``get_nearby_stations`` function.

HTTP requests are mocked so that the tests do not make network requests
to the SILO API.
"""

# pylint: disable=redefined-outer-name

from unittest.mock import Mock

import pytest
import requests

from postprocess.sources import silo
# for patching
from postprocess.sources.silo import (
    _requests,
)


@pytest.fixture
def mocked_get(monkeypatch, mocked_response):
    """Mock the SILO HTTP GET request."""
    response = Mock(return_value=mocked_response)
    monkeypatch.setattr(
        _requests,
        "get",
        response
    )
    return response

def test_empty_response_returns_empty_list(mocked_get):
    """Return an empty list when no stations are returned."""
    mocked_get.return_value.text = ""

    assert silo.get_nearby_stations(15526) == []


def test_returns_nearby_stations(mocked_get):
    """Parse nearby station records from the SILO response."""
    mocked_get.return_value.text = (
        "\n"
        "Number|Station name|Latitude|Longitud|Stat|Elevat.|Distance (km)\n"
        "\n"
        "15526|FINKE POST OFFICE|-25.5833|134.5667|NT|267.0|0.0\n"
        "15527|ANOTHER STATION|-25.6000|134.5000|NT|300.0|5.2\n"
    )

    result = silo.get_nearby_stations(15526)

    assert result == [
        silo.SILOStationRecord(
            station_id=15526,
            name="FINKE POST OFFICE",
            latitude=-25.5833,
            longitude=134.5667,
            state="NT",
            elevation_m=267.0,
            distance_km=0.0
        ),
        silo.SILOStationRecord(
            station_id=15527,
            name="ANOTHER STATION",
            latitude=-25.6,
            longitude=134.5,
            state="NT",
            elevation_m=300.0,
            distance_km=5.2
        ),

    ]


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
        radius_km=100,
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
            radius_km=radius,
        )


@pytest.mark.parametrize(
    "response_text",
    [
        "15526|FINKE POST OFFICE|-25.5833|134.5667|NT|267.0\n",
        "15526|FINKE POST OFFICE|-25.5833|134.5667|NT|267.0|0.0|extra\n",
    ],
)
def test_invalid_response_format_raises_value_error(
    mocked_get,
    response_text,
):
    """Raise ValueError when a station record has the wrong number of fields."""
    mocked_get.return_value.text = response_text

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
    mocked_get,
    response_text,
):
    """Raise ValueError when station fields cannot be converted."""
    mocked_get.return_value.text = response_text

    with pytest.raises(
        ValueError,
        match="Invalid SILO station response",
    ):
        silo.get_nearby_stations(15526)


def test_http_error_is_propagated(mocked_get):
    """Propagate HTTP errors from the SILO API."""
    error = requests.HTTPError("500 Server Error")
    mocked_get.return_value.raise_for_status.side_effect = error

    with pytest.raises(requests.HTTPError, match="500 Server Error"):
        silo.get_nearby_stations(15526)

    mocked_get.return_value.raise_for_status.assert_called_once_with()
