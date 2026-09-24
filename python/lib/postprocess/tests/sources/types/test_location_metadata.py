"""Unit tests for the LocationMetadata type."""

import pytest

from postprocess.sources.types import Coordinates, LocationMetadata

@pytest.mark.parametrize(
    "latitude, longitude, elevation, name",
    [
        (0.0, 0.0, None, ""),
        (-27.4698, 153.0251, 15.0, "Brisbane"),
        (51.5074, -0.1278, 11.0, "London"),
        (-33.8688, 151.2093, 58.0, "Sydney"),
        (None, None, None, None),
        (None, None, None, ""),
        (None, None, "", ""),
    ],
)
def test_location_metadata_attributes(
    latitude,
    longitude,
    elevation,
    name,
):
    """Verify that LocationMetadata stores the provided metadata correctly."""
    location = LocationMetadata(
        latitude,
        longitude,
        elevation,
        name,
    )

    assert location.latitude == latitude
    assert location.longitude == longitude
    assert location.elevation == elevation
    assert location.name == name


def test_location_metadata_with_defaults():
    """Create LocationMetadata with default elevation and name."""
    location = LocationMetadata(
        latitude=10.5,
        longitude=20.5,
    )

    assert location.latitude == 10.5
    assert location.longitude == 20.5
    assert location.elevation is None
    assert location.name == ""


def test_location_metadata_with_all_values():
    """Create LocationMetadata with all supplied values."""
    location = LocationMetadata(
        latitude=10.5,
        longitude=20.5,
        elevation=100.0,
        name="Test Location",
    )

    assert location.latitude == 10.5
    assert location.longitude == 20.5
    assert location.elevation == 100.0
    assert location.name == "Test Location"


def test_location_metadata_coordinates_returns_coordinates():
    """Return the location coordinates as a Coordinates instance."""
    location = LocationMetadata(
        latitude=10.5,
        longitude=20.5,
    )

    assert location.coordinates == Coordinates(
        latitude=10.5,
        longitude=20.5,
    )
    assert isinstance(location.coordinates, Coordinates)


def test_location_metadata_coordinates_reflect_current_values():
    """Return coordinates based on the current latitude and longitude."""
    location = LocationMetadata(
        latitude=10.5,
        longitude=20.5,
    )

    location.latitude = 30.5
    location.longitude = 40.5

    assert location.coordinates == Coordinates(
        latitude=30.5,
        longitude=40.5,
    )


# @pytest.mark.parametrize(
#     "latitude, longitude",
#     [
#         (90.1, 0),
#         (-90.1, 0),
#         (0, 180.1),
#         (0, -180.1),
#     ],
# )
# def test_location_metadata_rejects_invalid_coordinates(
#     latitude,
#     longitude,
# ):
#     """Raise ValueError for coordinates outside their valid ranges."""
#     with pytest.raises(ValueError):
#         LocationMetadata(
#             latitude=latitude,
#             longitude=longitude,
#         )


# @pytest.mark.parametrize(
#     "latitude, longitude",
#     [
#         ("10", 20),
#         (10, "20"),
#         (None, 20),
#         (10, None),
#     ],
# )
# def test_location_metadata_rejects_non_numeric_coordinates(
#     latitude,
#     longitude,
# ):
#     """Raise TypeError for non-numeric coordinates."""
#     with pytest.raises(TypeError):
#         LocationMetadata(
#             latitude=latitude,
#             longitude=longitude,
#         )


def test_location_metadata_coordinates_are_read_only():
    """Prevent assignment to the coordinates property."""
    location = LocationMetadata(
        latitude=10.5,
        longitude=20.5,
    )

    with pytest.raises(AttributeError):
        location.coordinates = Coordinates(
            latitude=30,
            longitude=40,
        )
