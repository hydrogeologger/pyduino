#include "timing.h"
#include "Arduino.h"
/*
set the new value for millis()
*/
void setMillis(unsigned long new_millis)
{
    uint8_t oldSREG = SREG;
    cli();
    timer0_millis = new_millis;
    SREG = oldSREG;
    sei();
}
