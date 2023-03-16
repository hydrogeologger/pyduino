#!/usr/bin/env python
import sys
import traceback
import time
import serial
import RPi.GPIO as GPIO            # import RPi.GPIO module
from textwrap import fill
from collections import OrderedDict
# from time import sleep,localtime,strftime
# import json
# from phant import Phant
# import paho.mqtt.client as mqtt
# from upload_phant import upload_phant


#-------------------- Check Python Version For Compatibility ------------------
if sys.version_info.major >= 3:
    pass
elif sys.version_info.major == 2:
    try:
        # Introduce Compatibility for input() and raw_input() between python2 and python3
        input = raw_input
    except NameError:
        pass
    # in_waiting = inWaiting
else:
    print ("Unknown python version - some functions may not function appropriately")


#------------------- Constants and Ports Information---------------------------
HARDWARE_NAME = "Datalogger V3"
SERIAL_PORT = '/dev/serial0' # Alias for default serial device, ttyS0/ttyAM0 or ttyS3
SOFT_SERIAL_PORT = '/dev/ttySOFT0' # Use primary uart
SERIAL_9600_BAUD = 9600
SERIAL_2400_BAUD = 2400
SERIAL_115200_BAUD = 115200
SERIAL_TIMEOUT_DEFAULT = 10 # Serial timeout in seconds
RPI_RESET_PIN = 27  #GPIO/BCM pin number to reset arduino

FONT_COLOUR_DEFAULT = "\033[0m"
FONT_BOLD_COLOUR_YELLOW = "\033[1;33m"

# Pin number alias literals
A8 = 62
A9 = 63
A10 = 64
A11 = 65
A12 = 66
A13 = 67
A14 = 68
A15 = 69

# RPI pins uses GPIO numbering (BCM)
RPI_DIGITAL_PINS = (3, 18, 9, 8, 12, 19, 20, 2, 17, 10, 11, 7, 13, 16, 21) # Pins in physical board order, bottom tier -> top tier
# RPI_DIGITAL_PINS = (2, 3, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21)
RPI_SWITCH_PINS = (4, 5, 6, 22, 23, 24, 25, 26)
ARDUINO_SWITCH_PINS = (8, 9, 10, 11, 12, 13, 22, 23, 24, 25, 26, 27, 28, \
        29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, \
        47, 48, 49)
ARDUINO_ANALOG_PINS = (1, 3, 5, 7, 9, 11, 13, 15, 0, 2, 4, 6, 8, 10, 12, 14) # Pins in physical order, bottom tier -> top tier
# ARDUINO_ANALOG_PINS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
ARDUINO_UART_PINS = (15, 16, 17, 18, 19)
ARDUINO_PWM_PINS = (3, 4, 5)
#Atmega2560 sdi12 compliant pins 0, 11, 12, 13, 14, 15, 50, 51, 52, 53, A8 (62),
# A9 (63), A10 (64), A11 (65), A12 (66), A13 (67), A14 (68), A15 (69)
ARDUINO_SDI12_PINS = (50, 51, 52, 53, \
                    A8, A9, A10, A11, A12, A13, A14, A15) # Digital numbering of analog pin
ARDUINO_ANALOG_SDI12_PINS = (8, 9, 10, 11, 12, 13, 14, 15)

## Debugging flag
_DEBUG = False
_DEBUG_REQUEST = True

#---------------------------- Functions Definition -----------------------------
def index_containing_substring(the_list, substring):
    for i, str_item in enumerate(the_list):
        if substring in str_item:
            return i
    return -1


def set_debug(debug):
    global _DEBUG
    _DEBUG = debug
    print("DEBUG Mode: " + str(_DEBUG))
    return _DEBUG

def set_serial_debug(debug):
    global _DEBUG_REQUEST
    _DEBUG_REQUEST = debug
    print("Serial Receive Debug Mode: " + str(_DEBUG_REQUEST))
    if _DEBUG_REQUEST:
        print("\"debug,1\" flag sent with message")
    return _DEBUG_REQUEST

def is_rpi_digital_pin(element):
    element = int(element)
    return element in RPI_DIGITAL_PINS

def is_rpi_switch(element):
    element = int(element)
    return element in RPI_SWITCH_PINS


def is_arduino_switch(element):
    element = int(element)
    return element in ARDUINO_SWITCH_PINS


def is_arduino_analog_pin(element):
    element = int(element)
    return element in ARDUINO_ANALOG_PINS


def is_arduino_digital_pin(element):
    element = int(element)
    return ((element in ARDUINO_UART_PINS) or
            (element in ARDUINO_PWM_PINS) or
            (element in ARDUINO_SDI12_PINS))

def is_arduino_pwm_pin(element):
    element = int(element)
    return element in ARDUINO_PWM_PINS

def is_arduino_sdi12(element):
    element = int(element)
    return ((element in ARDUINO_SDI12_PINS) or
            (element in ARDUINO_ANALOG_SDI12_PINS))

def is_escape(value):
    return (value == 'x') or (value == "exit")


def perform_handshake(arduino_serial):
    message_out = "abc"
    if _DEBUG:
        print("DEBUG: " + message_out)
    arduino_serial.flushInput()
    arduino_serial.write(message_out.encode())
    time.sleep(1)
    message_received = arduino_serial.readline().decode()
    if message_received == "abc\r\n":
        print("Success Handshake: Received ABC response from Arduino")
    else:
        print("Failed Handshake: No Response from Arduino")


def reset_arduino(pin=RPI_RESET_PIN, sleep_duration=5):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    print("Resetting Arduino...")
    if sleep_duration < 2:
        sleep_duration = 2
    time.sleep(sleep_duration)
    GPIO.cleanup()
    print("Reset Complete!")


def reset_rpi_by_arduino(arduino_serial):
    message_out = "RESET"
    if _DEBUG:
        print("DEBUG: " + message_out)
    arduino_serial.flushInput()
    arduino_serial.write(message_out.encode())
    time.sleep(1)
    message_received = arduino_serial.readline().decode()
    print(FONT_BOLD_COLOUR_YELLOW + message_received.rstrip() + FONT_COLOUR_DEFAULT)


def onboard_dht22_test(arduino_serial):
    # try:
    message_out = "dht22,54,power,2,points,2,dummies,1,interval_mm,200"
    if _DEBUG_REQUEST:
        message_out += ",debug,1"
    if _DEBUG:
        print("DEBUG: " + message_out)
    arduino_serial.flushInput()
    arduino_serial.write(message_out.encode())
    message_received = arduino_serial.readline().decode()
    current_read = message_received.split(',')[0:-1]
    print(FONT_BOLD_COLOUR_YELLOW + message_received.rstrip() + FONT_COLOUR_DEFAULT)
    print("Temp: " + current_read[-2])
    print("Humdity: " + current_read[-1])
    # except Exception as error:
    #     print('humidity sensor reading failed')


def rpi_digital_input_test():
    try:
        GPIO.setmode(GPIO.BCM)
        for pin in RPI_DIGITAL_PINS:
            GPIO.setup(pin, GPIO.IN)
            value = GPIO.input(pin)
            print(str(pin) + ": " + str(value))

    except Exception as error:
        print("RPI digital GPIO input test failed on pin " + str(pin))
        print(type(error))
        print(error)

    finally:
        GPIO.cleanup() #clean up rpi gpio setup when done


def rpi_digital_output_test():
    index = 0
    GPIO.setmode(GPIO.BCM)

    try:
        user_timer = input("Duration of RPI IO state in seconds, default 5 seconds: ")
        if is_escape(user_timer):
            return
        else:
            user_timer = float(user_timer)
            if user_timer <= 0:
                user_timer = 1
    except ValueError:
        #Defaults to 5 seconds if user input anything other than a number or x
        user_timer = float(5)

    try:
        while index < len(RPI_DIGITAL_PINS):
            gpio_pin = RPI_DIGITAL_PINS[index]

            try:
                user_pin = input("RPI IO pin, x escape, enter for #" + str(gpio_pin) + ": ")
                if user_pin == "":
                    pass
                elif is_escape(user_pin):
                    return
                elif is_rpi_digital_pin(user_pin):
                    gpio_pin = int(user_pin)
                    index = RPI_DIGITAL_PINS.index(int(user_pin))
                else:
                    continue

                GPIO.setup(gpio_pin, GPIO.OUT)
                GPIO.output(gpio_pin, GPIO.HIGH)
                print(FONT_BOLD_COLOUR_YELLOW + "GPIO #" + str(gpio_pin) + ": HIGH" + FONT_COLOUR_DEFAULT)

                time.sleep(user_timer)

                GPIO.output(gpio_pin, GPIO.LOW)
                print(FONT_BOLD_COLOUR_YELLOW + "GPIO #" + str(gpio_pin) + ": LOW" + FONT_COLOUR_DEFAULT)
                index = index + 1

            except ValueError:
                # Prompt again if is incorrect power pin
                continue

    except Exception as error:
        print("RPI digital GPIO Output test failed on pin " + str(gpio_pin))
        print(type(error))
        print(error)

    finally:
        GPIO.cleanup()



def rpi_switches_test():
    index = 0
    GPIO.setmode(GPIO.BCM)

    try:
        user_timer = input("Duration of switch state in seconds, default 5 seconds: ")
        if is_escape(user_timer):
            return
        else:
            user_timer = float(user_timer)
            if user_timer <= 0:
                user_timer = 1
    except ValueError:
        #Defaults to 5 seconds if user input anything other than a number or x
        user_timer = float(5)

    try:
        while index < len(RPI_SWITCH_PINS):
            power_pin = RPI_SWITCH_PINS[index]

            try:
                user_pin = input("RPI Switch, x escape, enter for #" + str(power_pin) + ": ")
                if user_pin == "":
                    pass
                elif is_escape(user_pin):
                    return
                elif is_rpi_switch(user_pin):
                    power_pin = int(user_pin)
                    index = RPI_SWITCH_PINS.index(int(user_pin))
                else:
                    continue

                GPIO.setup(power_pin, GPIO.OUT)
                GPIO.output(power_pin, GPIO.HIGH)
                print(FONT_BOLD_COLOUR_YELLOW + "Switch #" + str(power_pin) + ": ON" + FONT_COLOUR_DEFAULT)

                time.sleep(user_timer)

                GPIO.output(power_pin, GPIO.LOW)
                print(FONT_BOLD_COLOUR_YELLOW + "Switch #" + str(power_pin) + ": OFF" + FONT_COLOUR_DEFAULT)
                index = index + 1

            except ValueError:
                # Prompt again if is incorrect power pin
                continue

    except Exception as error:
        print("RPI Switch failed on Switch " + str(power_pin))
        print(type(error))
        print(error)

    finally:
        GPIO.cleanup()


def sdi12_sensor_test(arduino_serial):
    while True:
        try:
            sdi12_pin = input("SDI12 Pin, 'x' to escape: ")
            if is_escape(sdi12_pin):
                return
            elif is_arduino_sdi12(sdi12_pin):
                break

        except ValueError:
            # Try again if user input is not an sdi12 pin or x
            continue


    while True:
        try:
            power_pin = input("Power Pin, 'x' to escape: ")
            if is_escape(power_pin):
                return
            elif ((power_pin == "") or (power_pin == '-1')):
                power_pin = -1
                break
            elif is_arduino_switch(power_pin):
                break
            else:
                continue

        except ValueError:
            # Prompt for pin again if incorrect input
            continue

    try:
        message_out = "SDI-12,{0},power,{1},default_cmd,read".format(sdi12_pin, power_pin)
        if _DEBUG_REQUEST:
            message_out += ",debug,1"
        if _DEBUG:
            print("DEBUG: " + message_out)
        arduino_serial.flushInput()
        arduino_serial.write(message_out.encode())
        # SDI-12 takes roughly 13 seconds to scan for all SDI12 devices
        time.sleep(4) # Pad defualt 10sec timeout with 4sec
        while True:
            message_received = arduino_serial.read().decode()
            if message_received == "":
                break
            sys.stdout.write(FONT_BOLD_COLOUR_YELLOW + message_received + FONT_COLOUR_DEFAULT)
            sys.stdout.flush()

    except Exception as error:
        print('SDI12 sensor reading failed')
        print(type(error))
        print(error)



def arduino_switches_test(arduino_serial):
    index = 0

    try:
        user_timer = input("Duration of switch state in seconds, default 5 seconds: ")
        if is_escape(user_timer):
            return
        else:
            user_timer = float(user_timer)
            if user_timer <= 0:
                user_timer = 1
    except ValueError:
        #Defaults to 5 seconds if user input anything other than a number or x
        user_timer = float(5)


    while index < len(ARDUINO_SWITCH_PINS):

        power_pin = ARDUINO_SWITCH_PINS[index]

        try:
            user_pin = input("Arduino Switch, x escape, enter for #" + str(power_pin) + ": ")
            if user_pin == "":
                pass
            elif is_escape(user_pin):
                return
            elif is_arduino_switch(user_pin):
                power_pin = user_pin
                index = ARDUINO_SWITCH_PINS.index(int(user_pin))
            else:
                continue

            # message_out = "power,{0},analog,9,point,3,interval_mm,200,debug,1".format(power_pin)
            message_out = "power_switch,{0},power_switch_status,1".format(power_pin)
            if _DEBUG:
                print("DEBUG: " + message_out)
            arduino_serial.flushInput()
            arduino_serial.write(message_out.encode())
            message_received = arduino_serial.readline().decode()
            print(FONT_BOLD_COLOUR_YELLOW + message_received.rstrip() + FONT_COLOUR_DEFAULT)

            # Duration for switch to stay on
            time.sleep(user_timer)

            message_out = "power_switch,{0},power_switch_status,0".format(power_pin)
            if _DEBUG:
                print("DEBUG: " + message_out)
            arduino_serial.flushInput()
            arduino_serial.write(message_out.encode())
            message_received = arduino_serial.readline().decode()
            print(FONT_BOLD_COLOUR_YELLOW + message_received.rstrip() + FONT_COLOUR_DEFAULT)

            index = index + 1

        except ValueError:
            # Prompt again if is incorrect power pin
            continue


def arduino_analog_test(arduino_serial):
    index = 0
    while True:
        try:
            power_pin = input("Power Pin, 'x' to escape: ")
            if is_escape(power_pin):
                return
            elif ((power_pin == "") or (power_pin == '-1')):
                power_pin = -1
                break
            elif is_arduino_switch(power_pin):
                break
            else:
                continue

        except ValueError:
            # Prompt for pin again if incorrect input
            continue

    while index < len(ARDUINO_ANALOG_PINS):
        analog_pin = ARDUINO_ANALOG_PINS[index]
        try:
            user_pin = input("Arduino Analog, x escape, enter for #" + str(analog_pin) + ": ")
            if user_pin == "":
                pass
            elif is_escape(user_pin):
                return
            elif is_arduino_analog_pin(user_pin):
                analog_pin = user_pin
                index = ARDUINO_ANALOG_PINS.index(int(user_pin))
            else:
                continue

            message_out = "analog,{0},power,{1},points,3,dummies,1,interval_mm,100" \
                    .format(analog_pin, power_pin)
            if _DEBUG_REQUEST:
                message_out += ",debug,1"
            if _DEBUG:
                print("DEBUG: " + message_out)
            arduino_serial.flushInput()
            arduino_serial.write(message_out.encode())
            time.sleep(2)
            message_received = arduino_serial.readline().decode()
            print(FONT_BOLD_COLOUR_YELLOW + message_received.rstrip() + FONT_COLOUR_DEFAULT)

            index = index + 1

        except ValueError:
            # Prompt again if is incorrect power pin
            continue


def vsense_adc_check(arduino_serial):
    '''
    Reports the Vsense voltage (Battery Voltage) based on
    V_battery = ADC * (ADC_Resolution) * ((R2 + R3) / R3)
    '''
    vref = 5.1
    r2 = 0.0 #defined later
    r3 = 680.0

    while True:
        try:
            print("    1:   V2")
            print("    2:   V3")
            print("    3:   V3.2")
            logger_version = input("Select logger version, 'x' to escape: ")
            if is_escape(logger_version):
                return
            elif logger_version == "":
                break
            elif logger_version == '1': # datalogger V2
                r2 = 2200
                break
            elif logger_version == '2': # datalogger V3.0 - V3.1
                r2 = 2000
                break
            elif logger_version == '3': # datalogger V3.2
                r2 = 120e3
                r3 = 39e3
                break
            else:
                continue

        except ValueError:
            # Prompt for logger version again if incorrect input
            continue

    message_out = "analog,15,power,9,points,3,dummies,1,interval_mm,200"
    if _DEBUG_REQUEST:
        message_out += ",debug,1"
    if _DEBUG:
        print("DEBUG: " + message_out)
    arduino_serial.flushInput()
    arduino_serial.write(message_out.encode())
    time.sleep(2)
    message_received = arduino_serial.readline().decode()
    print(FONT_BOLD_COLOUR_YELLOW + message_received.rstrip() + FONT_COLOUR_DEFAULT)
    if r2 > 0:
        array_received = message_received.split(',')[0:-1]
        voltage_value = float(array_received[-1]) * float(((r2 + r3)/r3)) * float((vref/1024))
        print("Battery Voltage: {0:.3f} (V)".format(voltage_value))



def check_arduino_runtime_since_last_comm(arduino_serial):
    message_out = "check_millis"
    if _DEBUG:
        print("DEBUG: " + message_out)
    arduino_serial.flushInput()
    arduino_serial.write(message_out.encode())
    time.sleep(1)
    message_received = arduino_serial.readline().decode()
    print(FONT_BOLD_COLOUR_YELLOW + message_received.rstrip() + FONT_COLOUR_DEFAULT)


def scan_i2c_multiplexer(arduino_serial):
    while True:
        try:
            power_pin = input("Power Pin to switch for duration of scan, 'x' to escape: ")
            if is_escape(power_pin):
                return
            elif ((power_pin == "") or (power_pin == '-1')):
                power_pin = -1
                break
            elif is_arduino_switch(power_pin):
                break
            else:
                continue
        except ValueError:
            # Prompt for pin again if incorrect input
            continue

    if is_arduino_switch(power_pin):
        message_out = "power_switch,{0},power_switch_status,1".format(power_pin)
        if _DEBUG:
            print("DEBUG: " + message_out)
        arduino_serial.write(message_out.encode())
        time.sleep(1)
        arduino_serial.flushInput()

    message_out = "9548_search"
    if _DEBUG:
        print("DEBUG: " + message_out)
    arduino_serial.flushInput()
    arduino_serial.write(message_out.encode())
    time.sleep(1)
    while arduino_serial.inWaiting() > 0:
        message_received = arduino_serial.readline().decode()
        print(FONT_BOLD_COLOUR_YELLOW + message_received.rstrip() + FONT_COLOUR_DEFAULT)
        time.sleep(0.1)

    if is_arduino_switch(power_pin):
        message_out = "power_switch,{0},power_switch_status,0".format(power_pin)
        if _DEBUG:
            print("DEBUG: " + message_out)
        arduino_serial.write(message_out.encode())
        time.sleep(1)
        arduino_serial.flushInput()


def scan_for_ds18b20_suction(arduino_serial):
    while True:
        try:
            suction_pin = input("Suction Pin, 'x' to escape: ")
            if is_escape(suction_pin):
                return
            elif (is_arduino_digital_pin(suction_pin) or is_arduino_sdi12(suction_pin) or \
                    is_arduino_analog_pin(suction_pin)):
                break
            else:
                continue
        except ValueError:
            # Try again if user input is not an sdi12 pin or x
            continue

    while True:
        try:
            power_pin = input("Power Pin, 'x' to escape: ")
            if is_escape(power_pin):
                return
            elif is_arduino_switch(power_pin):
                break
            else:
                continue
        except ValueError:
            # Prompt for pin again if incorrect input
            continue

    message_out = "ds18b20_search,{0},power,{1}".format(suction_pin, power_pin)
    if _DEBUG_REQUEST:
        message_out += ",debug,1"
    if _DEBUG:
        print("DEBUG: " + message_out)
    arduino_serial.flushInput()
    arduino_serial.write(message_out.encode())
    time.sleep(1)
    while arduino_serial.inWaiting() > 0:
        message_received = arduino_serial.readline().decode()
        current_read = message_received.split(',')[0:-2]
        print(FONT_BOLD_COLOUR_YELLOW + message_received.rstrip() + FONT_COLOUR_DEFAULT)
        rom_addr_index = index_containing_substring(current_read, "ROM = ")
        if rom_addr_index > -1:
            rom_list = current_read[rom_addr_index].split(' ')[2:]
            rom_address = ""
            for rom in rom_list:
                rom_address += "{:0>2}".format(rom)
            if len(rom_address) == 16:
                print("Rom Address: {}".format(rom_address))
            else:
                print("Rom Address: Failed to decipher")
        time.sleep(0.5)


def serial_session(arduino_serial):
    arduino_serial.timeout = 5
    # Flush here so any subsequent serial input is still displayed on next cycle
    arduino_serial.flushInput()
    while True:
        user_input = input(">> ")
        if is_escape(user_input):
            arduino_serial.timout = SERIAL_TIMEOUT_DEFAULT
            return
        arduino_serial.write((user_input + "\r\n").encode())
        # message_received = arduino_serial.readline().decode()
        # while arduino_serial.in_waiting() > 0:
        #     msg_byte = arduino_serial.read(1)
        #     if (msg_byte == '\r' or msg_byte == '\n'):
        #         message_received += '!'
        #         arduino_serial.flushInput()
        #         break
        #     message_received += msg_byte

        # if message_received != "":
        while True:
            message_received = arduino_serial.read().decode()
            if message_received == "":
                break
            sys.stdout.write(FONT_BOLD_COLOUR_YELLOW + message_received + FONT_COLOUR_DEFAULT)
            sys.stdout.flush()


def desc(desc, indent, total_length):
    return fill(desc, width=total_length-indent, subsequent_indent=' '*indent)


def display_options_menu(mode_list):
    # from textwrap import fill
    WIDTH = 70
    LEFT_LEN = 7
    PAD = 2
    INDENT = LEFT_LEN + PAD + 1

    mode = OrderedDict(mode_list)

    print("Select the following options for [" + HARDWARE_NAME + "] testing:\n")
    for key, value in mode.items():
        print("{2:>{0}}:{1}{3}".format(LEFT_LEN, ' '*PAD, key, desc(value, INDENT, WIDTH)))

def general_callback(arduino_serial, user_option):
    global _DEBUG, _DEBUG_REQUEST
    if user_option == "debug":
        _DEBUG = set_debug(not _DEBUG)
    elif user_option == "debug0":
        _DEBUG_REQUEST = set_serial_debug(not _DEBUG_REQUEST)
    elif user_option == "serial":
        serial_session(arduino_serial)

def get_main_options_list():
    mode = OrderedDict()
    mode[1] = "Arduino Handshake Serial COM"
    mode[2] = "Reset Arduino"
    mode[3] = "Onboard DHT22 Humidity and Temperature Sensor"
    mode[4] = "RPI Switches"
    mode[5] = "RPI digital IO as OUTPUT"
    mode[6] = "RPI digital IO as INPUT"
    mode[7] = "Arduino Switches"
    mode[8] = "Arduino Analog IO as INPUT"
    mode[9] = "SDI12 Sensor Ports"
    mode[10] = "Scan I2C Multiplexer"
    mode[11] = "VSENSE DC Voltage, req vsense & SW9 jumper set correctly"
    mode[12] = "Sensor Tools"
    mode[13] = "Check Arduino Runtime Since Last Communication"
    mode["m"] = "Display This Main Options Menu"
    mode["x"] = "Exit"
    mode["reset"] = "Initiate RPI RESET request from Arduino"
    mode["serial"] = "Serial Session for Custom User Input"
    mode["debug0"] = "Toggle sending \"debug,1\" flag, default=True"
    mode["debug"] = "Debug Mode Toggle (Show sent command string)"
    return mode


def get_suction_util_list():
    mode = OrderedDict()
    mode[1] = "Get Suction ROM Address"
    mode["m"] = "Display This Main Options Menu"
    mode["x"] = "Exit"
    mode["serial"] = "Serial Session for Custom User Input"
    mode["debug0"] = "Toggle sending \"debug,1\" flag, default=True"
    mode["debug"] = "Debug Mode Toggle (Show sent command string)"
    return mode


def primary_menu_callback_loop(arduino_serial):
    while True:
        user_option = input("\r\nOption: ")

        if is_escape(user_option):
            break
        elif user_option == 'm':
            display_options_menu(get_main_options_list())
        elif user_option == '1':
            perform_handshake(arduino_serial)
        elif user_option == '2':
            reset_arduino()
        elif user_option == '3':
            onboard_dht22_test(arduino_serial)
        elif user_option == '4':
            rpi_switches_test()
        elif user_option == '5':
            rpi_digital_output_test()
        elif user_option == '6':
            rpi_digital_input_test()
        elif user_option == '7':
            arduino_switches_test(arduino_serial)
        elif user_option == '8':
            arduino_analog_test(arduino_serial)
        elif user_option == '9':
            sdi12_sensor_test(arduino_serial)
        elif user_option == '10':
            scan_i2c_multiplexer(arduino_serial)
        elif user_option == '11':
            vsense_adc_check(arduino_serial)
        elif user_option == '12':
            display_options_menu(get_suction_util_list())
            suction_util_callback_loop(arduino_serial)
        elif user_option == '13':
            check_arduino_runtime_since_last_comm(arduino_serial)
        elif user_option == 'reset':
            reset_rpi_by_arduino(arduino_serial)

        general_callback(arduino_serial, user_option)


def suction_util_callback_loop(arduino_serial):
    while True:
        user_option = input("\r\nSensor Tools: ")
        if is_escape(user_option):
            break
        elif user_option == 'm':
            display_options_menu(get_suction_util_list())
        elif user_option == '1':
            scan_for_ds18b20_suction(arduino_serial)

        general_callback(arduino_serial, user_option)


def serial_port_and_baudrate_selection():
    print("\r\nSelect Serial Baudrate:")
    print("{0:>2s}:  {1} ({2})".format("1", SERIAL_9600_BAUD, "Hardware"))
    print("{0:>2s}:  {1} ({2})".format("2", SERIAL_2400_BAUD, "SoftSerial/Hardware"))
    print("{0:>2s}:  {1} ({2})".format("3", "User Defined", "SoftSerial/Hardware/Other"))
    serial_port = SERIAL_PORT
    user_option = input("\r\nSelection (Default Enter = 1): ")
    if is_escape(user_option):
        exit()
    elif user_option == "2":
        serial_baud = SERIAL_2400_BAUD
        print("\r\nSelect Serial Port:")
        print("{0:>2s}:  {1} ({2})".format("1", SERIAL_PORT, "Hardware"))
        print("{0:>2s}:  {1} ({2})".format("2", SOFT_SERIAL_PORT, "SoftSerial"))
        user_option = input("\r\nSelection (Default Enter = 1): ")
        if is_escape(user_option):
            exit()
        elif user_option == "2":
            serial_port = SOFT_SERIAL_PORT
        else:
            serial_port = SERIAL_PORT
    elif user_option == "3":
        print("\r\nSelect Serial Port:")
        print("{0:>2s}:  {1} ({2})".format("1", SERIAL_PORT, "Hardware"))
        print("{0:>2s}:  {1} ({2})".format("2", SOFT_SERIAL_PORT, "SoftSerial"))
        print("{0:>2s}:  {1} ({2})".format("3", "Other", "User Defined"))
        user_option = input("\r\nSelection (Default Enter = 1): ")
        if is_escape(user_option):
            exit()
        elif user_option == "2":
            serial_port = SOFT_SERIAL_PORT
        elif user_option == "3":
            serial_port = input("Enter Serial Port (Example = {0}): ".format("/dev/ttyS0")).strip()
            if is_escape(serial_port):
                return
        else:
            serial_port = SERIAL_PORT
        try:
            serial_baud = input("Enter baudrate (Default = {0}): ".format(SERIAL_115200_BAUD))
            if is_escape(serial_baud):
                return
            else:
                serial_baud = int(serial_baud)
            if serial_baud <= 0:
                serial_baud = SERIAL_115200_BAUD
        except ValueError:
            serial_baud = SERIAL_115200_BAUD
    else:
        serial_baud = SERIAL_9600_BAUD

    return serial_port, serial_baud



#---------------------------- Main Loop ----------------------------------------
def main():
    arduino_serial = None
    try:
        while True:
            serial_port, serial_baud = serial_port_and_baudrate_selection()

            print("\r\nStarting {3}{0}{2} serial @ {3}{1}{2} baud..." \
                    .format(serial_port, serial_baud, \
                    FONT_COLOUR_DEFAULT, FONT_BOLD_COLOUR_YELLOW))
            try:
                arduino_serial = serial.Serial(port=serial_port, baudrate=serial_baud, \
                        timeout=SERIAL_TIMEOUT_DEFAULT)
            except serial.SerialException:
                print("Serial port not found!")
                input("Press the <ENTER> key to try again...")
            except ValueError:
                print("Invalid Serial Port Baudrate!")
                input("Press the <ENTER> key to try again...")
            else:
                break

        time.sleep(1)

        display_options_menu(get_main_options_list())
        primary_menu_callback_loop(arduino_serial)

    except KeyboardInterrupt:
        print("")
    # except Exception as error:
    #     print(type(error))
    #     print(error)
    except Exception:
        traceback.print_exc()
        # print(sys.exc_info()[0])
    finally:
        # Cleaning up
        if arduino_serial is not None and arduino_serial.isOpen():
            arduino_serial.close()
        exit()

if __name__ == "__main__":
    main()
