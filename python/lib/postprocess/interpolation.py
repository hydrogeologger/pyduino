"""Post processing interpolation module.

Provides interpolation class and functions to support interpolation of pandas
dataframe objects.

Dependencies:
- matplotlib
- numpy
- pandas
"""

__all__ = ["Interpolation"]


# TypeHinting
from datetime import datetime as _datetime
from datetime import timedelta as _timedelta
from warnings import warn as _warn

import matplotlib.pyplot as _plt
import pandas as _pd

# Package modules
from . import pandas_ext as _pandas_ext
from .extern import interpolate as _wf

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
                 start_time,  # type: _datetime|int|float
                 end_time,    # type: _datetime|int|float
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
            RuntimeError: No data provided for interpolation, either
                during initialization or during interpolation.
            RuntimeError: No key_name given if data is DataFrame.
        """
        if data is None and self.ref_data is not None:
            data = self.ref_data
        else:
            raise RuntimeError("No data provided for interpolation, either \
                during initialization or during interpolation.")

        if not isinstance(data, (_pd.Series, _pd.DataFrame)):
            raise TypeError("data expects DataFrame or Series.")

        # Get name of new key
        if isinstance(key_name, dict):
            key_name, key_new_name = key_name.popitem()

        # Determine x-axis data from DataFrame or Series
        if isinstance(data.index, _pd.MultiIndex):
            input_x = data.index.get_level_values(level=0)
        else:
            input_x = data.index

        # Determine y-axis data from DataFrame or Series
        if isinstance(data, _pd.DataFrame):
            if len(data.columns) > 1:
                if not key_name:
                    raise RuntimeError("key_name not specified.")
                input_y = data[key_name]
            else:
                input_y = data.iloc[:, 0]
        else:
            input_y = data

        # Set key names if declared
        if not key_name:
            key_name = input_y.name
        key_new_name = key_name

        x = input_x - input_x[0]
        # http://stackoverflow.com/questions/14920903/time-difference-in-seconds-from-numpy-timedelta64
        if isinstance(x, _pd.TimedeltaIndex):
            x = x.total_seconds()
        y = input_y

        # TO181023 making sure that we can name a new string
        # https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops
        if rm_nan:
            mask_idx = input_y.isnull()
            x = x[~mask_idx]
            y = y[~mask_idx]

        # warning, it is found that the Smoothspline is dependent on the x axis!!!
        interp_method = _wf.SmoothSpline(xx=x, yy=y, p=coef)

        # Determine interpreted timestamp in seconds for smoothspline
        # if input_x.is_numeric():
        #     self.date_time_interpolated = self.date_time_interpolated.astype(np.int64) // 10**9
        x_interp = self.df.index - input_x[0]
        if isinstance(x_interp, _pd.TimedeltaIndex):
            x_interp = x_interp.total_seconds()

        self.df[key_new_name] = interp_method(x_interp)

        if preview:
            fig = _plt.figure()
            fig.subplots_adjust(bottom=0.2)
            # fig.canvas.set_window_title('Interpolate ' + key_name)
            _plt.plot(input_x, input_y, 'b+', markersize=15)
            _plt.plot(self.df.index, self.df[key_new_name], 'r-')
            if key_new_name and key_name.lower() != key_new_name.lower():
                title = 'Interpolated "{}" ({}) result, coef={}'.format(
                        key_name, key_new_name, coef)
            else:
                title = 'Interpolated "{}" result, coef={}'.format(
                        key_name, coef)
            _plt.title(title)
            _plt.xticks(rotation=45)
            _plt.show(block=False)

    def swap_index(self):
        # type: (...) -> (str|bool)
        """Swap DataFrame index between "date_time" and "time_days".

        Returns:
            str or bool: Returns new index key name. False otherwise.
        """
        if _pandas_ext.swap_index(self.df, keys="time_days"):
            return "time_days"
        if _pandas_ext.swap_index(self.df, keys="date_time"):
            return "date_time"

        _warn("Interpolationg Index Swap: No swappable index and columns identified.",
              category=RuntimeWarning)
        return False
