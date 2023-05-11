"""Base sensor class module."""

class Sensor(object):
    """
    Base class to represent a sensor object.

    ...

    Attributes
    ----------
    name : str
        Name of sensor
    debug : bool
        Enable debugging
    """

    def __init__(self, name, debug = False):
        # type: (str, bool) -> None
        """
        Constructs all the necessary attributes for the sensor object.

        Parameters
        ----------
            name : str
                Name of sensor.
            debug : bool
                Enable debugging
        """
        self.name = name
        self.debug = debug
