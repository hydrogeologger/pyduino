/*
  AnalogReadSerial
  Reads an analog input on pin 0, prints the result to the serial monitor.
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.
 
 This example code is in the public domain.
 */

static const uint8_t analog_pins[]  = {A0,A1,A2,A3,A4,A5};
//static const uint8_t digital_pins[] = {2,3,4,5,6,7};
// the array below works for digital sensor arrays
int digital_pins[] = {2, 3, 4, 5, 6, 7};
float AnalogVals1[6];
float AnalogVals2[6];
int i;
// the delimiter between each reading. it is good to use ',' alwyas
char seperator=',';
//Arrays to store analog values after recieving them  
int number_sensors=3;
// the setup routine runs once when you press reset:


int number_readings=20;

int dummy_readings=30;
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // let all of the pins as output
//  pinMode(0,OUTPUT);
//  pinMode(1,OUTPUT);
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
  for (int i=0; i<number_sensors;i++){
    AnalogVals1[i]=0;
    digitalWrite(digital_pins[i],HIGH);
    delay(1000);

    for (int j=0;j<dummy_readings;j++){
      analogRead(analog_pins[i]);
      //delay(100);
    }

    for (int j=0;j<number_readings;j++){
      AnalogVals1[i]+=analogRead(analog_pins[i]);
      delay(10);
    }

    AnalogVals1[i]=AnalogVals1[i]/number_readings;
    digitalWrite(digital_pins[i],LOW);
 }
    
    for (int i=0; i<number_sensors;i++)
    {
    //Serial.print(i);
    //Serial.print(seperator);
    Serial.print(AnalogVals1[i]);
    Serial.print(seperator);

    }
    
    Serial.println();
    delay_min(30);
    }
    
/* delay in minutes 
the reason of having these functions, as compared to delay(60*60*1000) is the fact 
  that the later is not working, persumablly the maxmum value in arduino is 65536*/ 
void delay_min(int min){
  for (int i=0;i<min;i++)
  {
    for (int j=0;j<6;j++)
    {
      delay(10000);
      
    }
  }
}
//    //digitalWrite(3,LOW);    
//    //     
//    i=1;
//        Serial.print(i);
//        Serial.print(seperator);
//    digitalWrite(3,HIGH);
//    delay(1000);
//    //digitalWrite(5,HIGH);    
//
//
//
//
//    for (int j=0;j<50;j++){
//     analogRead(analog_pins[i]);
//    delay(100);
//    }
//
//
//    
//    for (int j=0;j<20;j++){
//    AnalogVals1[i]=analogRead(analog_pins[i]);
//    AnalogVals2[i]=analogRead(analog_pins[i]);
//    Serial.print(AnalogVals2[i]);
//    Serial.print(seperator);
//    //Serial.println();
//    delay(100);
//    }
//
//
//    
//    Serial.print(i);
//    Serial.println();
//    digitalWrite(3,LOW);
//    //digitalWrite(5,LOW);  
//  //}

/* I tested 
16_10_14  one sensor,on port 1: water soaked value: 608
                                short circuit value: 614

         one sensor,on port 3: water soaked value: 608
                               short circuit value: 614
         one sensor,on port 4: water soaked value: 608
                               short circuit value: 614
         one sensor,on port 5: water soaked value: 608
                               short circuit value: 614
         one sensor,on port 6: water soaked value: 608
                               short circuit value: 614
system working
  */
 
