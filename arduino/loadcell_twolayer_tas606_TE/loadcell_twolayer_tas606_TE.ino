#include "HX711.h"

#define DOUT2  5
#define CLK2   4

//HX711 scale_0(DOUT1, CLK1);
HX711 scale_1(DOUT2, CLK2);



float calibration_factor[5]= {23080,72800,72800,72800,72800};

float te_scale  = 0.;
float reading_1  = 0.;

float scale_data[5];

const int number_readings=7;
const int dummy_readings=3;

float reading_ind_1[number_readings];
char delimiter=',';



//---------------------below required by module heat_suction_sensor----------------------------------------------------#

const int te_analog_pin=3;

//---------------------above required by module heat_suction_sensor----------------------------------------------------#


void setup() {
  Serial.begin(9600);
  scale_1.set_scale();

  long zero_factor_1 = scale_1.read_average(); //Get a baseline reading

  pinMode(6, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(2, OUTPUT);

}

void loop() {
  //char temp = Serial.read();
  // be careful here! if it is a string, use double quote, if it is a char, use single quote
  // http://stackoverflow.com/questions/5697047/convert-serial-read-into-a-useable-string-using-arduino
  Serial.print("scale");
  Serial.print(delimiter);
  te_scale_read();
  delay(5000);
  tas606_read();
  Serial.println();
  delay_min(5);
}   //loop

void te_scale_read() {

  digitalWrite(2, HIGH);
  for (int j=0;j<dummy_readings;j++){
    analogRead(te_analog_pin);
  }
  
  float  te_scale=0.;
  for (int j=0;j<number_readings;j++){
    te_scale += float(analogRead(A0));
    delay(10);
  }
  te_scale = te_scale/float(number_readings);
   delay(3000);
  digitalWrite(2, LOW);
  Serial.print("te");
  Serial.print(delimiter);
  Serial.print(te_scale);
  Serial.print(delimiter);
}

void tas606_read() {

  scale_1.set_scale(calibration_factor[1]); //Adjust to this calibration factor

  for (int i=0;i<5;i++){
    scale_data[i]=0;
  }
  digitalWrite(6, HIGH);
  delay(100);
   
  // dummy readings
  for (int j=0;j<dummy_readings;j++){
    scale_1.get_value(1); 
  }


  for (int j=0;j<number_readings;j++){
    reading_ind_1[j]= scale_1.get_value(1);
    scale_data[1]+= reading_ind_1[j];
    delay(10);
  }
  digitalWrite(6, LOW); 

  reading_1=scale_data[1]/(float)number_readings;

  Serial.print("tas606");
  Serial.print(delimiter);

  Serial.print(reading_1);
  Serial.print(delimiter);
} //tas606_read


void delay_min(int min){
  for (int i=0;i<min;i++)
  {
    for (int j=0;j<12;j++)
    {
      delay(5000);

    }
  }
}  
