
#include <OneWire.h>
#include <DallasTemperature.h>


/*-----( Declare Constants )-----*/
#define ONE_WIRE_BUS 4

/*-----( Declare objects )-----*/
/* Set up a oneWire instance to communicate with any OneWire device*/
OneWire oneWire(ONE_WIRE_BUS);

/* Tell Dallas Temperature Library to use oneWire Library */
DallasTemperature sensors(&oneWire);

//const int heatingtime=30;
//int start_flag=0;
//float initial_tempA=0;
//float initial_tempB=0;
//float final_tempA=0;
//float final_tempB=0;
//float rise_tempA=0;
//float rise_tempB=0;
//float detect_tempA=0;
//float detect_tempB=0;
//int initial_moisture=0;
//int final_moisture=0;


//float tempA[heatingtime+1];
//float tempB[heatingtime+1];

// heating time
int heating_time_s=60;
int cooling_time_s=60;



void setup() {
  Serial.begin(9600); // open serial port, set the baud rate as 9600 bps
  pinMode(3, OUTPUT);
}


void loop() {

  if (start_flag==0)
  {
    suction_test ();
  }
  
}

void suction_test(){
//  digitalWrite(5, HIGH);
//  Serial.print("Heating to 30 C, please wait...");
//  Serial.print("\n");

  delay (1000);
  
  sensors.requestTemperatures();
  detect_tempA= sensors.getTempCByIndex(0);
//  detect_tempB= sensors.getTempCByIndex(1);
  
  
//  if (detect_tempA>=30 && detect_tempB>=30)
//  {
//   
//      initial_moisture = analogRead(1);
//  
// 
//  for (int i=0; i<=heatingtime; i++)
//  {
//
//  sensors.requestTemperatures();
//  tempA [i]= sensors.getTempCByIndex(0);
//  tempB [i]= sensors.getTempCByIndex(1);
//  
//  Serial.print(i);
//  Serial.print("  ");
//  Serial.print("18b20_A: ");
//  Serial.print(tempA [i]);
//  Serial.print("  ");
//  Serial.print("18b20_B: ");
//  Serial.print(tempB [i]);
//  Serial.print("\n");
//
//  delay(1000);
//  }
//  
//  final_moisture = analogRead(1);
//  digitalWrite(3, LOW);
//  
//  //sensors.requestTemperatures();
//  //final_tempA=sensors.getTempCByIndex(0);
//  //final_tempB=sensors.getTempCByIndex(1);
//  initial_tempA=tempA [0];
//  initial_tempB=tempB [0];
//  Serial.print("initial temperature for 18b20_A is: ");
//  Serial.print(initial_tempA);
//  Serial.print("\n");
//  Serial.print("initial temperature for 18b20_B is: ");
//  Serial.print(initial_tempB);
//  Serial.print("\n");
//  
//  final_tempA=tempA [heatingtime];
//  final_tempB=tempB [heatingtime];
//  Serial.print("final temperature for 18b20_A is: ");
//  Serial.print(final_tempA);
//  Serial.print("\n");
//  Serial.print("final temperature for 18b20_B is: ");
//  Serial.print(final_tempB);
//  Serial.print("\n");
//  
//  rise_tempA=final_tempA-initial_tempA;
//  rise_tempB=final_tempB-initial_tempB;
//  Serial.print(heatingtime);
//  Serial.print("s temperature rise for 18b20_A is: ");
//  Serial.print(rise_tempA);
//  Serial.print("\n");
//  Serial.print(heatingtime);
//  Serial.print("s temperature rise for 18b20_B is: ");
//  Serial.print(rise_tempB);
//  Serial.print("\n");
//  
//  
//  Serial.print("Moisture of soil is: ");
//  Serial.print((initial_moisture+final_moisture)/2); 
//  Serial.print("\n");
//  
//  
//  
//  start_flag=1;
//  
//  }
}




