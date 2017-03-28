static const uint8_t analog_pins[]  = {A0,A1,A2,A3,A4,A5,A6,A7,A8,A9};
// the array below works for digital sensor arrays
int digital_pins[] = {23, 25, 27, 29, 31, 33, 35, 37, 39, 41};
float AnalogVals1[10];
//float AnalogVals2[10];
int i;
// the delimiter between each reading. it is good to use ',' alwyas
char seperator=',';
//Arrays to store analog values after recieving them
int number_sensors=10;
// the setup routine runs once when you press reset:


int number_readings=11;

int dummy_readings=10;
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // let all of the pins as output

 for (int i=0; i<number_sensors;i++){
        pinMode(digital_pins[i],OUTPUT);
    }
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0
  for (int i=0; i<number_sensors;i++){
    AnalogVals1[i]=0.;
    digitalWrite(digital_pins[i],HIGH);
    delay(100);

    for (int j=0;j<dummy_readings;j++){
      analogRead(analog_pins[i]);
      //delay(100);
    }

    for (int j=0;j<number_readings;j++){
      AnalogVals1[i]+=analogRead(analog_pins[i]);
      delay(10);
    }

    AnalogVals1[i]=AnalogVals1[i]/float(number_readings);
    digitalWrite(digital_pins[i],HIGH);
 }

    for (int i=0; i<number_sensors;i++)
    {
    //Serial.print(i);
    //Serial.print(seperator);
    Serial.print(AnalogVals1[i]);
    Serial.print(seperator);

    }


    Serial.println();
    //delay_min(30);
    }

                                       
