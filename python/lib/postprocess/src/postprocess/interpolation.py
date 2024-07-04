"""Post processing interpolation module.

Provides interpolation class and functions to support interpolation of pandas
dataframe objects.

Dependencies:
- matplotlib
- numpy
- pandas
"""

__all__ = ["Interpolation"]


import warnings as _warnings
from datetime import timedelta as _timedelta
from typing import TYPE_CHECKING

import matplotlib.pyplot as _plt
import numpy as _np
import pandas as _pd

# Package modules
from . import pandas_utils as _pandas_utils
from .extern import interpolate as _wf

if TYPE_CHECKING:
    from datetime import (
        datetime,
    )

# Python 2 Compatibility
# pylint: disable=consider-using-f-string


def _versiontuple(v):
    return tuple(map(int, (v.split("."))))


# Compatilibity imports
if _versiontuple(_pd.__version__)[:2] == (0, 24):
    # pandas version 0.24.2 requires manual modifying of global matplotlib.units.registry
    _pd.plotting.register_matplotlib_converters()


class Interpolation():
    """Represents an interpolation object.

    Attributes:
        ref_data (DataFrame|Series): Reference to primary data used for interpolation.
        df (DataFrame): Reference to DataFrame for interpolated data storage.
    """

    def __init__(self,
                 start_time,  # type: datetime|int|float
                 end_time,    # type: datetime|int|float
                 interval,    # type: _timedelta|int|float
                 ref_data=None  # type: _pd.DataFrame|_pd.Series|None
                 ):  # type: (...) -> None
        """Generator for Interpolation object.

        Args:
            start_time (datetime | int | float): Start time of interpolation
                range. Accepts datetime or time in seconds.
            end_time (datetime | int | float): Stop time of interpolation range.
                Accepts datetime or time in seconds.
            interval (timedelta | int | float): Interval between timestamps (period).
                Accepts timedelta or time in seconds.
            ref_data (DataFrame | Series, optional): Reference data to be
                used for interpolation, able to be overriden at interpolation
                method calls. Defaults to None.

        Raises:
            TypeError: Data provided is not of type DataFrame or Series.
            ValueError: Incorrect elapsed time unit attribute.
        """
        if isinstance(ref_data, (type(None), _pd.Series, _pd.DataFrame)):
            self.ref_data = ref_data
            """Reference to primary data used for interpolation by instance (`DataFrame|Series`)."""
        else:
            raise TypeError("ref_data expects DataFrame or Series.")

        # Generate DataFrame for interpolated data storage
        if isinstance(interval, _timedelta):
            interval = interval.total_seconds()
        interpolated_date_time = _pd.date_range(
            start=start_time,
            end=end_time,
            freq=_pd.Timedelta(interval, unit="s"),
            name="date_time",
        )
        self.df = _pd.DataFrame(interpolated_date_time)
        """Reference to dataframe interpolated data is stored (`DataFrame`)."""

        # Add elapsed time column
        self.df["time_days"] = (self.df["date_time"] -
                                self.df["date_time"][0]).astype("timedelta64[s]")

        self.df.set_index("date_time", inplace=True, drop=True)

    def __str__(self):
        return str(self.ref_data)

    def interpolate_smooth(self,
                           data=None,  # type: _pd.DataFrame|_pd.Series|None
                           key_name=None,  # type: str|dict[str,str]|None
                           coef=1e-14,  # type: float|int|None
                           preview=False,  # type: bool|None
                           rm_nan=True,  # type: bool|None
                           ):  # type: (...) -> None
        """Performs a smooth spline interpolation.

        Args:
            data (DataFrame | Series, optional): Data for interpolation to be
                performed on. Defaults to None.
            key_name (str | dict[str,str], optional): key of DataFrame to
                perform interpolation on, not required for Series.
                Provide a dictionatry {"oldkey" : "newkey"} to rename the column
                heading. Defaults to None.
            coef (float | int, optional): Smoothing parameter between 0 and 1.
                '0' -> LS-straight line. '1' -> cubic spline
                interpolant. Defaults to 1e-14.
            preview (bool, optional): Preview plot of interpolated data
                with original. Defaults to False.
            rm_nan (bool, optional): Removes not a number "NaN" values. Defaults to True.

        Raises:
            TypeError: Data provided is not of type DataFrame or Series.
            ValueError: If no data is provided either during initialization or 
                when calling the method.
            ValueError: If `key_name` is not specified when a multi-column 
                DataFrame is provided as input.
        """
        if data is None:
            if self.ref_data is None:
                raise ValueError(
                    "No data provided for interpolation. Please supply data "
                    "either during initialization or when calling the method."
                )
            data = self.ref_data

        if not isinstance(data, (_pd.Series, _pd.DataFrame)):
            raise TypeError("data expects DataFrame or Series.")

        # Handle key_name configuration (support for string or mapping dictionary)
        column_name = key_name
        output_column_name = None
        if isinstance(column_name, dict):
            column_name, output_column_name = column_name.popitem()

        # Determine raw x-axis data from DataFrame or Series index
        if isinstance(data.index, _pd.MultiIndex):
            raw_x = data.index.get_level_values(level=0)
        else:
            raw_x = data.index

        # Determine raw y-axis data from DataFrame or Series
        if isinstance(data, _pd.DataFrame):
            if len(data.columns) > 1:
                if not column_name:
                    raise ValueError(
                        "A `key_name` must be specified when using a multi-column DataFrame."
                    )
                raw_y = data[column_name]
            else:
                raw_y = data.iloc[:, 0]
        else:
            raw_y = data

        # Set key names if declared
        if not column_name:
            column_name = raw_y.name
        if not output_column_name:
            output_column_name = column_name

        # Normalize x-axis (starting from 0) and handle Timedeltas
        x_normalized = raw_x - raw_x[0]
        # http://stackoverflow.com/questions/14920903/time-difference-in-seconds-from-numpy-timedelta64
        if isinstance(x_normalized, _pd.TimedeltaIndex):
            x_normalized = x_normalized.total_seconds()
        y_values = raw_y

        # TO181023 making sure that we can name a new string
        # https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops
        # Remove NaN values if requested
        if rm_nan:
            nan_mask = raw_y.isnull()
            x_normalized = x_normalized[~nan_mask]
            y_values = y_values[~nan_mask]

        # Fit the smoothing spline and compute target values
        #! warning, it is found that the Smoothspline is dependent on the x axis!!!
        interpolator = _wf.SmoothSpline(xx=x_normalized, yy=y_values, p=coef)

        # Determine interpreted timestamp in seconds for smoothspline
        # if input_x.is_numeric():
        #     self.date_time_interpolated = self.date_time_interpolated.astype(np.int64) // 10**9
        x_target = self.df.index - raw_x[0]
        if isinstance(x_target, _pd.TimedeltaIndex):
            x_target = x_target.total_seconds()

        self.df[output_column_name] = interpolator(x_target)

        # Optional preview plot
        if preview:
            min_marker_size, max_marker_size = 1, 15
            n = len(raw_x)

            # Soft decay scaling
            decay_rate = 0.005
            marker_size_scaled = min_marker_size + \
                (max_marker_size - min_marker_size) / (1 + decay_rate * n)

            fig, ax = _plt.subplots(
                figsize=(10, 5.625),
            )
            ax.plot(
                raw_x, raw_y,
                ".",
                label="Original Data",
                markersize=_np.clip(
                    a=marker_size_scaled,
                    a_min=min_marker_size,
                    a_max=max_marker_size,
                ),
                alpha=0.7,
            )
            ax.plot(
                self.df.index, self.df[output_column_name],
                "-",
                label="Interpolated ({})".format(
                    output_column_name,
                ),
                color="red",
            )

            if output_column_name and column_name.lower() != output_column_name.lower():
                title = 'Smooth Spline Interpolation: "{}" ({}) result, coef={}'.format(
                        column_name, output_column_name, coef)
            else:
                title = 'Smooth Spline Interpolation: "{}" result, coef={}'.format(
                        column_name, coef)

            ax.set_title(title)
            ax.tick_params(axis='x', rotation=45)
            fig.subplots_adjust(bottom=0.2)
            _plt.show(block=False)

    def swap_index(self):
        # type: (...) -> (str|bool)
        """Swap DataFrame index between "date_time" and "time_days".

        Returns:
            str or bool: Returns new index key name. False otherwise.
        """
        if _pandas_utils.swap_index(self.df, keys="time_days"):
            return "time_days"
        if _pandas_utils.swap_index(self.df, keys="date_time"):
            return "date_time"

        _warnings.warn(
            "Interpolationg Index Swap: No swappable index and columns identified.",
            category=RuntimeWarning
        )
        return False
