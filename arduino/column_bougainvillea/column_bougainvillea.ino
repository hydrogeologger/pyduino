/*This code combines: 
 1. mux schield 2 with 16 moisture sensor installed at port I/O 2,
 The sensor is powered by mux schield port I/O3. please be reminded that I/O2 needs to
 be set as input while I/O3 needs to set as ouput.
 2. digital pin at port 2 with 10 temperature sensor (DS18B20) installed
 Developed by Chenming TO160914
 Cable wiring hints: 
 1. A 10k ohm pull down resistor ( brown black orange gold with yellow background)
 needs to be installed between GND and I/O2 (i.e., A1)
so that interferences between neighbouring ports are prevented. (once interference 
occurrs, the downstream ports will have decreasing ghost values over the distance
from the the port with sensor installed. although having a sensor installed downstream
will prevent such )
 2. A 4.7k ohm (currenly red brown orange black green brown with light blue background )
 pull up resistor needs to be installed between 5V and signal
 
 */

// -------------------- needed by mux schield -----------------------
#include <MuxShield.h>
//Initialize the Mux Shield
MuxShield muxShield;
int digital_pins[] = {0, 5, 1, 6, 2, 7, 3, 8, 4, 9};


// the delimiter between each reading. it is good to use ',' alwyas
char seperator=',';
//Arrays to store analog values after recieving them  
int number_sensors=12;
// define toggles for I/O3, which are used for output;
//int toggle[16]=LOW;
//int IO1AnalogVals[16];
float IO2AnalogVals[10];
//int IO3AnalogVals[16];
//digitalWrite(A1, LOW);
//digitalWrite(A0, LOW);
// Defining the waiting time between each readings;


// the powered sensor reading, there are two properties, on and off
int delay_sensor_reading=100;

int number_dummy_readings=10;


int delay_after_reading_each_ports=50;

// finish writting 
//int delay_after_writting=1000;
int delay_after_writting=50;

//int delay_after_moisture_done=1000;  // this is working 

//int delay_after_moisture_done=60000;  // this is not working 

//int delay_after_moisture_done=60000; //not working
int delay_after_moisture_done=1000; //not working
//int delay_after_moisture_done=600000;

// -------------------- needed by digital sensor --------------------
//#include <OneWire.h>
//OneWire  ds(3);  // on digita pin 2 (a 4.7K resistor is necessary)


void setup()
{
    // -------------------- needed by mux schield -----------------------
     //open up the internal pull-up resistor
     // it is confirmed that if using a 10k ohm +-5% resistor between 5+ and gnd, 
     // the noise will be completely removed. This setup means to install a PULLDOWN
     // Resistor between signal and ground TO160905.
     // However: if both the resistor and the following code

    //Set I/O 1, I/O 2, and I/O 3 as analog inputs
    muxShield.setMode(2,DIGITAL_OUT);
    muxShield.setMode(1,ANALOG_IN);
    muxShield.setMode(3,DIGITAL_OUT);
    Serial.begin(9600);
    
    // -------------------- needed by digital sensor-------------------
}


void loop()
{

    read_muxschield();
    // Serial.println();
    //for (int i=0;i<120;i++)
    //{
    //delay(delay_after_moisture_done);
    //Serial.print(i);
    //Serial.print(seperator);
    //}
  
}



/* this subroutine reads all ports from I/O2, as powered by I/O 3.*/
void read_muxschield(){
// -------------------- needed by mux schield -----------------------
  for (int i=0; i<number_sensors; i++)
  {
    //Analog read on all 16 inputs on IO1, IO2, and IO3
    //IO1AnalogVals[i] =0;
    //IO1AnalogVals[i] = muxShield.analogReadMS(1,i);
    //muxShield.digitalWriteMS(2,i,HIGH);
    //delay(100);
    muxShield.digitalWriteMS(3,digital_pins[i],HIGH);


    for (int j=0;j<number_dummy_readings;j++){
    //delay(50);
    muxShield.analogReadMS(1,i);
    }

    IO2AnalogVals[i] =0;
    for (int j=0;j<20;j++){
    delay(delay_sensor_reading);
    muxShield.analogReadMS(1,i);
    IO2AnalogVals[i] += muxShield.analogReadMS(1,i);
    }
    IO2AnalogVals[i]=IO2AnalogVals[i]/20.0;
    
    

    
    
    muxShield.digitalWriteMS(3,digital_pins[i],LOW);
   



    delay(delay_after_reading_each_ports);
  }
   for (int i=0;i<number_sensors;i++){
     Serial.print("(");
     Serial.print(i);
     Serial.print(")");
     
        Serial.print(IO2AnalogVals[i]);
        Serial.print(seperator);
     Serial.print("  ");
    }
    
    Serial.println();
//  //Print IO1 values for inspection
//  Serial.print("IO2 analog");
//  Serial.print(seperator);
//  for (int i=0; i<number_sensors; i++)
//  {
//    //Serial.print(IO1AnalogVals[i]);
//    Serial.print(IO2AnalogVals[i]);
//    Serial.print(seperator);
//  }
//  
//  Serial.println();
//  delay(delay_after_writting);
}
 //
//orange brown red black green brown with light blue background 312 Ohms 0.5% 100ppm//
//brown green black red brown orange with light blue background 15k Ohms 1% 15 ppm//
//need to check the resistance from volt meter//

