#include "timing.h"
#include "common.h"
#include "Arduino.h"
void setMillis(unsigned long new_millis)
/*
set the new value for millis()
*/
{
    uint8_t oldSREG = SREG;   // save the current status of arduino 'register'
    cli(); // stop interrupt "background service" service, which means freeze loop service.
    timer0_millis = new_millis;
    SREG = oldSREG;// remove 
    sei();// resume the interrupt background service 
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
    if (content == "RESET") 
    {
        Serial.println("Reboot in 5 s....");
        delay(1000);  // usually it is safe to have 30 sec to allow rpi reboot
		Serial.println("Reboot in 4 s....");
		delay(1000);  // usually it is safe to have 30 sec to allow rpi reboot
		Serial.println("Reboot in 3 s....");
		delay(1000);  // usually it is safe to have 30 sec to allow rpi reboot
		Serial.println("Reboot in 2 s....");
		delay(1000);  // usually it is safe to have 30 sec to allow rpi reboot
		Serial.println("Reboot in 1 s....");
		delay(1000);  // usually it is safe to have 30 sec to allow rpi reboot
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
