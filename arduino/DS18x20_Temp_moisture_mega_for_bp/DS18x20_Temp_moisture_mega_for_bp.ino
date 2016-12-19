#include <OneWire.h>

// OneWire DS18S20, DS18B20, DS1822 Temperature Example
//
// http://www.pjrc.com/teensy/td_libs_OneWire.html
//
// The DallasTemperature library can do all this work for you!
// http://milesburton.com/Dallas_Temperature_Control_Library

OneWire  ds(24);  // on pin 10 (a 4.7K resistor is necessary)
const char delimiter=',';
/* above is needed for temperature sensor*/ 


// below is needed for analog sensor  

static const uint8_t analog_pins[]  = {A0,A1,A2,A3,A4,A5,A8,A9,A10,A11,A12,A13};
//static const uint8_t digital_pins[] = {2,3,4,5,6,7};
// the array below works for digital sensor arrays
int digital_pins[] = {2, 3, 4, 5, 6, 7,8,9,10,11,12,13};
float analogvals1[12];
int i;
// the delimiter between each reading. it is good to use ',' alwyas
char seperator=',';
//Arrays to store analog values after recieving them  
int number_sensors=12;
// the setup routine runs once when you press reset:

int number_readings=20;

int dummy_readings=30;

// above is needed for analog sensor




void setup(void) {
  Serial.begin(9600);

  // let all of the digital pins as output needed for analog sensor
  for (int i=0; i<number_sensors;i++){
      pinMode(digital_pins[i],OUTPUT);
  }
}

void loop(void) {
read_temp_sensors();
//delay_min(30);
}




// the loop routine runs over and over again forever:
void read_analog_loop() {
  // read the input on analog pin 0
  for (int i=0; i<number_sensors;i++){
    analogvals1[i]=0;
    digitalWrite(digital_pins[i],HIGH);
    delay(1000);

    for (int j=0;j<dummy_readings;j++){
      analogRead(analog_pins[i]);
      //delay(100);
    }

    for (int j=0;j<number_readings;j++){
      analogvals1[i]+=analogRead(analog_pins[i]);
      delay(10);
    }

    analogvals1[i]=analogvals1[i]/number_readings;
    digitalWrite(digital_pins[i],LOW);
 }
    
    for (int i=0; i<number_sensors;i++)
    {
    //serial.print(i);
    //serial.print(seperator);
    Serial.print(analogvals1[i]);
    Serial.print(seperator);

    }
    
    Serial.println();
    delay(5000);
    //delay_min(30);
    }
    
/* delay in minutes 
the reason of having these functions, as compared to delay(60*60*1000) is the fact 
  that the later is not working, persumablly the maxmum value in arduino is 65536*/ 
void delay_min(int min){
  for (int i=0;i<min;i++)
  {
    for (int j=0;j<6;j++)
    {
      delay(10000);
      
    }
  }
}

void read_temp_sensors(void) {

  byte i;
  byte present = 0;
  byte type_s;
  byte data[12];
  byte addr[8];
  float celsius;//, //fahrenheit;
  
  if ( !ds.search(addr)) {
    //Serial.println("No more addresses.");
    //Serial.println();
    Serial.print(delimiter);
    read_analog_loop();
    ds.reset_search();
    //delay_min(30);
    delay(100);
    return;
  }

  /*
  //Serial.print("ROM =");
  for( i = 0; i < 8; i++) {
    Serial.write(delimiter);
    Serial.print(addr[i], HEX);
    //Serial.print(addr[i].remove(5), HEX);
  }
  */
  // here only the second addr is print as it is suffice to distinguish the address
  Serial.write(delimiter);
  Serial.print(addr[1], HEX);
    
  if (OneWire::crc8(addr, 7) != addr[7]) {
      Serial.println("CRC is not valid!");
      return;
  }
  //Serial.println();
 
  // the first ROM byte indicates which chip
  /*
  switch (addr[0]) {
    case 0x10:
      Serial.println("  Chip = DS18S20");  // or old DS1820
      type_s = 1;
      break;
    case 0x28:
      Serial.println("  Chip = DS18B20");
      type_s = 0;
      break;
    case 0x22:
      Serial.println("  Chip = DS1822");
      type_s = 0;
      break;
    default:
      Serial.println("Device is not a DS18x20 family device.");
      return;
  } 
  */
  ds.reset();
  ds.select(addr);
  ds.write(0x44, 1);        // start conversion, with parasite power on at the end
  
  delay(1000);     // maybe 750ms is enough, maybe not
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
  //Serial.print(delimiter);
  //Serial.print("  Temperature = ");
  Serial.print(delimiter);
  Serial.print(celsius);
  //Serial.print(delimiter);
  //Serial.print(" Celsius, ");
  //Serial.print(delimiter);


}







