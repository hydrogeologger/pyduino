"""This module contains post processing functions for wind sensors."""

from ..base.sensor import SensorBase


class WindDirection(SensorBase):
    """A Class to represent an analog Wind Direction sensor.

    Default orientation for direction is Clockwise.

    Attributes:
        name (str): Name of sensor.
        debug (bool): Debugging mode flag.
        offset (float) : Angle offset of wind vane in degrees radius.
            (Positive: Clockwise, Negative: Counter-clockwise)

    Methods:

    In addition of `SensorBase()` methods.

    - `adc_to_degree(adc_raw)`:
            Calculates the angle from ADC value in degrees radius.
    - `get_calibrated_direction(adc_raw)`:
            Get calibrated angle from ADC value in degrees radius.
    """

    def __init__(self, name, offset=0, n_adc_bits=10, **kwargs):
        # type: (str, int|float|None, int|None, any) -> None
        """Constructs all the necessary attributes for the Davis Wind Anemometer Direction object.

        Args:
            name (str): Name of sensor.
            offset (float, optional): Angle offset of wind vane in degrees
                radius in clockwise direction. Defaults to 0.  
                Clockwise - Positive value. Counter-Clockwise - Negative value.
            n_adc_bits (int, optional): Resolution of ADC i.e 10bit = 10. Defaults to 10.

        Keyword Args:
            debug (bool, optional): Debuging mode flag. Defaults to False.
        """
        super(WindDirection, self).__init__(name, **kwargs)
        # Reference to maximum value able to be recorded by n-bits
        self._max_adc_value = (2 ** n_adc_bits) - 1
        self.offset = offset  # Reference to offset away from North, CW direction

    def adc_to_degree_radius(self, adc_raw, clockwise=True):
        # type: (int|float, bool|None) -> float
        """Convert ADC value to approximate angles in degrees radius.

        Mapping function.

        From http://cactus.io/hookups/weather/anemometer/davis/hookup-arduino-to-davis-anemometer
        North : 0/MAX ADC
        East : 1/4 * MAX ADC
        South : 1/2 * MAX ADC
        West : 3/4 * MAX ADC

        Args:
            adc_raw (int | float): ADC measurement of anemometer.
            clockwise (bool, optional): Direction of results to be returned.  
                    True: Clockwise, False: Counter-Clockwise.
                    Defaults to True.

        Returns:
            float: Clockwise angle in degrees radius unless clockwise is false.
        """
        in_min = 0.0  # Lower input mapping bound
        in_max = self._max_adc_value  # Upper input mapping bound
        if clockwise:
            out_min = 0.0
            out_max = 360.0
        else:
            out_min = 360.0
            out_max = 0.0
        return (adc_raw - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        # return (adc_raw - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    def get_calibrated_direction(self, adc_raw):
        # type: (int|float) -> float
        """Gets calibrated direction of wind vane in degrees radius (clockwise)."""
        calibrated_direction = self.adc_to_degree_radius(adc_raw) + self.offset
        if calibrated_direction > 360.0:
            calibrated_direction -= 360.0
        elif calibrated_direction < 0.0:
            calibrated_direction += 360.0
        return calibrated_direction
