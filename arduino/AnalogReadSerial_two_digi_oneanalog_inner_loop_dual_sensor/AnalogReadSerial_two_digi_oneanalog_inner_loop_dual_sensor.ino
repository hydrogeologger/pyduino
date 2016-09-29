/*
  AnalogReadSerial
  Reads an analog input on pin 0, prints the result to the serial monitor.
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.
 
 This example code is in the public domain.
 */

static const uint8_t analog_pins[] = {A0,A1,A2,A3,A4,A5};
int AnalogVals1[3];
int AnalogVals2[3];
int i;
// the delimiter between each reading. it is good to use ',' alwyas
char seperator=',';
//Arrays to store analog values after recieving them  
int number_sensors=1;
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
  // read the input on analog pin 0
  //for (int i=0; i<number_sensors;i++){
    i=0;
    Serial.print(i);
    Serial.print(seperator);
    digitalWrite(2,HIGH);
    delay(1000);
    //digitalWrite(3,HIGH);    



    for (int j=0;j<50;j++){
     analogRead(analog_pins[i]);
    delay(100);
    }


    
    for (int j=0;j<20;j++){
    AnalogVals1[i]=analogRead(analog_pins[i]);
    AnalogVals2[i]=analogRead(analog_pins[i]);
    Serial.print(AnalogVals2[i]);
    Serial.print(seperator);
    //Serial.println();
    delay(200);
    }


    
    digitalWrite(2,LOW);
    Serial.print(i);
    Serial.println();



    
    //digitalWrite(3,LOW);    
    //     
    i=1;
        Serial.print(i);
        Serial.print(seperator);
    digitalWrite(3,HIGH);
    delay(1000);
    //digitalWrite(5,HIGH);    




    for (int j=0;j<50;j++){
     analogRead(analog_pins[i]);
    delay(100);
    }


    
    for (int j=0;j<20;j++){
    AnalogVals1[i]=analogRead(analog_pins[i]);
    AnalogVals2[i]=analogRead(analog_pins[i]);
    Serial.print(AnalogVals2[i]);
    Serial.print(seperator);
    //Serial.println();
    delay(100);
    }


    
    Serial.print(i);
    Serial.println();
    digitalWrite(3,LOW);
    //digitalWrite(5,LOW);  
  //}
  
  
}
