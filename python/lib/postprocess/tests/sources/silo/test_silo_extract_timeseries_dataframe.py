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
        silo.extract_timeseries_dataframe(point_data,)


def test_empty_point_data_raises_value_error():
    """Raise ValueError when point data is empty."""
    with pytest.raises(ValueError, match="Empty data!"):
        silo.extract_timeseries_dataframe({})


def test_missing_timeseries_data_raises_key_error():
    """Raise KeyError when the response has no timeseries data."""
    with pytest.raises(KeyError, match="Missing timeseries data."):
        silo.extract_timeseries_dataframe({"data": []})


def test_extracts_timeseries_dataframe():
    """Convert SILO timeseries data into a DataFrame with MultiIndex columns."""
    point_data = {
        "data": [
            {
                "date": "20200101",
                "variables": [
                    {
                        "variable_code": "R",
                        "source": "observed",
                        "value": 10.5,
                    },
                    {
                        "variable_code": "X",
                        "source": "observed",
                        "value": 30.2,
                    },
                ],
            },
            {
                "date": "20200102",
                "variables": [
                    {
                        "variable_code": "R",
                        "source": "observed",
                        "value": 5.2,
                    },
                    {
                        "variable_code": "X",
                        "source": "estimated",
                        "value": 31.7,
                    },
                ],
            },
        ]
    }

    result = silo.extract_timeseries_dataframe(point_data)

    expected = pd.DataFrame(
        {
            ("R", "observed"): [10.5, 5.2],
            ("X", "observed"): [30.2, None],
            ("X", "estimated"): [None, 31.7],
        },
        index=pd.to_datetime(["20200101", "20200102"]),
    )
    expected.index.name = "date"
    expected.columns = pd.MultiIndex.from_tuples(
        expected.columns,
        names=["variable", "source"],
    )

    pd.testing.assert_frame_equal(result, expected)
