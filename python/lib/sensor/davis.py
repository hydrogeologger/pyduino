"""
This is a wrapper for Davis Weather Instruments Sensor

Dependencies:
-------------
    gpiozero : Button for button interrupts
"""

import time
from gpiozero import Button
from .sensor import Sensor


## Python 2/3 compatibility imports
# for time.monotonic() to time.time()
# if sys.version_info <= (3,3):
#     monotonic = time


class PulseSensor(Sensor):
    """
    A class to represent a device implementing pin Interrupts.

    ...

    Attributes
    ----------
    name : str
        Name of device
    debug : bool
        Enable debugging

    Methods
    -------
    In addition of Sensor.__init__() methods

    begin():
        Setup interrupt for pin trigger callback.
    end():
        Detach interrupt for pin trigger callback.
    update():
        Increment pulse counter by one.
    reset():
        Resets pulse counter.
    get_count():
        Getter pulse counter.
    """

    def __init__(self, name, pin, pull_up = True, debounce = None, debug = True, **kwargs):
        # type:(str, int, bool, float|None, bool, any) -> None
        """
        Constructs all the necessary attributes for the PulseSensor object.

        Base on the Button class of gpiozero, pull_up = True means the
        reading pin default state is high, so connect one pin to GND
        and one pin to the reading pin

        Parameters
        ----------
            name : str
                Name of sensor
            pin : int
                GPIO BCM pin to be attached to interrupt.
            pull_up : bool
                GPIO pin state. True: pin pulled high, False: pin pulled low.
                (Default - True)
            debounce : float or None
                Debounce of pin in seconds. If None (the default), no software
                bounce compensation will be performed. Otherwise, this is the
                length of time (in seconds)
                that the component will ignore changes in state after an initial
                change. (Default - None)
            debug : bool
                Enable debugging
        """
        super(PulseSensor, self).__init__(name, debug=debug, **kwargs)
        self._pin = Button(pin, pull_up=pull_up, bounce_time=debounce)
        self._count = 0

    def begin(self):
        '''
        Setup interrupt for pin trigger callback.
        Required for counter to be updated
        '''
        self._pin.when_pressed = self.update

    def end(self):
        """
        Detach interrupt for pin trigger callback
        """
        self._pin.when_pressed = None

    def update(self):
        """
        Increment pulse counter by one
        """
        self._count = self._count + 1
        if self.debug is True:
            print(self.name + " pulsed, new count = " + str(self._count))

    def reset(self):
        """
        Resets counter to zero
        """
        self._count = 0

    def get_count(self):
        # type: () -> int
        """
        Getter for counter
        """
        return self._count


class Rain(PulseSensor):
    """
    A Class to represent a Davis Tipping Bucket Rain Gauge

    ...

    Attributes
    ----------
    name : str
        Name of device
    debug : bool
        Debugging flag

    Methods
    -------
    In addition of Sensor.PulseDevice() methods

    get_volume():
        Getter for bucket volume.
    get_cumulative():
        Getter for cumulative rain volume in millilitres (mm)
    """

    def __init__(self, name, pin, debounce = 0.001, volume = 0.2, **kwargs):
        # type:(str, int, float|None, float, any) -> None
        """
        Constructs all the necessary attributes for the Davis Rain Tip Bucket object.

        Parameters
        ----------
            name : str
                Name of sensor
            pin : int
                BCM pin number of GPIO for interrupt attachment
            debounce : float or None
                Debounce of pin in seconds.  If None (the default), no software bounce
                compensation will be performed. Otherwise, this is the length of time (in seconds)
                that the component will ignore changes in state after an initial change.
            volume : float
                Volume of tip bucket in millimetres (mm)
            debug : bool
                Enable debugging
        """
        super(Rain, self).__init__(name, pin, debounce=debounce, **kwargs)
        #base on the Button class of gpiozero, pull_up = True means the reading pin default state is
        #high, so connect one pin to GND and one pin to the reading pin
        self._volume = volume

    def get_volume(self):
        # type: () -> float
        """
        Getter for bucket volume
        """
        return self._volume

    def get_cumulative(self):
        # type: () -> float
        """
        Getter for cumulative rain volume in millilitres (mm).
        Will reset counter
        """
        cumulative_volume = self._count * self._volume
        self.reset()
        return cumulative_volume


class WindSpeed(PulseSensor):
    """
    A Class to represent a Davis Anemometer Wind Speed


    Attributes
    ----------
    name : str
        Name of device
    debug : bool
        Debugging flag

    Methods
    -------
    In addition of Sensor.PulseDevice() methods

    calculate_average():
        Calculate wind speed in km/hr
    get_average():
        Getter for average wind speed in km/hr, will reset counter
    """

    def __init__(self, name, pin, debounce = None, **kwargs):
        # type: (str, int, float|None, any) -> None
        """
        Constructs all the necessary attributes for the Davis Wind Anemometer Speed object.

        Parameters
        ----------
            name : str
                Name of sensor
            pin : int
                BCM pin number on RPI to be setup for interrupt
            debounce : float or None
                Debounce of pin in seconds.  If None (the default), no software bounce
                compensation will be performed. Otherwise, this is the length of time (in seconds)
                that the component will ignore changes in state after an initial change.
            debug : bool
                Enable debugging
        """
        super(WindSpeed, self).__init__(name, pin, debounce=debounce, **kwargs)
        self._last_elapsed = 0

    def begin(self):
        super(WindSpeed, self).begin()
        try:
            self._last_elapsed = time.monotonic()
        except AttributeError:
            self._last_elapsed = time.time()

    def reset(self):
        super(WindSpeed, self).reset()
        try:
            self._last_elapsed = time.monotonic()
        except AttributeError:
            self._last_elapsed = time.time()

    def calculate_average(self, elapsed_time):
        # type: (float|int) -> float
        """
        Based on Davis tech document
            V = P*(2.25/T) the speed is in MPh

            P = no. of pulses per sample period

            T = sample period in seconds

        Parameters
        ----------
            elapsed_time : int
                Elapsed time in seconds

        Returns
        -------
            Average speed in km/hr

        """
        _MPH_2_KMH = 1.609 # mph to kmh  pylint: disable=invalid-name
        return self._count * (2.25 / elapsed_time) * _MPH_2_KMH

    def get_average(self):
        # type: () -> float
        """
        Getter for average wind speed in km/hr.

        Will reset counter

        Returns
            Average speed in km/hr
        """
        try:
            elapsed_time = time.monotonic() - self._last_elapsed
        except AttributeError:
            elapsed_time = time.time() - self._last_elapsed
        average_speed = self.calculate_average(elapsed_time)
        self.reset()
        return average_speed


class WindDirection(Sensor):
    """
    A Class to represent a Davis Anemometer Wind Direction (Clockwise)

    Attributes
    ----------
    name : str
        Name of device
    debug : bool
        Debugging flag
    offset : float
        Angle offset of wind vane in degrees radius
        (Positive: Clockwise, Negative: Counter-clockwise)

    Methods
    -------
    In addition of Sensor.Sensor() methods

    adc_to_degree(adc_raw):
        Calculates the angle from ADC value in degrees radius
    get_calibrated_direction(adc_raw):
        Get calibrated angle from ADC value in degrees radius
    """

    def __init__(self, name, offset = 0, adc_bit_size = 10, **kwargs):
        # type: (str, int|float, int, any) -> None
        """
        Constructs all the necessary attributes for the Davis Wind Anemometer Direction object.

        Parameters
        ----------
            name : str
                Name of sensor
            offset : float
                Angle offset of wind vane in degrees radius in clockwise direction.
                        Clockwise - Positive value. Counter-Clockwise - Negative value.
            adc_bit_size : int
                Resolution of ADC i.e 10bit = 10
            debug : bool
                Enable debugging
        """
        super(WindDirection, self).__init__(name, **kwargs)
        self.__max_adc_value = (2 ** adc_bit_size) - 1
        self.offset = offset

    def adc_to_degree_radius(self, adc_raw, clockwise=True):
        # type: (int|float, bool) -> float
        """
        Convert ADC value to approximate angles in degrees radius.

        From http://cactus.io/hookups/weather/anemometer/davis/hookup-arduino-to-davis-anemometer
        North : 0/MAX ADC
        East : 1/4 * MAX ADC
        South : 1/2 * MAX ADC
        West : 3/4 * MAX ADC

        Returns:
            Clockwise angle in degrees radius unless clockwise is false.

        """
        in_min = 0.0
        in_max = self.__max_adc_value
        if clockwise:
            out_min = 0.0
            out_max = 360.0
        else:
            out_min = 360.0
            out_max = 0.0
        return (adc_raw - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        # return (adc_raw - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    def get_calibrated_direction(self, adc_raw):
        ## type: (int|float) -> float
        """
        Gets calibrated direction of wind vane in degrees radius (clockwise).
        """
        calibrated_direction = self.adc_to_degree_radius(adc_raw) + self.offset
        if calibrated_direction > 360.0:
            calibrated_direction -= 360.0
        elif calibrated_direction < 0.0:
            calibrated_direction += 360.0
        return calibrated_direction
