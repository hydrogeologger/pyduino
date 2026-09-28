"""Tests for small test cases for :class:`StationFinder`."""


import pytest

from postprocess.sources.bom.cdio import (
    DWOStation,
    StationFinder,
)


@pytest.mark.parametrize(
    "record, expected",
    [
        (
            "3015_90035 Colac (Mt Gellibrand) VIC (112.2km away)    ",
            DWOStation(
                dwo_id=3015,
                station_id=90035,
                name="Colac (Mt Gellibrand)",
                state="VIC",
                distance_km=112.2,
                is_open=True,
            ),
        ),
        (
            "3103_85301 Yanakie VIC (149.9km away)",
            DWOStation(
                dwo_id=3103,
                station_id=85301,
                name="Yanakie",
                state="VIC",
                distance_km=149.9,
                is_open=False,
            ),
        ),
    ],
)
def test_returns_parsed_station(record, expected):
    """Parse a raw BOM DWO station record."""
    # pylint: disable-next=protected-access
    result = StationFinder._parse_dwo_station_record(record)

    assert result == expected
