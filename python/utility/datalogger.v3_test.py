#!/usr/bin/python
import sys
import serial
import RPi.GPIO as GPIO            # import RPi.GPIO module
import time
# from time import sleep,localtime,strftime
# import json
# from phant import Phant
# import paho.mqtt.client as mqtt
# from upload_phant import upload_phant


#-------------------- Check Python Version For Compatibility ------------------
# Introduce Compatibility for input() and raw_input() between python2 and python3
PY3 = sys.version_info.major >= 3

if sys.version_info.major >= 3:
    pass
elif sys.version_info.major == 2:
    try:
        input = raw_input
        pass
    except NameError:
        pass
else:
    print ("Unknown python version - input function not safe")


#------------------- Constants and Ports Information---------------------------
HARDWARE_NAME = "Datalogger V3"
DEBUG = False
# SERIAL_PORT = '/dev/ttyS0' # datalogger version 2 uses ttyS0
SERIAL_PORT = '/dev/serial0' # Use primary uart
#SERIAL_PORT = '/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2:1.0' # datalogger version 1 uses ttyACM0
SERIAL_TIMEOUT_DEFAULT = 10 # Serial timeout in seconds
RPI_RESET_PIN = 27  #GPIO/BCM pin number to reset arduino

# RPI pins uses GPIO numbering (BCM)
rpi_digital_pins = (2, 17, 10, 11, 7, 13, 16, 21, 3, 18, 9, 8, 12, 19, 20) # Pins in physical board order
# rpi_digital_pins = (2, 3, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21)
rpi_switch_pins = (4, 5, 6, 22, 23, 24, 25, 26)
arduino_swich_pins = (8, 9, 10, 11, 12, 13, 22, 23, 24, 25, 26, 27, 28,
        29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46,
        47, 48, 49)
arduino_analog_pins = (0, 2, 4, 6, 8, 10, 12, 14, 1, 3, 5, 7, 9, 11, 13, 15) # Pins in physical order
# arduino_analog_pins = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
arduino_digital_only_pins = (5,)
arduino_pwm_pins = (3, 4)
arduino_sdi12_pins = (50, 51, 52, 53)


#---------------------------- Functions Definition -----------------------------
def toggle_debug(DEBUG):
    DEBUG = not DEBUG
    print("DEBUG Mode: " + str(DEBUG))
    return DEBUG

def is_rpi_digital_pin(element):
    element = int(element)
    return element in rpi_digital_pins
    
def is_rpi_switch(element):
    element = int(element)
    return element in rpi_switch_pins


def is_arduino_switch(element):
    element = int(element)
    return element in arduino_swich_pins


def is_arduino_analog_pin(element):
    element = int(element)
    return element in arduino_analog_pins


def is_arduino_digital_pin(element):
    element = int(element)
    return ((element in arduino_digital_only_pins) or
            (element in arduino_pwm_pins) or
            (element in arduino_sdi12_pins))

def is_arduino_pwm_pin(element):
    element = int(element)
    return element in arduino_pwm_pins
    
def is_arduino_sdi12(element):
    element = int(element)
    return element in arduino_sdi12_pins
    
def is_escape(value):
    return (value == 'x')


def perform_handshake():
    arduino_serial.write("abc")
    arduino_serial.flushInput()
    time.sleep(1)
    message_received = arduino_serial.readline()
    if (message_received == "abc\r\n"):
        print("Success Handshake: Received ABC response from Arduino")
    else:
        print("Failed Handshake: No Response from Arduino")


def reset_arduino(pin = RPI_RESET_PIN, sleep_duration = 5):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    print("Resetting Arduino...")
    time.sleep(5)
    GPIO.cleanup()
    print("Reset Complete!")


def reset_rpi_by_arduino():
    message_out = "RESET"
    if DEBUG: print("DEBUG: " + message_out)
    arduino_serial.write(message_out)
    arduino_serial.flushInput()
    time.sleep(1)
    message_received = arduino_serial.readline()
    print(message_received.rstrip())


def onboard_dht22_test():
    # try:
        arduino_serial.write("dht22,54,power,2,points,2,dummies,1,interval_mm,200,debug,1")
        arduino_serial.flushInput()
        message_received = arduino_serial.readline()
        current_read = message_received.split(',')[0:-1]
        print(message_received.rstrip())
        print("Temp: " + current_read[-2])
        print("Humdity: " + current_read[-1])
    # except Exception as error:
    #     print('humidity sensor reading failed')


def rpi_digital_input_test():
    try:
        GPIO.setmode(GPIO.BCM)
        for pin in rpi_digital_pins:
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
        if (user_timer =='x'):
            return
        else:
            user_timer = float(user_timer)
    except ValueError:
        #Defaults to 5 seconds if user input anything other than a number or x
        user_timer = float(5)

    try:
        while index < len(rpi_digital_pins):
            gpio_pin = rpi_digital_pins[index]

            try:
                user_pin = input("RPI IO pin, x escape, enter for #" + str(gpio_pin) + ": ")
                if (user_pin == ""):
                    pass
                elif (is_escape(user_pin)):
                    return
                elif (is_rpi_digital_pin(user_pin)):
                    gpio_pin = int(user_pin)
                    index = rpi_digital_pins.index(int(user_pin))
                else:
                    continue

                GPIO.setup(gpio_pin, GPIO.OUT)
                GPIO.output(gpio_pin, GPIO.HIGH)

                time.sleep(user_timer)

                GPIO.output(gpio_pin, GPIO.LOW)
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
        if (user_timer =='x'):
            return
        else:
            user_timer = float(user_timer)
    except ValueError:
        #Defaults to 5 seconds if user input anything other than a number or x
        user_timer = float(5)

    try:
        while index < len(rpi_switch_pins):
            power_pin = rpi_switch_pins[index]

            try:
                user_pin = input("RPI Switch, x escape, enter for #" + str(power_pin) + ": ")
                if (user_pin == ""):
                    pass
                elif (is_escape(user_pin)):
                    return
                elif (is_rpi_switch(user_pin)):
                    power_pin = int(user_pin)
                    index = rpi_switch_pins.index(int(user_pin))
                else:
                    continue

                GPIO.setup(power_pin, GPIO.OUT)
                GPIO.output(power_pin, GPIO.HIGH)

                time.sleep(user_timer)

                GPIO.output(power_pin, GPIO.LOW)
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


def sdi12_sensor_test():
    while True:
        try:
            # if (PY3):
            #     sdi12_pin = input("SDI12 Pin, 'x' to escape: ")
            # else:
            #     sdi12_pin = raw_input("SDI12 Pin, 'x' to escape: ")
            sdi12_pin = input("SDI12 Pin, 'x' to escape: ")
            if (is_escape(sdi12_pin)):
                return
            elif (is_arduino_sdi12(sdi12_pin)):
                break
                
        except (ValueError):
            # Try again if user input is not an sdi12 pin or x
            continue
            
            
    while True:
        try:
            # if (PY3):
            #     power_pin = input("Power Pin, 'x' to escape: ")
            # else:
            #     power_pin = raw_input("Power Pin, 'x' to escape: ")
            power_pin = input("Power Pin, 'x' to escape: ")
            if (is_escape(power_pin)):
                return
            elif ((power_pin == "") or (power_pin == '-1')):
                power_pin = -1
                break
            elif (power_pin.isalpha()):
                continue
            elif (is_arduino_switch(power_pin)):
                break
                
        except (ValueError):
            # Prompt for pin again if incorrect input
            print("SDI12 Test, Power Pin ValueError")
            break
    
    try:
        message_out = "SDI-12,{0},power,{1},default_cmd,read,debug,1".format(
                sdi12_pin, power_pin)
        if DEBUG: print("DEBUG: " + message_out)
        arduino_serial.write(message_out)
        arduino_serial.flushInput()
        time.sleep(2)
        message_received = arduino_serial.readline() # Get DEBUG response
        print(message_received.rstrip())
        # time.sleep(5)
        message_received = arduino_serial.readline() # Get sensor Data
        print(message_received.rstrip())
    
    except Exception as error:
        print('SDI12 sensor reading failed')
        print(type(error))
        print(error)



def arduino_switches_test():
    index = 0

    try:
        user_timer = input("Duration of switch state in seconds, default 5 seconds: ")
        if (user_timer =='x'):
            return
        else:
            user_timer = float(user_timer)
    except ValueError:
        #Defaults to 5 seconds if user input anything other than a number or x
        user_timer = float(5)
    

    while index < len(arduino_swich_pins):
        
        power_pin = arduino_swich_pins[index]
        
        try:
            # if (PY3):
            #     user_pin = input("Arduino Switch, x escape, enter for #" + str(pin) + ": ")
            # else:
            #     user_pin = raw_input("Arduino Switch, x escape, enter for #" + str(pin) + ": ")
            user_pin = input("Arduino Switch, x escape, enter for #" + str(power_pin) + ": ")
            if (user_pin == ""):
                pass
            elif (is_escape(user_pin)):
                return
            elif (is_arduino_switch(user_pin)):
                power_pin = user_pin
                index = arduino_swich_pins.index(int(user_pin))
            else:
                continue
            
            # message_out = "power,{0},analog,9,point,3,interval_mm,200,debug,1".format(power_pin)
            message_out = "power_switch,{0},power_switch_status,1".format(power_pin)
            if DEBUG: print("DEBUG: " + message_out)
            arduino_serial.write(message_out)
            arduino_serial.flushInput()
            message_received = arduino_serial.readline()
            print(message_received.rstrip())

            # Duration for switch to stay on
            time.sleep(user_timer)

            message_out = "power_switch,{0},power_switch_status,0".format(power_pin)
            if DEBUG: print("DEBUG: " + message_out)
            arduino_serial.write(message_out)
            arduino_serial.flushInput()
            message_received = arduino_serial.readline()
            print(message_received.rstrip())

            index = index + 1
                
        except ValueError:
            # Prompt again if is incorrect power pin
            continue


def arduino_analog_test():
    index = 0
    while True:
        try:
            power_pin = input("Power Pin, 'x' to escape: ")
            if (is_escape(power_pin)):
                return
            elif ((power_pin == "") or (power_pin == '-1')):
                power_pin = -1
                break
            elif (power_pin.isalpha()):
                continue
            elif (is_arduino_switch(power_pin)):
                break
                
        except (ValueError):
            # Prompt for pin again if incorrect input
            print("Arduino Analog Test, Power Pin ValueError")
            break

    while index < len(arduino_analog_pins):

        analog_pin = arduino_analog_pins[index]

        try:
            user_pin = input("Arduino Analog, x escape, enter for #" + str(analog_pin) + ": ")
            if (user_pin == ""):
                pass
            elif (is_escape(user_pin)):
                return
            elif (is_arduino_analog_pin(user_pin)):
                analog_pin = user_pin
                index = arduino_analog_pins.index(int(user_pin))
            else:
                continue
            
            message_out = "analog,{0},power,{1},points,3,dummies,1,interval_mm,200,debug,1".format(analog_pin, power_pin)
            if DEBUG: print("DEBUG: " + message_out)
            arduino_serial.write(message_out)
            arduino_serial.flushInput()
            time.sleep(8)
            message_received = arduino_serial.readline()
            print(message_received.rstrip())

            index = index + 1
                
        except ValueError:
            # Prompt again if is incorrect power pin
            continue


def vsense_adc_check():
    vref = 5.1
    r1 = 0.0 #defined later
    r2 = 680.0

    while True:
        try:
            print("    1:   V2")
            print("    2:   V3")
            logger_version = input("Select logger version, 'x' to escape: ")
            if (is_escape(logger_version)):
                return
            elif (logger_version == ""):
                break
            elif (logger_version.isalpha()):
                continue
            elif (logger_version == '1'): # datalogger V2
                r1 = 2200
                break
            elif (logger_version == '2'): # datalogger V3.x
                r1 = 2000
                break
                
        except (ValueError):
            # Prompt for logger version again if incorrect input
            print("Vsense Test, logger version ValueError")
            break
    
    message_out = "analog,15,power,9,point,3,interval_mm,200,debug,1"
    if DEBUG: print("DEBUG: " + message_out)
    arduino_serial.write(message_out)
    arduino_serial.flushInput()
    time.sleep(1)
    message_received = arduino_serial.readline()
    print(message_received.rstrip())
    if (r1 > 0):
        array_received = message_received.split(',')[0:-1]
        voltage_value = float(array_received[-1]) * float(((r1 + r2)/r2)) * float((vref/1024))
        print("Battery Voltage: {0} (V)".format(str(voltage_value)))



def check_arduino_runtime_since_last_comm():
    message_out = "check_millis"
    if DEBUG: print("DEBUG: " + message_out)
    arduino_serial.write(message_out)
    arduino_serial.flushInput()
    time.sleep(1)
    message_received = arduino_serial.readline()
    print(message_received.rstrip())


def scan_i2c_multiplexer():
    while True:
        try:
            power_pin = input("Power Pin to switch for duration of scan, 'x' to escape: ")
            if (is_escape(power_pin)):
                return
            elif ((power_pin == "") or (power_pin == '-1')):
                power_pin = -1
                break
            elif (power_pin.isalpha()):
                continue
            elif (is_arduino_switch(power_pin)):
                break
                
        except (ValueError):
            # Prompt for pin again if incorrect input
            print("I2C Power Pin ValueError")
            continue
    
    if is_arduino_switch(power_pin):
        message_out = "power_switch,{0},power_switch_status,1".format(power_pin)
        if DEBUG: print("DEBUG: " + message_out)
        arduino_serial.write(message_out)
        arduino_serial.flushInput()
        time.sleep(1)

    message_out = "9548_search"
    if DEBUG: print("DEBUG: " + message_out)
    arduino_serial.write(message_out)
    arduino_serial.flushInput()
    time.sleep(1)
    message_received = ""
    while message_received != "Done\r\n":
        message_received = arduino_serial.readline()
        print(message_received.rstrip())
    
    if is_arduino_switch(power_pin):
        message_out = "power_switch,{0},power_switch_status,0".format(power_pin)
        if DEBUG: print("DEBUG: " + message_out)
        arduino_serial.write(message_out)
        arduino_serial.flushInput()
        time.sleep(1)



def display_options_menu():
    print("Select the following options for [" + HARDWARE_NAME + "] testing:\n")
    print("    1:   Arduino Handshake Serial COM")
    print("    2:   Reset Arduino")
    print("    3:   Onboard DHT22 Humidity and Temperature Sensor")
    print("    4:   RPI Switches")
    print("    5:   RPI digital IO as OUTPUT")
    print("    6:   RPI digital IO as INPUT")
    print("    7:   Arduino Switches")
    print("    8:   Arduino Analog IO as INPUT")
    print("    9:   SDI12 Sensor Ports")
    print("   10:   Scan I2C Multiplexer")
    print("   11:   Get onboard DC voltage via VSENSE, requires vsense\n         and jumper (switch 9) set correctly")
    print("   12:   Check Arduino Runtime Since Last Communication")
    print("    m:   Display This Main Options Menu")
    print("    x:   Exit")
    print("reset:   Initiate RPI RESET request from Arduino")
    print("debug:   Debug Mode Toggle")


#---------------------------- Main Loop ----------------------------------------
print("Starting serial...")
arduino_serial = serial.Serial(port = SERIAL_PORT, timeout = SERIAL_TIMEOUT_DEFAULT)
time.sleep(2)

display_options_menu()

while True:

    try:
        print("")
        user_option = input("Option: ")

        if (user_option == 'x'):
            break
        if (user_option == '1'):
            perform_handshake()
        elif (user_option == '2'):
            reset_arduino()
        elif (user_option == '3'):
            onboard_dht22_test()
        elif (user_option == '4'):
            rpi_switches_test()
        elif (user_option == '5'):
            rpi_digital_output_test()
        elif (user_option == '6'):
            rpi_digital_input_test()
        elif (user_option == '7'):
            arduino_switches_test()
        elif (user_option == '8'):
            arduino_analog_test()
        elif (user_option == '9'):
            sdi12_sensor_test()
        elif (user_option == '10'):
            scan_i2c_multiplexer()
        elif (user_option == '11'):
            vsense_adc_check()
        elif (user_option == '12'):
            check_arduino_runtime_since_last_comm()
        elif (user_option == 'm'):
            display_options_menu()
        elif (user_option == 'reset'):
            reset_rpi_by_arduino()
        elif (user_option == 'debug'):
            DEBUG = toggle_debug(DEBUG)

    except KeyboardInterrupt:
        arduino_serial.close()
        print("")
        exit()
    # except Exception as error:
            # print(type(error))
            # print(error)

#---------------------------- Cleaning Up --------------------------------------
arduino_serial.close()