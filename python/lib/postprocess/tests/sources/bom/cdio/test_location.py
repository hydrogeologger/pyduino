"""Tests for the :class:`Location` class."""

import pytest

from postprocess.sources.bom.cdio import Location

# pylint: disable=protected-access


@pytest.mark.parametrize(
    "name,state,latitude,longitude,expected",
    [
        (
            "Melbourne",
            "VIC",
            -37.84,
            144.98,
            "Melbourne,VIC,-37.84,144.98",
        ),
        (
            "Brisbane",
            "QLD",
            -27.47,
            153.03,
            "Brisbane,QLD,-27.47,153.03",
        ),
        (
            "Perth",
            "WA",
            -31.95,
            115.86,
            "Perth,WA,-31.95,115.86",
        ),
    ],
)
def test_str(name, state, latitude, longitude, expected):
    """Return the location as a BOM location record."""
    location = Location(name, state, latitude, longitude)

    assert str(location) == expected


@pytest.mark.parametrize(
    "value,name,state,latitude,longitude",
    [
        ("Melbourne, VIC, 37.84°S, 144.98°E",
            "Melbourne", "VIC", -37.84, 144.98),
        ("Brisbane, QLD, 27.47°S, 153.03°E",
            "Brisbane", "QLD", -27.47, 153.03),
        ("Sydney, NSW, 33.86°S, 151.21°E", "Sydney", "NSW", -33.86, 151.21),
        ("Darwin, NT, 12.46°S, 130.84°E", "Darwin", "NT", -12.46, 130.84),
    ],
)
def test_from_string(value, name, state, latitude, longitude):
    """Parse a BOM location record into signed coordinates."""
    location = Location.from_string(value)

    assert location.name == name
    assert location.state == state
    assert location.latitude == latitude
    assert location.longitude == longitude


@pytest.mark.parametrize(
    "name,state,latitude,longitude,expected",
    [
        ("Melbourne", "VIC", -37.84, 144.98,
            "Melbourne,VIC,37.84,144.98"),
        ("Brisbane", "QLD", -27.47, 153.03,
            "Brisbane,QLD,27.47,153.03"),
        ("Sydney", "NSW", -33.86, 151.21,
            "Sydney,NSW,33.86,151.21"),
        ("Darwin", "NT", -12.46, 130.84,
            "Darwin,NT,12.46,130.84"),
        ("north_hemisphere", "NT", 12.46, 130.84,
            "north_hemisphere,NT,12.46,130.84"),
        ("west_hemisphere", "NT", -12.46, -130.84,
            "west_hemisphere,NT,12.46,-130.84"),
        ("test", "NT", 0.0, 144.98,
            "test,NT,0.0,144.98"),
    ],
)
def test_to_bom_string(name, state, latitude, longitude, expected):
    """Convert a location to the BOM API location representation."""
    location = Location(name, state, latitude, longitude)

    assert location.to_bom_string() == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("37.84°S", -37.84),
        ("37.84°s", -37.84),
        ("144.98°W", -144.98),
        ("144.98°w", -144.98),
        ("27.47°N", 27.47),
        ("27.47°n", 27.47),
        ("153.03°E", 153.03),
        ("153.03°e", 153.03),
    ],
)
def test_parse_coordinate(value, expected):
    """Parse a hemisphere-qualified coordinate into signed decimal degrees."""
    assert Location._parse_coordinate(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "37.84°X",
        "144.98°Q",
    ],
)
def test_parse_coordinate_invalid_hemisphere(value):
    """Raise ValueError for unsupported coordinate hemispheres."""
    with pytest.raises(
        ValueError,
        match="Invalid coordinate hemisphere",
    ):
        Location._parse_coordinate(value)


@pytest.mark.parametrize(
    "value",
    [
        "invalid",
        "",
        None,
    ],
)
def test_parse_coordinates_invalid_coordinate(value):
    """Raise ValueError for invalid coordinate."""
    with pytest.raises(
        ValueError
    ):
        Location._parse_coordinate(value)
