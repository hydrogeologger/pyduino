"""This module contains the base class for Sensor object. Not for direct import."""


class SensorBase(object):
    """Base class to represent a sensor object.

    Attributes:
        name (str): Name of sensor.
        debug (bool): Debugging mode flag.
    """

    def __init__(self, name, debug=False):
        # type: (str, bool|None) -> None
        """Constructs all the necessary attributes for the sensor object.

        Args:
            name (str): Name of sensor.
            debug (bool, optional): Debuging mode flag. Defaults to False.
        """
        self.name = name  # Reference to sensor name object
        self.debug = debug  # Reference to debug mode flag
