//This example shows how to use the Mux Shield for analog inputs

#include <MuxShield.h>

//Initialize the Mux Shield
MuxShield muxShield;

void setup()
{
     //open up the internal pull-up resistor
     // it is confirmed that if using a 10k ohm +-5% resistor between 5+ and gnd, 
     // the noise will be completely removed. TO160905.
     // However: if both the resistor and the following code
    pinMode(A0,INPUT_PULLDOWN);
    pinMode(A1,INPUT_PULLDOWN);
    pinMode(A2,INPUT_PULLDOWN);

    //Set I/O 1, I/O 2, and I/O 3 as analog inputs
    muxShield.setMode(1,ANALOG_IN);
    muxShield.setMode(2,ANALOG_IN);
    muxShield.setMode(3,ANALOG_IN);
    
    Serial.begin(9600);
}

//Arrays to store analog values after recieving them
//int IO1AnalogVals[16];
int IO2AnalogVals[16];
//int IO3AnalogVals[16];

void loop()
{
  //digitalWrite(A1, LOW);
  //digitalWrite(A0, LOW);
  int delay_mmsec=200;
  int number_sensors=16;
  for (int i=0; i<number_sensors; i++)
  {
    //Analog read on all 16 inputs on IO1, IO2, and IO3
    //IO1AnalogVals[i] =0;
    //IO1AnalogVals[i] = muxShield.analogReadMS(1,i);
    IO2AnalogVals[i] = muxShield.analogReadMS(2,i);
    //IO3AnalogVals[i] = muxShield.analogReadMS(3,i);
    delay(delay_mmsec);
  }
  
  //Print IO1 values for inspection
  Serial.print("IO1 analog values: ");
  for (int i=0; i<number_sensors; i++)
  {
    //Serial.print(IO1AnalogVals[i]);
    Serial.print(IO2AnalogVals[i]);
    Serial.print('\t');
  }
  Serial.println();
  delay(2000);
}
