static const uint8_t analog_pins[]  = {A0,A1,A2,A3,A4,A5,A6,A7,A8,A9};
// the array below works for digital sensor arrays
int digital_pins[] = {22, 23, 24, 25, 26, 27, 28, 29, 30, 31};
float AnalogVals1[10];
//float AnalogVals2[10];
int i;
// the delimiter between each reading. it is good to use ',' alwyas
char delimiter=',';
//Arrays to store analog values after recieving them
int number_sensors=10;
// the setup routine runs once when you press reset:


int number_readings=11;

int dummy_readings=4;
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // let all of the pins as output

 for (int i=0; i<number_sensors;i++){
        pinMode(digital_pins[i],OUTPUT);
    }
}


void loop(){
    String content = "";
    char character;
    while(Serial.available()) {
        character = Serial.read();
        content.concat(character); 
        delay (10); 
    }
    if (content != ""){
        if (content == "All") { 
            Serial.print("All");
            Serial.print(delimiter);
            read_moisture_loop();
            Serial.println("AllDone");
        }
        else if (content == "SoilMoisture") {
            Serial.print("SoilMoisture");
            Serial.print(delimiter);
            read_moisture_loop();
            Serial.println("SoilMoistureDone");
        }
        else {
          Serial.println(content);
        } 
    } //content != ""
} //void loop




//// the loop routine runs over and over again forever:
//void read_moisture_loop() {
//  // read the input on analog pin 0
//  for (int i=0; i<number_sensors;i++){
//    AnalogVals1[i]=0.;
//    digitalWrite(digital_pins[i],HIGH);
//    delay(100);
//
//    for (int j=0;j<dummy_readings;j++){
//      analogRead(analog_pins[i]);
//      //delay(100);
//    }
//
//    for (int j=0;j<number_readings;j++){
//      AnalogVals1[i]+=analogRead(analog_pins[i]);
//      delay(10);
//    }
//
//    AnalogVals1[i]=AnalogVals1[i]/float(number_readings);
//    digitalWrite(digital_pins[i],HIGH);
// }
//
//    for (int i=0; i<number_sensors;i++)
//    {
//    Serial.print(AnalogVals1[i]);
//    Serial.print(delimiter);
//
//    }
//
//
//    }
//
void read_moisture_loop() {
  // read the input on analog pin 0
  for (int i=0; i<moist_number_sensors;i++){
    moist_data[i]=0;
    digitalWrite(moist_digital_pins[i],HIGH);
    delay(1000);

    for (int j=0;j<moist_dummy_readings;j++){
      analogRead(moist_analog_pins[i]);
      delay(100);
    }

    for (int j=0;j<moist_number_readings;j++){
      moist_data[i]+=analogRead(moist_analog_pins[i]);
      delay(10);
    }

    moist_data[i]=moist_data[i]/moist_number_readings;
    digitalWrite(moist_digital_pins[i],LOW);
  }

    for (int i=0; i<moist_number_sensors;i++)
    {
    Serial.print("Mo");
    Serial.print(delimiter);
    //Serial.print((char)moist_analog_pins[i]);   // how to convert this to strings?
    Serial.print(moist_digital_pins[i]);
    Serial.print(delimiter);
    Serial.print(moist_data[i]);
    Serial.print(delimiter);

    }

    //delay_min(30);
    }
                                       
