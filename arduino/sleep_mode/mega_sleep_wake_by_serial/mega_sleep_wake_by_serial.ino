/* Sleep Demo Serial
 *  https://arduino.stackexchange.com/questions/13167/put-atmega328-in-very-deep-sleep-and-listen-to-serial
 * -----------------
 * Example code to demonstrate the sleep functions in a Arduino. Arduino will wake up
 * when new data is received in the serial port USART
 * Based on Sleep Demo Serial from http://www.arduino.cc/playground/Learning/ArduinoSleepCode
 *
 * Copyright © 2006 MacSimski 2006-12-30
 * Copyright © 2007 D. Cuartielles 2007-07-08 - Mexico DF
 *
 * With modifications from Ruben Laguna 2008-10-15
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 *
 */

#include <avr/power.h>
#include <avr/sleep.h>

int sleepStatus = 0; // variable to store a request for sleep
int count = 0; // counter

void setup()
{

Serial.begin(9600);
}

void sleepNow()
{
/* Now is the time to set the sleep mode. In the Atmega8 datasheet
 * http://www.atmel.com/dyn/resources/prod_documents/doc2486.pdf on page 35
 * there is a list of sleep modes which explains which clocks and
 * wake up sources are available in which sleep modus.
 *
 * In the avr/sleep.h file, the call names of these sleep modus are to be found:
 *
 * The 5 different modes are:
 * SLEEP_MODE_IDLE -the least power savings % the only one that can be wake up by serial
 * SLEEP_MODE_ADC  % not wake up by serial
 * SLEEP_MODE_PWR_SAVE  % not wake up by serial
 * SLEEP_MODE_STANDBY  % not wake up by serial
 * SLEEP_MODE_PWR_DOWN -the most power savings %not wake up by serial
 *
 * the power reduction management <avr/power.h> is described in
 * http://www.nongnu.org/avr-libc/user-manual/group_avr_power.html
 */

set_sleep_mode(SLEEP_MODE_IDLE); // sleep mode is set here

sleep_enable(); // enables the sleep bit in the mcucr register
// so sleep is possible. just a safety pin

power_adc_disable();
power_spi_disable();
power_timer0_disable();
power_timer1_disable();
power_timer2_disable();
power_twi_disable();

sleep_mode(); // here the device is actually put to sleep!!

// THE PROGRAM CONTINUES FROM HERE AFTER WAKING UP
sleep_disable(); // first thing after waking from sleep:
// disable sleep...

power_all_enable();

}

void loop()
{
// display information about the counter
Serial.print("Awake for ");
Serial.print(count);
Serial.println("sec");
count++;
delay(1000); // waits for a second

// compute the serial input
if (Serial.available()) {
int val = Serial.read();
if (val =='S') {
      Serial.println("Serial: Entering Sleep mode");
      delay(100);     // this delay is needed, the sleep
                      //function will provoke a Serial error otherwise!!
      count = 0;
      sleepNow();     // sleep function called here
    }
    if (val=='A') {
Serial.println("Hola Caracola"); // classic dummy message
}
}

// check if it should go asleep because of time
if (count >= 10) {
Serial.println("Timer: Entering Sleep mode");
delay(100); // this delay is needed, the sleep
//function will provoke a Serial error otherwise!!
count = 0;
sleepNow(); // sleep function called here
}
} //loop
