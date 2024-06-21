"""This module contains post processing functions for suction sensors."""

from ..base.sensor import SensorBase
from .common import normalise as _normalise


class SuctionHeatDissipation(SensorBase):
    """A Class to represent a heat dissipation Suction sensor.

    Attributes:
        name (str): Name of sensor.
        debug (bool): Debugging mode flag.
        dry_dt (int | float): Dry condition differential temperature value.
        wet_dt (int | float): Saturated wet condition differential temperature value.

    Methods:

    In addition of `SensorBase()` methods.
    """

    def __init__(self, name, dry, wet, **kwargs):
        # type: (str, int|float, int|float, any) -> None
        """Constructs all the necessary attributes for Suction sensor object.

        Args:
            name (str): Name of sensor.
            dry (int | float): Dry condition differential temperature value.
            wet (int | float): Saturated wet condition differential temperature value.

        Keyword Args:
            debug (bool, optional): Debuging mode flag. Defaults to False.
        """
        super(SuctionHeatDissipation, self).__init__(name, **kwargs)
        self.wet_dt = wet  # Reference to dry condition base differential temperature
        self.dry_dt = dry  # Reference to wet condition base differential temperature

    def get_kpa(self, value):
        # type: (int|float) -> int|float
        """Converts a heat dissipation temperature delta to pressure.

        Args:
            value (float): Differenential temperature measurement.

        Returns:
            float: Suction (kPa).
        """
        return SuctionHeatDissipation.delta_temperature_to_kpa(value=value,
                                                               dry=self.dry_dt,
                                                               wet=self.wet_dt)

    @staticmethod
    def delta_temperature_to_kpa(value, dry, wet):
        # type: (int|float, int|float, int|float) -> int|float
        """Converts a heat dissipation temperature delta to pressure.

        Args:
            value (float): Differenential temperature measurement.
            dry (float, optional): Dry condition differential temperature value.
            wet (float, optional): Wet condition differential temperature value.

        Returns:
            float: Suction (kPa).
        """
        alpha = _normalise(value=value, min_=wet, max_=dry)
        return pow(10, 6 * alpha)
