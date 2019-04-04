#include "timing.h"
#include "common.h"
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

void timeout_reset_pi() {
    if (millis() > TIMEOUT)
    {
        /*reset*/
        setMillis(0);
        isComm = FALSE;
        digitalWrite(PI_SW, HIGH);
        delay(DOWN_TIME);
        digitalWrite(PI_SW, LOW);
    }
}

void command_reset_pi(String content) {
    if (content == "RESET\n")
    {
        Serial.println("Reboot in 20 s....");
        delay(20000);
        setMillis(0);
        isComm = FALSE;
        digitalWrite(PI_SW, HIGH);
        delay(DOWN_TIME);
        digitalWrite(PI_SW, LOW);
    }
}

void timing_no_comm() {
    /*No communication reset millis*/
    if (isComm == TRUE)
    {
        setMillis(0);
        isComm = FALSE;
    }
}

void reset_timer() {
    setMillis(0);
    isComm = TRUE;
}