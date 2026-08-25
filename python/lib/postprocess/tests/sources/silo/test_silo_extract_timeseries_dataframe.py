"""Tests for the SILO ``extract_timeseries_dataframe`` function."""

import pandas as pd
import pytest

from postprocess.sources import silo


@pytest.mark.parametrize(
    "point_data",
    [None, [], (), "not a dict", 123],
)
def test_point_data_must_be_dict(point_data):
    """Raise TypeError when the API response is not a dictionary."""
    with pytest.raises(TypeError, match="`point_data` must be a dictionary"):
        silo.dataframe_from_data(point_data,)


def test_empty_point_data_raises_value_error():
    """Raise ValueError when point data is empty."""
    with pytest.raises(ValueError, match="Empty data!"):
        silo.dataframe_from_data({})


def test_missing_timeseries_data_raises_key_error():
    """Raise KeyError when the response has no timeseries data."""
    with pytest.raises(KeyError, match="Missing timeseries data."):
        silo.dataframe_from_data({"data": []})


def test_extracts_timeseries_dataframe():
    """Convert SILO timeseries data into a DataFrame with MultiIndex columns."""
    point_data = {
        "data": [
            {
                "date": "2010-01-01",
                "variables": [
                    {
                        "source": 0,
                        "value": 4.0,
                        "variable_code": "daily_rain"
                    },
                    {
                        "source": 25,
                        "value": 22.2,
                        "variable_code": "max_temp"
                    }
                ]
            },
            {
                "date": "2010-01-02",
                "variables": [
                    {
                        "source": 0,
                        "value": 1.6,
                        "variable_code": "daily_rain"
                    },
                    {
                        "source": 25,
                        "value": 16.1,
                        "variable_code": "max_temp"
                    }
                ]
            },
        ]
    }

    result = silo.dataframe_from_data(point_data, include_source=True)

    expected = pd.DataFrame(
        {
            ('daily_rain', 'value'): {'2010-01-01': 4.0, '2010-01-02': 1.6},
            ('daily_rain', 'source'): {'2010-01-01': 0, '2010-01-02': 0},
            ('max_temp', 'value'): {'2010-01-01': 22.2, '2010-01-02': 16.1},
            ('max_temp', 'source'): {'2010-01-01': 25, '2010-01-02': 25}
        },
    )
    expected.index = pd.to_datetime(expected.index)
    expected.index.name = "date"
    expected.columns.names = ["variable", "property"]

    pd.testing.assert_frame_equal(result, expected)
