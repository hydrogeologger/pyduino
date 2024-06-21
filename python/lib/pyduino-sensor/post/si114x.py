"""This module contains post processing functions for SI114X sensors."""

from ..base.sensor import SensorBase


class SI114X(SensorBase):
    """A Class to represent a Si1145/46/47 Ultraviolet (UV) Index, Gesture, Proximity,
    and Ambient Light sensor.

    Attributes:
        name (str): Name of sensor.
        debug (bool): Debugging mode flag.

    Methods:

    In addition of `SensorBase()` methods.
    """

    def __init__(self, name, **kwargs):
        # type: (str, bool|None, any) -> None
        """Constructs all the necessary attributes for Si1145/46/47 sensor object.

        Args:
            name (str): Name of sensor.

        Keyword Args:
            debug (bool, optional): Debuging mode flag. Defaults to False.
        """
        super(SI114X, self).__init__(name, **kwargs)

    @staticmethod
    def ir_intensity(adc, gain=1, high_range=True):
        # type: (int, int|float, bool) -> int|float
        """Converts Silicon Lab Si1145/46/47 ADC value to intensity (W/m^2).

        Args:
            adc (int): ADC reading from registers.
            gain (int|float, optional): ADC gain multiplier (1–128), bit-aligned. Defaults to 1.
            high_range (bool, optional): High signal range mode, i.e for direct sunlight.
                Defaults to True.

        Returns:
            (float): Intensity (W/m^2).
        """
        return SI114X.calculate(adc=adc, typical=452.38,
                                gain=gain, range_factor=SI114X._range_factor(high_range))

    @staticmethod
    def vis_intensity(adc, gain=1, high_range=True):
        # type: (int, int|float, bool) -> int|float
        """Converts Silicon Lab Si1145/46/47 ADC value to intensity (W/m^2).

        Args:
            adc (int): ADC reading from registers.
            gain (int|float, optional): ADC gain multiplier (1–128), bit-aligned. Defaults to 1.
            high_range (bool, optional): High signal range mode, i.e for direct sunlight.
                Defaults to True.

        Returns:
            (float): Intensity (W/m^2).
        """
        return SI114X.calculate(adc=adc, typical=8.277,
                                gain=gain, range_factor=SI114X._range_factor(high_range))

    @staticmethod
    def calculate_uv_index(value):
        # type: (int|float) -> float
        """Converts Silicon Lab Si1145/46/47 UV reading to UV Index.

        Args:
            value (int): ADC reading from registers.

        Returns:
            (float): UV Index (unitless).
        """
        # The index is multiplied by 100 as read from SI1145 registers,
        # so to get the integer index, divide by 100!
        return value / 100.0

    @staticmethod
    def calculate(adc, typical, range_factor=1.0, gain=1):
        # type: (int|float, float|int, float|int, int|float) -> float|int
        """Transform Silicon Lab Si1145/46/47 ADC value to another unit.

        Args:
            adc (int|float): ADC values as read from register.
            typical (float|int): Typical value for unit conversion.
            range_factor (float|int, optional): Range scaling factor for ADC. Defaults to 1.
                - 1.0 for normal range mode
                - 14.5 for high range mode
            gain (int|float, optional): ADC gain multiplier (1–128), bit-aligned value,
                used for conversion of raw ADC values. Defaults to 1.

        Returns:
            (float): User decided unit.
        """
        return (adc * range_factor) / (typical * gain)

    @staticmethod
    def _range_factor(high_range):
        # type: (bool) -> float
        """Returns Si1145/46/47 range scaling factor.

        Args:
            high_range (bool): True if high range mode is enabled, otherwise False.

        Returns:
            float: 14.5 when high_range is True, otherwise 1.0.
        """
        return 14.5 if high_range else 1.0
