char delimiter =',';


//---------------------below required by module heat_suction_sensor----------------------------------------------------#
#include <OneWire.h>
OneWire  ds(3);  // on pin 10 (a 4.7K resistor is necessary)
// OneWire DS18S20, DS18B20, DS1822 Temperature Example
//
// http://www.pjrc.com/teensy/td_libs_OneWire.html
//
// The DallasTemperature library can do all this work for you!
// http://milesburton.com/Dallas_Temperature_Control_Library

byte heat_suction_sensor_1_addr[8];



int  heat_suction_sensor_heat_sw_1= 2;
//int  heat_suction_sensor_heat_sw_2= 3;
int  temp_sampling_number =20;
int  temp_sampling_interval_ms=9000;
//int  temp_sampling_number =20;
//int  temp_sampling_interval_ms=100;

//---------------------above required by module heat_suction_sensor----------------------------------------------------#




void setup() {
  Serial.begin(9600); // open serial port, set the baud rate as 9600 bps
  pinMode(heat_suction_sensor_heat_sw_1, OUTPUT);




//---------------------below required by module heat_suction_sensor----------------------------------------------------#
// define the address
//const char  addr='28E5A34A8007F'; the first generation of sensor hucheng have made
//heat_suction_sensor_1_addr[0]=0x28;
//heat_suction_sensor_1_addr[1]=0xE5;
//heat_suction_sensor_1_addr[2]=0xA3;
//heat_suction_sensor_1_addr[3]=0x4A;
//heat_suction_sensor_1_addr[4]=0x08;
//heat_suction_sensor_1_addr[5]=0x00;
//heat_suction_sensor_1_addr[6]=0x00;
//heat_suction_sensor_1_addr[7]=0x7F;

//addr[0]=0x2847A686800B4;the first generation of sensor hucheng have made
//heat_suction_sensor_2_addr[0]=0x28;
//heat_suction_sensor_2_addr[1]=0x47;
//heat_suction_sensor_2_addr[2]=0xA6;
//heat_suction_sensor_2_addr[3]=0x86;
//heat_suction_sensor_2_addr[4]=0x08;
//heat_suction_sensor_2_addr[5]=0x00;
//heat_suction_sensor_2_addr[6]=0x00;
//heat_suction_sensor_2_addr[7]=0xB4;

//addr[0]=0x28-96-A2-29-8-0-0-6B;the second generation of sensor LC, XM and CM made. 17-03-14 15.8ohm
//heat_suction_sensor_1_addr[0]=0x28;
//heat_suction_sensor_1_addr[1]=0x96;
//heat_suction_sensor_1_addr[2]=0xA2;
//heat_suction_sensor_1_addr[3]=0x29;
//heat_suction_sensor_1_addr[4]=0x08;
//heat_suction_sensor_1_addr[5]=0x00;
//heat_suction_sensor_1_addr[6]=0x00;
//heat_suction_sensor_1_addr[7]=0x6B;

// one minute result at arduino voltage (4.xV) in the air 17-03-14 ddr[0]=0x28-96-A2-29-8-0-0-6B
//Soil1,SucHeat,2896,Heating,25.00,25.44,26.12,26.94,27.69,28.50,29.25,29.94,30.69,31.31,32.00,32.63,33.25,33.88,34.50,35.06,35.63,36.19,36.75,37.25,37.81,Dsping,38.25,38.44,38.31,38.06,37.75,37.50,37.25,36.94,36.75,36.50,36.31,36.13,35.94,35.81,35.63,35.44,35.31,35.19,35.06,34.88,34.75,

// three minute result at arduino voltage (4.xV) in the air 17-03-14
//Soil1,SucHeat,2896,Heating,27.19,29.00,30.75,32.44,33.94,35.38,36.69,38.00,39.25,40.38,41.50,42.56,43.63,44.63,45.56,46.50,47.38,48.25,49.06,49.88,50.69,Dsping,50.75,49.81,48.75,47.81,47.00,46.25,45.50,44.81,44.19,43.50,42.88,42.31,41.75,41.19,40.69,40.19,39.75,39.31,38.94,38.50,38.06,
// SUM: 50.69-27.19=23.5 delt_last_step=0.8 celsius

// three minute result at arduino voltage (4.xV) in water, ddr[0]=0x28-96-A2-29-8-0-0-6B 17-03-14
//Soil1,SucHeat,2896,Heating,25.81,27.06,28.19,29.06,29.75,30.25,30.69,31.00,31.25,31.50,31.62,31.75,31.87,31.94,32.06,32.13,32.19,32.19,32.25,32.31,32.25,Dsping,31.62,30.00,28.56,27.44,26.62,25.94,25.44,25.06,24.69,24.50,24.31,24.12,24.00,23.94,23.81,23.81,23.75,23.69,23.62,23.62,23.62,
//Sum:  delt_heat=32.25-25.81= 6.44 degree celsist delt_last_step= 0 degree celsist
//  delt_desipate=31.62-23.62=8 degree celsist degree celsium delt_last_step= 0 degree celsist, equilibrium achieved


// three minute result at arduino voltate (4.xV) in dry sand,  ddr[0]=0x28-96-A2-29-8-0-0-6B, 15.8ohm, 17-03-15 note that the ceramic was wetted the day before
//Soil1,SucHeat,2896,Heating,25.56,27.25,28.81,30.12,31.25,32.19,33.06,33.81,34.44,35.06,35.63,36.13,36.56,37.00,37.44,37.81,38.13,38.44,38.75,39.06,39.31,Dsping,38.88,37.38,36.06,34.94,34.06,33.31,32.63,32.13,31.62,31.19,30.81,30.50,30.19,29.94,29.69,29.44,29.25,29.06,28.81,28.69,28.50,
//Sum:  delt_heat=39.31-25.56= 13.75 degree celsium delt_last_step= 0.25 degree celsist
//  delt_desipate=10.38 degree celsium delt_last_step= 0.19 degree celsist


//28 45 49 29 8 0 0 5C, 13.9ohm, three minute result at arduino voltate (5.01V) in dry sand, 17-03-14
heat_suction_sensor_1_addr[0]=0x28;
heat_suction_sensor_1_addr[1]=0x45;
heat_suction_sensor_1_addr[2]=0x49;
heat_suction_sensor_1_addr[3]=0x29;
heat_suction_sensor_1_addr[4]=0x08;
heat_suction_sensor_1_addr[5]=0x00;
heat_suction_sensor_1_addr[6]=0x00;
heat_suction_sensor_1_addr[7]=0x5C;

// three minute result at arduino voltate (4.xV) in dry sand,  ddr[0]=28 45 49 29 8 0 0 5C, 13.9ohm, 17-03-15 note that the ceramic was wetted the day before

//Soil1,SucHeat,2845,Heating,27.62,30.00,32.13,33.94,35.50,36.81,37.94,38.94,39.81,40.63,41.31,41.94,42.56,43.06,43.63,44.06,44.50,44.88,45.25,45.63,45.94,Dsping,45.13,43.00,41.13,39.56,38.25,37.13,36.19,35.38,34.63,34.00,33.44,33.00,32.56,32.13,31.81,31.44,31.12,30.87,30.62,30.37,30.19,
//Sum1:  delt_heat=45.94-27.62= 18.32, degree celsium delt_last_step= 0.31   degree celsist
//Sum2:  delt_disp=45.13-30.19=14.94,  degree celsium delt_last_step= 0.18   degree celsist



////Soil1,SucHeat,2845,Heating,26.56,28.87,30.87,32.50,33.81,34.94,35.88,36.63,37.31,37.88,38.38,38.75,39.13,39.44,39.69,39.94,40.19,40.31,40.50,40.69,40.81,Dsping,39.75,37.56,35.69,34.13,32.88,31.81,30.94,30.19,29.62,29.06,28.62,28.25,27.94,27.69,27.37,27.19,26.94,26.81,26.69,26.56,26.44,

//Sum1:  delt_heat=40.81-26.56= 14.25, degree celsium delt_last_step= 0.12   degree celsist
//Sum2:  delt_disp=39.75-26.44= 13.31, degree celsist,delt_last_step=0.12 degree celsist 

// efficiency = (delt_dry-delt_wet)/delt_dry = (18.32-14.25)/18.32 = 0.22 


SucHeat,2845,Heating,26.06,28.31,30.19,31.75,33.00,34.06,34.88,35.63,36.19,36.69,37.13,37.44,37.75,38.06,38.25,38.50,38.63,38.81,38.94,39.06,39.19,Dsping,38.13,35.94,34.06,32.56,31.31,30.31,29.56,28.87,28.37,27.87,27.44,27.12,26.87,26.62,26.44,26.25,26.06,25.94,25.87,25.75,25.62,
//Sum1:  delt_heat=39.19-26.06= 13.13, degree celsium delt_last_step= 0.13   degree celsist
//Sum2:  delt_disp=38.13-26.62= 11.51, degree celsist,delt_last_step=0.13    degree celsist 


pinMode(heat_suction_sensor_heat_sw_1, OUTPUT);  // switch for heating sucktion sensor 1
//(heat_suction_sensor_heat_sw_2, OUTPUT);  // switch for heating sucktion sensor 2
//---------------------above required by module heat_suction_sensor----------------------------------------------------#

}


void loop() {
Serial.print("Soil1,");
heat_suction_sensor(heat_suction_sensor_1_addr,heat_suction_sensor_heat_sw_1,temp_sampling_number,temp_sampling_interval_ms); 
delay(2000);
Serial.println();
//delay_min(30);
}

void heat_suction_sensor(byte heat_suction_sensor_addr[8],int heat_sw,int sampling_number, int sampling_interval_ms){

  Serial.print("SucHeat");
  Serial.print(delimiter);
  Serial.print(heat_suction_sensor_addr[0],HEX);
  Serial.print(heat_suction_sensor_addr[1],HEX);
  Serial.print(delimiter);
  Serial.print("Heating");
  Serial.print(delimiter);
//  int heat_sw;
//  byte heat_suction_sensor_addr[8];
  digitalWrite(heat_sw, HIGH);
  for (int i=0; i<=sampling_number; i++)
  {
      delay (sampling_interval_ms);
      read_DS18B20_by_addr(heat_suction_sensor_addr) ;
  }

  Serial.print("Dsping");
  Serial.print(delimiter);
  digitalWrite(heat_sw, LOW);
  for (int i=0; i<=sampling_number; i++)
  {
      delay (sampling_interval_ms);
      read_DS18B20_by_addr(heat_suction_sensor_addr) ;
  }
      //Serial.println();
}  // heat_suction_sensor





void read_DS18B20_by_addr(byte addr[8]) {
  //byte addr[8];
  byte i;
  byte present = 0;
  byte type_s;
  byte data[12];
//  byte addr[8];
  float celsius;
        
      if (OneWire::crc8(addr, 7) != addr[7]) {
          Serial.println("CRC is not valid!");
          return;
      }
    
      ds.reset();
      ds.select(addr);
      ds.write(0x44, 1);        // start conversion, with parasite power on at the end
      
      delay(1000);     // maybe 750ms is enough, maybe not
      // we might do a ds.depower() here, but the reset will take care of it.
      
      present = ds.reset();
      ds.select(addr);    
      ds.write(0xBE);         // Read Scratchpad
    
      //Serial.print("  Data = ");
      //Serial.print(present, HEX);
      //Serial.print(" ");
      for ( i = 0; i < 9; i++) {           // we need 9 bytes
        data[i] = ds.read();
        //Serial.print(data[i], HEX);
        //Serial.print(" ");
      }
      //Serial.print(" CRC=");
      //Serial.print(OneWire::crc8(data, 8), HEX);
      //Serial.println();
    
      // Convert the data to actual temperature
      // because the result is a 16 bit signed integer, it should
      // be stored to an "int16_t" type, which is always 16 bits
      // even when compiled on a 32 bit processor.
      int16_t raw = (data[1] << 8) | data[0];
      if (type_s) {
        raw = raw << 3; // 9 bit resolution default
        if (data[7] == 0x10) {
          // "count remain" gives full 12 bit resolution
          raw = (raw & 0xFFF0) + 12 - data[6];
        }
      } else {
        byte cfg = (data[4] & 0x60);
        // at lower res, the low bits are undefined, so let's zero them
        if (cfg == 0x00) raw = raw & ~7;  // 9 bit resolution, 93.75 ms
        else if (cfg == 0x20) raw = raw & ~3; // 10 bit res, 187.5 ms
        else if (cfg == 0x40) raw = raw & ~1; // 11 bit res, 375 ms
        //// default is 12 bit resolution, 750 ms conversion time
      }
      celsius = (float)raw / 16.0;
      //Serial.print(delimiter);
      Serial.print(celsius);
      Serial.write(delimiter);
  
  return;
}



