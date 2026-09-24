"""Tests for the Open-Meteo ``get_location_meta`` function."""

from postprocess.sources import openmeteo


def test_returns_location_metadata():
    """Create LocationBase from API location fields."""
    data = {
        "latitude": -27.47,
        "longitude": 153.02,
        "elevation": 15.5,
    }

    result = openmeteo.location_meta_from_data(data)

    assert result.latitude == -27.47
    assert result.longitude == 153.02
    assert result.elevation_m == 15.5


def test_missing_values_become_none():
    """Use None when location metadata fields are absent."""
    result = openmeteo.location_meta_from_data({})

    assert result is None


def test_extra_fields_are_ignored():
    """Ignore API fields that are not part of LocationBase."""
    data = {
        "latitude": -27.47,
        "longitude": 153.02,
        "elevation": 15.5,
        "timezone": "Australia/Brisbane",
        "extra": "ignored",
    }

    result = openmeteo.location_meta_from_data(data)

    assert result.latitude == -27.47
    assert result.longitude == 153.02
    assert result.elevation_m == 15.5
