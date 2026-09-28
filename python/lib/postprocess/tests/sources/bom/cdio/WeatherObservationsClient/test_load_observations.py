"""Tests for :meth:`WeatherObservationsClient.load_observations`."""
from datetime import date
from unittest.mock import Mock

import pandas as pd
import pytest

from postprocess.sources.bom.cdio import _pd  # Mocking
from postprocess.sources.bom.cdio import _requests  # Mocking
from postprocess.sources.bom.cdio import (
    DWOStation,
    WeatherObservationsClient,
)

# pylint: disable=redefined-outer-name


@pytest.fixture
def station():
    """Return a test DWO station."""
    return DWOStation(
        dwo_id=1,
        station_id=12345,
        name="test station",
        state="sta",
        distance_km=0,
        is_open=True,
    )


def test_load_observations_without_station():
    """Raise ValueError when no station has been set."""
    client = WeatherObservationsClient()

    with pytest.raises(ValueError):
        client.load_observations(
            date(2024, 3, 1),
            date(2024, 3, 31),
        )


@pytest.mark.parametrize("start_date, end_date", [
    ("2024-03-01", date(2024, 3, 31)),
    (date(2024, 3, 1), "2024-03-31"),
])
def test_load_observations_invalid_date_type(station, start_date, end_date):
    """Raise TypeError when a date argument is invalid."""
    client = WeatherObservationsClient()
    client.set_station(station)

    with pytest.raises(TypeError):
        client.load_observations(start_date, end_date)


def test_load_observations_end_before_start(station):
    """Raise ValueError if end_date precedes start_date."""
    client = WeatherObservationsClient()
    client.set_station(station)

    with pytest.raises(ValueError):
        client.load_observations(
            date(2024, 4, 1),
            date(2024, 3, 1),
        )


def test_load_observations_as_single_dataframe(station, monkeypatch):
    """Return observations as a single DataFrame."""
    client = WeatherObservationsClient()
    client.set_station(station)

    response = Mock(status_code=200)
    response.content = b"csv data"
    response.raise_for_status.return_value = None

    monkeypatch.setattr(_requests, "get", Mock(return_value=response))
    monkeypatch.setattr(
        _pd,
        "read_csv",
        Mock(return_value=_pd.DataFrame()),
    )

    result = client.load_observations(
        date(2024, 3, 15),
        date(2024, 3, 20),
    )

    assert isinstance(result, _pd.DataFrame)


def test_load_observations_as_dict(station, monkeypatch):
    """Return monthly observations as a dictionary."""
    client = WeatherObservationsClient()
    client.set_station(station)

    response = Mock(status_code=200)
    response.content = b"csv data"
    response.raise_for_status.return_value = None

    dataframe = pd.DataFrame(
        {"Temperature": [20]},
        index=pd.to_datetime(["2024-03-01"]),
    )
    dataframe.index.name = "Date"

    monkeypatch.setattr(_requests, "get", Mock(return_value=response))
    monkeypatch.setattr(_pd, "read_csv", Mock(return_value=dataframe))

    result = client.load_observations(
        date(2024, 3, 15),
        date(2024, 3, 20),
        as_single_dataframe=False,
    )

    assert result == {"202403": dataframe}
