"""This file contains post processing functions for SI114X sensors."""

from ..sensor import Sensor


class SI114X(Sensor):
    """A Class to represent a heat dissipation Suction sensor.

    Attributes:
        name (str): Name of sensor.
        debug (bool): Debugging mode flag.

    Methods:

    In addition of `Sensor.Sensor()` methods.
    """

    def __init__(self, name, high_range=True, **kwargs):
        # type: (str, bool, any) -> None
        """Constructs all the necessary attributes for Suction sensor object.

        Args:
            name (str): Name of sensor.
            high_range (bool, optional): Sensor configured to use high signal \
                    range ie. for direct sunlight. Defaults to True.
            debug (bool, optional): Debuging mode flag. Defaults to True.
        """
        super(SI114X, self).__init__(name, **kwargs)
        # Gain modifier for low and high range mode
        if high_range:
            self._gain = 14.5
        else:
            self._gain = 1

    def ir_intensity(self, adc):
        # type: (int, int|float) -> int|float
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

    def uv_index(self, value):
        # type: (int, int|float) -> int|float
        """Converts Silicon Lab SI114X UV reading to UV Index.

        Args:
            value (int): ADC reading from SI114X registers.

        Returns:
            (int | float): Intensity (W/m^2).
        """
        # The index is multiplied by 100 as read from SI1145 registers,
        # so to get the integer index, divide by 100!
        return value / 100.0

    @staticmethod
    def calculate(adc, gain, typical):
        """Transform Silicon Lab SI1145 ADC value to another unit.

        Args:
            adc (int): ADC values as read from SI114X register.
            typical (float): Typical value for unit conversion.

        Returns:
            (int | float): User decided unit.
        """
        return adc * gain / typical
