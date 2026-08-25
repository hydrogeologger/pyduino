"""Tests for the SILO ``find_nearby_stations`` function."""

from unittest.mock import Mock

import pytest

from postprocess.sources import silo
# For patching
from postprocess.sources.silo import (
    get_nearby_stations,
    haversine_distance,
)


@pytest.mark.parametrize(
    "location",
    [
        (100, 153.02),
        (-27.47, 200),
    ],
)
def test_invalid_coordinates_raise_value_error(location):
    """Raise ValueError for invalid coordinates."""
    with pytest.raises(ValueError):
        silo.find_nearby_stations(location)


def test_station_id_location_delegates_to_get_nearby_stations(monkeypatch):
    """Delegate station-number searches to get_nearby_stations."""
    mocked_get_nearby = Mock(return_value=[])

    monkeypatch.setattr(
        silo,
        get_nearby_stations.__name__,
        mocked_get_nearby,
    )

    result = silo.find_nearby_stations(
        location=15526,
        radius_km=50,
        timeout=10,
    )

    assert result == []

    mocked_get_nearby.assert_called_once_with(
        station_id=15526,
        radius_km=50,
        sortby=None,
        timeout=10,
    )


@pytest.mark.parametrize(
    ("radius", "expected_reference_radius"),
    [
        (50, 10000),
        (999, 10000),
        (1000, 1000),
        (5000, 5000),
    ],
)
def test_coordinate_location_queries_reference_station(
    monkeypatch,
    radius,
    expected_reference_radius,
):
    """Use station 15603 with the appropriate reference radius."""
    mocked_get_nearby = Mock(return_value=[])

    monkeypatch.setattr(
        silo,
        get_nearby_stations.__name__,
        mocked_get_nearby,
    )

    result = silo.find_nearby_stations(
        location=(-27.47, 153.02),
        radius_km=radius,
    )

    assert result == []

    mocked_get_nearby.assert_called_once_with(
        station_id=15603,
        radius_km=expected_reference_radius,
        sortby="name",
        timeout=(5, 30),
    )


def test_coordinate_location_calculates_filters_and_sorts_stations(
    monkeypatch,
):
    """Calculate distances, filter by radius, and sort stations by distance."""
    stations = [
        silo.SILOStationRecord(
            station_id=1,
            name="Far",
            latitude=-27.47,
            longitude=153.02,
            state="QLD",
            elevation_m=10.0,
            distance_km=999.0,
        ),
        silo.SILOStationRecord(
            station_id=2,
            name="Near",
            latitude=-27.48,
            longitude=153.03,
            state="QLD",
            elevation_m=10.0,
            distance_km=999.0,
        ),
        silo.SILOStationRecord(
            station_id=3,
            name="Closest",
            latitude=-27.49,
            longitude=153.04,
            state="QLD",
            elevation_m=10.0,
            distance_km=999.0,
        ),
    ]

    mocked_get_nearby = Mock(return_value=stations)
    mocked_haversine = Mock(
        side_effect=[20.12345, 5.67891, 60.0],
    )

    monkeypatch.setattr(
        silo,
        get_nearby_stations.__name__,
        mocked_get_nearby,
    )
    monkeypatch.setattr(
        silo,
        haversine_distance.__name__,
        mocked_haversine,
    )

    result = silo.find_nearby_stations(
        location=(-27.47, 153.02),
        radius_km=50,
    )

    assert [station.station_id for station in result] == [2, 1]
    assert [station.distance_km for station in result] == [
        5.679,
        20.123,
    ]

    mocked_haversine.assert_any_call(
        (-27.47, 153.02),
        (-27.47, 153.02),
    )
    mocked_haversine.assert_any_call(
        (-27.47, 153.02),
        (-27.48, 153.03),
    )
    mocked_haversine.assert_any_call(
        (-27.47, 153.02),
        (-27.49, 153.04),
    )
