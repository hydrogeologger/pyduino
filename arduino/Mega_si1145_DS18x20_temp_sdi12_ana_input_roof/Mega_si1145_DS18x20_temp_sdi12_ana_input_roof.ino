// this script is used for combining si1145 with all commercial systems

//--------------------below is required by Adafruit si1145 sensor ----------------

#include <Wire.h>
#include "Adafruit_SI1145.h"
Adafruit_SI1145 uv = Adafruit_SI1145();
//--------------------above is required by Adafruit si1145 sensor ----------------

//---------------------below required by temperature sensor-----------------------------------------------------------#
#include <OneWire.h>

// OneWire DS18S20, DS18B20, DS1822 Temperature Example
//
// http://www.pjrc.com/teensy/td_libs_OneWire.html
//
// The DallasTemperature library can do all this work for you!
// http://milesburton.com/Dallas_Temperature_Control_Library

OneWire  ds(11);  // on pin 10 (a 4.7K resistor is necessary)

//---------------------above required by temperature sensor-----------------------------------------------------------#


//---------------------below required by sdi12-----------------------------------------------------------#
#include <SDI12.h>

#define DATAPIN 10         // change to the proper pin,pwm pins are needed, see tutorial, only limited pins are able to get this
SDI12 mySDI12(DATAPIN); 

// keeps track of active addresses
// each bit represents an address:
// 1 is active (taken), 0 is inactive (available)
// setTaken('A') will set the proper bit for sensor 'A'
// set 
byte addressRegister[8] = { 
  0B00000000, 
  0B00000000, 
  0B00000000, 
  0B00000000, 
  0B00000000, 
  0B00000000, 
  0B00000000, 
  0B00000000 
}; 
//---------------------above required by sdi12-----------------------------------------------------------#


//-------------------below required by analog digital for moisture ---------------------

static const uint8_t analog_pins[]  = {A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13};
// the array below works for digital sensor arrays
//int digital_pins[] = {2, 3, 4, 5, 6, 7,  8, 9,10,11,12,13};
int digital_pins[] = {22,24,26,28,30,32,34,36,38,40,42,44};
float analogvals1[12];
int i;
// the delimiter between each reading. it is good to use ',' alwyas
char seperator=',';
//Arrays to store analog values after recieving them  
int number_sensors=12;
// the setup routine runs once when you press reset:

int number_readings=20;
int dummy_readings=30;
const char delimiter=',';
// -----------------ubove required by analog digital for moisture --------------------



void setup(void) {
  Serial.begin(9600);
  sdi12_init();
  // let all of the digital pins as output
  for (int i=0; i<number_sensors;i++){
      pinMode(digital_pins[i],OUTPUT);
  }
// -----------------------------below is required by si1145 sensor ------------

  if (! uv.begin()) {
    Serial.println("Didn't find Si1145");
    while (1);
  }
// -----------------------------above is required by si1145 sensor ------------

}

//void loop(void) {
//Serial.print("Soil");
//Serial.print(seperator);
//read_temp_sensors();
//ana_digi_loop();
//sdi12_loop();
//si1145_loop();
//Serial.println();
//delay(10000);
//delay_min(30);
//}

void loop(void) { 
    String content = "";
    char character;
    while(Serial.available()) {
        character = Serial.read();
        content.concat(character); 
        delay (10); 
    }
    if (content == "All") { 
        Serial.print("All");
        Serial.print(seperator);
        read_temp_sensors();
        ana_digi_loop();
        sdi12_loop();
        si1145_loop();
        Serial.println("AllDone");
    }
    else if (content == "Soil") {
        Serial.print("Soil");
        Serial.print(seperator);
        read_temp_sensors();
        ana_digi_loop();
        sdi12_loop();
        Serial.println("SoilDone");
    }
    else if (content == "Solar") {
        Serial.print("Solar");
        Serial.print(seperator);
        si1145_loop();
        Serial.println("SolarDone");
    }
    else {
      Serial.println(content);
    }
    }

}




// loop routine to obtain si1145 result
void si1145_loop() {
  Serial.print("Vis");
  Serial.print(seperator);
  Serial.print(uv.readVisible());
  Serial.print(seperator);
  Serial.print("IR");
  Serial.print(seperator);
  Serial.print(uv.readIR());
  Serial.print(seperator);
  
  // Uncomment if you have an IR LED attached to LED pin!
  //Serial.print("Prox: "); Serial.println(uv.readProx());

  float UVindex = uv.readUV();
  // the index is multiplied by 100 so to get the
  // integer index, divide by 100!
  UVindex /= 100.0;  
  Serial.print("UV");  
  Serial.print(seperator);
  Serial.print(UVindex);
  Serial.print(seperator);
  delay(1000);
}


// the loop routine runs over and over again forever:
void ana_digi_loop() {
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
    Serial.print("Mo");
    Serial.print(seperator);
    Serial.print(i);
    Serial.print(seperator);
    Serial.print(analogvals1[i]);
    Serial.print(seperator);

    }
    
    //delay_min(30);
    }


void sdi12_init(void) {
  Serial.begin(9600); 
  mySDI12.begin(); 
  delay(500); // allow things to settle

  //Serial.println("Scanning all addresses, please wait..."); 
  /*
      Quickly Scan the Address Space
   */

  for(byte i = '0'; i <= '9'; i++) if(checkActive(i)) setTaken(i);   // scan address space 0-9
  //for(byte i = 'a'; i <= 'z'; i++) if(checkActive(i)) setTaken(i);   // scan address space a-z
  //for(byte i = 'A'; i <= 'Z'; i++) if(checkActive(i)) setTaken(i);   // scan address space A-Z
  /*
      See if there are any active sensors. 
   */
  boolean found = false; 

  for(byte i = 0; i < 62; i++){
    if(isTaken(i)){
      found = true;
      break;
    }
  }

  if(!found) {
    Serial.println("No sensors found, please check connections and restart the Arduino."); 
    while(true);
  } // stop here
  
}

void read_temp_sensors(void) {

  byte i;
  byte present = 0;
  byte type_s;
  byte data[12];
  byte addr[8];
  float celsius;

  while ( ds.search(addr)) {
      // here only the second addr is print as it is suffice to distinguish the address
      Serial.write("Tp");
      Serial.write(delimiter);
      Serial.print(addr[1], HEX);
        
      if (OneWire::crc8(addr, 7) != addr[7]) {
          Serial.println("CRC is not valid!");
          return;
      }
    
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
      Serial.print(delimiter);
      Serial.print(celsius);
      Serial.write(delimiter);
  }
  
  ds.reset_search();
  delay(100);
  return;
}

void sdi12_loop(void){

  // scan address space 0-9
  for(char i = '0'; i <= '9'; i++) if(isTaken(i)){
    //Serial.print(millis()/1000);  //print the time since start
    //Serial.print(",");
    printInfo(i);   
    takeMeasurement_sdi12(i);
  }
  //Serial.println();
  //// scan address space a-z
  //for(char i = 'a'; i <= 'z'; i++) if(isTaken(i)){
  //  Serial.print(millis()/1000);
  //  Serial.print(",");
  //  printInfo(i);   
  //  takeMeasurement_sdi12(i);
  //} 

  //// scan address space A-Z
  //for(char i = 'A'; i <= 'Z'; i++) if(isTaken(i)){
  //  Serial.print(millis()/1000);
  //  Serial.print(",");
  //  printInfo(i);   
  //  takeMeasurement_sdi12(i);
  //};   
  
  delay(10000); // wait ten seconds between measurement attempts. 

}

void takeMeasurement_sdi12(char i){
  String command = ""; 
  command += i;
  command += "M!"; // SDI-12 measurement command format  [address]['M'][!]
  mySDI12.sendCommand(command); 
  while(!mySDI12.available()>5); // wait for acknowlegement with format [address][ttt (3 char, seconds)][number of measurments available, 0-9]
  delay(100); 
  
  mySDI12.read(); //consume address
  
  // find out how long we have to wait (in seconds).
  int wait = 0; 
  wait += 100 * mySDI12.read()-'0';
  wait += 10 * mySDI12.read()-'0';
  wait += 1 * mySDI12.read()-'0';
  
  mySDI12.read(); // ignore # measurements, for this simple examlpe
  mySDI12.read(); // ignore carriage return
  mySDI12.read(); // ignore line feed
  
  long timerStart = millis(); 
  while((millis() - timerStart) > (1000 * wait)){
    if(mySDI12.available()) break;                //sensor can interrupt us to let us know it is done early
  }
  
  // in this example we will only take the 'DO' measurement  
  mySDI12.flush(); 
  command = "";
  command += i;
  command += "D0!"; // SDI-12 command to get data [address][D][dataOption][!]
  mySDI12.sendCommand(command);
  while(!mySDI12.available()>1); // wait for acknowlegement  
  delay(300); // let the data transfer
  printBufferToScreen(); 
  mySDI12.flush(); 
}

void printBufferToScreen(){
  String buffer = "";
  mySDI12.read(); // consume address
  while(mySDI12.available()){
    char c = mySDI12.read();
    if(c == '+' || c == '-'){
      buffer += ',';   
      if(c == '-') buffer += '-'; 
    } 
    else {
      buffer += c;  
    }
    delay(100); 
  }
 buffer.replace("\n","");  // to remove the cartriage from the buffer
 buffer.replace("\r","");  // added to make sure all cartriage is removed
 //Serial.print(delimiter);
 Serial.print(buffer);
 Serial.print(delimiter);
}


// this checks for activity at a particular address     
// expects a char, '0'-'9', 'a'-'z', or 'A'-'Z'
boolean checkActive(char i){              

  String myCommand = "";
  myCommand = "";
  myCommand += (char) i;                 // sends basic 'acknowledge' command [address][!]
  myCommand += "!";

  for(int j = 0; j < 3; j++){            // goes through three rapid contact attempts
    mySDI12.sendCommand(myCommand);
    if(mySDI12.available()>1) break;
    delay(30); 
  }
  if(mySDI12.available()>2){       // if it hears anything it assumes the address is occupied
    mySDI12.flush(); 
    return true;
  } 
  else {   // otherwise it is vacant. 
    mySDI12.flush(); 
  }
  return false; 
}


// this sets the bit in the proper location within the addressRegister
// to record that the sensor is active and the address is taken. 
boolean setTaken(byte i){          
  boolean initStatus = isTaken(i);
  i = charToDec(i); // e.g. convert '0' to 0, 'a' to 10, 'Z' to 61. 
  byte j = i / 8;   // byte #
  byte k = i % 8;   // bit #
  addressRegister[j] |= (1 << k); 
  return !initStatus; // return false if already taken
}

// THIS METHOD IS UNUSED IN THIS EXAMPLE, BUT IT MAY BE HELPFUL. 
// this unsets the bit in the proper location within the addressRegister
// to record that the sensor is active and the address is taken. 
boolean setVacant(byte i){
  boolean initStatus = isTaken(i);
  i = charToDec(i); // e.g. convert '0' to 0, 'a' to 10, 'Z' to 61. 
  byte j = i / 8;   // byte #
  byte k = i % 8;   // bit #
  addressRegister[j] &= ~(1 << k); 
  return initStatus; // return false if already vacant
}


// this quickly checks if the address has already been taken by an active sensor           
boolean isTaken(byte i){         
  i = charToDec(i); // e.g. convert '0' to 0, 'a' to 10, 'Z' to 61. 
  byte j = i / 8;   // byte #
  byte k = i % 8;   // bit #
  return addressRegister[j] & (1<<k); // return bit status
}

// gets identification information from a sensor, and prints it to the serial port
// expects a character between '0'-'9', 'a'-'z', or 'A'-'Z'. 
char printInfo(char i){
  int j; 
  String command = "";
  command += (char) i; 
  command += "I!";
  for(j = 0; j < 1; j++){
    mySDI12.sendCommand(command);
    delay(30); 
    if(mySDI12.available()>1) break;
    if(mySDI12.available()) mySDI12.read(); 
  }

  Serial.write("SuTp");
  Serial.print(delimiter);
  while(mySDI12.available()){
    char c = mySDI12.read();
    if((c!='\n') && (c!='\r')) 
    {
      Serial.write(c); //print sensor info and type
    }
    delay(5); 
  } 
  //Serial.print(delimiter);
}

// converts allowable address characters '0'-'9', 'a'-'z', 'A'-'Z',
// to a decimal number between 0 and 61 (inclusive) to cover the 62 possible addresses
byte charToDec(char i){
  if((i >= '0') && (i <= '9')) return i - '0';
  if((i >= 'a') && (i <= 'z')) return i - 'a' + 10;
  if((i >= 'A') && (i <= 'Z')) return i - 'A' + 37;
}

// THIS METHOD IS UNUSED IN THIS EXAMPLE, BUT IT MAY BE HELPFUL. 
// maps a decimal number between 0 and 61 (inclusive) to 
// allowable address characters '0'-'9', 'a'-'z', 'A'-'Z',
char decToChar(byte i){
  if((i >= 0) && (i <= 9)) return i + '0';
  if((i >= 10) && (i <= 36)) return i + 'a' - 10;
  if((i >= 37) && (i <= 62)) return i + 'A' - 37;
}

void delay_min(int min){
  for (int i=0;i<min;i++)
  {
    for (int j=0;j<12;j++)
    {
      delay(5000);

    }
  }
}

