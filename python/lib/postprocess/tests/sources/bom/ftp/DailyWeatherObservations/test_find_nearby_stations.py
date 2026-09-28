"""Tests for :meth:`DailyWeatherObservations.find_nearby_stations`."""

from unittest.mock import Mock

import pytest

from postprocess.sources.bom.ftp import (
    BOMStationRecord,
    DailyWeatherObservations,
)


def test_find_nearby_stations():
    """Return stations within the specified radius, sorted by distance."""
    client = DailyWeatherObservations()

    near_station = BOMStationRecord(
        station_id=1,
        name="Near Station",
        latitude=-27.4705,
        longitude=153.0260,
        state="QLD",
        region="",
        start_date="",
        end_date="",
        source="",
        elevation_m=None,
        barometer_height_m=None,
        wmo_id=None,
    )
    far_station = BOMStationRecord(
        station_id=2,
        name="Far Station",
        latitude=-27.4800,
        longitude=153.0400,
        state="QLD",
        region="",
        start_date="",
        end_date="",
        source="",
        elevation_m=None,
        barometer_height_m=None,
        wmo_id=None,
    )
    outside_station = BOMStationRecord(
        station_id=3,
        name="Outside Station",
        latitude=-28.0000,
        longitude=153.5000,
        state="QLD",
        region="",
        start_date="",
        end_date="",
        source="",
        elevation_m=None,
        barometer_height_m=None,
        wmo_id=None,
    )

    client.stations_list = [
        outside_station,
        far_station,
        near_station,
    ]

    result = client.find_nearby_stations(
        (-27.4698, 153.0251),
        radius_km=10,
    )

    assert [record.station for record in result] == [
        near_station,
        far_station,
    ]
    assert result[0].distance_km < result[1].distance_km


def test_find_nearby_stations_unresolved_location(monkeypatch):
    """Raise ValueError when the reference location cannot be resolved."""
    client = DailyWeatherObservations()

    mock_resolve_station = Mock(return_value=None)
    monkeypatch.setattr(
        client,
        "resolve_station",
        mock_resolve_station,
    )

    with pytest.raises(ValueError):
        client.find_nearby_stations("unknown station")
