#include <avr/sleep.h>
#include <avr/power.h>
#include <SoftwareSerial.h>

const byte AWAKE_LED = 8;
const byte GREEN_LED = 9;
const unsigned long WAIT_TIME = 5000;
const byte RX_PIN = 4;
const byte TX_PIN = 5;

SoftwareSerial mySerial(RX_PIN, TX_PIN); // RX, TX

void setup() 
{
  pinMode (GREEN_LED, OUTPUT);
  pinMode (AWAKE_LED, OUTPUT);
  digitalWrite (AWAKE_LED, HIGH);
  mySerial.begin(9600);
} // end of setup

unsigned long lastSleep;

void loop() 
{
  if (millis () - lastSleep >= WAIT_TIME)
  {
    lastSleep = millis ();

    noInterrupts ();

    byte old_ADCSRA = ADCSRA;
    // disable ADC
    ADCSRA = 0;  

    set_sleep_mode (SLEEP_MODE_PWR_DOWN);  
    power_adc_disable();
    power_spi_disable();
    power_timer0_disable();
    power_timer1_disable();
    power_timer2_disable();
    power_twi_disable();

    sleep_enable();
    digitalWrite (AWAKE_LED, LOW);
    interrupts ();
    sleep_cpu ();      
    digitalWrite (AWAKE_LED, HIGH);
    sleep_disable();
    power_all_enable();

    ADCSRA = old_ADCSRA;
  }  // end of time to sleep

  if (mySerial.available () > 0)
  {
    byte flashes = mySerial.read () - '0';
    if (flashes > 0 && flashes < 10)
      {
      // flash LED x times 
      for (byte i = 0; i < flashes; i++)
        {
        digitalWrite (GREEN_LED, HIGH);
        delay (200);  
        digitalWrite (GREEN_LED, LOW);
        delay (200);  
        }
      }        
  }  // end of if

}  // end of loop
