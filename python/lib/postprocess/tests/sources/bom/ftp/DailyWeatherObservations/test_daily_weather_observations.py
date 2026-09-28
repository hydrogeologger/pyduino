"""Tests the DailyWeatherObservations FTP client that are trivial"""

from postprocess.sources.bom.ftp import DailyWeatherObservations


def test_initializes_without_station():
    """Test that a new client has no resolved station."""
    client = DailyWeatherObservations()

    assert client._station is None
