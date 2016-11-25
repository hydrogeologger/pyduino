#include "HX711.h"

#define DOUT1  3
#define CLK1   2
#define DOUT2  5
#define CLK2   4
//#define DOUT3  7
//#define CLK3   6
//#define DOUT4  9
//#define CLK4   8
//#define DOUT5  11
//#define CLK5   10

HX711 scale_0(DOUT1, CLK1);
HX711 scale_1(DOUT2, CLK2);
//HX711 scale_2(DOUT3, CLK3);
//HX711 scale_3(DOUT4, CLK4);
//HX711 scale_4(DOUT5, CLK5);



//float calibration_factor = -7050; //-7050 worked for my 440lb max scale setup
//float calibration_factor_1= 22000;
//float calibration_factor_2= 73500;
//float calibration_factor_3= 77650;
//float calibration_factor_4= 77650;
//float calibration_factor_5= 77650;


//float calibration_factor[5]= {23500,71600,71600,71600,71600};
//float calibration_factor[5]= {23500,72500,72500,72500,72500};
//float calibration_factor[5]= {23000,72800,72800,72800,72800};
float calibration_factor[5]= {23080,72800,72800,72800,72800};



float reading_0  = 0;
float reading_1  = 0;
//float reading_2  = 0;
//float reading_3  = 0;
//float reading_4  = 0;
//float reading_1_4= 0;

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
  //scale_0.tare(); //Reset the scale to 0
  scale_1.set_scale();
  //scale_1.tare(); //Reset the scale to 0
  //scale_2.set_scale();
  //scale_2.tare(); //Reset the scale to 0
  //scale_3.set_scale();
  //scale_3.tare(); //Reset the scale to 0
  //scale_4.set_scale();
 // scale_4.tare(); //Reset the scale to 0

  long zero_factor_0 = scale_0.read_average(); //Get a baseline reading
  long zero_factor_1 = scale_1.read_average(); //Get a baseline reading
  //long zero_factor_2 = scale_2.read_average(); //Get a baseline reading
  //long zero_factor_3 = scale_3.read_average(); //Get a baseline reading
  //long zero_factor_4 = scale_4.read_average(); //Get a baseline reading

  //Serial.print("Zero factor: "); //This can be used to remove the need to tare the scale. Useful in permanent scale projects.
  //Serial.println(zero_factor_0);
  pinMode(6, OUTPUT);
}

void loop() {

  scale_0.set_scale(calibration_factor[0]); //Adjust to this calibration factor
  scale_1.set_scale(calibration_factor[1]); //Adjust to this calibration factor
  //scale_2.set_scale(calibration_factor[2]); //Adjust to this calibration factor
  //scale_3.set_scale(calibration_factor[3]); //Adjust to this calibration factor
  //scale_4.set_scale(calibration_factor[4]); //Adjust to this calibration factor


  for (int i=0;i<5;i++){
  scale_data[i]=0;
  }

  digitalWrite(6, HIGH);
  delay(100);
  // dummy readings
  for (int j=0;j<dummy_readings;j++){
    //scale_0.get_units(2); 
   //scale_1.get_units(2); 
    scale_0.get_value(1); 
    scale_1.get_value(1); 
    //scale_2.get_units(); 
    //scale_3.get_units(); 
    //scale_4.get_units(); 
  }


  for (int j=0;j<number_readings;j++){
//    scale_data[0]+= scale_0.get_value(1);
//    scale_data[1]+= scale_1.get_value(1);
    reading_ind_0[j]= scale_0.get_value(1);
    reading_ind_1[j]= scale_1.get_value(1);
    scale_data[0]+= reading_ind_0[j];
    scale_data[1]+= reading_ind_1[j];
    //scale_data[2]+= scale_2.get_units(10);
    //scale_data[3]+= scale_3.get_units(10);
    //scale_data[4]+= scale_4.get_units(10);
    delay(10);
  }
  digitalWrite(6, LOW); 

  reading_0=scale_data[0]/(float)number_readings;
  reading_1=scale_data[1]/(float)number_readings;
  //reading_2=scale_data[2]/number_readings;
  //reading_3=scale_data[3]/number_readings;
  //reading_4=scale_data[4]/number_readings;



  Serial.print("2nd,");
  for (int j=0;j<number_readings;j++){
  Serial.print(reading_ind_1[j],1);
  Serial.print(",");
  }
    Serial.print("avgdata,");
  //Serial.println();
  /*
  Serial.print("2nd,");
  for (int j=0;j<number_readings;j++){
  Serial.print(reading_ind_1[j],2);
  Serial.print(',');
  }
  Serial.println();

  Serial.print("Reading: ");
   */
  


  
  Serial.print(reading_0);
  Serial.print(',');
  Serial.print(reading_1);
  Serial.print(',');
  //Serial.print(reading_2,10);
  //Serial.print(',');
  //Serial.print(reading_3,10);
  //Serial.print(',');
  //Serial.print(reading_4,10);
  //Serial.print(',');
  //Serial.print(reading_1_4,10);
  //Serial.print(',');

  //Serial.print(" kg"); //Change this to kg and re-adjust the calibration factor if you follow SI units like a sane person
  //Serial.print(" calibration_factor: ");
  //Serial.print(calibration_factor[0]);
  //Serial.print(',');
  //Serial.print(calibration_factor[1]);
  //Serial.print(',');
  //Serial.print(calibration_factor[2]);
  //Serial.print(',');
  //Serial.print(calibration_factor[3]);
  //Serial.print(',');
  //Serial.print(calibration_factor[4]);

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
       //calibration_factor[3]=secondValue_int;
       //calibration_factor[4]=secondValue_int;
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
    }

}




