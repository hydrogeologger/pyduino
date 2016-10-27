/*
 Example using the SparkFun HX711 breakout board with a scale
 By: Nathan Seidle
 SparkFun Electronics
 Date: November 19th, 2014
 License: This code is public domain but you buy me a beer if you use this and we meet someday (Beerware license).

 This is the calibration sketch. Use it to determine the calibration_factor that the main example uses. It also
 outputs the zero_factor useful for projects that have a permanent mass on the scale in between power cycles.

 Setup your scale and start the sketch WITHOUT a weight on the scale
 Once readings are displayed place the weight on the scale
 Press +/- or a/z to adjust the calibration_factor until the output readings match the known weight
 Use this calibration_factor on the example sketch

 This example assumes pounds (lbs). If you prefer kilograms, change the Serial.print(" lbs"); line to kg. The
 calibration factor will be significantly different but it will be linearly related to lbs (1 lbs = 0.453592 kg).

 Your calibration factor may be very positive or very negative. It all depends on the setup of your scale system
 and the direction the sensors deflect from zero state
 This example code uses bogde's excellent library: https://github.com/bogde/HX711
 bogde's library is released under a GNU GENERAL PUBLIC LICENSE
 Arduino pin 2 -> HX711 CLK
 3 -> DOUT
 5V -> VCC
 GND -> GND

 Most any pin on the Arduino Uno will be compatible with DOUT/CLK.

 The HX711 board can be powered from 2.7V to 5V so the Arduino 5V power should be fine.

*/

#include "HX711.h"

#define DOUT  3
#define CLK  2

HX711 scale(DOUT, CLK);

//float calibration_factor = -7050; //-7050 worked for my 440lb max scale setup
float calibration_factor = 77650;
int length_of_temp =0;
//75160.00
void setup() {
  Serial.begin(9600);
  Serial.println("HX711 calibration sketch");
  Serial.println("Remove all weight from scale");
  Serial.println("After readings begin, place known weight on scale");
  Serial.println("Press + or a to increase calibration factor");
  Serial.println("Press - or z to decrease calibration factor");

  scale.set_scale();
  scale.tare(); //Reset the scale to 0

  long zero_factor = scale.read_average(); //Get a baseline reading
  Serial.print("Zero factor: "); //This can be used to remove the need to tare the scale. Useful in permanent scale projects.
  Serial.println(zero_factor);
}

void loop() {

  scale.set_scale(calibration_factor); //Adjust to this calibration factor

  Serial.print("Reading: ");
  Serial.print(scale.get_units(), 10); // the 10 here says the number of effective number
  Serial.print(" kg"); //Change this to kg and re-adjust the calibration factor if you follow SI units like a sane person
  Serial.print(" calibration_factor: ");
  Serial.print(calibration_factor);
  Serial.println();
  delay(5000);

    //char temp = Serial.read();
    // be careful here! if it is a string, use double quote, if it is a char, use single quote
    // http://stackoverflow.com/questions/5697047/convert-serial-read-into-a-useable-string-using-arduino

char tmp;
String temp="";
  while(Serial.available()) { 
    tmp = Serial.read(); 
    temp.concat(tmp); 
    delay (10); 
  } 
    
  //  char tmp= Serial.read();
   // String temp="";
//    temp.concat(tmp);
    //temp.trim();
    Serial.println(temp);
    //length_of_temp=sizeof(temp);
    length_of_temp=temp.length() ;
    Serial.println(length_of_temp);
    if (temp.length() == 1)
    {
        if( temp.equals("+")   )
           {Serial.println(temp);
           calibration_factor += 10;}
        else if(temp == "-" )
          calibration_factor -= 10;
        else if(temp == "w" )
          calibration_factor -= 100;
        else if(temp == "e" )
          calibration_factor += 100;      
        else if(temp == "q" )
          calibration_factor -= 1000;
        else if(temp == "r" )
          calibration_factor += 1000;    
        else if(temp == "Q" )
          calibration_factor -= 10000;
        else if(temp == "L" )
          calibration_factor += 10000;         
        else if (temp == "t")
          scale.tare();
	}
     else if(length_of_temp!=0) 
   //     temp.toCharArray(temp, sizeof(temp));
//	int f = (temp);
    {
    Serial.println( temp.toInt());
   	calibration_factor=temp.toInt();
    }
    
}

