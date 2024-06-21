"""This module contains post processing functions for SI114X sensors."""

from ..base.sensor import SensorBase


class SI114X(SensorBase):
    """A Class to represent a Si114x Ultraviolet (UV) Index, Gesture, Proximity,
    and Ambient Light sensor.

    Attributes:
        name (str): Name of sensor.
        debug (bool): Debugging mode flag.

    Methods:

    In addition of `SensorBase()` methods.
    """

    def __init__(self, name, high_range=True, **kwargs):
        # type: (str, bool|None, any) -> None
        """Constructs all the necessary attributes for Suction sensor object.

        Args:
            name (str): Name of sensor.
            high_range (bool, optional): Sensor configured to use high signal
                range ie. for direct sunlight. Defaults to True.

        Keyword Args:
            debug (bool, optional): Debuging mode flag. Defaults to False.
        """
        super(SI114X, self).__init__(name, **kwargs)
        # Gain modifier for low and high range mode
        self._gain = 1
        """Reference to gain multiplier of sensor."""
        if high_range:
            self._gain = 14.5

    def ir_intensity(self, adc):
        # type: (int|float) -> int|float
        """Converts Silicon Lab SI114X ADC value to intensity (W/m^2).

        Args:
            adc (int): ADC reading from SI114X registers.

        Returns:
            (int | float): Intensity (W/m^2).
        """
        return SI114X.calculate(adc=adc, gain=self._gain, typical=452.38)

    def vis_intensity(self, adc):
        # type: (int, int|float) -> int|float
        """Converts Silicon Lab SI114X ADC value to intensity (W/m^2).

        Args:
            adc (int): ADC reading from SI114X registers.

        Returns:
            (int | float): Intensity (W/m^2).
        """
        return SI114X.calculate(adc=adc, gain=self._gain, typical=8.277)

    @staticmethod
    def calculate_uv_index(value):
        # type: (int|float) -> float
        """Converts Silicon Lab SI114X UV reading to UV Index.

        Args:
            value (int): ADC reading from SI114X registers.

        Returns:
            (float): UV Index (unitless).
        """
        # The index is multiplied by 100 as read from SI1145 registers,
        # so to get the integer index, divide by 100!
        return value / 100.0

    @staticmethod
    def calculate_intensity_from_typical(type_, value, high_range=True):
        # type: (str, int|float, bool) -> float
        """Calculate intensity value from typical SI114X specifications.

        Args:
            type_ (str): Data type, allowable (`'ir'|'vis'|'uv'`).
            value (int): Value as read from SI114X register.
            high_range (bool, optional): Sensor configured to use high signal
                range ie. for direct sunlight. Defaults to True.

        Raises:
            ValueError: Incorrect "type" declared.

        Returns:
            (float): Intensity (W/m^2).
        """
        if type_:
            type_ = type_.lower()
        if type_ not in ("vis", "ir"):
            raise ValueError("Type must be of `vis`, `ir`.")

        if type_ == "ir":
            typical = 452.38
        elif type_ == "vis":
            typical = 8.277

        gain = 14.5 if high_range else 1
        return SI114X.calculate(adc=value, gain=gain, typical=typical)  # pylint: disable=possibly-used-before-assignment

    @staticmethod
    def calculate(adc, gain, typical):
        # type: (int|float, float|int, float|int) -> float|int
        """Transform Silicon Lab SI1145 ADC value to another unit.

        Args:
            adc (int): ADC values as read from SI114X register.
            typical (float): Typical value for unit conversion.

        Returns:
            (int | float): User decided unit.
        """
        return adc * gain / typical
