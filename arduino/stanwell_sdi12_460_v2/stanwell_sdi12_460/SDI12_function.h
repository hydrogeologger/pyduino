#ifndef _SDI12_FUNCTION_H_
#define _SDI12_FUNCTION_H_

#include "Arduino.h"
#include <SDI12.h>

#define MAX_NUM_ADDR 62
static volatile uint64_t addressSpace = (uint64_t)0x00;

static SDI12 mySDI12(0);
static boolean isInit = false;

boolean sdi12_check_pin(int sdi12_data);
boolean sdi12_init(int sdi12_data);
void sdi12_loop();
void takeMeasurement_sdi12(char i);
void printBufferToScreen();
boolean checkActive(char i);
uint8_t convert_char_to_bit_number(char c);
char convert_bit_number_to_char(uint8_t bit);
boolean setTaken(char c);
boolean isTaken(char c);
void printInfo(char i);
#endif