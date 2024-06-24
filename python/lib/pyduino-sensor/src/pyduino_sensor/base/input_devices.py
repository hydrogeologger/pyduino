"""This module contains base classes for input devices which access RPI GPIO hardware.
Not for direct import.

This module is used in submodules, and is preferrable to import them i.e.
`pyduino_sensor.davis`

Dependencies:
- gpiozero.input_devices : DigitalInputDevice for pin interrupt.
"""

from gpiozero.input_devices import DigitalInputDevice as _DigitalInputDevice

from .sensor import SensorBase


class PulseDeviceBase(SensorBase):
    """A class to represent a device implementing pin Interrupts.

    Attributes:
        name (str): Name of sensor.
        debug (bool): Debugging mode flag.

    Methods:

    In addition of `SensorBase()` methods

    - `begin()`:
            Setup interrupt for pin trigger callback.
    - `end()`:
            Detach interrupt for pin trigger callback.
    - `update()`:
            Increment pulse counter by one.
    - `reset()`:
            Resets pulse counter.
    - `get_count()`:
            Getter pulse counter.
    """

    def __init__(self, name, pin, pull_up=True, debounce=None, debug=False, **kwargs):
        # type:(str, int, bool|None, float|None, bool|None, **any) -> None
        """Constructs all the necessary attributes for the PulseSensor object.

        Base on the Button class of gpiozero, pull_up = True means the
        reading pin default state is high, so connect one pin to GND
        and one pin to the reading pin.

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
        super(PulseDeviceBase, self).__init__(name, debug=debug, **kwargs)
        # base on the Button class of gpiozero, pull_up = True means the
        # reading pin default state is high, so connect one pin to GND and one
        # pin to the reading pin
        self._pin = _DigitalInputDevice(
            pin=pin,
            pull_up=pull_up,
            bounce_time=None if debounce == 0 else debounce)
        self._count = 0  # Interupt trigger counter

    def begin(self):
        """Setup interrupt for pin trigger callback.

        Required for counter to be updated.
        """
        self._pin.when_activated = self.update

    def end(self):
        """Detach interrupt for pin trigger callback."""
        self._pin.when_activated = None

    def update(self):
        """Increment pulse counter by one."""
        self._count = self._count + 1
        if self.debug is True:
            print(self.name + " pulsed, new count = " + str(self._count))

    def reset(self):
        """Resets counter to zero."""
        self._count = 0

    def get_count(self):
        # type: () -> int
        """Getter for counter."""
        return self._count
