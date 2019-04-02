#ifndef _SDI12_FUNCTION_H_
#define _SDI12_FUNCTION_H_

#include "Arduino.h"

/*
keeps track of active addresses
each bit represents an address:
1 is active (taken), 0 is inactive (available)
setTaken('A') will set the proper bit for sensor 'A'
set
*/

static volatile byte addressRegister[8] = {
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000
};

boolean sdi12_init(int sdi12_data);
void sdi12_loop(int sdi12_data);
void takeMeasurement_sdi12(char i, int sdi12_data);
void printBufferToScreen(int sdi12_data);
boolean checkActive(char i, int sdi12_data);
boolean setTaken(byte i);
boolean setVacant(byte i);
boolean isTaken(byte i);
void printInfo(char i, int sdi12_data);
byte charToDec(char i);
char decToChar(byte i);

#endif