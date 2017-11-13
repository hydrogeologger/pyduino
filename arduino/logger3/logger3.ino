/*

*/
static const uint8_t analog_pins[]  = {A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15};
int const number_analog_pins=sizeof(analog_pins);

static int digi_out_pins[] = {43,45,47,49,35,37,39,41,27,29,31,33,24,22,23,25,9,8,7,6,32,30,28,26,40,38,36,42,44,46,48};
//first, for some reasons, the system does not support size of putting into const
//second, turns out, the best way to put in library is to copy the library into library folder
//int const number_digi_out_pins=sizeof(digi_out_pins);
int const number_digi_out_pins=31;
//#include "hydrogeolog/hydrogeolog.h"
#include <hydrogeolog.h>
//#include "/home/chenming/Dropbox/scripts/github/pyduino/arduino/libraries/hydrogeolog/hydrogeolog.h"
const char delimiter=',';
hydrogeolog hydrogeolog1(delimiter);
String str_ay[20];

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial2.begin(9600);
  Serial3.begin(9600);
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



        String lumino2=hydrogeolog1.parse_argument_string("lumino2","",str_ay_size,str_ay);
        power_sw_pin    = hydrogeolog1.parse_argument("power",-1,str_ay_size,str_ay);
        int serial_pin   = hydrogeolog1.parse_argument("serial",-1,str_ay_size,str_ay);
        int measure_time_interval_ms=hydrogeolog1.parse_argument("interval_mm",1000,str_ay_size,str_ay);

       /*luminox sensor
       lumino2,M 2,power,42,serial,2
       lumino2,M 1,power,42,serial,2
       lumino2,M 0,power,42,serial,2
       lumino2,A,power,42,serial,2
       
       */
       if ( (lumino2!="") && (power_sw_pin!=-1) && (serial_pin!=-1))   //&&(number_of_measurement!=-1) && (number_of_dummies!=-1) 
           {
                String input_linebreak=hydrogeolog1.parse_argument_string("inp_linebreak","\r\n",str_ay_size,str_ay);
                char ouput_linebreak=hydrogeolog1.parse_argument_char("otp_linebreak",'\n',str_ay_size,str_ay);
                hydrogeolog1.print_string_delimiter_value("lumino2_cmd"  ,lumino2  );
                hydrogeolog1.print_string_delimiter_value("pow" ,String(power_sw_pin)  );
                hydrogeolog1.print_string_delimiter_value("serial",String(serial_pin)  );
                hydrogeolog1.print_string_delimiter_value("delay",String(measure_time_interval_ms)  );
                if (measure_time_interval_ms<1000) {measure_time_interval_ms=1000;}

              
               if (serial_pin==1){
                  Serial.print("result,");
                  Serial1.print(lumino2);
                  Serial1.print(input_linebreak);
                  delay(measure_time_interval_ms);
                  Serial.print("result,");
                  String aa= Serial1.readStringUntil(ouput_linebreak);
                  Serial.println(aa);
               }
               if (serial_pin==2){
                  Serial.print("result,");
                  Serial2.print(lumino2);
                  Serial2.print("\r\n");
                  delay(measure_time_interval_ms);
                  String aa= Serial2.readStringUntil('\n');
                  Serial.println(aa);
               }
               if (serial_pin==3){
                  Serial.print("result,");
                  Serial3.print(lumino2);
                  Serial3.print("\r\n");
                  delay(measure_time_interval_ms);
                  String aa= Serial3.readStringUntil('\n');
                  Serial.println(aa);
               }
        } // lumino2








       /*ds18b20 search
        ds18b20_search,13,power,42
       */
        int ds18b20_search_pin   = hydrogeolog1.parse_argument("ds18b20_search",-1,str_ay_size,str_ay);
        power_sw_pin    = hydrogeolog1.parse_argument("power",-1,str_ay_size,str_ay);
        if ( (ds18b20_search_pin!=-1) && (power_sw_pin!=-1))   
            {
            hydrogeolog1.print_string_delimiter_value("ds18b20_search",String(ds18b20_search_pin));  
            digitalWrite(power_sw_pin,HIGH);
            delay(1000);
            //for (int i=0; i<10;i++){

            hydrogeolog1.search_ds18b20(ds18b20_search_pin,power_sw_pin);
          
            //}
            digitalWrite(power_sw_pin,LOW);
            } //if ds18b20_search

         /*
         thermal_suction_ds18b20,28E5A34A0800007F,power,4,numbersd,1
         thermal_suction_ds18b20,A3CF969B,digital_input,13,power,42
         thermal_suction_ds18b20,464CBABE,digital_input,13,power,42
         RESULT FROM 8
         thermal_suction_ds18b20,28E5A34A0800007F,power,4,50,56,69,53,65,51,52,0,40,229,163,74,8,0,0,127
         RESULT FROM 2
         thermal_suction_ds18b20,28E5A34A0800007F,power,4,50,0,5,74,5,0,0,3,40,229,163,74,8,0,0,127
         thermal_suction_ds18b20,28E5A34A,power,4,numbersd,1
         28 A3 CF 96 8 0 0 9B
         
         */
         String thermal_suction_ds18b20=hydrogeolog1.parse_argument_string("thermal_suction_ds18b20","",str_ay_size,str_ay);
         power_sw_pin    = hydrogeolog1.parse_argument("power",-1,str_ay_size,str_ay);
         int thermal_suction_digi_pin= hydrogeolog1.parse_argument("digital_input",-1,str_ay_size,str_ay);
         //int numbersd= hydrogeolog1.parse_argument("numbersd",-1,str_ay_size,str_ay);

         if ( (thermal_suction_ds18b20!="") && (power_sw_pin!=-1))
             {
              hydrogeolog1.print_string_delimiter_value("thermal_suction_ds18b20",String(thermal_suction_ds18b20));
              hydrogeolog1.print_string_delimiter_value("power"  ,String(power_sw_pin)  );
              //hydrogeolog1.print_string_delimiter_value("numbersd"  ,String(numbersd)  );
              //the reason i did not wrap this in hydrogeolog is because function in c normally can not return an array
              byte CardNumberByte[4];          // https://stackoverflow.com/questions/347949/how-to-convert-a-stdstring-to-const-char-or-char
              const char * CardNumber = thermal_suction_ds18b20.c_str();
              unsigned long number = strtoul( CardNumber, nullptr, 16);
              for(int i=3; i>=0; i--)    // start with lowest byte of number
              {
                //Serial.println(number,HEX);
                //Serial.println(byte(number));
                //Serial.println(byte(number),HEX);
                  CardNumberByte[i] = byte( number);
                  number >>= 8;            // get next byte into position
              }   
//                 
            for(int i=0; i<4; i++)
            {
              Serial.print("0x");
              Serial.print(CardNumberByte[i], HEX);
              Serial.print(delimiter);
            }
            byte heat_suction_sensor_addr[8];
            heat_suction_sensor_addr[0]=0x28;
            heat_suction_sensor_addr[1]=CardNumberByte[0];
            heat_suction_sensor_addr[2]=CardNumberByte[1];
            heat_suction_sensor_addr[3]=CardNumberByte[2];
            heat_suction_sensor_addr[4]=0x08;
            heat_suction_sensor_addr[5]=0x00;
            heat_suction_sensor_addr[6]=0x00;
            heat_suction_sensor_addr[7]=CardNumberByte[3]; 
                       
            
            digitalWrite(power_sw_pin,HIGH);
            delay(1000);
     
            hydrogeolog1.read_DS18B20_by_addr(heat_suction_sensor_addr,thermal_suction_digi_pin) ;
            //hydrogeolog1.search_ds18b20(ds18b20_search_pin,power_sw_pin);
            Serial.println();
            digitalWrite(power_sw_pin,LOW);               
//          thermal_suction_sensor[0]=char(thermal_suction_ds18b20);
//          thermal_suction_ds18b20.getBytes(thermal_suction_sensor, numbersd) ;
                    
         }  // ds18b20 temperature by search.
         
         /*
         thermal_suction_ds18b20,28E5A34A0800007F,power,4,numbersd,1
         thermal_suction_ds18b20,A3CF969B,digital_input,13,power,42
         thermal_suction_ds18b20,464CBABE,digital_input,13,sensor_power,42,power_heating_pin,35,output_temp_interval,2000,output_number_temp,5
         fredlund_ds18b20,464CBABE,digital_input,13,sensor_power,42,heating_pin,35,interval,2000,output_number,5
         fred,464CBABE,digi_inp,13,senpow,42,heatpow,35,itval,2000,opt_no,5
         fred,DE9F96DC,digi_inp,13,senpow,42,heatpow,35,itval,2000,opt_no,5
28 DE 9F 96 8 0 0 DC
         RESULT FROM 8
         thermal_suction_ds18b20,28E5A34A0800007F,power,4,50,56,69,53,65,51,52,0,40,229,163,74,8,0,0,127
         RESULT FROM 2
         thermal_suction_ds18b20,28E5A34A0800007F,power,4,50,0,5,74,5,0,0,3,40,229,163,74,8,0,0,127
         thermal_suction_ds18b20,28E5A34A,power,4,numbersd,1
         28 A3 CF 96 8 0 0 9B
         
         */
         String fredlund_suction_ds18b20=hydrogeolog1.parse_argument_string("fred","",str_ay_size,str_ay);
         power_sw_pin                 = hydrogeolog1.parse_argument("senpow",-1,str_ay_size,str_ay);
         int digital_input            = hydrogeolog1.parse_argument("digi_inp",-1,str_ay_size,str_ay);
         int power_heating_pin        = hydrogeolog1.parse_argument("heatpow",-1,str_ay_size,str_ay);
         int output_temp_interval_ms  = hydrogeolog1.parse_argument("itval",-1,str_ay_size,str_ay);
         int output_number_temp       = hydrogeolog1.parse_argument("opt_no",-1,str_ay_size,str_ay);

         if ( (fredlund_suction_ds18b20!="") && (power_sw_pin!=-1))
             {
              hydrogeolog1.print_string_delimiter_value("input",content);
              hydrogeolog1.print_string_delimiter_value("fredlund_ds18b20",String(fredlund_suction_ds18b20));
              hydrogeolog1.print_string_delimiter_value("sensor_power"  ,String(power_sw_pin)  );
              hydrogeolog1.print_string_delimiter_value("digital_input"  ,String(digital_input)  );
              hydrogeolog1.print_string_delimiter_value("power_heating_pin"  ,String(power_heating_pin)  );
              hydrogeolog1.print_string_delimiter_value("interval_ms"  ,String(output_temp_interval_ms)  );
              hydrogeolog1.print_string_delimiter_value("output_numbe"  ,String(output_number_temp)  );
              
              //the reason i did not wrap this in hydrogeolog is because function in c normally can not return an array
              byte CardNumberByte[4];          // https://stackoverflow.com/questions/347949/how-to-convert-a-stdstring-to-const-char-or-char
              const char * CardNumber = fredlund_suction_ds18b20.c_str();
              unsigned long number = strtoul( CardNumber, nullptr, 16);
              for(int i=3; i>=0; i--)    // start with lowest byte of number
              {
                //Serial.println(number,HEX);
                //Serial.println(byte(number));
                //Serial.println(byte(number),HEX);
                  CardNumberByte[i] = byte( number);
                  number >>= 8;            // get next byte into position
              }   
//                 
            for(int i=0; i<4; i++)
            {
              Serial.print("0x");
              Serial.print(CardNumberByte[i], HEX);
              Serial.print(delimiter);
            }
            byte heat_suction_sensor_addr[8];
            heat_suction_sensor_addr[0]=0x28;
            heat_suction_sensor_addr[1]=CardNumberByte[0];
            heat_suction_sensor_addr[2]=CardNumberByte[1];
            heat_suction_sensor_addr[3]=CardNumberByte[2];
            heat_suction_sensor_addr[4]=0x08;
            heat_suction_sensor_addr[5]=0x00;
            heat_suction_sensor_addr[6]=0x00;
            heat_suction_sensor_addr[7]=CardNumberByte[3]; 
                       
            
            digitalWrite(power_sw_pin,HIGH);
            delay(1000);
     
            hydrogeolog1.read_DS18B20_by_addr(heat_suction_sensor_addr,digital_input) ;
            digitalWrite(power_heating_pin,HIGH);
            for(int i=0;i<output_number_temp;i++)
            {
                delay(output_temp_interval_ms);
                hydrogeolog1.read_DS18B20_by_addr(heat_suction_sensor_addr,digital_input) ;
            }
            digitalWrite(power_heating_pin,LOW);
            for(int i=0;i<output_number_temp;i++)
            {
                delay(output_temp_interval_ms);
                hydrogeolog1.read_DS18B20_by_addr(heat_suction_sensor_addr,digital_input) ;
            }

            //hydrogeolog1.search_ds18b20(ds18b20_search_pin,power_sw_pin);

            Serial.println();
            digitalWrite(power_sw_pin,LOW);               
//          thermal_suction_sensor[0]=char(thermal_suction_ds18b20);
//          thermal_suction_ds18b20.getBytes(thermal_suction_sensor, numbersd) ;
                    
         }  // fred temperature by search.




}//if string is not empty


}//loop
