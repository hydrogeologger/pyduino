"""Tests for the SILO ``get_location_meta`` function."""

import pytest

from postprocess.sources import silo
from postprocess.sources.types import LocationMetadata


@pytest.mark.parametrize(
    ("number", "state"),
    [
        (40004, "QLD"),
        ("40004", "QLD"),
        (40004, None),
    ],
)
def test_returns_station_metadata(number, state):
    """Create SILO station metadata from station data."""
    data = {
        "station": {
            "number": number,
            "name": "AMBERLEY AMO",
            "latitude": -27.63,
            "longitude": 152.71,
            "elevation": 19.0,
            "state": state,
        }
    }

    result = silo.get_location_meta(data)

    assert isinstance(result, silo.SILOStationMetadata)
    assert result.number == number
    assert result.name == "AMBERLEY AMO"
    assert result.latitude == -27.63
    assert result.longitude == 152.71
    assert result.elevation == 19.0
    assert result.state == state


def test_returns_location_metadata():
    """Create location metadata when station data is unavailable."""
    data = {
        "location": {
            "latitude": -27.47,
            "longitude": 153.02,
            "elevation": 15.5,
            "name": "Brisbane",
        }
    }

    result = silo.get_location_meta(data)

    assert type(result) is LocationMetadata
    assert result.latitude == -27.47
    assert result.longitude == 153.02
    assert result.elevation == 15.5
    assert result.name == "Brisbane"


def test_station_metadata_takes_precedence():
    """Prefer station metadata when both station and location exist."""
    data = {
        "station": {
            "number": 40004,
            "name": "AMBERLEY AMO",
            "latitude": -27.63,
            "longitude": 152.71,
            "elevation": 19.0,
            "state": "QLD",
        },
        "location": {
            "latitude": -27.47,
            "longitude": 153.02,
            "elevation": 15.5,
            "name": "Brisbane",
        },
    }

    result = silo.get_location_meta(data)

    assert isinstance(result, silo.SILOStationMetadata)
    assert result.number == 40004
    assert result.name == "AMBERLEY AMO"


def test_missing_station_values_become_none():
    """Use None for missing station values."""
    result = silo.get_location_meta({"station": {}})

    assert isinstance(result, silo.SILOStationMetadata)
    assert result.number is None
    assert result.latitude is None
    assert result.longitude is None
    assert result.elevation is None
    assert result.state is None
    assert result.name == ""


def test_missing_location_values_become_none():
    """Use None for missing location values."""
    result = silo.get_location_meta({"location": {}})

    assert type(result) is LocationMetadata
    assert result.latitude is None
    assert result.longitude is None
    assert result.elevation is None
    assert result.name == ""


def test_returns_none_when_metadata_is_missing():
    """Return None when no station or location metadata exists."""
    assert silo.get_location_meta({}) is None
