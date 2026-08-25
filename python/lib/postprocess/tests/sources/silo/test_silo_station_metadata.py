"""Tests for the SILOStationMetadata class in the SILO source module."""

import pytest

from postprocess.sources.silo import SILOStationMetadata


class TestSILOStationMetadata:
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
        station = SILOStationMetadata(
            number=number,
            name="AMBERLEY AMO",
            latitude=-27.64,
            longitude=152.71,
            elevation=28.0,
            state=state,
        )

        assert station.number == number
        assert station.state == state
