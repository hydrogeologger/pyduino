# test_tb_pandas.py
# pylint: disable=protected-access, missing-function-docstring, missing-module-docstring
import pandas as pd

from thingsboard_api import tb_pandas


def test_no_change_for_unique_single_level_index():
    # Test when no levels need to be dropped
    arrays = [['A', 'B', 'C']]
    index = pd.MultiIndex.from_arrays(arrays)
    df = pd.DataFrame([[1, 2, 3]], columns=index)

    # Process the DataFrame
    tb_pandas.unique_column_headings_only(df)

    # Assert that columns haven't changed
    assert df.columns.equals(index)


def test_no_change_for_single_column_multiindex():
    # Test when no levels need to be dropped
    arrays = [['A'], ['foo']]
    multi_col = pd.MultiIndex.from_arrays(arrays)
    df = pd.DataFrame([[42]], columns=multi_col)

    # Process the DataFrame
    tb_pandas.unique_column_headings_only(df)

    # Assert that columns haven't changed
    assert df.columns.equals(multi_col)


def test_drop_value_for_single_column_multiindex():
    # Test when second level need to be dropped
    # Create a DataFrame with a 2-level MultiIndex where the second level is 'value'
    arrays = [['A'], ['value'], ['x']]
    index = pd.MultiIndex.from_arrays(arrays)
    df = pd.DataFrame([[42]], columns=index)

    # Process the DataFrame
    tb_pandas.unique_column_headings_only(df)

    # The expected columns should drop the 'values' level and keep only the 'letters' level
    expected_columns = pd.MultiIndex.from_arrays([['A'], ['x']])

    # Assert that the columns have been changed correctly (second level dropped)
    assert df.columns.equals(
        expected_columns), f"Expected {expected_columns}, but got {df.columns}"


def test_drop_level_when_condition_met():
    # Test when the level is dropped (e.g., when header_size <= 1)
    arrays = [['A', 'A', 'A'], ['foo', 'bar', 'foo']]
    index = pd.MultiIndex.from_arrays(arrays)
    df = pd.DataFrame([[1, 2, 3]], columns=index)

    # Process the DataFrame
    tb_pandas.unique_column_headings_only(df)

    # The result should be a single-level index with the 'letters' level
    expected_columns = pd.Index(['foo', 'bar', 'foo'])
    # Assert that the columns have been changed correctly (second level dropped)
    assert df.columns.equals(
        expected_columns), f"Expected {expected_columns}, but got {df.columns}"


def test_drop_multiple_levels():
    # Test when multiple levels are dropped from MultiIndex
    arrays = [['A', 'A', 'B', 'B'], ['A', 'A', 'A', 'A'], [
        'B', 'B', 'B', 'B'], ['foo', 'bar', 'foo', 'bar']]
    index = pd.MultiIndex.from_arrays(arrays)
    df = pd.DataFrame([[1, 2, 3, 4]], columns=index)

    # Process the DataFrame
    tb_pandas.unique_column_headings_only(df)

    # The result should be a single-level index, 'letters', after dropping the 'values' level
    expected_columns = pd.MultiIndex.from_arrays(arrays[i] for i in [0, 3])
    # Assert that the columns have been changed correctly (second level dropped)
    assert df.columns.equals(
        expected_columns), f"Expected {expected_columns}, but got {df.columns}"


def test_drop_level_when_value_is_in_header():
    # Test when the 'value' header is in one of the levels (specific condition)
    arrays = [['A', 'A', 'B', 'B'], ['value', 'value', 'value', 'value']]
    index = pd.MultiIndex.from_arrays(arrays)
    df = pd.DataFrame([[1, 2, 3, 4]], columns=index)

    # Process the DataFrame
    tb_pandas.unique_column_headings_only(df)

    # The 'values' level should be dropped because 'value' is in the header
    expected_columns = pd.Index(['A', 'A', 'B', 'B'])
    assert df.columns.equals(
        expected_columns), f"Expected {expected_columns}, but got {df.columns}"
