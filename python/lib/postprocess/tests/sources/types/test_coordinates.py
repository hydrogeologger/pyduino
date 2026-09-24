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

class TestCoordinatesValidateDecimalDegree:
    """Testing Coordinates.validate_decimal_degreee function."""
    @pytest.mark.parametrize(
        "coordinates",
        [
            (0, 0),  # integer
            (45.5, 90.25),  # floats
            (-45.5, -90.25),  # floats
            (90, 180),  # boundary, integer
            (-90, -180),  # boundary, integer
            (90.0, 180.0),  # boundary, floats
            (-90.0, -180.0),  # boundary, floats
        ],
    )
    def test_validate_decimal_degree_valid(self, coordinates):
        """Accept valid latitude and longitude coordinates."""
        assert Coordinates.validate_decimal_degree(coordinates) is None

    @pytest.mark.parametrize(
        "coordinates",
        [
            (90.1, 0),
            (-90.1, 0),
            (0, 180.1),
            (0, -180.1),
        ],
    )
    def test_validate_decimal_degree_out_of_range(self, coordinates):
        """Raise ValueError for coordinates outside their valid ranges."""
        with pytest.raises(ValueError):
            Coordinates.validate_decimal_degree(coordinates)

    @pytest.mark.parametrize(
        "coordinates",
        [
            [10, 20],
            "10,20",
        ],
    )
    def test_validate_decimal_degree_must_be_tuple(self, coordinates):
        """Raise TypeError when coordinates are not provided as a tuple."""
        with pytest.raises(TypeError):
            Coordinates.validate_decimal_degree(coordinates)

    @pytest.mark.parametrize(
        "coordinates",
        [
            (),
            (10,),
            (10, 20, 30),
        ],
    )
    def test_validate_decimal_degree_must_contain_two_values(self, coordinates):
        """Raise ValueError when coordinates do not contain exactly two values."""
        with pytest.raises(ValueError):
            Coordinates.validate_decimal_degree(coordinates)

    @pytest.mark.parametrize(
        "coordinates",
        [
            ("10", 20),
            (10, "20"),
            (None, 20),
            (10, None),
            (True, 20),
            (10, False),
        ],
    )
    def test_validate_decimal_degree_must_be_numeric(self, coordinates):
        """Raise TypeError when either coordinate is not numeric."""
        with pytest.raises(TypeError):
            Coordinates.validate_decimal_degree(coordinates)
