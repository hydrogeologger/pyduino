#include "HX711.h"

#define DOUT1  3
#define CLK1   2
#define DOUT2  5
#define CLK2   4

HX711 scale_0(DOUT1, CLK1);
HX711 scale_1(DOUT2, CLK2);



float calibration_factor[5]= {23080,72800,72800,72800,72800};



float reading_0  = 0;
float reading_1  = 0;
//float reading_2  = 0;

float scale_data[5];


const int number_readings=7;
const int dummy_readings=10;

float reading_ind_0[number_readings];
float reading_ind_1[number_readings];

void setup() {
  Serial.begin(9600);
  //Serial.println("HX711 calibration sketch");
  //Serial.println("Remove all weight from scale");
  //Serial.println("After readings begin, place known weight on scale");
  //Serial.println("Press + or a to increase calibration factor");
  //Serial.println("Press - or z to decrease calibration factor");

  scale_0.set_scale();
  scale_1.set_scale();

  long zero_factor_0 = scale_0.read_average(); //Get a baseline reading
  long zero_factor_1 = scale_1.read_average(); //Get a baseline reading

  //Serial.print("Zero factor: "); //This can be used to remove the need to tare the scale. Useful in permanent scale projects.
  //Serial.println(zero_factor_0);
  pinMode(6, OUTPUT);
}

void loop() {

  scale_0.set_scale(calibration_factor[0]); //Adjust to this calibration factor
  scale_1.set_scale(calibration_factor[1]); //Adjust to this calibration factor


  for (int i=0;i<5;i++){
  scale_data[i]=0;
  }

  digitalWrite(6, HIGH);
  delay(100);
   
 
  // dummy readings
  for (int j=0;j<dummy_readings;j++){
    scale_0.get_value(1); 
    scale_1.get_value(1); 
  }


  for (int j=0;j<number_readings;j++){
    reading_ind_0[j]= scale_0.get_value(1);
    reading_ind_1[j]= scale_1.get_value(1);
    scale_data[0]+= reading_ind_0[j];
    scale_data[1]+= reading_ind_1[j];
    delay(10);
  }
  digitalWrite(6, LOW); 

  reading_0=scale_data[0]/(float)number_readings;
  reading_1=scale_data[1]/(float)number_readings;

  Serial.print("2nd,");
  
  for (int j=0;j<number_readings;j++){
      Serial.print(reading_ind_1[j],1);
      Serial.print(",");
  }
  Serial.print("avgdata,");

  
  Serial.print(reading_0);
  Serial.print(',');
  Serial.print(reading_1);
  Serial.print(',');

  Serial.println();
  delay(240000);
  //delay(5000);

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
    float secondValue_int=secondValue.toFloat();
    
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
      }
    else if (secondValue_int==0)
      {
        scale_0.tare();
        scale_1.tare();
        //scale_2.tare();
        //scale_3.tare();
        //scale_4.tare();
      }
    else
      {
      calibration_factor[firstValue_int]=secondValue_int;
      }
    }   // temp length

}   //loop




