/*
  AnalogReadSerial
  Reads an analog input on pin 0, prints the result to the serial monitor.
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.
 
 This example code is in the public domain.
 */

static const uint8_t analog_pins[] = {A0,A1,A2,A3,A4,A5};
int AnalogVals1[6];
int AnalogVals2[6];
// the delimiter between each reading. it is good to use ',' alwyas
char seperator=',';
//Arrays to store analog values after recieving them  
int number_sensors=6;
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // let all of the pins as output
  pinMode(0,OUTPUT);
  pinMode(1,OUTPUT);
  pinMode(2,OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:

  
  for (int i=0; i<number_sensors;i++){
    digitalWrite(i+2,HIGH);
    delay(500);
    AnalogVals1[i]=analogRead(analog_pins[i]);
    AnalogVals2[i]=analogRead(analog_pins[i]);
    delay(500);
    digitalWrite(i+2,LOW);
  }
  
  
    for (int i=0; i<number_sensors; i++)
  {
    //Serial.print(IO1AnalogVals[i]);
    Serial.print(AnalogVals2[i]);
    Serial.print(seperator);
  }
    Serial.println();
}
