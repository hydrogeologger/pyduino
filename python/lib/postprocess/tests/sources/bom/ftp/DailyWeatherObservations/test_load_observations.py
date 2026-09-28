"""Tests for :meth:`DailyWeatherObservations.load_observations`."""

from datetime import date
from unittest.mock import Mock

import pytest

from postprocess.sources.bom import ftp as _ftp_module
from postprocess.sources.bom.ftp import _ftplib  # For mocking and patching
from postprocess.sources.bom.ftp import _pd  # For Mocking and Patching
from postprocess.sources.bom.ftp import DailyWeatherObservations

# pylint: disable=redefined-outer-name


@pytest.fixture
def fixture_dataframe():
    """Return a test observations DataFrame."""
    return _pd.DataFrame(
        {
            "Date": [
                date(2024, 3, 1),
                date(2024, 3, 2),
            ],
            "Temperature": [20, 21],
        }
    )


@pytest.mark.parametrize(
    "start_date, end_date",
    [
        ("2024-03-01", date(2024, 3, 31)),
        (date(2024, 3, 1), "2024-03-31"),
    ],
)
def test_load_observations_invalid_date_type(start_date, end_date):
    """Raise TypeError when a date argument is invalid."""
    with pytest.raises(TypeError):
        DailyWeatherObservations.load_observations_for_station(
            "test station",
            "sta",
            start_date,
            end_date,
        )


@pytest.mark.parametrize(
    "station_name, state",
    [
        ("", "sta"),
        ("test station", ""),
    ],
)
def test_load_observations_invalid_station(station_name, state):
    """Raise ValueError when station name or state is empty."""
    with pytest.raises(ValueError):
        DailyWeatherObservations.load_observations_for_station(
            station_name,
            state,
            date(2024, 3, 1),
            date(2024, 3, 31),
        )


def test_load_observations_end_before_start():
    """Raise ValueError when end_date precedes start_date."""
    with pytest.raises(ValueError):
        DailyWeatherObservations.load_observations_for_station(
            "test station",
            "sta",
            date(2024, 4, 1),
            date(2024, 3, 1),
        )


def test_load_observations_as_single_dataframe(
    monkeypatch,
    fixture_dataframe,
):
    """Return observations as a single DataFrame."""
    mock_ftp = Mock()

    def write_csv_data(_, callback):
        callback(b"csv data")

    mock_ftp.retrbinary.side_effect = write_csv_data

    monkeypatch.setattr(
        _ftplib,
        "FTP",
        Mock(return_value=mock_ftp),
    )
    monkeypatch.setattr(
        _pd,
        "read_csv",
        Mock(return_value=fixture_dataframe.copy()),
    )
    monkeypatch.setattr(
        _ftp_module,
        "_flatten_column_headers",
        lambda columns: columns,
    )
    result = DailyWeatherObservations.load_observations_for_station(
        "test station",
        "sta",
        date(2024, 3, 15),
        date(2024, 3, 20),
    )

    assert isinstance(result, _pd.DataFrame)


def test_load_observations_as_dict(monkeypatch, fixture_dataframe):
    """Return observations as a dictionary of monthly DataFrames."""
    mock_ftp = Mock()

    def write_csv_data(_, callback):
        callback(b"csv data")

    mock_ftp.retrbinary.side_effect = write_csv_data

    monkeypatch.setattr(
        _ftplib,
        "FTP",
        Mock(return_value=mock_ftp),
    )
    monkeypatch.setattr(
        _pd,
        "read_csv",
        Mock(return_value=fixture_dataframe.copy()),
    )
    monkeypatch.setattr(
        _ftp_module,
        "_flatten_column_headers",
        lambda columns: columns,
    )

    result = DailyWeatherObservations.load_observations_for_station(
        "test station",
        "sta",
        date(2024, 3, 15),
        date(2024, 3, 20),
        as_single_dataframe=False,
    )

    assert isinstance(result, dict)
