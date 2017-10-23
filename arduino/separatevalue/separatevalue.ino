/*
  AnalogReadSerial
  Reads an analog input on pin 0, prints the result to the serial monitor.
  Graphical representation is available using serial plotter (Tools > Serial Plotter menu)
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.
*/
static const uint8_t analog_pins[]  = {A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15};
int const number_analog_pins=sizeof(analog_pins);

static int digi_out_pins[] = {43,45,47,49,35,37,39,41,27,29,31,33,24,22,23,25,9,8,7,6,32,30,28,26,40,38,36};
int const number_digi_out_pins=sizeof(digi_out_pins);

#include "hydrogeolog/hydrogeolog.h"
//#include "/home/chenming/Dropbox/scripts/github/pyduino/arduino/libraries/hydrogeolog/hydrogeolog.h"
//include <hydrogeolog.h>
const char delimiter=',';
hydrogeolog hydrogeolog1(delimiter);
String str_ay[20];

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  for (int i=0; i<number_digi_out_pins;i++){
      pinMode(digi_out_pins[i],OUTPUT);
  }
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
        Serial.println(str_ay_size);
	      Serial.print(delimiter);
        hydrogeolog1.print_str_ay(str_ay_size,str_ay);
        // assign power pins
        int ana_pow_sw_idx  = hydrogeolog1.strcmpi("power",str_ay_size,str_ay);
        int analog_idx    = hydrogeolog1.strcmpi("analog",str_ay_size,str_ay);
        //int number_of_measurement_idx = hydrogeolog1.strcmpi("points",str_ay_size,str_ay);
        //int number_of_dummies_idx = hydrogeolog1.strcmpi("dummies",str_ay_size,str_ay);
        //int measure_time_interval_ms_idx = hydrogeolog1.strcmpi("interval_mm",str_ay_size,str_ay);

        //analog reading
        if ( (ana_pow_sw_idx!=-1) && (analog_idx!=-1))   //&&(number_of_measurement!=-1) && (number_of_dummies!=-1) 
            {
            //int power_sw_pin  = str_ay[ana_pow_sw_idx+1].toInt();
            //int analog_in_pin = str_ay[analog_idx+1].toInt();
            //int number_of_measurement=5;
            //int number_of_dummies=3;
            //int measure_time_interval_ms=10;
            
            //if (number_of_measurement_idx   !=-1){number_of_measurement=str_ay[number_of_measurement_idx+1].toInt();}
            //if (number_of_dummies_idx       !=-1){number_of_dummies    =str_ay[number_of_dummies_idx    +1].toInt();}
            //if (measure_time_interval_ms_idx!=-1){measure_time_interval_ms    =str_ay[measure_time_interval_ms_idx    +1].toInt();}
            int number_of_measurement=hydrogeolog1.parse_argument("points",5,str_ay_size,str_ay);
            int number_of_dummies=hydrogeolog1.parse_argument("dummies",3,str_ay_size,str_ay);
            int measure_time_interval_ms=hydrogeolog1.parse_argument("interval_mm",10,str_ay_size,str_ay);
            
            Serial.print("power");
            Serial.print(delimiter);
            Serial.print(power_sw_pin);
            Serial.print(delimiter);
            Serial.print("analog");
            Serial.print(delimiter);
            Serial.print(analog_in_pin);
            Serial.print(delimiter);
            Serial.print("points");
            Serial.print(delimiter);
            Serial.print(number_of_measurement);
            Serial.print(delimiter);
            Serial.print("interval_mm");
            Serial.print(delimiter);
            Serial.print(measure_time_interval_ms);
            Serial.print(delimiter);
            float outcome=hydrogeolog1.analog_excite_read(power_sw_pin,analog_in_pin,number_of_dummies,number_of_measurement,measure_time_interval_ms);    
            Serial.println(outcome);   
              } // analog read

            // assign powerswitch
            int pow_sw_idx        = hydrogeolog1.strcmpi("power_switch",str_ay_size,str_ay);
            int pow_sw_status_idx = hydrogeolog1.strcmpi("power_switch_status",str_ay_size,str_ay);
            
            if ( (pow_sw_idx!=-1) )  
            {
                pow_sw_status = 0;
                //if (number_of_measurement_idx   !=-1){number_of_measurement=str_ay[number_of_measurement_idx+1].toInt();}

                Serial.print("power_switch");
                Serial.print(delimiter);
                Serial.println(pow_sw_idx);              
                Serial.print("power_switch");
                Serial.print(delimiter);
                Serial.println(pow_sw_status);             

	
            }  //power switch
}//loop



