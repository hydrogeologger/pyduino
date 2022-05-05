#!/usr/bin/python
'''
SIM7600 4G modem utility python script
'''
import sys
import traceback
import time
import serial
import RPi.GPIO as GPIO

GPIO_BCM_POWER_KEY = 6

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
    print("Unknown python version - some functions may not function appropriately")


def send_at(ser, at_send, at_back, delay=1, display=True):
    '''
    AT command message wrapper.

    :param ser: Serial object
    :param at_send: AT message to send
    :param at_back: Expected response
    :param delay: Time to wait after sending to retrieve in seconds, default=1
    :param display: Displays response, default=True
    :returns: 1 expected response, 0 incorrect response to AT message
    '''
    rec_buff = ""
    ser.flushInput()
    ser.write((at_send+'\r\n').encode())
    time.sleep(delay)
    if ser.inWaiting():
        time.sleep(0.01)
        rec_buff = ser.read(ser.inWaiting())
    if at_back not in rec_buff.decode():
        if (display):
            print(at_send + ' ERROR')
            print(at_send + ' back:\t' + rec_buff.decode())
        return 0
    else:
        if (display):
            print(rec_buff.decode())
        return 1

def sim7600_is_on(ser):
    '''
    Checks if SIM7600 module is on

    :param ser: Serial object
    :returns: True (on)/False (Off)
    '''
    ser.flushInput()
    ser.write(("AT\r\n").encode())
    time.sleep(0.1)
    if ser.inWaiting():
        time.sleep(0.01)
        rec_buff = ser.read(ser.inWaiting())
        if ("OK" in rec_buff.decode()):
            return True
    return False

def power_on(power_key):
    '''
    Toggles PWRKEY via GPIO to turn SIM7600 on.

    :param power_key: BCM GPIO number for PWRKEY
    '''
    print('SIM7600X is starting:')
    GPIO.output(power_key, GPIO.HIGH)
    # Minimum time to hold PWRKEY low to turn on is 100ms, 0.5seconds typical
    time.sleep(0.5)
    GPIO.output(power_key, GPIO.LOW)
    # time.sleep(20)

def power_down(power_key):
    '''
    Toggles PWRKEY via GPIO to turn SIM7600 off.

    :param power_key: BCM GPIO number for PWRKEY
    '''
    print('SIM7600X is loging off:')
    GPIO.output(power_key, GPIO.HIGH)
    # Minimum time to hold PWRKEY low to turn off is 2.5seconds
    time.sleep(3)
    GPIO.output(power_key, GPIO.LOW)
    # time.sleep(18)
    print('Good bye')

def gpio_init(power_key):
    '''
    Configure and initialize PWRKEY GPIO pin

    :param power_key: BCM GPIO number for PWRKEY
    '''
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(power_key, GPIO.OUT)
    time.sleep(0.1)

def serial_session(ser):
    '''
    Serial AT command session

    :param ser: Serial object
    '''
    rec_buff = ""
    ser.flushInput()
    while True:
        command_input = input('Please input the AT command:')
        if command_input == "exit":
            return
        ser.write((command_input + "\r\n").encode())
        time.sleep(0.1)
        if ser.inWaiting():
            time.sleep(0.01)
            rec_buff = ser.read(ser.inWaiting())
        if rec_buff != '':
            print(rec_buff.decode())
            rec_buff = ''

def display_menu():
    print("{0:>2s}:  {1}".format("1", "AT command Serial Session"))
    print("{0:>2s}:  {1}".format("2", "Send \"AT\""))
    print("{0:>2s}:  {1}".format("3", "Send \"AT+CSQ\" Get signal strength"))
    print("{0:>2s}:  {1}".format("4", "Send \"AT+CGREG?\" Registration Status"))
    print("{0:>2s}:  {1}".format("5", "Send \"AT+COPS?\" Current mobile network"))
    print("{0:>2s}:  {1}".format("6", "Send \"AT+CPSI?\" Get UE sys information"))
    print("{0:>2s}:  {1}".format("7", "Send \"AT+CRESET\" Reboot sys"))
    print("{0:>2s}:  {1}".format("8", "Toggle PWRKEY to reboot"))
    print("{0:>2s}:  {1}".format("m", "Display menu"))
    print("")

def main():
    # if (len(sys.argv) > 1):
    #     arg = sys.argv[1]
    # else:
    #     arg = ""
    try:
        ser = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=2)
        
        if (not sim7600_is_on(ser)):
            gpio_init(GPIO_BCM_POWER_KEY)
            power_on(GPIO_BCM_POWER_KEY)
            print("Wait 16 seconds for boot sequence")
            time.sleep(16)
            print('SIM7600X is ready')
        else:
            print("SIM7600X already on")

        display_menu()
        while True:
            user_option = input("Selection: ")
            if user_option == "x" or user_option == "exit":
                exit()
            elif user_option == "1":
                serial_session(ser)
            elif user_option == "2":
                send_at(ser, 'AT', 'OK', 1)
            elif user_option == "3":
                send_at(ser, "AT+CSQ", "OK", 1)
            elif user_option == "4":
                send_at(ser, "AT+CGREG?", "OK", 1)
            elif user_option == "5":
                send_at(ser, "AT+COPS?", "OK", 1)
            elif user_option == "6":
                send_at(ser, "AT+CPSI?", "OK", 1)
            elif user_option == "7":
                send_at(ser, "AT+CRESET", "OK", 1)
            elif user_option == "8":
                power_down(GPIO_BCM_POWER_KEY)
                print("Wait 26 seconds for boot sequence")
                time.sleep(26)
                power_on(GPIO_BCM_POWER_KEY)
                print("Wait 16 seconds for boot sequence")
                time.sleep(16)
                print('SIM7600X is ready')
            elif user_option == "m":
                display_menu()

    # try:
        # if arg == "off":
        #     gpio_init(GPIO_BCM_POWER_KEY)
        #     power_down(GPIO_BCM_POWER_KEY)

        # elif arg == "status":
        #     send_at(ser, 'AT', 'OK', 1)

        # elif arg == "reboot":
        #     send_at(ser, "AT+CRESET", "OK", 1)

        # elif arg == "serial":
        #     if (not sim7600_is_on(ser)):
        #         gpio_init(GPIO_BCM_POWER_KEY)
        #         power_on(GPIO_BCM_POWER_KEY)
        #         print("Wait 16 seconds for boot sequence")
        #         time.sleep(16)
        #         print('SIM7600X is ready')
        #     serial_session(ser)

        # else:
        #     if (not sim7600_is_on(ser)):
        #         gpio_init(GPIO_BCM_POWER_KEY)
        #         power_on(GPIO_BCM_POWER_KEY)
        #     else:
        #         print("SIM7600X already on")

    except KeyboardInterrupt:
        print("")
    except Exception:
        traceback.print_exc()
    finally:
        if ser.isOpen():
            ser.close()
        GPIO.setwarnings(False)
        GPIO.cleanup()

if __name__ == "__main__":
    main()
