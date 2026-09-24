"""Tests for the Open-Meteo ``get_historical`` function.

HTTP requests are mocked so that the tests do not make network requests
to the Open-Meteo API.
"""

# pylint: disable=redefined-outer-name

from datetime import date
from unittest.mock import Mock

import pytest
import requests

from postprocess.sources import openmeteo


REQUESTS_GET = "postprocess.sources.openmeteo._requests.get"


@pytest.fixture(autouse=True)
def mocked_get(monkeypatch, mocked_response):
    """Mock the Open-Meteo HTTP GET request."""
    get = Mock(return_value=mocked_response)
    monkeypatch.setattr(REQUESTS_GET, get)
    return get


def test_single_coordinate_with_date_objects(mocked_get, mocked_response):
    """Return API JSON for a single coordinate using date objects."""
    mocked_response.json.return_value = {"foo": "bar"}

    result = openmeteo.get_historical(
        coordinates=(-27.4705, 153.0260),
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 2),
    )

    assert result == {"foo": "bar"}

    mocked_get.assert_called_once_with(
        url="https://archive-api.open-meteo.com/v1/archive",
        params={
            "start_date": "2024-01-01",
            "end_date": "2024-01-02",
            "latitude": -27.4705,
            "longitude": 153.026,
        },
        headers={"Accept": "application/json"},
        timeout=(5, 30),
    )

    mocked_response.raise_for_status.assert_called_once_with()


def test_single_coordinate_with_string_dates(mocked_get):
    """Accept ISO-formatted date strings."""
    result = openmeteo.get_historical(
        coordinates=(-27.47, 153.02),
        start_date="2024-01-01",
        end_date="2024-01-31",
    )

    assert result == {}

    params = mocked_get.call_args.kwargs["params"]

    assert params["start_date"] == "2024-01-01"
    assert params["end_date"] == "2024-01-31"
    assert params["latitude"] == -27.47
    assert params["longitude"] == 153.02


def test_multiple_coordinates(mocked_get):
    """Encode multiple coordinates as comma-separated API parameters."""
    coordinates = [
        (-27.47, 153.02),
        (-33.87, 151.21),
    ]

    openmeteo.get_historical(
        coordinates=coordinates,
        start_date="2024-01-01",
        end_date="2024-01-02",
    )

    params = mocked_get.call_args.kwargs["params"]

    assert params["latitude"] == "-27.47,-33.87"
    assert params["longitude"] == "153.02,151.21"


@pytest.mark.parametrize(
    ("hourly", "daily", "expected_hourly", "expected_daily"),
    [
        (
            ["temperature_2m", "precipitation"],
            ["temperature_2m_max", "temperature_2m_min"],
            "temperature_2m,precipitation",
            "temperature_2m_max,temperature_2m_min",
        ),
        (
            "temperature_2m,precipitation",
            "temperature_2m_max",
            "temperature_2m,precipitation",
            "temperature_2m_max",
        ),
    ],
)
def test_hourly_and_daily_variables(
    mocked_get,
    hourly,
    daily,
    expected_hourly,
    expected_daily,
):
    """Accept hourly and daily variables as lists or strings."""
    openmeteo.get_historical(
        coordinates=(-27.47, 153.02),
        start_date="2024-01-01",
        end_date="2024-01-02",
        hourly=hourly,
        daily=daily,
    )

    params = mocked_get.call_args.kwargs["params"]

    assert params["hourly"] == expected_hourly
    assert params["daily"] == expected_daily


def test_timezone_is_added(mocked_get):
    """Include the requested timezone in the API parameters."""
    openmeteo.get_historical(
        coordinates=(-27.47, 153.02),
        start_date="2024-01-01",
        end_date="2024-01-02",
        tz="Australia/Brisbane",
    )

    params = mocked_get.call_args.kwargs["params"]

    assert params["timezone"] == "Australia/Brisbane"


@pytest.mark.parametrize("settings", [None, {}])
def test_empty_settings_use_api_defaults(mocked_get, settings):
    """Do not send settings when settings is None or an empty dictionary."""
    openmeteo.get_historical(
        coordinates=(-27.47, 153.02),
        start_date="2024-01-01",
        end_date="2024-01-02",
        settings=settings,
    )

    params = mocked_get.call_args.kwargs["params"]

    assert "temperature_unit" not in params
    assert "wind_speed_unit" not in params
    assert "precipitation_unit" not in params
    assert "timeformat" not in params


def test_partial_settings_use_defaults(mocked_get):
    """Use defaults for settings that are not explicitly supplied."""
    openmeteo.get_historical(
        coordinates=(-27.47, 153.02),
        start_date="2024-01-01",
        end_date="2024-01-02",
        settings={
            "temperature_unit": "fahrenheit",
        },
    )

    params = mocked_get.call_args.kwargs["params"]

    assert params["temperature_unit"] == "fahrenheit"
    assert params["wind_speed_unit"] == "kmh"
    assert params["precipitation_unit"] == "mm"
    assert params["timeformat"] == "iso8601"


def test_custom_settings(mocked_get):
    """Pass custom API settings through to the request."""
    settings = {
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timeformat": "unixtime",
    }

    openmeteo.get_historical(
        coordinates=(-27.47, 153.02),
        start_date="2024-01-01",
        end_date="2024-01-02",
        settings=settings,
    )

    params = mocked_get.call_args.kwargs["params"]

    assert params["temperature_unit"] == "fahrenheit"
    assert params["wind_speed_unit"] == "mph"
    assert params["precipitation_unit"] == "inch"
    assert params["timeformat"] == "unixtime"


def test_custom_timeout(mocked_get):
    """Pass a custom request timeout to requests.get."""
    openmeteo.get_historical(
        coordinates=(-27.47, 153.02),
        start_date="2024-01-01",
        end_date="2024-01-02",
        timeout=10,
    )

    assert mocked_get.call_args.kwargs["timeout"] == 10


@pytest.mark.parametrize(
    "coordinates",
    [
        "not-a-coordinate",
        123,
    ],
)
def test_invalid_coordinate_type(coordinates):
    """Raise TypeError when coordinates are not a tuple or list."""
    with pytest.raises(TypeError, match="Coordinates must be"):
        openmeteo.get_historical(
            coordinates=coordinates,
            start_date="2024-01-01",
            end_date="2024-01-02",
        )


@pytest.mark.parametrize(
    "coordinates",
    [
        (100, 153.02),
        (-27.47, 200),
        [
            (-27.47, 153.02),
            (100, 153.02),
        ],
    ],
)
def test_invalid_coordinates(coordinates):
    """Raise ValueError when coordinates are outside valid bounds."""
    with pytest.raises(ValueError):
        openmeteo.get_historical(
            coordinates=coordinates,
            start_date="2024-01-01",
            end_date="2024-01-02",
        )


def test_http_error_is_propagated(mocked_response):
    """Propagate HTTP errors raised by the response."""
    error = requests.HTTPError("500 Server Error")
    mocked_response.raise_for_status.side_effect = error

    with pytest.raises(requests.HTTPError, match="500 Server Error"):
        openmeteo.get_historical(
            coordinates=(-27.47, 153.02),
            start_date="2024-01-01",
            end_date="2024-01-02",
        )
