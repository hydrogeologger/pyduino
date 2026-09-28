"""Tests for :meth:`StationFinder.find_nearest_stations`."""

from unittest.mock import Mock

import pytest

from postprocess.sources.bom.cdio import _requests  # Monkeypatch and Mocking
from postprocess.sources.bom.cdio import (
    NCC_OBS_CODES,
    DWOStation,
    Location,
    StationFinder,
)

# pylint: disable=redefined-outer-name


@pytest.fixture
def mock_get(monkeypatch):
    """Mock get requests"""
    get_mock = Mock()
    monkeypatch.setattr(_requests, "get", get_mock)
    return get_mock


@pytest.fixture
def mock_response():
    """Return a successful mocked BOM response."""
    response = Mock(
        status_code=200,
        text=(
            "3015_90035 Colac (Mt Gellibrand) VIC (112.2km away)    "
            "||3103_85301 Yanakie VIC (149.9km away)"
        ),
    )
    response.raise_for_status.return_value = None
    return response


def test_maps_observation_code_202_to_200(
    mock_get,
    mock_response,
):
    """Map observation code 202 to BOM's station-search code 200."""
    mock_get.return_value = mock_response

    StationFinder.find_nearest_stations(
        nccObsCode=202,
        location=(-37.84, 144.98),
    )

    params = mock_get.call_args.kwargs["params"]

    assert params["p_match"].endswith("LATLON,200")


@pytest.mark.usefixtures("mock_get")
@pytest.mark.parametrize(
    "ncc_obs_code",
    sorted(NCC_OBS_CODES.keys()),
)
def test_accepts_valid_observation_codes(ncc_obs_code):
    """Accept every supported BOM observation code."""
    StationFinder.find_nearest_stations(
        nccObsCode=ncc_obs_code, location=(-37.84, 144.98)
    )


@pytest.mark.usefixtures("mock_get")
@pytest.mark.parametrize(
    "ncc_obs_code",
    [
        0,
        1,
        100,
        999,
        -1,
        None,
        "201",
    ],
)
def test_rejects_invalid_observation_codes(ncc_obs_code):
    """Raise ValueError for unsupported observation codes."""
    with pytest.raises(ValueError, match="Invalid `nccObsCode`"):
        StationFinder.find_nearest_stations(
            nccObsCode=ncc_obs_code, location=(-37.84, 144.98)
        )


def test_returns_open_stations_by_default(
    mock_get,
    mock_response,
):
    """Return only open stations by default."""
    mock_get.return_value = mock_response

    stations = StationFinder.find_nearest_stations(
        nccObsCode=201,
        location=(-37.84, 144.98),
    )

    assert stations == [
        DWOStation(
            dwo_id=3015,
            station_id=90035,
            name="Colac (Mt Gellibrand)",
            state="VIC",
            distance_km=112.2,
            is_open=True,
        )
    ]


def test_returns_open_and_closed_stations_when_open_only_disabled(
    mock_get,
    mock_response,
):
    """Return closed stations when open_only is False."""
    mock_get.return_value = mock_response

    stations = StationFinder.find_nearest_stations(
        nccObsCode=201,
        location=(-37.84, 144.98),
        open_only=False,
    )

    assert stations == [
        DWOStation(
            dwo_id=3015,
            station_id=90035,
            name="Colac (Mt Gellibrand)",
            state="VIC",
            distance_km=112.2,
            is_open=True,
        ),
        DWOStation(
            dwo_id=3103,
            station_id=85301,
            name="Yanakie",
            state="VIC",
            distance_km=149.9,
            is_open=False,
        ),
    ]


@pytest.mark.parametrize(
    "location, expected_match",
    [
        (
            (-37.84, 144.98),
            "50,,37.84,144.98,,LATLON,201",
        ),
        (
            90035,
            "50,90035,,,,S_NUM,201",
        ),
        (
            "90035",
            "50,90035,,,,S_NUM,201",
        ),
        (
            Location(
                name="Melbourne",
                state="VIC",
                latitude=-37.84,
                longitude=144.98,
            ),
            "Melbourne,VIC,37.84,144.98,,LATLON,201",
        ),
        (
            "Melbourne,VIC,37.84,144.98",
            "Melbourne,VIC,37.84,144.98,,LATLON,201",
        ),
    ],
)
def test_builds_expected_match_parameter(
    mock_get,
    mock_response,
    location,
    expected_match,
):
    """Build the expected BOM p_match parameter for each location type."""
    mock_get.return_value = mock_response

    StationFinder.find_nearest_stations(nccObsCode=201, location=location)

    params = mock_get.call_args.kwargs["params"]

    assert params["p_match"] == expected_match


def test_converts_southern_latitude_to_positive_bom_value(
    mock_get,
    mock_response,
):
    """Convert signed Southern Hemisphere latitude to BOM's format."""
    mock_get.return_value = mock_response

    StationFinder.find_nearest_stations(
        nccObsCode=201,
        location=(-37.84, 144.98),
    )

    params = mock_get.call_args.kwargs["params"]

    assert params["p_match"] == "50,,37.84,144.98,,LATLON,201"


@pytest.mark.usefixtures("mock_get")
@pytest.mark.parametrize(
    "coordinates, match",
    [
        (
            (1.0, 144.98),
            "Latitude must be in the Southern Hemisphere",
        ),
        (
            (-37.84, -1.0),
            "Longitude must be in the Eastern Hemisphere",
        ),
    ],
)
def test_rejects_coordinates_outside_bom_hemispheres(
    coordinates,
    match,
):
    """Reject coordinates outside BOM's expected hemispheres."""
    with pytest.raises(ValueError, match=match):
        StationFinder.find_nearest_stations(nccObsCode=201, location=coordinates)


@pytest.mark.parametrize(
    "response_text",
    [
        "Empty resultset",
        "<!DOCTYPE html><html></html>",
    ],
)
def test_returns_empty_list_for_empty_response(mock_get, response_text):
    """Return an empty list when BOM has no matching stations."""
    response = Mock(
        status_code=200,
        text=response_text,
    )
    response.raise_for_status.return_value = None

    mock_get.return_value = response

    result = StationFinder.find_nearest_stations(
        nccObsCode=201,
        location=(-37.84, 144.98),
    )

    assert result == []


def test_propagates_http_error(
    mock_get,
):
    """Propagate an exception raised by the HTTP response."""
    response = Mock(
        status_code=500,
        text="Internal Server Error",
    )
    response.raise_for_status.side_effect = RuntimeError("HTTP error")

    mock_get.return_value = response

    with pytest.raises(RuntimeError, match="HTTP error"):
        StationFinder.find_nearest_stations(nccObsCode=201, location=(-37.84, 144.98))
