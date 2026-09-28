"""Tests for BOM shared type definitions.

Tests the station metadata types defined in
:mod:`postprocess.sources.bom.types`.
"""

import pytest

from postprocess.sources.bom.types import BOMStationBase, BOMStationRecord


class TestBOMStationRecord:
    """Tests for :class:`BOMStationRecord`."""

    @pytest.mark.parametrize(
        "values",
        [
            (
                86071,
                "VIC",
                "Melbourne",
                "1855",
                "20240101",
                -37.84,
                144.98,
                "GPS",
                "VIC",
                25.0,
                1.5,
                94866,
            ),
            (
                94510,
                "QLD",
                "Brisbane",
                "20000101",
                "99999999",
                -27.47,
                153.03,
                "Unknown",
                "QLD",
                None,
                None,
                None,
            ),
        ],
    )
    def test_fields(self, values):
        """Store and expose the supplied station record fields."""
        assert BOMStationRecord(*values) == values


class TestBOMStationBase:
    """Tests for :class:`BOMStationBase`."""

    @pytest.mark.parametrize(
        "station_id,name,latitude,longitude,state,elevation_m",
        [
            (86071, "Melbourne", -37.84, 144.98, "VIC", 25.0),
            (94510, "Brisbane", -27.47, 153.03, "QLD", None),
            ("12345", "Example", 0.0, 0.0, "NSW", 100.0),
        ],
    )
    def test_fields(
        self,
        station_id,
        name,
        latitude,
        longitude,
        state,
        elevation_m,
    ):
        """Expose the supplied station metadata."""
        station = BOMStationBase(
            station_id,
            name,
            latitude,
            longitude,
            state,
            elevation_m,
        )

        assert (
            station.station_id,
            station.name,
            station.latitude,
            station.longitude,
            station.state,
            station.elevation_m,
            station.coordinates,
        ) == (
            station_id,
            name,
            latitude,
            longitude,
            state,
            elevation_m,
            (latitude, longitude),
        )

    def test_elevation_defaults_to_none(self):
        """Default elevation_m to None when it is omitted."""
        station = BOMStationBase(
            86071,
            "Melbourne",
            -37.84,
            144.98,
            "VIC",
        )

        assert station.elevation_m is None
