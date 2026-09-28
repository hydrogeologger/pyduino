"""Tests for :meth:`DailyWeatherObservations.resolve_station`."""

import pytest
from unittest.mock import Mock

from postprocess.sources.bom.ftp import (
    DailyWeatherObservations,
)
from postprocess.sources.bom.types import BOMStationBase

# pylint: disable=protected-access


def test_set_station_with_object():
    """Set station directly using a BOMStationBase instance."""
    client = DailyWeatherObservations()
    station = Mock(spec=BOMStationBase)

    client.set_station(station)
    assert client._station == station


def test_set_station_with_int_resolution(monkeypatch):
    """Resolve and set station when given a valid integer ID."""
    client = DailyWeatherObservations()
    station = Mock(spec=BOMStationBase)

    mock_resolve = Mock(return_value=station)
    monkeypatch.setattr(client, "resolve_station", mock_resolve)

    client.set_station(12345)

    mock_resolve.assert_called_once_with(
        location=12345,
        set_station=False
    )
    assert client._station == station


def test_set_station_raises_value_error_on_none(monkeypatch):
    """Raise ValueError if integer ID resolves to None."""
    client = DailyWeatherObservations()
    monkeypatch.setattr(client, "resolve_station", Mock(return_value=None))

    with pytest.raises(ValueError, match="No station found"):
        client.set_station(99999)


def test_set_station_raises_type_error_on_invalid_type():
    """Raise TypeError if station is neither an int nor a BOMStationBase."""
    client = DailyWeatherObservations()

    with pytest.raises(TypeError, match="`station` must be a valid"):
        client.set_station("invalid-type")
