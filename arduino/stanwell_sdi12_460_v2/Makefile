## How to use
# make upload   -   upload over hardware serial (normal bootloader)
# make upload 2400  -   upload over hardware serial (modified bootloader)
# make softupload   -   for uploading over software serial (modified bootloader)

BOARD_TAG = mega
BOARD_SUB = atmega2560
USER_LIB_PATH = /home/$(USER)/pyduino/arduino/libraries/
ARDUINO_LIBS = SDI12 hydrogeolog SparkFun_MS5803_I2C Sensirion OneWire dht DallasTemperature Adafruit_SI1145_Library Wire rc-switch Adafruit_SHT31 ICM20948_WE

.PHONY: softupload 2400

# Declares Port and baudrate settings
ifndef MONITOR_PORT
    ifneq ($(filter softupload, $(MAKECMDGOALS)),)
        # is software serial upload
        export MONITOR_PORT = /dev/ttySOFT0
        export AVRDUDE_ARD_BAUDRATE = 2400
    else
        # Is hardware serial upload, serial0 reference to primary UART
        # RPI: ttyS0, BPI: ttyS3
        export MONITOR_PORT = /dev/serial0
        ifneq ($(filter 2400, $(MAKECMDGOALS)),)
            # If modified bootloader, modify upload baudrate
            export AVRDUDE_ARD_BAUDRATE = 2400
        endif
    endif
    $(info uploading over $(MONITOR_PORT) at $(AVRDUDE_ARD_BAUDRATE))
endif

softupload: upload

include /usr/share/arduino/Arduino.mk
