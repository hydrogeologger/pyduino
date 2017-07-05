char delimiter =',';
//---------------------below required by sdi12-----------------------------------------------------------#
#include <SDI12.h>

#define DATAPIN 12         // change to the proper pin,pwm pins are needed, see tutorial, only limited pins are able to get this
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


//---------------------below required by module heat_suction_sensor----------------------------------------------------#
#include <OneWire.h>
OneWire  ds(3);  // on pin 10 (a 4.7K resistor is necessary)
// OneWire DS18S20, DS18B20, DS1822 Temperature Example
//
// http://www.pjrc.com/teensy/td_libs_OneWire.html
//
// The DallasTemperature library can do all this work for you!
// http://milesburton.com/Dallas_Temperature_Control_Library

byte heat_suction_sensor_1_addr[8];
byte heat_suction_sensor_2_addr[8];
byte heat_suction_sensor_3_addr[8];

int  heat_suction_sensor_heat_sw_1= 6;
int  heat_suction_sensor_heat_sw_2= 5;
int  heat_suction_sensor_heat_sw_3= 4;
int  temp_sampling_number =20;
int  temp_sampling_interval_ms=10;
//int  temp_sampling_number =20;
//int  temp_sampling_interval_ms=100;

//---------------------above required by module heat_suction_sensor----------------------------------------------------#


//---------------------below required by module salinity_humidity_sensor----------------------------------------------------#

#include <dht.h>
dht DHT;
#define DHT22_PIN_1 2
#define DHT22_PIN_2 11
//---------------------above required by module salinity_humidity_sensor----------------------------------------------------#



//-------------------below required by analog digital for moisture ---------------------

static const uint8_t moist_analog_pins[]  = {A1,A2,A3,A4};
int moist_digital_pins[] = {7,8,9,10};
int moist_number_readings=7;
int moist_dummy_readings=3;
int const moist_number_sensors=sizeof(moist_analog_pins);
float moist_data[moist_number_sensors];

//-------------------above required by analog digital for moisture ---------------------

void setup() {
  Serial.begin(9600); // open serial port, set the baud rate as 9600 bps
  sdi12_init();
  pinMode(3, OUTPUT);



//---------------------below required by module analog moisture sensor----------------------------------------------------#

  for (int i=0; i<moist_number_sensors;i++){
      pinMode(moist_digital_pins[i],OUTPUT);
  }
//---------------------above required by module analog moisture sensor----------------------------------------------------#



//---------------------below required by module heat_suction_sensor----------------------------------------------------#
// define the address
////const char  addr='28E5A34A8007F';
//heat_suction_sensor_1_addr[0]=0x28;
//heat_suction_sensor_1_addr[1]=0xE5;
//heat_suction_sensor_1_addr[2]=0xA3;
//heat_suction_sensor_1_addr[3]=0x4A;
//heat_suction_sensor_1_addr[4]=0x08;
//heat_suction_sensor_1_addr[5]=0x00;
//heat_suction_sensor_1_addr[6]=0x00;
//heat_suction_sensor_1_addr[7]=0x7F;
////addr[0]=0x2847A686800B4;
//heat_suction_sensor_2_addr[0]=0x28;
//heat_suction_sensor_2_addr[1]=0x47;
//heat_suction_sensor_2_addr[2]=0xA6;
//heat_suction_sensor_2_addr[3]=0x86;
//heat_suction_sensor_2_addr[4]=0x08;
//heat_suction_sensor_2_addr[5]=0x00;
//heat_suction_sensor_2_addr[6]=0x00;
//heat_suction_sensor_2_addr[7]=0xB4;

// define the address
//const char  addr='28E5A34A8007F';
// the digital channel for this sensor is 3
heat_suction_sensor_1_addr[0]=0x28;
heat_suction_sensor_1_addr[1]=0x96;
heat_suction_sensor_1_addr[2]=0xA2;
heat_suction_sensor_1_addr[3]=0x29;
heat_suction_sensor_1_addr[4]=0x08;
heat_suction_sensor_1_addr[5]=0x00;
heat_suction_sensor_1_addr[6]=0x00;
heat_suction_sensor_1_addr[7]=0x6B;


//ROM = 28 70 13 CE 8 0 0 BD,  Temperature = 23.00 Celsius, 73.40 Fahrenheit
//ROM = 28 96 A2 29 8 0 0 6B,  Temperature = 22.50 Celsius, 72.50 Fahrenheit
//ROM = 28 A7 B6 96 8 0 0 D9,  Temperature = 22.62 Celsius, 72.72 Fahrenheit

heat_suction_sensor_2_addr[0]=0x28;
heat_suction_sensor_2_addr[1]=0x70;
heat_suction_sensor_2_addr[2]=0x13;
heat_suction_sensor_2_addr[3]=0xCE;
heat_suction_sensor_2_addr[4]=0x08;
heat_suction_sensor_2_addr[5]=0x00;
heat_suction_sensor_2_addr[6]=0x00;
heat_suction_sensor_2_addr[7]=0xBD;

heat_suction_sensor_3_addr[0]=0x28;
heat_suction_sensor_3_addr[1]=0xA7;
heat_suction_sensor_3_addr[2]=0xB6;
heat_suction_sensor_3_addr[3]=0x96;
heat_suction_sensor_3_addr[4]=0x08;
heat_suction_sensor_3_addr[5]=0x00;
heat_suction_sensor_3_addr[6]=0x00;
heat_suction_sensor_3_addr[7]=0xD9;

pinMode(heat_suction_sensor_heat_sw_1, OUTPUT);  // switch for heating sucktion sensor 1
pinMode(heat_suction_sensor_heat_sw_2, OUTPUT);  // switch for heating sucktion sensor 2
pinMode(heat_suction_sensor_heat_sw_3, OUTPUT);  // switch for heating sucktion sensor 3

//---------------------above required by module heat_suction_sensor----------------------------------------------------#

}


//void loop() {
//Serial.print("Soil1,");
//heat_suction_sensor(heat_suction_sensor_1_addr,heat_suction_sensor_heat_sw_1,temp_sampling_number,temp_sampling_interval_ms); 
//delay(2000);
//heat_suction_sensor(heat_suction_sensor_2_addr,heat_suction_sensor_heat_sw_2,temp_sampling_number,temp_sampling_interval_ms); 
//delay(2000);
//read_salinity_humidity_sensor(DHT22_PIN_2);
//delay(2000);
//read_salinity_humidity_sensor(DHT22_PIN_1);
//delay(2000);
//read_analog_moisture_sensor();
//delay(2000);
//Serial.println();
//}
void loop(void) {
    String content = "";
    char character;
    while(Serial.available()) {
        character = Serial.read();
        content.concat(character);
        delay (10);
    }
    if (content != ""){
        if (content == "All") {
            Serial.print("All");
            Serial.print(delimiter);

            heat_suction_sensor(heat_suction_sensor_3_addr,heat_suction_sensor_heat_sw_3,temp_sampling_number,temp_sampling_interval_ms); 
            heat_suction_sensor(heat_suction_sensor_2_addr,heat_suction_sensor_heat_sw_2,temp_sampling_number,temp_sampling_interval_ms); 
            heat_suction_sensor(heat_suction_sensor_1_addr,heat_suction_sensor_heat_sw_1,temp_sampling_number,temp_sampling_interval_ms);     
            read_salinity_humidity_sensor(DHT22_PIN_1);
            read_salinity_humidity_sensor(DHT22_PIN_2);
            read_analog_moisture_sensor();
            sdi12_loop();

            Serial.println("AllDone");
        }
        else if (content == "SoilMoisture") {
            Serial.print("SoilMoisture");
            Serial.print(delimiter);
            read_analog_moisture_sensor();
            Serial.println("SoilMoistureDone");
        }
        else if (content == "SoilSalinity") {
            Serial.print("SoilSalinity");
            Serial.print(delimiter);
            read_salinity_humidity_sensor(DHT22_PIN_2);
            read_salinity_humidity_sensor(DHT22_PIN_1);
            Serial.println("SoilSalinityDone");
        }
        else if (content == "SoilSuction") {
            Serial.print("SoilSuction");
            Serial.print(delimiter);
            heat_suction_sensor(heat_suction_sensor_3_addr,heat_suction_sensor_heat_sw_3,temp_sampling_number,temp_sampling_interval_ms); 
            heat_suction_sensor(heat_suction_sensor_2_addr,heat_suction_sensor_heat_sw_2,temp_sampling_number,temp_sampling_interval_ms); 
            heat_suction_sensor(heat_suction_sensor_1_addr,heat_suction_sensor_heat_sw_1,temp_sampling_number,temp_sampling_interval_ms); 
            
            Serial.println("SoilSuctionDone");
        }
        
        else if (content == "gs3") {
            Serial.print("gs3");
            Serial.print(delimiter);
            sdi12_loop();
            Serial.println("gs3Done");
        }
        else {
          Serial.println(content);
        }
    } //content != ""
}  //loop

void heat_suction_sensor(byte heat_suction_sensor_addr[8],int heat_sw,int sampling_number, int sampling_interval_ms){

  Serial.print("SucHeat");
  Serial.print(delimiter);
  Serial.print(heat_suction_sensor_addr[0],HEX);
  Serial.print(heat_suction_sensor_addr[1],HEX);
  Serial.print(delimiter);
  Serial.print("Heating");
  Serial.print(delimiter);
//  int heat_sw;
//  byte heat_suction_sensor_addr[8];
  digitalWrite(heat_sw, HIGH);
  for (int i=0; i<=sampling_number; i++)
  {
      delay (sampling_interval_ms);
      read_DS18B20_by_addr(heat_suction_sensor_addr) ;
  }

  Serial.print("Dsping");
  Serial.print(delimiter);
  digitalWrite(heat_sw, LOW);
  for (int i=0; i<=sampling_number; i++)
  {
      delay (sampling_interval_ms);
      read_DS18B20_by_addr(heat_suction_sensor_addr) ;
  }
      //Serial.println();
}  // heat_suction_sensor


void read_salinity_humidity_sensor(int digi_pin){

  Serial.print("SaltRH");
  Serial.print(delimiter);
  Serial.print(digi_pin);
  Serial.print(delimiter);
  int chk1=DHT.read22(digi_pin);
  Serial.print(DHT.temperature);
  Serial.print(delimiter);
  Serial.print(DHT.humidity);
  Serial.print(delimiter);
}


void read_DS18B20_by_addr(byte addr[8]) {
  //byte addr[8];
  byte i;
  byte present = 0;
  byte type_s;
  byte data[12];
//  byte addr[8];
  float celsius;
        
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
      //Serial.print(delimiter);
      Serial.print(celsius);
      Serial.write(delimiter);
  
  return;
}



void read_analog_moisture_sensor() {
  // read the input on analog pin 0
  for (int i=0; i<moist_number_sensors;i++){
    moist_data[i]=0;
    digitalWrite(moist_digital_pins[i],HIGH);
    delay(1000);

    for (int j=0;j<moist_dummy_readings;j++){
      analogRead(moist_analog_pins[i]);
      //delay(100);
    }

    for (int j=0;j<moist_number_readings;j++){
      moist_data[i]+=analogRead(moist_analog_pins[i]);
      delay(10);
    }

    moist_data[i]=moist_data[i]/moist_number_readings;
    digitalWrite(moist_digital_pins[i],LOW);
  }
    
    for (int i=0; i<moist_number_sensors;i++)
    {
    Serial.print("Mo");
    Serial.print(delimiter);
    //Serial.print((char)moist_analog_pins[i]);   // how to convert this to strings?
    Serial.print(moist_digital_pins[i]);
    Serial.print(delimiter); 
    Serial.print(moist_data[i]);
    Serial.print(delimiter);

    }

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
      buffer += delimiter;   // the comma in between the results
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
 //Serial.print(delimiter);
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
  int ii;
  String command = "";
  command += (char) i; 
  command += "I!";
  for(j = 0; j < 1; j++){
    mySDI12.sendCommand(command);
    delay(30); 
    if(mySDI12.available()>1) {
        Serial.write("SuTp");
        Serial.print(delimiter);
        break;
    }
    if(mySDI12.available()) mySDI12.read(); 
  }



//      ii=0;
  while(mySDI12.available()){
    char c = mySDI12.read();
    if((c!='\n') && (c!='\r')) 
    {

//            if (ii ==1){
//        Serial.write("SuTp");
//      Serial.print(delimiter);
//      }
      Serial.write(c); //print sensor info and type
    }
    delay(5); 
  } 
  Serial.print(delimiter);
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




