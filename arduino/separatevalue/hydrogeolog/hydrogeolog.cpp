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
    {
        int comma_idx = inp2.indexOf(',');
        int number_strings=0;
        str_ay2[number_strings]=inp2;
        while (comma_idx!=-1){ //there is comma
              str_ay2[number_strings]= inp2.substring(0, comma_idx);
              number_strings+=1;
              str_ay2[number_strings]= inp2.substring(comma_idx+1);
              inp2=str_ay2[number_strings];
              comma_idx=inp2.indexOf(',');
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





float hydrogeolog::analog_excite_read(int power_sw_idx,int analog_idx,int number_of_dummies,int number_of_measurements,int measure_time_interval)
    {
        digitalWrite(power_sw_idx,HIGH);
        delay(1000);
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
    digitalWrite(power_sw_idx,LOW);

    return results;

    } // analog_excite_read



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
        float results=0.0;
    //for (int j=0;j<number_of_dummies;j++){
    //    int chk1=DHT.read22(digi_idx);
    //    delay(100);
    //}

    float t_results=0.;
    float rh_results=0.;
    //for (int j=0;j<number_of_measurements;j++){
    //  t_results+=DHT.temperature;
    //  delay(measure_time_interval);

    //}
      //Serial.print(t_results);  
      int chk1=DHT.read22(DHT22_PIN);
      Serial.print(DHT.temperature);  
      Serial.print(delimiter);
      Serial.println(DHT.humidity);  
      //results+=analogRead(analog_idx);
//    }
//
//    //results=results/float(number_of_measurements);
    digitalWrite(power_sw_idx,LOW);
//
//    return results;
//
    } // analog_excite_read



 
