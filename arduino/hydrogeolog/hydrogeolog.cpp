/*
Morse.cpp - Library for flashing Morse code.
Created by David A. Mellis, November 2, 2007.
Released into the public domain.
*/

#include "Arduino.h"
#include "hydrogeolog.h"


hydrogeolog::hydrogeolog(const char delimiter)
{
  //pinMode(pin, OUTPUT);
  //  _pin = pin;
}

 
int hydrogeolog::split_strings(String inp2,String str_ay2[20])
/* returns the number of strings */
    {
        int comma_idx = inp2.indexOf(',');
        int number_strings=0;
        str_ay2[number_strings]=inp2;
        while (comma_idx!=-1){ //there is comma
              str_ay2[number_strings]= inp2.substring(0, comma_idx);
              number_strings+=1;
              str_ay2[number_strings]= inp2.substring(comma_idx+1);
              inp2=str_ay2[number_strings]; comma_idx=inp2.indexOf(',');
              //Serial.print("the number of string so far is: ");
              //Serial.println(number_strings);
              //Serial.print("rest is: ");
              //Serial.println(str_ay2[number_strings]);
              //Serial.print("comma_idx_is: ");
              //Serial.println(comma_idx);
        }
        number_strings+=1;
        return number_strings;
    } //
    
void hydrogeolog::print_str_ay(int number_opts,String str_ay2[20])
    {
            for (int i=0;i<number_opts;i++){
              Serial.print(str_ay2[i]);
              Serial.print(delimiter);
            }
        Serial.println();
    }//print_str_ay

int hydrogeolog::strcmpi(String str_source, int number_opts,String str_ay2[20])
    /* string match */
    {
      int str_index=-1;
      for (int i=0;i<number_opts;i++)
      {
          if (str_source == str_ay2[i]){
              str_index=i;
              break;
          }
      }
      return str_index;
     } //strcmpi


int hydrogeolog::parse_argument(String str_source, int default_values, int number_opts, String str_ay2[20])
    /* parse argument */
    {
    //strcmpi(str_source,number_opts,str_ay2[20]);
    int str_idx=strcmpi(str_source,number_opts,str_ay2);
    int str_value=default_values;
    if (str_idx!=-1){str_value=str_ay2[str_idx+1].toInt();}
    return str_value;
     } //parse_argument

String hydrogeolog::parse_argument_string(String str_source, String default_values, int number_opts, String str_ay2[20])
    /* parse argument */
    {
    int str_idx=strcmpi(str_source,number_opts,str_ay2);
    String str_value=default_values;
    if (str_idx!=-1){str_value=str_ay2[str_idx+1];}
    return str_value;
     } //parse_argument

char hydrogeolog::parse_argument_char(String str_source, char default_values, int number_opts, String str_ay2[20])
    /* parse argument */
    {
    int str_idx=strcmpi(str_source,number_opts,str_ay2);
    char str_value=default_values;
    if (str_idx!=-1){str_value=str_ay2[str_idx+1][0];}
    return str_value;
     } //parse_argument



void hydrogeolog::analog_excite_read(int power_sw_idx,int analog_idx,int number_of_dummies,int number_of_measurements,int measure_time_interval)
    {
        digitalWrite(power_sw_idx,HIGH);
        delay(1000);
        analog_read(analog_idx,number_of_dummies,number_of_measurements,measure_time_interval);
        //for (int j=0;j<number_of_dummies;j++){
        //  analogRead(analog_idx);
        //  delay(100);
        //}

        //for (int j=0;j<number_of_measurements;j++){
        //  results+=analogRead(analog_idx);
        //  delay(measure_time_interval);
        //}

        //results=results/float(number_of_measurements);
        digitalWrite(power_sw_idx,LOW);

        //return results;

    } // analog_excite_read


//float hydrogeolog::analog_read(int analog_idx,int number_of_dummies,int number_of_measurements,int measure_time_interval)
void hydrogeolog::analog_read(int analog_idx,int number_of_dummies,int number_of_measurements,int measure_time_interval)
    {
        float results=0.0;
        for (int j=0;j<number_of_dummies;j++){
          analogRead(analog_idx);
          delay(100);
        }

        for (int j=0;j<number_of_measurements;j++){
          results+=analogRead(analog_idx);
          delay(measure_time_interval);
        }

        results=results/float(number_of_measurements);
	Serial.print(results);
	Serial.print(delimiter);
        //return results;

    } // analog_read

void hydrogeolog::switch_power(int power_sw_idx,int status)
    {
    if (status==1)
    {
        digitalWrite(power_sw_idx,HIGH);
    }
    else
    {
        digitalWrite(power_sw_idx,LOW);
    }


    } // switch_power


void hydrogeolog::dht22_excite_read(int power_sw_idx,int digi_idx,int number_of_dummies,int number_of_measurements,int measure_time_interval)
    {
    dht DHT;
    #define DHT22_PIN digi_idx

    digitalWrite(power_sw_idx,HIGH);
    delay(1000);
//    float results=0.0;
//    for (int j=0;j<number_of_dummies;j++){
//        int chk1=DHT.read22(digi_idx);
//        delay(1000);
//    }
//
//    float t_results=0.;
//    float rh_results=0.;
//    for (int j=0;j<number_of_measurements;j++){
//    //  t_results+=DHT.temperature;
//
//    //}
//      //Serial.print(t_results);  
//      int chk1=DHT.read22(DHT22_PIN);
//      t_results+=DHT.temperature;
//      rh_results+= DHT.humidity;
//      //t_results+= temp.toFloat();
//      //rh_results+= DHT.humidity.toFloat();
//      delay(measure_time_interval);
//      }
//
//      t_results/= float(number_of_measurements);
//      rh_results/=float(number_of_measurements);
//      Serial.print(t_results);  
//      Serial.print(delimiter);
//      Serial.println(rh_results); 

      dht22_read(digi_idx, number_of_dummies, number_of_measurements, measure_time_interval);

      //Serial.print(DHT.temperature);  
      //Serial.print(delimiter);
      //Serial.println(DHT.humidity);  
      //results+=analogRead(analog_idx);
//    }
//
//    //results=results/float(number_of_measurements);
    digitalWrite(power_sw_idx,LOW);
//
//    return results;
//
    } // dht_excite_read


void hydrogeolog::dht22_read(int digi_idx,int number_of_dummies,int number_of_measurements,int measure_time_interval)
    {
    dht DHT;
    #define DHT22_PIN digi_idx
    if (measure_time_interval<1000) {measure_time_interval=1000;}

    float results=0.0;
    for (int j=0;j<number_of_dummies;j++){
        int chk1=DHT.read22(digi_idx);
        delay(1000);
    }
    float t_results=0.;
    float rh_results=0.;
    for (int j=0;j<number_of_measurements;j++){
      int chk1=DHT.read22(DHT22_PIN);
      t_results+=DHT.temperature;
      rh_results+= DHT.humidity;
      delay(measure_time_interval);
      }

      t_results/= float(number_of_measurements);
      rh_results/=float(number_of_measurements);
      Serial.print(t_results);  
      Serial.print(delimiter);
      Serial.print(rh_results); 
      Serial.print(delimiter);
    } // dht_read



void hydrogeolog::print_string_delimiter_value(String string_input,String value)
    {
    Serial.print(string_input);
    Serial.print(delimiter);
    Serial.print(value);
    Serial.print(delimiter);
    }






void hydrogeolog::search_ds18b20(int digi_pin,int power_switch) {
    OneWire  ds(digi_pin);  // on pin 2 (a 4.7K resistor is necessary)
    digitalWrite(power_switch,HIGH);
    delay(1000);

    byte i;
    byte present = 0;
    byte type_s;
    byte data[12];
    byte addr[8];
    float celsius, fahrenheit;
    int loop_time=3;
  int j=0; 
  for (int kk=0; kk<loop_time;kk++){
  Serial.print(kk);
  boolean while_indicator=true;
  while ( while_indicator==true){
    if ( !ds.search(addr)) {
      Serial.println("No more addresses.");
      ds.reset_search();
      delay(3000);
      //j+=1;
      while_indicator=false;

      break;
    }
  
    Serial.print("ROM =");
    for( i = 0; i < 8; i++) {
      Serial.write(' ');
      Serial.print(addr[i], HEX);
    }
  
//  if (OneWire::crc8(addr, 7) != addr[7]) {
//      Serial.println("CRC is not valid!");
//      return;
//  }
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
      fahrenheit = celsius * 1.8 + 32.0;
      Serial.print(",  Temperature = ");
      Serial.print(celsius);
      Serial.print(" Celsius, ");
      Serial.print(fahrenheit);
      Serial.println(" Fahrenheit");
      }//while true
      } // looptime
}//search_ds18b20


void hydrogeolog::read_DS18B20_by_addr(byte addr[8],int digi_pin) {
  //byte addr[8];
  byte i;
  byte present = 0;
  byte type_s;
  byte data[12];
//  byte addr[8];
  float celsius;
  OneWire  ds(digi_pin);  // on pin 2 (a 4.7K resistor is necessary)

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
      Serial.print(delimiter);

    return;
}

void hydrogeolog::tcaselect(int i) {
    #define TCAADDR 0x70
    if (i > 7) return;
    Wire.beginTransmission(TCAADDR);
    Wire.write(1 << i);
    Wire.endTransmission();
}


void  hydrogeolog::ms5803(int number_of_dummies,int number_of_measurements,int measure_time_interval_ms)
    {
    //  ADDRESS_HIGH = 0x76
    //  ADDRESS_LOW  = 0x77
    MS5803 sensor(ADDRESS_HIGH);
    float temperature_c;
    double pressure_abs;
    sensor.reset();
    delay(1000);
    sensor.begin();
    delay(1000);
    temperature_c = sensor.getTemperature(CELSIUS, ADC_512);
    



    for (int j=0;j<number_of_dummies;j++){
        sensor.getPressure(ADC_4096);
    }
    float t_results=0.;
    for (int j=0;j<number_of_measurements;j++){
        pressure_abs += double(sensor.getPressure(ADC_4096));
        delay(measure_time_interval_ms);
        }

    pressure_abs /= double(number_of_measurements);

    Serial.print(temperature_c);
    Serial.print(delimiter);
    Serial.print(pressure_abs);
    Serial.print(delimiter);
    }

