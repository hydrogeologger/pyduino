
//---------------------below required by temperature sensor-DS18S20----------------------------------------------------------#
#include <OneWire.h>

// OneWire DS18S20, DS18B20, DS1822 Temperature Example
//
// http://www.pjrc.com/teensy/td_libs_OneWire.html
//
// The DallasTemperature library can do all this work for you!
// http://milesburton.com/Dallas_Temperature_Control_Library

OneWire  ds(3);  // on pin 10 (a 4.7K resistor is necessary)
//---------------------above required by temperature sensor-----------------------------------------------------------#




////-------------------below required by analog digital for moisture ---------------------
//
////static const uint8_t analog_pins[]  = {A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13};
////// the array below works for digital sensor arrays
//////int digital_pins[] = {2, 3, 4, 5, 6, 7,  8, 9,10,11,12,13};
////int digital_pins[] = {22,24,26,28,30,32,34,36,38,40,42,44};
//
//static const uint8_t analog_pins[]  = {A0,A1,A2,A3,A4,A5,A8,A9,A10,A11,A12,A13};
////static const uint8_t digital_pins[] = {2,3,4,5,6,7};
//// the array below works for digital sensor arrays
//int digital_pins[] = {2, 3, 4, 5, 6, 7,8,9,10,11,12,13};
//
//float analogvals1[12];
//int i;
////Arrays to store analog values after recieving them  
//int number_sensors=12;
//// the setup routine runs once when you press reset:
//
int number_readings=7;
//int dummy_readings=5;
const char delimiter=',';
//
////-------------------above required by analog digital for moisture ---------------------




// -------------------- below needed by mux schield -----------------------
#include <MuxShield.h>
MuxShield muxShield;


//Arrays to store analog values after recieving them  
int const number_sensors=12;
// define toggles for I/O3, which are used for output;
float io1analogvals[number_sensors];
// Defining the waiting time between each readings;


// the powered sensor reading, there are two properties, on and off
int delay_sensor_reading=100;

int number_dummy_readings=3;

int delay_after_reading_each_ports=100;

int delay_after_writting=100;

int delay_after_moisture_done=100;

// -------------------- ablve needed by mux schield -----------------------






// -----------------ubove required by analog digital for moisture --------------------

#include "DHT.h"
#define DHTPIN1 5     // what digital pin we're connected to
#define DHTPIN2 9     // what digital pin we're connected to
// Uncomment whatever type you're using!
#define DHTTYPE DHT22   // DHT 11
//#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

  DHT dht1(DHTPIN1, DHTTYPE);
  DHT dht2(DHTPIN2, DHTTYPE);
// -----------------ubove required by analog digital for moisture --------------------


void setup(void) {



  muxShield.setMode(1,ANALOG_IN);
  muxShield.setMode(3,DIGITAL_OUT);

  Serial.begin(9600);

  dht1.begin();
  dht2.begin();
}

void loop(void) {
    Serial.print("Soil");
    Serial.print(delimiter);
    read_muxschield();
    read_temp_sensors();
    //ana_digi_loop();
    //sdi12_loop();
    dht11_loop(dht1,5);
    dht11_loop(dht2,9);
    Serial.println();
    delay_min(30);
}




void read_muxschield(){
  for (int i=0; i<number_sensors; i++)
  {
        muxShield.digitalWriteMS(3,i,HIGH);
        delay(100);

    for (int j=0;j<number_dummy_readings;j++){
        muxShield.analogReadMS(1,i);
    }




    io1analogvals[i] = 0.0 ;
    for (int j=0;j<number_readings;j++){
        delay(delay_sensor_reading);
        muxShield.analogReadMS(1,i);
        io1analogvals[i] += muxShield.analogReadMS(1,i);
    }

    io1analogvals[i] = io1analogvals[i]/float(number_readings);

    muxShield.digitalWriteMS(3,i,LOW);

    delay(delay_after_reading_each_ports);
  }
  


    for (int i=0; i<number_sensors;i++)
    {
        Serial.print("Mo");
        Serial.print(delimiter);
        Serial.print(i);
        Serial.print(delimiter);
        Serial.print(io1analogvals[i]);
        Serial.print(delimiter);
    }


}


//// the loop routine runs over and over again forever:
//void ana_digi_loop() {
//  // read the input on analog pin 0
//  for (int i=0; i<number_sensors;i++){
//    analogvals1[i]=0;
//    digitalWrite(digital_pins[i],HIGH);
//    delay(1000);
//
//    for (int j=0;j<dummy_readings;j++){
//      analogRead(analog_pins[i]);
//      //delay(100);
//    }
//
//    for (int j=0;j<number_readings;j++){
//      analogvals1[i]+=analogRead(analog_pins[i]);
//      delay(10);
//    }
//
//    analogvals1[i]=analogvals1[i]/number_readings;
//    digitalWrite(digital_pins[i],LOW);
//  }
//    
//    for (int i=0; i<number_sensors;i++)
//    {
//    //serial.print(i);
//    //serial.print(dilimiter);
//    Serial.print("Mo");
//    Serial.print(dilimiter);
//    Serial.print(i);
//    Serial.print(dilimiter);
//    Serial.print(analogvals1[i]);
//    Serial.print(dilimiter);
//
//    }
//    
//    //delay_min(30);
//    }



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


void delay_min(int min){
  for (int i=0;i<min;i++)
  {
    for (int j=0;j<12;j++)
    {
      delay(5000);

    }
  }
}



void dht11_loop(DHT dht,int i) {
  // Wait a few seconds between measurements.
  delay(2000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.print("Failed to read from DHT sensor!");
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);
  Serial.print("ht11");
  Serial.print(delimiter);
  Serial.print(i);
  Serial.print(delimiter);
  //Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print(delimiter);
  //Serial.print(" %\t");
  //Serial.print("Temperature: ");
  Serial.print(t);
  Serial.print(delimiter);
  //Serial.print(" *C ");
  //Serial.print(f);
  //Serial.print(" *F\t");
 // Serial.print("Heat index: ");
  //Serial.print(hic);
  //Serial.print(" *C ");
  //Serial.print(hif);
  //Serial.println(" *F");
}


