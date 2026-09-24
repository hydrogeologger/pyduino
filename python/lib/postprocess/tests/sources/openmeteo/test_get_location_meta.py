"""Tests for the Open-Meteo ``get_location_meta`` function."""

from postprocess.sources import openmeteo


def test_returns_location_metadata():
    """Create LocationMetadata from API location fields."""
    data = {
        "latitude": -27.47,
        "longitude": 153.02,
        "elevation": 15.5,
    }

    result = openmeteo.get_location_meta(data)

    assert result.latitude == -27.47
    assert result.longitude == 153.02
    assert result.elevation == 15.5


def test_missing_values_become_none():
    """Use None when location metadata fields are absent."""
    result = openmeteo.get_location_meta({})

    assert result.latitude is None
    assert result.longitude is None
    assert result.elevation is None


def test_extra_fields_are_ignored():
    """Ignore API fields that are not part of LocationMetadata."""
    data = {
        "latitude": -27.47,
        "longitude": 153.02,
        "elevation": 15.5,
        "timezone": "Australia/Brisbane",
        "extra": "ignored",
    }

    result = openmeteo.get_location_meta(data)

    assert result.latitude == -27.47
    assert result.longitude == 153.02
    assert result.elevation == 15.5
