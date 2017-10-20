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




