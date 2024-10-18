<!-- markdownlint-disable -->

# API Overview

## Modules

- [`pyduino_sensor.base`](./pyduino_sensor.base.md#module-pyduino_sensorbase): Sub package containing base classes for pyduino-sensor. Not for direct import.
- [`pyduino_sensor.base.input_devices`](./pyduino_sensor.base.input_devices.md#module-pyduino_sensorbaseinput_devices): This module contains base classes for input devices which access RPI GPIO hardware. Not for direct import.
- [`pyduino_sensor.base.sensor`](./pyduino_sensor.base.sensor.md#module-pyduino_sensorbasesensor): This module contains the base class for Sensor object. Not for direct import.
- [`pyduino_sensor.davis`](./pyduino_sensor.davis.md#module-pyduino_sensordavis): This is a wrapper for Davis Weather Instruments Sensors.
- [`pyduino_sensor.post`](./pyduino_sensor.post.md#module-pyduino_sensorpost): Sub package for post processing support of sensor data.
- [`pyduino_sensor.post.common`](./pyduino_sensor.post.common.md#module-pyduino_sensorpostcommon): This module contain simple and common methods used in sensor post process package.
- [`pyduino_sensor.post.si114x`](./pyduino_sensor.post.si114x.md#module-pyduino_sensorpostsi114x): This module contains post processing functions for SI114X sensors.
- [`pyduino_sensor.post.suction`](./pyduino_sensor.post.suction.md#module-pyduino_sensorpostsuction): This module contains post processing functions for suction sensors.
- [`pyduino_sensor.post.wind`](./pyduino_sensor.post.wind.md#module-pyduino_sensorpostwind): This module contains post processing functions for wind sensors.
- [`pyduino_sensor.pyduino`](./pyduino_sensor.pyduino.md#module-pyduino_sensorpyduino): This module provides helper functions for pyduino datalogger.
- [`pyduino_sensor.scales`](./pyduino_sensor.scales.md#module-pyduino_sensorscales): This module provides helper functions to communicate with Scale devices.

## Classes

- [`input_devices.PulseDeviceBase`](./pyduino_sensor.base.input_devices.md#class-pulsedevicebase): A class to represent a device implementing pin Interrupts.
- [`sensor.SensorBase`](./pyduino_sensor.base.sensor.md#class-sensorbase): Base class to represent a sensor object.
- [`davis.Rain`](./pyduino_sensor.davis.md#class-rain): A Class to represent a Davis Tipping Bucket Rain Gauge.
- [`davis.WindSpeed`](./pyduino_sensor.davis.md#class-windspeed): A Class to represent a Davis Anemometer Wind Speed sensor.
- [`si114x.SI114X`](./pyduino_sensor.post.si114x.md#class-si114x): A Class to represent a Si114x Ultraviolet (UV) Index, Gesture, Proximity, and Ambient Light sensor.
- [`suction.SuctionHeatDissipation`](./pyduino_sensor.post.suction.md#class-suctionheatdissipation): A Class to represent a heat dissipation Suction sensor.
- [`wind.WindDirection`](./pyduino_sensor.post.wind.md#class-winddirection): A Class to represent an analog Wind Direction sensor.
- [`scales.OhausScale`](./pyduino_sensor.scales.md#class-ohausscale): A Class to represent an Ohaus Scale with serial interface.

## Functions

- [`common.normalise`](./pyduino_sensor.post.common.md#function-normalise): Map a value to between 0 and 1.
- [`pyduino.arduino_comms_is_good`](./pyduino_sensor.pyduino.md#function-arduino_comms_is_good): Test communication between RPI and secondary MCU.
- [`pyduino.comms_check_reset_arduino`](./pyduino_sensor.pyduino.md#function-comms_check_reset_arduino): Verify comms between RPI and secondary MCU with auto MCU reset.
- [`pyduino.exec_remote_command_subprocess`](./pyduino_sensor.pyduino.md#function-exec_remote_command_subprocess): Executes a command on a remote host using the system's ssh client via subprocess.
- [`pyduino.reset_arduino`](./pyduino_sensor.pyduino.md#function-reset_arduino): Resets secondary MCU.
