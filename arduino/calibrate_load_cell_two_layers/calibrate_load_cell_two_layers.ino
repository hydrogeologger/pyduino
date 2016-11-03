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

#define DOUT1  3
#define CLK1   2
#define DOUT2  5
#define CLK2   4
#define DOUT3  7
#define CLK3   6
#define DOUT4  9
#define CLK4   8
#define DOUT5  11
#define CLK5   10

HX711 scale_0(DOUT1, CLK1);
HX711 scale_1(DOUT2, CLK2);
HX711 scale_2(DOUT3, CLK3);
HX711 scale_3(DOUT4, CLK4);
HX711 scale_4(DOUT5, CLK5);

//float calibration_factor = -7050; //-7050 worked for my 440lb max scale setup
//float calibration_factor_1= 22500;
//float calibration_factor_2= 77650;
//float calibration_factor_3= 77650;
//float calibration_factor_4= 77650;
//float calibration_factor_5= 77650;


float calibration_factor[5]= {22500,22500,22500,22500,22500};



float reading_0  = 0;
float reading_1  = 0;
float reading_2  = 0;
float reading_3  = 0;
float reading_4  = 0;
float reading_1_4= 0;

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 calibration sketch");
  Serial.println("Remove all weight from scale");
  Serial.println("After readings begin, place known weight on scale");
  Serial.println("Press + or a to increase calibration factor");
  Serial.println("Press - or z to decrease calibration factor");

  scale_0.set_scale();
  scale_0.tare(); //Reset the scale to 0
  scale_1.set_scale();
  scale_1.tare(); //Reset the scale to 0
  scale_2.set_scale();
  scale_2.tare(); //Reset the scale to 0
  scale_3.set_scale();
  scale_3.tare(); //Reset the scale to 0
  scale_4.set_scale();
  scale_4.tare(); //Reset the scale to 0

  long zero_factor_0 = scale_0.read_average(); //Get a baseline reading
  long zero_factor_1 = scale_1.read_average(); //Get a baseline reading
  long zero_factor_2 = scale_2.read_average(); //Get a baseline reading
  long zero_factor_3 = scale_3.read_average(); //Get a baseline reading
  long zero_factor_4 = scale_4.read_average(); //Get a baseline reading

  Serial.print("Zero factor: "); //This can be used to remove the need to tare the scale. Useful in permanent scale projects.
  Serial.println(zero_factor_0);
}

void loop() {

  scale_0.set_scale(calibration_factor[0]); //Adjust to this calibration factor
  scale_1.set_scale(calibration_factor[1]); //Adjust to this calibration factor
  scale_2.set_scale(calibration_factor[2]); //Adjust to this calibration factor
  scale_3.set_scale(calibration_factor[3]); //Adjust to this calibration factor
  scale_4.set_scale(calibration_factor[4]); //Adjust to this calibration factor

  reading_0=scale_0.get_units(); 
  reading_1=scale_1.get_units(); 
  reading_2=scale_2.get_units(); 
  reading_3=scale_3.get_units(); 
  reading_4=scale_4.get_units(); 
  

  reading_1_4=reading_1+reading_2+reading_3+reading_4;



  Serial.print("Reading: ");

  

  //Serial.print(scale_1.get_units(), 10); // the 10 here says the number of effective number
  //Serial.print(scale_2.get_units(), 10); // the 10 here says the number of effective number
  //Serial.print(scale_3.get_units(), 10); // the 10 here says the number of effective number
  //Serial.print(scale_4.get_units(), 10); // the 10 here says the number of effective number
  //Serial.print(scale_5.get_units(), 10); // the 10 here says the number of effective number
  
  Serial.print(reading_0,10);
  Serial.print(',');
  Serial.print(reading_1,10);
  Serial.print(',');
  Serial.print(reading_2,10);
  Serial.print(',');
  Serial.print(reading_3,10);
  Serial.print(',');
  Serial.print(reading_4,10);
  Serial.print(',');
  Serial.print(reading_1_4,10);
  Serial.print(',');

  Serial.print(" kg"); //Change this to kg and re-adjust the calibration factor if you follow SI units like a sane person
  Serial.print(" calibration_factor: ");
  Serial.print(calibration_factor[0]);
  Serial.print(',');
  Serial.print(calibration_factor[1]);
  Serial.print(',');
  Serial.print(calibration_factor[2]);
  Serial.print(',');
  Serial.print(calibration_factor[3]);
  Serial.print(',');
  Serial.print(calibration_factor[4]);

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


    //length_of_temp=temp.length() ;
    //Serial.println(length_of_temp);
    if (temp.length()!=0)
    {
    int commaIndex = temp.indexOf(',');
    String firstValue = temp.substring(0, commaIndex);
    int firstValue_int=firstValue.toInt();
    String secondValue = temp.substring(commaIndex+1); 
    int secondValue_int=secondValue.toInt();
    
    Serial.print(temp);
      Serial.print(',');
    Serial.print(firstValue_int);
      Serial.print(',');
    Serial.print(secondValue_int);
    Serial.print(',');
    Serial.print(firstValue);
      Serial.print(',');
    Serial.println(secondValue);
    if (firstValue_int==5)
      {
       calibration_factor[1]=secondValue_int;
       calibration_factor[2]=secondValue_int;
       calibration_factor[3]=secondValue_int;
       calibration_factor[4]=secondValue_int;
      }
    else
      {
       calibration_factor[firstValue_int]=secondValue_int;
      }
    }

}



