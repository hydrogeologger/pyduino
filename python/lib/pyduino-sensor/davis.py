"""This is a wrapper for Davis Weather Instruments Sensors.

Dependencies:
- gpiozero : Used by PulseDeviceBase
"""

import time as _time

from .base.input_devices import PulseDeviceBase
# Expose classes from post to this module namespace
from .post.wind import WindDirection  # pylint: disable=unused-import

# Python 2/3 compatibility imports
# for time.monotonic() to time.time()
# if sys.version_info <= (3,3):
#     monotonic = time


class Rain(PulseDeviceBase):
    """A Class to represent a Davis Tipping Bucket Rain Gauge.

    Attributes:
        name (str): Name of sensor.
        debug (bool): Debugging mode flag.

    Methods:

    In addition of `PulseDeviceBase()` methods

    - `get_cumulative()`:
            Getter for cumulative rain in millilitres (mm).
    """

    def __init__(self, name, pin, debounce=0.001, resolution=0.2, debug=False, **kwargs):
        # type:(str, int, float|None, float|None, bool|None, any) -> None
        """Constructs all the necessary attributes for the Davis Rain Tip Bucket object.

        Args:
            name (str): Name of sensor.
            pin (int): GPIO BCM pin to be attached to interrupt.
            debounce (float | None, optional): Debounce of pin in seconds.
                If None, no software bounce compensation will be performed.  
                Otherwise, this is the length of time (in seconds) that
                the component will ignore changes in state after an initial
                change. Defaults to 0.001.
            resolution (float, optional): Resolution of tip bucket in millimetres (mm).
                Defaults to 0.2.
            debug (bool, optional): Debuging mode flag. Defaults to False.
        """
        super(Rain, self).__init__(name, pin, debounce=debounce, debug=debug, **kwargs)
        self._resolution = resolution  # Resolution of each trigger

    @property
    def resolution(self):
        # type: () -> float
        """Getter for bucket resolution."""
        return self._resolution

    def get_cumulative(self, reset=True):
        # type: (bool) -> float
        """Getter for cumulative rain.

        Will reset counter

        Args:
            reset (bool, optional): Reset counter. Defaults to True.

        Returns:
            float: Cumulative rain in mililitres (mm).
        """
        cumulative_rain = self._count * self._resolution
        if reset:
            self.reset()
        return cumulative_rain


class WindSpeed(PulseDeviceBase):
    """A Class to represent a Davis Anemometer Wind Speed sensor.

    Attributes:
        name (str): Name of sensor.
        debug (bool): Debugging mode flag.

    Methods:

    In addition of `PulseDeviceBase()` methods.

    - `calculate_average()`:
            Calculate wind speed in km/hr.
    - `get_average()`:
            Getter for average wind speed in km/hr, will reset counter.
    """

    def __init__(self, name, pin, debounce=None, debug=False, **kwargs):
        # type: (str, int, float|None, bool|None, any) -> None
        """
        Constructs all the necessary attributes for the Davis Wind Anemometer Speed object.

        Args:
            name (str): Name of sensor.
            pin (int): GPIO BCM pin to be attached to interrupt.
            pull_up (bool, optional): GPIO pin state.  
                True: pin pulled high, False: pin pulled low. Defaults to True.
            debounce (float | None, optional): Debounce of pin in seconds.
                If None, no software bounce compensation will be performed.  
                Otherwise, this is the length of time (in seconds) that
                the component will ignore changes in state after an initial
                change. Defaults to None.
            debug (bool, optional): Debuging mode flag. Defaults to False.
        """
        super(WindSpeed, self).__init__(name, pin, debounce=debounce, debug=debug, **kwargs)
        self._last_elapsed = 0  # Reference to time since last measurement was reset

    def begin(self):
        """Start wind speed capture."""
        super(WindSpeed, self).begin()
        self.reset()

    def reset(self):
        """Reset counter and set timestamp."""
        super(WindSpeed, self).reset()
        try:
            self._last_elapsed = _time.monotonic()
        except AttributeError:
            self._last_elapsed = _time.time()

    def calculate_average(self, elapsed_time):
        # type: (float|int) -> float
        """Calculate average wind speed.

        Based on Davis tech document
            V = P*(2.25/T) the speed is in MPh

            P = no. of pulses per sample period

            T = sample period in seconds

        Args:
            elapsed_time (float | int): Elapsed time in seconds.

        Returns:
            float: Average wind speed in km/hr.
        """
        _MPH_2_KMH = 1.609  # mph to kmh  pylint: disable=invalid-name
        return self._count * (2.25 / elapsed_time) * _MPH_2_KMH

    def get_average(self, reset=True):
        # type: (bool) -> float
        """Getter for average wind speed.

        Counter reset dependant on reset argument.

        Args:
            reset (bool, optional): Reset counter. Defaults to True.

        Returns:
            float: Average wind speed (km/hr).
        """
        try:
            elapsed_time = _time.monotonic() - self._last_elapsed
        except AttributeError:
            elapsed_time = _time.time() - self._last_elapsed
        average_speed = self.calculate_average(elapsed_time)
        if reset:
            self.reset()
        return average_speed
