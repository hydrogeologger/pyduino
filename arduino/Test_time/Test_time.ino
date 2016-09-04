/*
  AnalogReadSerial
  Reads an analog input on pin 0, prints the result to the serial monitor.
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.
 
 This example code is in the public domain.
 */
// http://playground.arduino.cc/Code/time
#include <Time.h>  

#define TIME_MSG_LEN  11   // time sync to PC is HEADER followed by Unix time_t as ten ASCII digits
#define TIME_HEADER  'T'   // Header tag for serial time sync message
#define TIME_REQUEST  7    // ASCII bell character requests a time sync message 


// the setup routine runs once when you press reset:
void setup() {
//  // all defination associated with time
//  // http://playground.arduino.cc/Code/DateTime
//  #include <DateTime.h>
//  #include <DateTimeStrings.h>
//  
//  #define TIME_MSG_LEN  11   // time sync to PC is HEADER and unix time_t as ten ascii digits
//  #define TIME_HEADER  255   // Header tag for serial time sync message

  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  pinMode(0,INPUT_PULLUP);
  pinMode(1,INPUT_PULLUP);
  pinMode(2,INPUT_PULLUP);
  //getPCtime();   // try to get time sync from pc
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue0 = analogRead(A0);
  delay(1000);
  int sensorValue1 = analogRead(A1);
  delay(1000);
  int sensorValue2 = analogRead(A2);
  // print out the value you read:
  Serial.print(year());
  Serial.print('/');
  Serial.print(month());
  Serial.print('/');
  Serial.print(day());
  Serial.print(',');
  Serial.print(hour());
  Serial.print(':');
  Serial.print(minute());
  Serial.print(':');
  Serial.print(second());
  Serial.print(',');

  Serial.print(sensorValue0);  
  // by this way data could be print in a row
  Serial.print(',');
  // if it is println, the next print will start from the beginning of the next row
  Serial.print(sensorValue1); 
  Serial.print(',');
  // if it is println, the next print will start from the beginning of the next row
  Serial.println(sensorValue2); 
  //Serial.print('\t') //this prints a tab
  delay(3000);        // delay in between reads for stability
}





void processSyncMessage() {
  // if time sync available from serial port, update time and return true
  while(Serial.available() >=  TIME_MSG_LEN ){  // time message consists of header & 10 ASCII digits
    char c = Serial.read() ; 
    Serial.print(c);  
    if( c == TIME_HEADER ) {       
      time_t pctime = 0;
      for(int i=0; i < TIME_MSG_LEN -1; i++){   
        c = Serial.read();          
        if( c >= '0' && c <= '9'){   
          pctime = (10 * pctime) + (c - '0') ; // convert digits to a number    
        }
      }   
      setTime(pctime);   // Sync Arduino clock to the time received on the serial port
    }  
  }
}
