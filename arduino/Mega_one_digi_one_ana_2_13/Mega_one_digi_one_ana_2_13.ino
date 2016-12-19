
// below is needed for analog sensor  

static const uint8_t analog_pins[]  = {A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13};
// the array below works for digital sensor arrays
int digital_pins[] = {2, 3, 4, 5, 6, 7,8,9,10,11,12,13};
float analogvals1[12];
int i;
// the delimiter between each reading. it is good to use ',' alwyas
char seperator=',';
//Arrays to store analog values after recieving them  
int number_sensors=12;
// the setup routine runs once when you press reset:

int number_readings=20;

int dummy_readings=30;

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // let all of the digital pins as output
  for (int i=0; i<number_sensors;i++){
      pinMode(digital_pins[i],OUTPUT);
  }
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0
  for (int i=0; i<number_sensors;i++){
    analogvals1[i]=0;
    digitalWrite(digital_pins[i],HIGH);
    delay(1000);

    for (int j=0;j<dummy_readings;j++){
      analogRead(analog_pins[i]);
      //delay(100);
    }

    for (int j=0;j<number_readings;j++){
      analogvals1[i]+=analogRead(analog_pins[i]);
      delay(10);
    }

    analogvals1[i]=analogvals1[i]/number_readings;
    digitalWrite(digital_pins[i],LOW);
 }
    
    for (int i=0; i<number_sensors;i++)
    {
    //serial.print(i);
    //serial.print(seperator);
    Serial.print(analogvals1[i]);
    Serial.print(seperator);

    }
    
    Serial.println();
    delay(5000);
    //delay_min(30);
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
 
