/*

*/
static const uint8_t analog_pins[]  = {A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15};
int const number_analog_pins=sizeof(analog_pins);

static int digi_out_pins[] = {43,45,47,49,35,37,39,41,27,29,31,33,24,22,23,25,9,8,7,6,32,30,28,26,40,38,36,42,44,46,48};
int const number_digi_out_pins=sizeof(digi_out_pins);
#include "hydrogeolog/hydrogeolog.h"
//#include "/home/chenming/Dropbox/scripts/github/pyduino/arduino/libraries/hydrogeolog/hydrogeolog.h"
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
        //Serial.println(content);
        int str_ay_size=hydrogeolog1.split_strings(content,str_ay);
        //Serial.println(str_ay_size);
	      //Serial.print(delimiter);
        //hydrogeolog1.print_str_ay(str_ay_size,str_ay);
        // assign power pins
        //power,43,analog,15,point,3,interval_mm,200,debug,1 checking voltage
        //
        int debug_sw        = hydrogeolog1.parse_argument("debug",0,str_ay_size,str_ay);
        int analog_in_pin   = hydrogeolog1.parse_argument("analog",-1,str_ay_size,str_ay);


        
        int power_sw_pin    = hydrogeolog1.parse_argument("power",-1,str_ay_size,str_ay);
    
        //analog reading
        if ( (analog_in_pin!=-1) && (power_sw_pin!=-1))   //&&(number_of_measurement!=-1) && (number_of_dummies!=-1) 
        {
            int number_of_measurement=hydrogeolog1.parse_argument("points",5,str_ay_size,str_ay);
            int number_of_dummies=hydrogeolog1.parse_argument("dummies",3,str_ay_size,str_ay);
            int measure_time_interval_ms=hydrogeolog1.parse_argument("interval_mm",10,str_ay_size,str_ay);
            hydrogeolog1.print_string_delimiter_value("analog"  ,String(analog_in_pin)  );

            if (debug_sw==1)
            {            
                hydrogeolog1.print_string_delimiter_value("power"  ,String(power_sw_pin)  );
                hydrogeolog1.print_string_delimiter_value("points" ,String(number_of_measurement)  );
                hydrogeolog1.print_string_delimiter_value("dummies",String(number_of_dummies)  );
                hydrogeolog1.print_string_delimiter_value("interval_mm",String(measure_time_interval_ms)  );                
            }
            float outcome=hydrogeolog1.analog_excite_read(power_sw_pin,analog_in_pin,number_of_dummies,number_of_measurement,measure_time_interval_ms);    
            Serial.println(outcome);   
              } // analog read

            // assign powerswitch
            // power_switch,46,power_switch_status,1   //switch for raspberry pi
            
            int pow_sw   = hydrogeolog1.parse_argument("power_switch",-1,str_ay_size,str_ay);
            int pow_sw_status    = hydrogeolog1.parse_argument("power_switch_status",0,str_ay_size,str_ay);            
            if ( (pow_sw!=-1) )  
            { 
                hydrogeolog1.print_string_delimiter_value("power_switch"  ,String(pow_sw)  );
                hydrogeolog1.print_string_delimiter_value("power_switch_status"  ,String(pow_sw_status) );
                hydrogeolog1.switch_power(pow_sw,pow_sw_status);
            }  //power switch

        int dht22_in_pin   = hydrogeolog1.parse_argument("dht22",-1,str_ay_size,str_ay);
        power_sw_pin    = hydrogeolog1.parse_argument("power",-1,str_ay_size,str_ay);


       /*dht22 measurement
       
       dht22,10,power,48,points,2,dummies,1,interval_mm,1000,debug,1
       a 10 k resistor is required to put between digi 10 and ground
       */
       if ( (dht22_in_pin!=-1) && (power_sw_pin!=-1))   //&&(number_of_measurement!=-1) && (number_of_dummies!=-1) 
        {
            int number_of_measurement=hydrogeolog1.parse_argument("points",1,str_ay_size,str_ay);
            int number_of_dummies=hydrogeolog1.parse_argument("dummies",0,str_ay_size,str_ay);
            int measure_time_interval_ms=hydrogeolog1.parse_argument("interval_mm",1000,str_ay_size,str_ay);
            if (measure_time_interval_ms<1000) {measure_time_interval_ms=1000;}
            // needs to be at leaset 1000 ms
            hydrogeolog1.print_string_delimiter_value("dht22"  ,String(dht22_in_pin)  );
            if (debug_sw==1)
            {            
                hydrogeolog1.print_string_delimiter_value("power"  ,String(power_sw_pin)  );
                hydrogeolog1.print_string_delimiter_value("points" ,String(number_of_measurement)  );
                hydrogeolog1.print_string_delimiter_value("dummies",String(number_of_dummies)  );
                hydrogeolog1.print_string_delimiter_value("interval_mm",String(measure_time_interval_ms)  );
            }
            hydrogeolog1.dht22_excite_read(power_sw_pin,dht22_in_pin,number_of_dummies,number_of_measurement,measure_time_interval_ms);    
              } // analog read

       /*ds18b20 search
        ds18b20_search,13,power,42
       */
        int ds18b20_search_pin   = hydrogeolog1.parse_argument("ds18b20_search",-1,str_ay_size,str_ay);
        power_sw_pin    = hydrogeolog1.parse_argument("power",-1,str_ay_size,str_ay);
        if ( (ds18b20_search_pin!=-1) && (power_sw_pin!=-1))   
            {
            digitalWrite(power_sw_pin,HIGH);
            delay(1000);
            hydrogeolog1.search_ds18b20(ds18b20_search_pin,power_sw_pin);

            digitalWrite(power_sw_pin,LOW);
            } //if ds18b20_search






            
}//if


}//loop
