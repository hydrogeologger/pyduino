"""Tests for :meth:`DailyWeatherObservations.resolve_station`."""

import pytest

from postprocess.sources.bom.ftp import (
    DailyWeatherObservations,
)
from postprocess.sources.bom.types import BOMStationBase, BOMStationRecord


@pytest.fixture(autouse=True, scope="class")
def setup_station_cache():
    """Populate station lookup caches with representative stations."""
    station = BOMStationRecord(
        station_id=86071,
        region="Q10001",
        name="Brisbane Airport",
        start_date="19400101",
        end_date="",
        latitude=-27.39,
        longitude=153.13,
        source="",
        state="QLD",
        elevation_m=None,
        barometer_height_m=None,
        wmo_id=None,
    )

    other_station = BOMStationRecord(
        station_id=86072,
        region="Q10002",
        name="Brisbane",
        start_date="19400101",
        end_date="",
        latitude=-27.47,
        longitude=153.03,
        source="",
        state="QLD",
        elevation_m=None,
        barometer_height_m=None,
        wmo_id=None,
    )

    DailyWeatherObservations.stations_list[:] = [
        station,
        other_station,
    ]

    DailyWeatherObservations.stations_by_id.clear()
    DailyWeatherObservations.stations_by_id.update({
        station.station_id: station,
        other_station.station_id: other_station,
    })

    DailyWeatherObservations.stations_by_name.clear()
    DailyWeatherObservations.stations_by_name.update({
        station.name.lower(): station,
        other_station.name.lower(): other_station,
    })

    DailyWeatherObservations.stations_by_coordinates.clear()
    DailyWeatherObservations.stations_by_coordinates.update({
        (station.latitude, station.longitude): station,
        (other_station.latitude, other_station.longitude): other_station,
    })

    yield

    DailyWeatherObservations.stations_list.clear()
    DailyWeatherObservations.stations_by_id.clear()
    DailyWeatherObservations.stations_by_name.clear()
    DailyWeatherObservations.stations_by_coordinates.clear()


@pytest.mark.parametrize(
    "location",
    [
        86071,
        "86071",
    ],
)
def test_resolves_station_by_id(location):
    """Test that integer and numeric string IDs resolve a station."""
    client = DailyWeatherObservations()

    result = client.resolve_station(location)

    assert isinstance(result, BOMStationBase)
    assert result.station_id == 86071
    assert result.name == "Brisbane Airport"
    assert result.state == "QLD"
    assert result.latitude == pytest.approx(-27.39)
    assert result.longitude == pytest.approx(153.13)


def test_resolves_station_by_name():
    """Test that a station name resolves a matching station."""
    client = DailyWeatherObservations()

    result = client.resolve_station("Brisbane Airport")

    assert isinstance(result, BOMStationBase)
    assert result.station_id == 86071
    assert result.name == "Brisbane Airport"


@pytest.mark.parametrize(
    "location",
    [
        "Brisbane Airport",
        "BRISBANE AIRPORT",
        "brisbane airport",
        "BrIsBaNe AiRpOrT",
    ],
)
def test_resolves_station_by_name_case_insensitively(

    location,
):
    """Test that station names are resolved case-insensitively."""
    client = DailyWeatherObservations()

    result = client.resolve_station(location)

    assert isinstance(result, BOMStationBase)
    assert result.station_id == 86071


def test_resolves_station_by_coordinates():
    """Test that coordinates resolve a nearby station."""
    client = DailyWeatherObservations()

    result = client.resolve_station((-27.39, 153.13))

    assert isinstance(result, BOMStationBase)
    assert result.station_id == 86071
    assert result.name == "Brisbane Airport"


@pytest.mark.parametrize(
    "location",
    [
        None,
        "",
        "not-a-station",
        [],
        {},
    ],
)
def test_returns_none_for_invalid_location(location):
    """Test that unsupported location types return None."""
    client = DailyWeatherObservations()

    assert client.resolve_station(location) is None


@pytest.mark.parametrize(
    "location",
    [
        999999,
        "999999",
        "Unknown Station",
        (-30.0, 150.0),
    ],
)
def test_returns_none_when_station_is_not_found(location):
    """Test that unmatched valid locations return None."""
    client = DailyWeatherObservations()

    assert client.resolve_station(location) is None

# @pytest.mark.parametrize(
#     "tolerance",
#     [
#         (0, 0),
#         (0.0001, 0.0001),
#     ],
# )
# def test_resolves_coordinates_within_tolerance( tolerance):
#     """Test that coordinates within 0.05 degrees match."""
#     client = DailyWeatherObservations()

#     result = client.resolve_station(
#         (-27.39 + tolerance[0], 153.13 + tolerance[1])
#     )

#     assert result is not None
#     assert result.station_id == 86071


def test_resolves_coordinates_exactly():
    """Test that coorrdinates match exactly to resolve station."""
    client = DailyWeatherObservations()

    result = client.resolve_station((-27.39, 153.13))
    # assert result is not None
    assert result.station_id == 86071


def test_rejects_coordinates_outside_tolerance():
    """Test that coordinates outside 0.05 degrees do not match."""
    client = DailyWeatherObservations()

    result = client.resolve_station(
        (-27.39 + 0.051, 153.13)
    )

    assert result is None


def test_stores_resolved_station():
    """Test that a resolved station is stored on the client."""
    client = DailyWeatherObservations()

    result = client.resolve_station(86071, set_station=True)

    assert client._station is result


def test_preserves_existing_station_after_failed_lookup():
    """Test that a failed lookup does not clear the existing station."""
    client = DailyWeatherObservations()

    existing = client.resolve_station(86071, set_station=True)

    result = client.resolve_station(999999, set_station=True)

    assert result is None
    assert client._station is existing
