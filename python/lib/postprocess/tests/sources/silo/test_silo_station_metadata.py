"""Tests for the SILOStation class in the SILO source module."""

import pytest

from postprocess.sources.silo import SILOStation


class TestSILOStation:
    """Tests for SILO-specific station metadata behaviour."""

    @pytest.mark.parametrize(
        ("number", "state"),
        [
            (40004, "QLD"),
            ("040004", "QLD"),
            ("40004", "QLD"),
            (40004, None),
        ],
    )
    def test_station_specific_attributes(self, number, state):
        """Store the SILO station number and state unchanged."""
        station = SILOStation(
            station_id=number,
            name="AMBERLEY AMO",
            latitude=-27.64,
            longitude=152.71,
            elevation_m=28.0,
            state=state,
        )

        assert station.station_id == number
        assert station.state == state
