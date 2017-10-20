/*
  AnalogReadSerial
  Reads an analog input on pin 0, prints the result to the serial monitor.
  Graphical representation is available using serial plotter (Tools > Serial Plotter menu)
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.
*/
#include "../libraries/hydrogeolog/hydrogeolog.h"
//#include "/home/chenming/Dropbox/scripts/github/pyduino/arduino/libraries/hydrogeolog/hydrogeolog.h"
//include <hydrogeolog.h>
const char delimiter=',';
hydrogeolog hydrogeolog1(delimiter);

String str_ay[20];

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
    String content = "";
    char character;
    while(Serial.available()) {
        character = Serial.read();
        content.concat(character); 
        delay (10); 
    }
    if (content != ""){
        Serial.println(content);
        int str_ay_size=hydrogeolog1.split_strings(content,str_ay);
        Serial.print("The number of output is: ");
        Serial.println(str_ay_size);
        hydrogeolog1.print_str_ay(str_ay_size,str_ay);
    }
}



