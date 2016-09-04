/*
  AnalogReadSerial
  Reads an analog input on pin 0, prints the result to the serial monitor.
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.
 
 This example code is in the public domain.
 */

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  pinMode(0,INPUT_PULLUP);
  pinMode(1,INPUT_PULLUP);
  pinMode(2,INPUT_PULLUP);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  delay(1000);
  int sensorValue1 = analogRead(A1);
  delay(1000);
  int sensorValue2 = analogRead(A2);
  // print out the value you read:
  Serial.print(sensorValue);  
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
