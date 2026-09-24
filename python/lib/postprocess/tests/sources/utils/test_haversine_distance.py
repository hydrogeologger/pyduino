"""Unit tests for the haversine_distance utility."""

import pytest

from postprocess.sources.utils import haversine_distance


def test_same_coordinates_returns_zero():
    """Return zero distance when both coordinates are identical."""
    coordinates = (10.5, 20.5)

    assert haversine_distance(coordinates, coordinates) == pytest.approx(0.0)


@pytest.mark.parametrize(
    "coord1, coord2, expected_distance",
    [
        ((0, 0), (0, 1), 111.195),
        ((0, 0), (1, 0), 111.195),
        ((0, 0), (0, 180), 20015.087),
        ((0, 0), (90, 0), 10007.543),
        ((-90, 0), (90, 0), 20015.087),
    ],
)
def test_haversine_distance(coord1, coord2, expected_distance):
    """Calculate the expected great-circle distance between coordinates."""
    assert haversine_distance(coord1, coord2) == pytest.approx(
        expected_distance,
        rel=1e-4,
    )


def test_distance_is_symmetric():
    """Return the same distance regardless of coordinate order."""
    coord1 = (10.5, 20.5)
    coord2 = (-30.5, 120.5)

    assert haversine_distance(coord1, coord2) == pytest.approx(
        haversine_distance(coord2, coord1)
    )


def test_custom_radius():
    """Scale the calculated distance using the supplied radius."""
    coord1 = (0, 0)
    coord2 = (0, 1)

    distance = haversine_distance(
        coord1,
        coord2,
        radius=1.0,
    )

    assert distance == pytest.approx(0.0174532925)


def test_none_radius_uses_earth_radius():
    """Use the default Earth radius when radius is None."""
    coord1 = (0, 0)
    coord2 = (0, 1)

    assert haversine_distance(
        coord1,
        coord2,
        radius=None,
    ) == pytest.approx(
        haversine_distance(coord1, coord2),
    )


@pytest.mark.parametrize(
    "coord1",
    [
        [0, 0],
        "0,0",
        (0,),
        (0, 0, 0),
        ("0", 0),
        (0, "0"),
    ],
)
def test_invalid_coord1_raises(coord1):
    """Raise an exception when coord1 is invalid."""
    with pytest.raises((TypeError, ValueError)):
        haversine_distance(coord1, (0, 0))


@pytest.mark.parametrize(
    "coord2",
    [
        [0, 0],
        "0,0",
        (0,),
        (0, 0, 0),
        ("0", 0),
        (0, "0"),
    ],
)
def test_invalid_coord2_raises(coord2):
    """Raise an exception when coord2 is invalid."""
    with pytest.raises((TypeError, ValueError)):
        haversine_distance((0, 0), coord2)


@pytest.mark.parametrize(
    "coord1",
    [
        (90.1, 0),
        (-90.1, 0),
        (0, 180.1),
        (0, -180.1),
    ],
)
def test_invalid_coord1_range_raises(coord1):
    """Raise ValueError when coord1 is outside valid coordinate ranges."""
    with pytest.raises(ValueError):
        haversine_distance(coord1, (0, 0))


@pytest.mark.parametrize(
    "coord2",
    [
        (90.1, 0),
        (-90.1, 0),
        (0, 180.1),
        (0, -180.1),
    ],
)
def test_invalid_coord2_range_raises(coord2):
    """Raise ValueError when coord2 is outside valid coordinate ranges."""
    with pytest.raises(ValueError):
        haversine_distance((0, 0), coord2)
