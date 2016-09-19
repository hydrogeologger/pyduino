/*This code combines: 
 1. mux schield 2 with 16 moisture sensor installed at port I/O 2,
 The sensor is powered by mux schield port I/O3. please be reminded that I/O2 needs to
 be set as input while I/O3 needs to set as ouput.
 2. digital pin at port 2 with 10 temperature sensor (DS18B20) installed
 Developed by Chenming TO160914
 Cable wiring hints: 
 1. A 10k ohm pull down resistor ( brown black orange gold with yellow background)
 needs to be installed between GND and I/O2 (i.e., A1)
so that interferences between neighbouring ports are prevented. (once interference 
occurrs, the downstream ports will have decreasing ghost values over the distance
from the the port with sensor installed. although having a sensor installed downstream
will prevent such )
 2. A 4.7k ohm (currenly red brown orange black green brown with light blue background )
 pull up resistor needs to be installed between 5V and signal
 
 */

// -------------------- needed by mux schield -----------------------
#include <MuxShield.h>
//Initialize the Mux Shield
MuxShield muxShield;


// the delimiter between each reading. it is good to use ',' alwyas
char seperator=',';
//Arrays to store analog values after recieving them
int number_sensors=3;
// define toggles for I/O3, which are used for output;
//int toggle[16]=LOW;
//int IO1AnalogVals[16];
int IO2AnalogVals[3];
//int IO3AnalogVals[16];
//digitalWrite(A1, LOW);
//digitalWrite(A0, LOW);
// Defining the waiting time between each readings;

int delay_mmsec=100;

// the powered sensor reading, there are two properties, on and off
int delay_sensor_reading=2000;
// finish writting 
int delay_after_writting=1000;

int delay_reading_each_ports=1000;





// -------------------- needed by digital sensor --------------------
#include <OneWire.h>
OneWire  ds(3);  // on digita pin 2 (a 4.7K resistor is necessary)


void setup()
{
    // -------------------- needed by mux schield -----------------------
     //open up the internal pull-up resistor
     // it is confirmed that if using a 10k ohm +-5% resistor between 5+ and gnd, 
     // the noise will be completely removed. This setup means to install a PULLDOWN
     // Resistor between signal and ground TO160905.
     // However: if both the resistor and the following code

    //Set I/O 1, I/O 2, and I/O 3 as analog inputs
    muxShield.setMode(1,ANALOG_IN);
    muxShield.setMode(2,ANALOG_IN);
    //muxShield.setMode(3,ANALOG_IN);
    muxShield.setMode(3,DIGITAL_OUT);
    Serial.begin(9600);
    
    // -------------------- needed by digital sensor-------------------
}


void loop()
{
// -------------------------------- required by onewire  -------------------
  byte i;
  byte present = 0;
  byte type_s;
  byte data[12];
  byte addr[8];
  //float celsius, fahrenheit;
  float celsius;

  if ( !ds.search(addr)) {
    Serial.print(",No more addresses.,");
    read_muxschield();
    // Serial.println();
    ds.reset_search();
    delay(3000);
    return;
  }

  Serial.print("ROM =");
  for( i = 0; i < 8; i++) {
    Serial.write(' ');
    Serial.print(addr[i], HEX);
  }

  if (OneWire::crc8(addr, 7) != addr[7]) {
      Serial.println("CRC is not valid!");
      return;
  }
  //Serial.println();

  // the first ROM byte indicates which chip
  switch (addr[0]) {
    case 0x10:
      //Serial.println("  Chip = DS18S20");  // or old DS1820
      type_s = 1;
      break;
    case 0x28:
      //Serial.println("  Chip = DS18B20");
      type_s = 0;
      break;
    case 0x22:
      //Serial.println("  Chip = DS1822");
      type_s = 0;
      break;
    default:
      //Serial.println("Device is not a DS18x20 family device.");
      return;
  } 

  ds.reset();
  ds.select(addr);
  ds.write(0x44);        // start conversion, use ds.write(0x44,1) with parasite power on at the end

  delay(100);     // maybe 750ms is enough, maybe not
  // we might do a ds.depower() here, but the reset will take care of it.

  present = ds.reset();
  ds.select(addr);    
  ds.write(0xBE);         // Read Scratchpad

  //Serial.print("  Data = ");
  //Serial.print(present, HEX);
  //Serial.print(" ");
  for ( i = 0; i < 9; i++) {           // we need 9 bytes
    data[i] = ds.read();
    //Serial.print(data[i], HEX);
    //Serial.print(" ");
  }
  //Serial.print(" CRC=");
  //Serial.print(OneWire::crc8(data, 8), HEX);
  //Serial.println();

  // Convert the data to actual temperature
  // because the result is a 16 bit signed integer, it should
  // be stored to an "int16_t" type, which is always 16 bits
  // even when compiled on a 32 bit processor.
  int16_t raw = (data[1] << 8) | data[0];
  if (type_s) {
    raw = raw << 3; // 9 bit resolution default
    if (data[7] == 0x10) {
      // "count remain" gives full 12 bit resolution
      raw = (raw & 0xFFF0) + 12 - data[6];
    }
  } else {
    byte cfg = (data[4] & 0x60);
    // at lower res, the low bits are undefined, so let's zero them
    if (cfg == 0x00) raw = raw & ~7;  // 9 bit resolution, 93.75 ms
    else if (cfg == 0x20) raw = raw & ~3; // 10 bit res, 187.5 ms
    else if (cfg == 0x40) raw = raw & ~1; // 11 bit res, 375 ms
    //// default is 12 bit resolution, 750 ms conversion time
  }
  celsius = (float)raw / 16.0;
  //fahrenheit = celsius * 1.8 + 32.0;
  Serial.print(",Temp.,");
  Serial.print(celsius);
  Serial.print(" ,Celsius, ");
  //Serial.print(fahrenheit);
  //Serial.println(" ,Fahrenheit");
  
}



/* this subroutine reads all ports from I/O2, as powered by I/O 3.*/
void read_muxschield(){
// -------------------- needed by mux schield -----------------------
  for (int i=0; i<number_sensors; i++)
  {
    //Analog read on all 16 inputs on IO1, IO2, and IO3
    //IO1AnalogVals[i] =0;
    //IO1AnalogVals[i] = muxShield.analogReadMS(1,i);
    muxShield.digitalWriteMS(3,i,HIGH);
    delay(delay_sensor_reading);
    IO2AnalogVals[i] = muxShield.analogReadMS(2,i);
    delay(delay_sensor_reading);
    muxShield.digitalWriteMS(3,i,LOW);

    //IO3AnalogVals[i] = muxShield.analogReadMS(3,i);
    delay(delay_reading_each_ports);
  }
  
  //Print IO1 values for inspection
  Serial.print("IO2 analog");
  Serial.print(seperator);
  for (int i=0; i<number_sensors; i++)
  {
    //Serial.print(IO1AnalogVals[i]);
    Serial.print(IO2AnalogVals[i]);
    Serial.print(seperator);
  }
  //Serial.println();
  delay(delay_after_writting);
}
 //
//orange brown red black green brown with light blue background 312 Ohms 0.5% 100ppm//
//brown green black red brown orange with light blue background 15k Ohms 1% 15 ppm//
//need to check the resistance from volt meter//

