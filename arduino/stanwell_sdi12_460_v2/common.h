#ifndef _COMMON_H_
#define _COMMON_H_

#include "Arduino.h"

#define TRUE 1
#define FALSE 0
#define INVALID -1
#define DEFAULT_POINTS 5
#define DEFAULT_DUMMIES 3
#define DEFAULT_INTERVAL 10

/*
v 2.0 PCB global pins variables
*/
#define PI_SW 6
#define HUMIDITY_SEN_SW 2
#define MULTIPLEXER_SW 7
#define REVERSE_SW_1 10
#define REVERSE_SW_2 11
#define REVERSE_SW_3 12
#define REVERSE_SW_4 13
#define _12V5V_SW_1 8
#define _12V5V_SW_2 9

#define DIGITAL_DHT_COUNT = 6;
volatile static const int digi_dht_ay[] = {3, 4, 5};

#define ANALOG_MOIS_COUNT 6
volatile static const uint8_t ana_o2_ay[] = {A0, A1, A2, A3, A5, A6};
volatile static const uint8_t ana_moisture_ay[] = {A7, A8, A9, A10, A11, A12};

#define ANALOG_PIN_COUNT 16;
volatile static const uint8_t analog_pins[] = {A0, A1, A2, A3, A4,
                                      A5, A6, A7, A8, A9,
                                      A10, A11, A12, A13, A14,
                                      A15};

/* ATmega2560 / Arduino Mega or Mega 2560 compatible SDi-12 Pins
    0 (Rx0), 11, 12, 13, 14 (Tx3), 15 (Rx3), 50, 51, 52, 53, A8 (62), A9 (63),
    A10 (64), A11 (65), A12 (66), A13 (67), A14 (68), A15 (69)
*/
#define SDI12_PIN_COUNT 12
volatile static const uint8_t sdi12_pins[] = {50, 51, 52, 53, A8, A9, A10, A11,
        A12, A13, A14, A15};

#define PWM_PIN_COUNT 9
volatile static const uint8_t pwm_pins[] = {3, 4, 5, _12V5V_SW_1, _12V5V_SW_2,
        REVERSE_SW_1, REVERSE_SW_2, REVERSE_SW_3, REVERSE_SW_4};

#define DIGITAL_PIN_COUNT 37
volatile static int digi_out_pins[] = {
    22, 23, 24, 25, 26, 27, 28,
    29, 30, 31, 32, 33, 34, 35,
    36, 37, 38, 39, 40, 41, 42,
    43, 44, 45, 46, 47, 48, 49,
    MULTIPLEXER_SW, PI_SW, HUMIDITY_SEN_SW,
    REVERSE_SW_1, REVERSE_SW_2, REVERSE_SW_3, REVERSE_SW_4,
    _12V5V_SW_1, _12V5V_SW_2};

#define DELIMITER ','

#endif
