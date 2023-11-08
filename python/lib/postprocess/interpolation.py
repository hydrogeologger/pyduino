#!/usr/bin/env python
"""Post processing interpolation module.

Provides interpolation class and functions to support interpolation of pandas \
    dataframe objects.
"""

__all__ = ["Interpolation"]


from datetime import (datetime, timedelta) # TypeHinting pylint: disable=unused-import
import pandas
import matplotlib.pyplot as plt

# Package modules
from .extern import interpolate as wf

# Python 2 Compatibility
# pylint: disable=consider-using-f-string

def _versiontuple(v):
    return tuple(map(int, (v.split("."))))

# Compatilibity imports
if _versiontuple(pandas.__version__)[:2] == (0, 24):
    # pandas version  0.24.2 requires
    from pandas.plotting import register_matplotlib_converters
    register_matplotlib_converters()


class Interpolation():
    """Represents an interpolation object."""
    def __init__(self,
                 start_time,  # type: datetime|int|float
                 end_time,    # type: datetime|int|float
                 interval,    # type: timedelta|int|float
                 data=None    # type: pandas.DataFrame|pandas.Series
                 ): # type: (...) -> None
        """
        Generator for Interpolation object.

        Args:
            start_time (datetime | int | float): Start time of interpolation \
                range. Accepts datetime or time in seconds.
            end_time (datetime | int | float): Stop time of interpolation range. \
                Accepts datetime or time in seconds.
            interval (timedelta | int |float): Interval between timestamps (period). \
                Accepts timedelta or time in seconds.
            data (DataFrame | Series, optional): Data for interpolation to be \
                performed on. Defaults to None.

        Raises:
            TypeError: Data provided is not of type DataFrame or Series
        """
        if isinstance(data, (type(None), pandas.Series, pandas.DataFrame)):
            self._input_data = data
        else:
            raise TypeError("data attribute expects DataFrame or Series.")
        if isinstance(interval, timedelta):
            interval = interval.total_seconds()
        interpolated_date_time = pandas.date_range(
            start = start_time,
            end = end_time,
            freq = pandas.Timedelta(interval, unit="s"),
            name = "date_time",
        )
        self.df = pandas.DataFrame(interpolated_date_time)
        self.df["time_days"] = (self.df["date_time"] - self.df["date_time"][0]).astype(
                "timedelta64[s]") / 86400.0
        self.df.set_index("date_time", inplace=True, drop=True)

    def __str__(self):
        return str(self._input_data)

    def interpolate_smooth(self,
                           data=None, # type: pandas.DataFrame|pandas.Series|None
                           key_name=None, # type: str|dict[str,str]|None
                           coef=1e-14, # type: float|int|None
                           preview=False, # type: bool
                           rm_nan=True, # type: bool
                           ): # type: (...) -> None
        """
        Performs a smooth spline interpolation.

        Args:
            data (DataFrame | Series, optional): Data for interpolation to be \
                performed on if Interpolation object not initialized with data. \
                Defaults to None.
            key_name (str | dict[str,str], optional): key of DataFrame to
                perform interpolation on, not required for Series. Provide a \
                dictionatry {"oldkey" : "newkey"} to rename the column heading. \
                Defaults to None.
            coef (float | int, optional): Smoothing parameter between 0 and 1. \
                '0' -> LS-straight line. '1' -> cubic spline \
                interpolant. Defaults to 1e-14.
            preview (bool, optional): Preview plot of interpolated data \
                with original. Defaults to False.
            rm_nan (bool, optional): Removes not a number "NaN" values. Defaults to True.

        Raises:
            TypeError: Data provided is not of type DataFrame or Series
            RuntimeError: No data given if Interpolation object not initialized \
                with data.
            RuntimeError: No key_name given if data is DataFrame.
        """
        if data is None:
            if self._input_data is not None:
                data = self._input_data
            else:
                raise RuntimeError("Data is required as Interpolation object "
                                   "not initially initialized with data.")

        if isinstance(data, (pandas.Series, pandas.DataFrame)):
            # Get name of new key name
            if isinstance(key_name, dict):
                key_name, key_new_name = key_name.popitem()

            # Determine x-axis data from DataFrame or Series
            if isinstance(data.index, pandas.MultiIndex):
                input_x = data.index.get_level_values(level=0)
            else:
                input_x = data.index

            # Determine y-axis data from DataFrame or Series
            if isinstance(data, pandas.DataFrame):
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
        else:
            raise TypeError("data attribute expects DataFrame or Series.")

        x = input_x - input_x[0]
        # http://stackoverflow.com/questions/14920903/time-difference-in-seconds-from-numpy-timedelta64
        if isinstance(x, pandas.TimedeltaIndex):
            x = x.total_seconds()
        y = input_y

        # TO181023 making sure that we can name a new string
        # https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops
        if rm_nan:
            mask_idx = input_y.isnull()
            x = x[~mask_idx]
            y = y[~mask_idx]

        # warning, it is found that the Smoothspline is dependent on the x axis!!!
        interp_method = wf.SmoothSpline(xx = x, yy = y, p = coef)

        # Determine interpreted timestamp in seconds for smoothspline
        # if input_x.is_numeric():
        #     self.date_time_interpolated = self.date_time_interpolated.astype(np.int64) // 10**9
        x_interp = self.df.index - input_x[0]
        if isinstance(x_interp, pandas.TimedeltaIndex):
            x_interp = x_interp.total_seconds()

        self.df[key_new_name] = interp_method(x_interp)

        if preview:
            fig = plt.figure()
            fig.subplots_adjust(bottom=0.2)
            # fig.canvas.set_window_title('Interpolate ' + key_name)
            plt.plot(input_x, input_y,'b+', markersize=15)
            plt.plot(self.df.index, self.df[key_new_name],'r-')
            if key_new_name and key_name.lower() != key_new_name.lower():
                title = 'Interpolated "{}" ({}) result, coef={}'.format(
                        key_name, key_new_name, coef)
            else:
                title = 'Interpolated "{}" result, coef={}'.format(
                        key_name, coef)
            plt.title(title)
            plt.xticks(rotation=45)
            plt.show(block=False)

    def swap_index(self):
        """Swap DataFrame index between "date_time" and "time_days"."""
        if "time_days" in self.df.columns:
            key_name = "time_days"
        elif "date_time" in self.df.columns:
            key_name = "date_time"
        else:
            print("Interpolationg Index Swap: No swappable index and columns identified")
            return
        self.df.reset_index(inplace=True, drop=False)
        self.df.set_index(keys=key_name, inplace=True, drop=True)
