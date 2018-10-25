#include <SPI.h>
#include <WiFi.h>

char ssid[] = "giraffe_and_robots";                     // your network SSID (name)
char key[] = "qy7ttvj7vg7qphyqxhd3";       // your network key
int keyIndex = 0;                                // your network key Index number
int status = WL_IDLE_STATUS;                     // the Wifi radio's status

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }

  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue:
    while (true);
  }

  // attempt to connect to Wifi network:
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WEP network, SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, keyIndex, key);

    // wait 10 seconds for connection:
    delay(10000);
  }

  // once you are connected :
  Serial.print("You're connected to the network");
}

void loop() {
  // check the network status connection once every 10 seconds:
  delay(10000);
 Serial.println(WiFi.status());
}
