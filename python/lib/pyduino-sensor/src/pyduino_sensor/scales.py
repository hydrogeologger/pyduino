"""This module provides helper functions to communicate with Scale devices.

Dependencies:
- pyserial : Used for serial communication.
"""

import time as _time
from collections import namedtuple as _namedtuple

from serial import Serial as _Serial

from .base.sensor import SensorBase


class OhausScale(SensorBase):
    """A Class to represent an Ohaus Scale with serial interface.

    Attributes:
        name (str): Name of sensor.
        debug (bool): Debugging mode flag.

    Methods:

    In addition of `SensorBase()` methods.

    - `get_weight()`:
            Get weight reading from scale.
    """

    def __init__(self, name, port, baudrate=9600, timeout=10, **kwargs):
        # type: (str, str, int, int|float, any) -> None
        """Constructs all the necessary attributes for Ohaus Scale object.

        Args:
            name (_type_): User given name.
            port (_type_): Serial Port.
            baudrate (int, optional): _description_. Defaults to 9600.
            timeout (int, optional): _description_. Defaults to 10.

         Keyword Args:
            debug (bool, optional): Debuging mode flag. Defaults to False.
        """
        super(OhausScale, self).__init__(name, **kwargs)
        self._port = port
        """Scale Serial Port."""
        self._baudrate = baudrate
        """Scale Serial baudrate."""
        self._timeout = timeout
        """Scale Serial device timeout."""
        self._serial_obj = None
        """Scale Serial object."""

    def get_weight(self, max_tries=5, tolerance=2, delay=1, interval=1):
        # type: (int, float, float, float) -> tuple[int|float, str]
        """Get weight reading from scale, auto open and close serial device.

        Args:
            max_tries (int, optional): Maximum tries to read scale. Defaults to 5.
            tolerance (float, optional): Edge case reading resolution.
                Tolerance is ignored if max_tries=1. Defaults to 2.
            delay (float, optional): Delay post serial device initialization. Defaults to 1.
            interval (float, optional): Delay between serial write. Defaults to 1.

        Raises:
            errors.: Re-raise errors.
            RuntimeError: Exceeded maximum number of tries reading weight within tolerance.

        Returns:
            namedtuple(value, unit): Scale value and unit.
        """
        # pylint: disable-next=invalid-name
        Weight = _namedtuple("Weight", ["value", "unit"])
        attempt_count = 0  # Attempts counter
        old_weight = -999  # Last value read
        new_weight = -999  # Reference to new scale value
        max_tries = max(max_tries, 1)
        delay = max(delay, 0)
        interval = max(interval, 0)

        try:
            self._serial_obj = _Serial(port=self._port, baudrate=self._baudrate,
                                       timeout=self._timeout)
            if delay > 0:
                _time.sleep(delay)
            while attempt_count <= max_tries:
                attempt_count += 1
                self._serial_obj.flushInput()
                self._serial_obj.write('IP\r\n')
                str_scale = self._serial_obj.readline().strip('\x00')
                try:
                    new_weight = float(str_scale.split()[0].strip('\x00'))
                    if new_weight.is_integer():
                        new_weight = int(new_weight)
                    scale_unit = str_scale.split()[1].strip('\x00')
                    if max_tries == 1 or abs(new_weight - old_weight) <= tolerance:
                        return Weight(new_weight, scale_unit)
                    old_weight = new_weight
                except ValueError as error:
                    if attempt_count <= max_tries:
                        pass
                    else:
                        raise error
                if interval > 0:
                    _time.sleep(interval)
        except Exception as error:
            raise error
        finally:
            try:
                if self._serial_obj.isOpen():
                    self._serial_obj.close()
            except (NameError, AttributeError):
                pass
        raise RuntimeError("Exceeded maximum number of tries.")
