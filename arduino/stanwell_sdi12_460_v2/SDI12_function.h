#ifndef _SDI12_FUNCTION_H_
#define _SDI12_FUNCTION_H_

#include "Arduino.h"
#include <SDI12.h>

#define MAX_NUM_ADDR 62

static volatile uint32_t addressSpace[2] = {(uint32_t)0x00, (uint32_t)0x00};

static SDI12 mySDI12(0);


void process_command(String cmd, int sensors, String new_addr, boolean isCustom);
boolean sdi12_check_pin(int sdi12_data);
boolean sdi12_init(int sdi12_pin);
int8_t sdi12_scan(void);
void sdi12_end(void);
void sdi12_loop_get_measurements();
void sdi12_loop();
void takeMeasurement_sdi12(char i);
uint8_t printBufferToScreen(void);
boolean checkActive(char i);
uint8_t convert_char_to_bit_number(char c);
char convert_bit_number_to_char(uint8_t bit);
boolean setTaken(char c);
boolean isTaken(char c);
void printInfo(char i);
boolean sdi12_change(char new_addr);
void sdi12_send_command(String cmd, boolean read);
#endif