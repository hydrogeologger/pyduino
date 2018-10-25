/*
File: RestClient.ino
This example makes an HTTP request after 10 seconds and shows the result both in
serial monitor and in the wifi console of the Arduino Uno WiFi.

Note: works only with Arduino Uno WiFi Developer Edition.

http://www.arduino.org/learning/tutorials/boards-tutorials/restserver-and-restclient
*/

#include <Wire.h>
#include <UnoWiFiDevEd.h>
  const char* connector = "rest";
  const char* server = "144.6.225.24";
  const char* method = "GET";
  //const char* method = "POST";
  //const char* resource = "/latest.txt";
  const char* resource = "/input/2DG1298g0PSMaX9JeYJeHwNQPxma?private_key=vVW3MzgNmDt3BD7ja5jaH7LrMAlg&humidity=3.51&temp=22.69";
void setup() {
  //http://144.6.225.24:8080/input/2DG1298g0PSMaX9JeYJeHwNQPxma?private_key=vVW3MzgNmDt3BD7ja5jaH7LrMAlg&humidity=3.51&temp=22.69

  //String uri = "/input/2DG1298g0PSMaX9JeYJeHwNQPxma?private_key=vVW3MzgNmDt3BD7ja5jaH7LrMAlg&humidity=3.51&temp=22.69";
	Serial.begin(9600);
	Ciao.begin();

	pinMode(2, INPUT);
  //char * CONNECTOR   = "rest"; 
  //char * SERVER_ADDR   = "144.6.225.24:8080";
	delay(10000);
	//doRequest(connector, server, resource, method);
  //CiaoData data = Ciao.write(CONNECTOR,SERVER_ADDR, uri,method);
  Serial.println(server);
  Serial.println(resource);
  CiaoData data = Ciao.write(connector, server, resource);
}

void loop() {
  delay(5000);
 CiaoData data = Ciao.write(connector, server, resource);
}

void doRequest(const char* conn, const char* server, const char* command, const char* method){
	CiaoData data = Ciao.write(conn, server, command, method);
	if (!data.isEmpty()){
		Ciao.println( "State: " + String (data.get(1)) );
		Ciao.println( "Response: " + String (data.get(2)) );
		Serial.println( "State: " + String (data.get(1)) );
		Serial.println( "Response: " + String (data.get(2)) );
	}
	else{
		Ciao.println ("Write Error");
		Serial.println ("Write Error");
	}
  delay(5000);
}
