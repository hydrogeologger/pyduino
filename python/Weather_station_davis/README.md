# Davis weather station set up
To set up a weather station, you should prepare:
  1. One Davis rain gauge;
  2. One Davis wind anemometer & vane;
  3. One radiation shield (one SHT31 humidity sensor inside);
  4. One UV sensor;
  5. One enclosure box;
  6. One solar panel assembled with steel angle, a lead acid battery and a solar regulator;
  7. One tripod to support all the sensors, solar panel and enclosue;
  8. One datalogger;
  9. One WLAN adapter and antenna.

The main components of the weather station are shown as follows:
![main components of the weaterh station on the roof](https://user-images.githubusercontent.com/44887873/105043996-f15c4780-5ab1-11eb-9a32-de825d602f75.png)

## Sensors' wiring 
### Sensors' wiring sketch
Note: For Davis anemometer, it is necessary to connect a pull-up resistor (4k7 Ohm or larger) to Analog pin in datalogger.
![sensors' wiring sketch](https://user-images.githubusercontent.com/44887873/105043943-de497780-5ab1-11eb-89cf-29fe453180ef.png)

### Sensors' connection to datalogger V3

![sensors' connecntion to datalogger v3](https://user-images.githubusercontent.com/44887873/105043972-e7d2df80-5ab1-11eb-9cb5-1b1a620dfede.png)

## Davis vane - wind direction measurement diagram

![wind direction](https://user-images.githubusercontent.com/44887873/105043981-ea353980-5ab1-11eb-9dbc-c56854234272.png)
The wind vane has a 20k linear potentiometer attached to it. The output from the wind direction circuit is connected to a analog pin on the Arduino. 
As we move the wind vane around we should get a reading between 0 and 1023. The Arduino has a 10 bit A to D converter which gives us the range of 0 to 1023. 
This would also correspond to a voltage of 0 to 5V. In the software we need to convert the 0 to 1023 to a 0 to 360 range to give us the wind direction.

How to hoopup Davis anemometer to Arduino:
http://cactus.io/hookups/weather/anemometer/davis/hookup-arduino-to-davis-anemometer

## The completed weather station set up on the roof

![the view of the weather station](https://user-images.githubusercontent.com/44887873/105043988-ec979380-5ab1-11eb-8953-e74d46c381ec.png)

Please note: it is quite important to put weight on the tripod feet or fix with mouniting wires to protect the weather station from being blew down by strong wind.

