#ifndef _TIMMING_H_
#define _TIMMING_H_

#include "Arduino.h"

extern volatile unsigned long timer0_millis;
#define TIMEOUT (unsigned long)(5ul * 60ul * 60ul * 1000ul)
#define DOWN_TIME 3 * 1000 //seconds

void setMillis(unsigned long new_millis);

#endif
