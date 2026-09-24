"""Unit tests for coordinate utilities in the postprocess.sources.utils package."""

import pytest

from postprocess.sources.utils import validate_decimal_degree_coordinates


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
def test_valid_coordinates(coordinates):
    """Accept valid latitude and longitude coordinates."""
    assert validate_decimal_degree_coordinates(coordinates) is None


@pytest.mark.parametrize(
    "coordinates",
    [
        (90.1, 0),
        (-90.1, 0),
        (0, 180.1),
        (0, -180.1),
    ],
)
def test_coordinates_out_of_range(coordinates):
    """Raise ValueError for coordinates outside their valid ranges."""
    with pytest.raises(ValueError):
        validate_decimal_degree_coordinates(coordinates)


@pytest.mark.parametrize(
    "coordinates",
    [
        [10, 20],
        "10,20",
    ],
)
def test_coordinates_must_be_tuple(coordinates):
    """Raise TypeError when coordinates are not provided as a tuple."""
    with pytest.raises(TypeError):
        validate_decimal_degree_coordinates(coordinates)


@pytest.mark.parametrize(
    "coordinates",
    [
        (),
        (10,),
        (10, 20, 30),
    ],
)
def test_coordinates_must_contain_exactly_two_values(coordinates):
    """Raise ValueError when coordinates do not contain exactly two values."""
    with pytest.raises(ValueError):
        validate_decimal_degree_coordinates(coordinates)


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
def test_coordinates_must_be_numeric(coordinates):
    """Raise TypeError when either coordinate is not numeric."""
    with pytest.raises(TypeError):
        validate_decimal_degree_coordinates(coordinates)
