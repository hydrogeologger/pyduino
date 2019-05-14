#include "timing.h"
#include "common.h"
#include "Arduino.h"
/*
set the new value for millis()
*/
void setMillis(unsigned long new_millis)
{
    uint8_t oldSREG = SREG;   // what are these?
    cli(); // what are these?
    timer0_millis = new_millis;
    SREG = oldSREG;// what are these?
    sei();// what are these?
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
    //if (content == "RESET\n")
    if (content == "RESET") 
    {
        Serial.println("Reboot in 30 s....");
        delay(30000);  // usually it is safe to have 30 sec to allow rpi reboot
        setMillis(0);
        isComm = FALSE;
        digitalWrite(PI_SW, HIGH);
        delay(DOWN_TIME);
        digitalWrite(PI_SW, LOW);
    }
}

void command_check_millis(String content) {
    if (content == "check_millis") 
    {
        Serial.print("The current mill is: ");
        Serial.println(millis());
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
