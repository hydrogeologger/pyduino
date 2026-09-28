"""Tests for the WeatherObservationsClient."""

from unittest.mock import Mock

import pytest

from postprocess.sources.bom.cdio import (
    DWOStation,
    WeatherObservationsClient,
)


def test_weather_observations_client_station():
    """Client initializes without a station."""
    client = WeatherObservationsClient()
    assert client.station is None
    assert client._WeatherObservationsClient__NCC_OBS_CODE == 201  # pylint: disable=protected-access


def test_weather_observations_client_set_station():
    """Set station using a DWOStation instance."""
    client = WeatherObservationsClient()
    mock_station = DWOStation(dwo_id=1,
                              station_id=12345,
                              name="test station",
                              state="sta",
                              distance_km=0,
                              is_open=True
                              )

    client.set_station(mock_station)

    assert client.station == mock_station


def test_weather_observations_client_set_station_by_id(monkeypatch):
    """Set station using a BOM station ID."""
    client = WeatherObservationsClient()
    mock_station = DWOStation(dwo_id=1,
                              station_id=12345,
                              name="test station",
                              state="sta",
                              distance_km=0,
                              is_open=True
                              )

    mock_find_nearest_stations = Mock(return_value=[mock_station])
    monkeypatch.setattr(
        WeatherObservationsClient,
        "find_nearest_stations",
        mock_find_nearest_stations,
    )

    client.set_station(12345)

    mock_find_nearest_stations.assert_called_once_with(12345)
    assert client.station == mock_station


def test_weather_observations_client_set_station_invalid_type():
    """Raise TypeError when station is not a DWOStation or station ID."""
    client = WeatherObservationsClient()

    with pytest.raises(TypeError):
        client.set_station("invalid")


def test_weather_observations_client_set_station_not_found(monkeypatch):
    """Raise ValueError when no station is found for a station ID."""
    monkeypatch.setattr(
        WeatherObservationsClient,
        "find_nearest_stations",
        Mock(return_value=[]),
    )
    client = WeatherObservationsClient()

    with pytest.raises(ValueError):
        client.set_station(12345)
