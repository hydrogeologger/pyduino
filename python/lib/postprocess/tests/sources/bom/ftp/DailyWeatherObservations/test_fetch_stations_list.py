"""Tests for :meth:`DailyWeatherObservations.fetch_stations_list`."""

from unittest.mock import Mock

import pytest

from postprocess.sources.bom.ftp import (
    BOM_FTP_DOMAIN,
    DailyWeatherObservations,
    _ftplib,  # For mocking and patching
)
from postprocess.sources.bom.types import BOMStationRecord


# pylint: disable=redefined-outer-name

@pytest.fixture
def mock_ftp(monkeypatch):
    """Mock the FTP connection used by the module."""
    mock = Mock()
    monkeypatch.setattr(
        _ftplib,
        "FTP",
        mock,
    )
    return mock


@pytest.fixture
def station_line():
    """Return a representative BOM station database record."""
    line = [" "] * 100

    line[0:6] = "086071".ljust(6)  # station id
    line[8:11] = "QLD".ljust(3)  # state
    line[12:18] = "Q10001".ljust(6)  # region/district
    line[18:59] = "Brisbane Airport".ljust(41)  # name
    line[59:67] = "19400101".ljust(8)  # start date
    line[67:69] = ".."  # end date
    line[75:83] = "-27.391".ljust(8)  # latitude
    line[84:92] = "153.13".ljust(8)  # longitude

    return "".join(line)


@pytest.fixture(autouse=True)
def clear_station_cache():
    """Clear class-level station caches before and after each test."""
    DailyWeatherObservations.stations_list.clear()
    DailyWeatherObservations.stations_by_id.clear()
    DailyWeatherObservations.stations_by_name.clear()
    DailyWeatherObservations.stations_by_coordinates.clear()

    yield

    DailyWeatherObservations.stations_list.clear()
    DailyWeatherObservations.stations_by_id.clear()
    DailyWeatherObservations.stations_by_name.clear()
    DailyWeatherObservations.stations_by_coordinates.clear()


def test_fetch_stations_list_is_constructor(mock_ftp):
    """Test that ``fetch_stations_list`` returns a new instance"""
    result = DailyWeatherObservations.fetch_stations_list()
    mock_ftp.assert_called_once()
    assert isinstance(result, DailyWeatherObservations)


def test_loads_station_records(
    mock_ftp,
    station_line,
):
    """Test that station records are downloaded and parsed."""
    ftp = mock_ftp.return_value
    ftp.retrbinary.side_effect = (
        lambda command, callback: callback(
            (station_line + "\n").encode("utf-8")
        )
    )

    DailyWeatherObservations.fetch_stations_list()

    assert len(DailyWeatherObservations.stations_list) == 1

    station = DailyWeatherObservations.stations_list[0]

    assert isinstance(station, BOMStationRecord)
    assert station.station_id == 86071
    assert station.state == "QLD"
    assert station.region == "Q10001"
    assert station.name == "Brisbane Airport"
    assert station.start_date == "19400101"
    assert station.latitude == pytest.approx(-27.391)
    assert station.longitude == pytest.approx(153.13)
    assert station.source == ""
    assert station.elevation_m is None
    assert station.barometer_height_m is None
    assert station.wmo_id is None


def test_connects_to_bom_ftp(mock_ftp):
    """Test that the BOM FTP server and directory are used."""
    ftp = mock_ftp.return_value

    DailyWeatherObservations.fetch_stations_list()

    mock_ftp.assert_called_once()
    assert mock_ftp.call_args.kwargs["host"] == BOM_FTP_DOMAIN
    ftp.login.assert_called_once_with()
    ftp.cwd.assert_called_once_with(
        DailyWeatherObservations._BASE_DIR # pylint: disable=protected-access
    )


def test_downloads_station_database(mock_ftp):
    """Test that the station database is downloaded."""
    ftp = mock_ftp.return_value

    DailyWeatherObservations.fetch_stations_list()

    ftp.retrbinary.assert_called_once()

    command = ftp.retrbinary.call_args.args[0]

    assert command == "RETR stations_db.txt"


def test_replaces_existing_station_list(

    mock_ftp,
    station_line,
):
    """Test that refreshing the station list replaces old records."""
    old_station = BOMStationRecord(
        station_id=1,
        region="OLD",
        name="Old Station",
        start_date="19000101",
        end_date="",
        latitude=-27.0,
        longitude=153.0,
        source="",
        state="QLD",
        elevation_m=None,
        barometer_height_m=None,
        wmo_id=None,
    )

    DailyWeatherObservations.stations_list.append(old_station)

    ftp = mock_ftp.return_value
    ftp.retrbinary.side_effect = (
        lambda command, callback: callback(
            (station_line + "\n").encode("utf-8")
        )
    )

    DailyWeatherObservations.fetch_stations_list()

    assert DailyWeatherObservations.stations_list == [
        DailyWeatherObservations.stations_list[0]
    ]

    assert (
        DailyWeatherObservations.stations_list[0].station_id
        == 86071
    )


def test_updates_station_lookup_caches(

    mock_ftp,
    station_line,
):
    """Test that station lookup dictionaries are populated."""
    ftp = mock_ftp.return_value
    ftp.retrbinary.side_effect = (
        lambda command, callback: callback(
            (station_line + "\n").encode("utf-8")
        )
    )

    DailyWeatherObservations.fetch_stations_list()

    station = DailyWeatherObservations.stations_list[0]

    assert (
        DailyWeatherObservations.stations_by_id[station.station_id]
        == station
    )

    assert (
        DailyWeatherObservations.stations_by_name[station.name.lower()]
        == station
    )


def test_skips_blank_lines(

    mock_ftp,
    station_line,
):
    """Test that blank lines in the station file are ignored."""
    ftp = mock_ftp.return_value
    ftp.retrbinary.side_effect = (
        lambda command, callback: callback(
            ("\n\n" + station_line + "\n\n").encode("utf-8")
        )
    )

    DailyWeatherObservations.fetch_stations_list()

    assert len(DailyWeatherObservations.stations_list) == 1


def test_closes_ftp_connection(

    mock_ftp,
):
    """Test that the FTP connection is closed after downloading."""
    ftp = mock_ftp.return_value

    DailyWeatherObservations.fetch_stations_list()

    ftp.quit.assert_called_once_with()
    ftp.close.assert_not_called()


def test_closes_ftp_connection_when_quit_fails(mock_ftp):
    """Test that the FTP connection is closed when quit fails."""
    ftp = mock_ftp.return_value
    ftp.quit.side_effect = Exception

    DailyWeatherObservations.fetch_stations_list()

    ftp.quit.assert_called_once_with()
    ftp.close.assert_called_once_with()
