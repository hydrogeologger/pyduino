"""Unit tests for the Coordinates type."""

import pytest

from postprocess.sources.types import Coordinates


@pytest.mark.parametrize(
    "latitude, longitude",
    [
        (0, 0),
        (45.5, 90.25),
        (-45.5, -90.25),
        (90, 180),
        (-90, -180),
    ],
)
def test_coordinates(latitude, longitude):
    """Create Coordinates with latitude and longitude values."""
    coordinates = Coordinates(
        latitude=latitude,
        longitude=longitude,
    )

    assert coordinates.latitude == latitude
    assert coordinates.longitude == longitude


def test_coordinates_is_named_tuple():
    """Coordinates provides named tuple behaviour."""
    coordinates = Coordinates(
        latitude=10.5,
        longitude=20.5,
    )

    assert coordinates == (10.5, 20.5)
    assert coordinates[0] == 10.5
    assert coordinates[1] == 20.5


def test_coordinates_supports_unpacking():
    """Coordinates can be unpacked into latitude and longitude."""
    coordinates = Coordinates(
        latitude=10.5,
        longitude=20.5,
    )

    latitude, longitude = coordinates

    assert latitude == 10.5
    assert longitude == 20.5


def test_coordinates_is_immutable():
    """Coordinates fields cannot be modified after creation."""
    coordinates = Coordinates(
        latitude=10.5,
        longitude=20.5,
    )

    with pytest.raises(AttributeError):
        coordinates.latitude = 30.0


def test_coordinates_has_expected_fields():
    """Coordinates exposes latitude and longitude as named fields."""
    assert Coordinates._fields == ("latitude", "longitude")
