"""Tests for the Open-Meteo ``extract_timeseries_dataframe`` function.

The tests cover timeseries extraction, timestamp conversion, timezone
handling, DataFrame structure, units, and validation of invalid or
incomplete API response data.
"""

import pandas as pd
import pytest

from postprocess.sources import openmeteo

VALID_POINT_DATA_EXAMPLE = {
    "latitude": -27.4705,
    "longitude": 153.0260,
    "generationtime_ms": 0.11897087097167969,
    "utc_offset_seconds": 36000,
    "timezone": "Australia/Brisbane",
    "timezone_abbreviation": "GMT+10",
    "elevation": 38,
    "hourly": {
        "time": [
            "2024-01-01T00:00",
            "2024-01-01T01:00",
        ],
        "temperature_2m": [25.1, 24.8],
        "precipitation": [0.0, 0.2],
    },
    "hourly_units": {
        "time": "iso8601",
        "temperature_2m": "°C",
        "precipitation": "mm",
    },
    "daily": {
        "time": [
            "2024-01-01",
            "2024-01-02",
        ],
        "temperature_2m_max": [31.2, 30.5],
        "temperature_2m_min": [22.1, 21.8],
    },
    "daily_units": {
        "time": "iso8601",
        "temperature_2m_max": "°C",
        "temperature_2m_min": "°C",
    },
}


@pytest.mark.parametrize(
    "point_data",
    [None, [], (), "not a dict", 123],
)
def test_point_data_must_be_dict(point_data):
    """Raise TypeError when the API response is not a dictionary."""
    with pytest.raises(TypeError, match="`point_data` must be a dictionary"):
        openmeteo.extract_timeseries_dataframe(point_data, "hourly")


@pytest.mark.parametrize(
    "freq",
    [
        "weekly",
        "monthly",
        "",
        None,
        123,
    ],
)
def test_invalid_frequency(freq):
    """Raise ValueError for unsupported frequencies."""
    with pytest.raises(ValueError, match="Invalid freq"):
        openmeteo.extract_timeseries_dataframe(VALID_POINT_DATA_EXAMPLE, freq)


@pytest.mark.parametrize(
    "freq",
    [
        "hourly", "HOURLY",
        "daily", "DAILY",
    ],
)
def test_valid_frequency(freq):
    """Test valid frequencies, should be case insensitive."""
    result = openmeteo.extract_timeseries_dataframe(VALID_POINT_DATA_EXAMPLE,
                                                    freq)
    assert isinstance(result, pd.DataFrame)


def test_extracts_hourly_dataframe():
    """Convert hourly API data into a timezone-aware DataFrame."""
    result = openmeteo.extract_timeseries_dataframe(VALID_POINT_DATA_EXAMPLE,
                                                    "hourly")

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2

    assert list(result.index) == [
        pd.Timestamp(
            "2024-01-01T00:00",
            tz="Australia/Brisbane",
        ),
        pd.Timestamp(
            "2024-01-01T01:00",
            tz="Australia/Brisbane",
        ),
    ]

    assert result[("temperature_2m", "°C")].tolist() == [25.1, 24.8]
    assert result[("precipitation", "mm")].tolist() == [0.0, 0.2]


def test_extracts_daily_dataframe():
    """Convert daily API data into a DataFrame."""
    result = openmeteo.extract_timeseries_dataframe(VALID_POINT_DATA_EXAMPLE,
                                                    "daily")

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert result.index.name == "time"

    assert result[("temperature_2m_max", "°C")].tolist() == [31.2, 30.5]
    assert result[("temperature_2m_min", "°C")].tolist() == [22.1, 21.8]


def test_columns_are_multiindex():
    """Store field names and units in a two-level MultiIndex."""
    point_data = {
        "timezone": "UTC",
        "hourly": {
            "time": ["2024-01-01T00:00"],
            "temperature_2m": [20.0],
            "wind_speed_10m": [15.0],
        },
        "hourly_units": {
            "time": "iso8601",
            "temperature_2m": "°C",
            "wind_speed_10m": "km/h",
        },
    }

    result = openmeteo.extract_timeseries_dataframe(point_data, "hourly")

    assert isinstance(result.columns, pd.MultiIndex)
    assert result.columns.names == ["field", "unit"]

    assert ("temperature_2m", "°C") in result.columns
    assert ("wind_speed_10m", "km/h") in result.columns


def test_missing_unit_gets_empty_string():
    """Use an empty string when a variable has no unit in the response."""
    point_data = {
        "timezone": "UTC",
        "hourly": {
            "time": ["2024-01-01T00:00"],
            "temperature_2m": [20.0],
        },
        "hourly_units": {
            "time": "iso8601",
        },
    }

    result = openmeteo.extract_timeseries_dataframe(point_data, "hourly")

    assert ("temperature_2m", "") in result.columns


def test_iso8601_gmt_is_utc_aware():
    """Convert GMT ISO 8601 timestamps into UTC-aware timestamps."""
    point_data = {
        "timezone": "GMT",
        "hourly": {
            "time": [
                "2024-01-01T00:00",
                "2024-01-01T01:00",
            ],
            "temperature_2m": [20.0, 21.0],
        },
        "hourly_units": {
            "time": "iso8601",
            "temperature_2m": "°C",
        },
    }

    result = openmeteo.extract_timeseries_dataframe(point_data, "hourly")

    assert result.index.tz is not None
    assert str(result.index.tz) == "UTC"


def test_unix_time_is_converted_to_timezone():
    """Convert Unix timestamps from UTC into the requested timezone."""
    point_data = {
        "timezone": "Australia/Brisbane",
        "hourly": {
            "time": [
                1704067200,
                1704070800,
            ],
            "temperature_2m": [25.0, 26.0],
        },
        "hourly_units": {
            "time": "unixtime",
            "temperature_2m": "°C",
        },
    }

    result = openmeteo.extract_timeseries_dataframe(point_data, "hourly")

    assert result.index[0] == pd.Timestamp(
        "2024-01-01T10:00:00+10:00"
    )
    assert result.index[1] == pd.Timestamp(
        "2024-01-01T11:00:00+10:00"
    )
    assert str(result.index.tz) == "Australia/Brisbane"


def test_missing_frequency_key():
    """Raise KeyError when the requested timeseries is absent."""
    point_data = {
        "timezone": "UTC",
        "daily": {},
        "daily_units": {},
    }

    with pytest.raises(KeyError, match="Missing 'hourly'"):
        openmeteo.extract_timeseries_dataframe(point_data, "hourly")


def test_missing_time_key():
    """Raise KeyError when the timeseries has no time field."""
    point_data = {
        "timezone": "UTC",
        "hourly": {
            "temperature_2m": [20.0],
        },
        "hourly_units": {
            "temperature_2m": "°C",
        },
    }

    with pytest.raises(KeyError, match="Missing 'time'"):
        openmeteo.extract_timeseries_dataframe(point_data, "hourly")


def test_mismatched_array_lengths_raise_value_error():
    """Raise ValueError when timeseries arrays have different lengths."""
    point_data = {
        "timezone": "UTC",
        "hourly": {
            "time": [
                "2024-01-01T00:00",
                "2024-01-01T01:00",
            ],
            "temperature_2m": [20.0],
        },
        "hourly_units": {
            "time": "iso8601",
            "temperature_2m": "°C",
        },
    }

    with pytest.raises(ValueError):
        openmeteo.extract_timeseries_dataframe(point_data, "hourly")


def test_invalid_datetime_raises_value_error():
    """Raise ValueError when timestamps cannot be parsed."""
    point_data = {
        "timezone": "UTC",
        "hourly": {
            "time": ["not-a-date"],
            "temperature_2m": [20.0],
        },
        "hourly_units": {
            "time": "iso8601",
            "temperature_2m": "°C",
        },
    }

    with pytest.raises(ValueError):
        openmeteo.extract_timeseries_dataframe(point_data, "hourly")
