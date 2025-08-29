/*
Morse.cpp - Library for flashing Morse code.
Created by David A. Mellis, November 2, 2007.
Released into the public domain.
*/

#include "Arduino.h"
#include "hydrogeolog.h"

hydrogeolog::hydrogeolog(const char delimiter)
{
    //pinMode(pin, OUTPUT);
    //  _pin = pin;
}

int hydrogeolog::split_strings(String inp2, String str_ay2[20])
/* returns the number of strings */
{
    int comma_idx = inp2.indexOf(',');
    int number_strings = 0;
    str_ay2[number_strings] = inp2;
    while (comma_idx != -1)
    { //there is comma
        str_ay2[number_strings] = inp2.substring(0, comma_idx);
        number_strings += 1;
        str_ay2[number_strings] = inp2.substring(comma_idx + 1);
        inp2 = str_ay2[number_strings];
        comma_idx = inp2.indexOf(',');
    }
    number_strings += 1;
    return number_strings;
} //

void hydrogeolog::print_str_ay(int number_opts, String str_ay2[20])
{
    for (int i = 0; i < number_opts; i++)
    {
        Serial.print(str_ay2[i]);
        Serial.print(delimiter);
    }
    Serial.println();
} //print_str_ay

int hydrogeolog::strcmpi(String str_source, int number_opts, String str_ay2[20])
/* string match */
{
    int str_index = HYDROGEOLOG_ERR_INVALID;
    for (int i = 0; i < number_opts; i++)
    {
        if (str_source == str_ay2[i])
        {
            str_index = i;
            break;
        }
    }
    return str_index;
} //strcmpi

long hydrogeolog::parse_argument(String str_source, long default_values, int number_opts, String str_ay2[20], bool allow_empty)
/* parse argument */
{
    //strcmpi(str_source,number_opts,str_ay2[20]);
    int str_idx = strcmpi(str_source, number_opts, str_ay2);
    long str_value = default_values;
    if (str_idx != HYDROGEOLOG_ERR_INVALID) {
        str_ay2[str_idx + 1].trim(); // Remove leading, trailing spaces
        // Test for empty string
        if (str_ay2[str_idx + 1] == "") {
            if (allow_empty) {
                return HYDROGEOLOG_ERR_EMPTY_INT;
            } else {
                return default_values;
            }
        }
        
        if (str_ay2[str_idx + 1].startsWith("0x")) {
            str_value = strtoul(str_ay2[str_idx + 1].c_str() + 2, NULL, HEX);
        } else if (str_ay2[str_idx + 1].startsWith("0b")) {
            str_value = strtoul(str_ay2[str_idx + 1].c_str() + 2, NULL, BIN);
        } else {
            str_value = str_ay2[str_idx + 1].toInt();
        }
        // Test for edge case if toInt returns 0 and string is not "0"
        if (strcmp("0", str_ay2[str_idx + 1].c_str()) != 0 && str_value == 0) {
            return default_values;
        }
    }
    return str_value;
} //parse_argument

String hydrogeolog::parse_argument_string(String str_source, String default_values, int number_opts, String str_ay2[20])
/* parse argument */
{
    int str_idx = strcmpi(str_source, number_opts, str_ay2);
    String str_value = default_values;
    if (str_idx != HYDROGEOLOG_ERR_INVALID)
    {
        str_value = str_ay2[str_idx + 1];
    }
    return str_value;
} //parse_argument

char hydrogeolog::parse_argument_char(String str_source, char default_values, int number_opts, String str_ay2[20])
/* parse argument */
{
    int str_idx = strcmpi(str_source, number_opts, str_ay2);
    if (str_idx == HYDROGEOLOG_ERR_INVALID || str_ay2[str_idx + 1].length() > 1) {
        return default_values;
    }
    return str_ay2[str_idx + 1][0];
} //parse_argument

void hydrogeolog::analog_excite_read(int power_sw_idx, int analog_idx, int number_of_dummies, int number_of_measurements, int measure_time_interval)
{
    if (power_sw_idx > 0) {
        digitalWrite(power_sw_idx, HIGH);
        delay(1000);
    }
    analog_read(analog_idx, number_of_dummies, number_of_measurements, measure_time_interval);

    if (power_sw_idx > 0) {
        digitalWrite(power_sw_idx, LOW);
    }

} // analog_excite_read

//float hydrogeolog::analog_read(int analog_idx,int number_of_dummies,int number_of_measurements,int measure_time_interval)
void hydrogeolog::analog_read(int analog_idx, int number_of_dummies, int number_of_measurements, int measure_time_interval)
{
    float results = 0.0;
    for (int j = 0; j < number_of_dummies; j++)
    {
        analogRead(analog_idx);
        delay(100);
    }

    for (int j = 0; j < number_of_measurements; j++)
    {
        results += (float)analogRead(analog_idx);
        delay(measure_time_interval);
    }

    results = results / float(number_of_measurements);
    Serial.print(results);
    Serial.print(delimiter);
    //return results;

} // analog_read


void hydrogeolog::pwm_switch_power(int power_sw_idx, int status)
{
    analogWrite(power_sw_idx, status);
    Serial.print("PWM value ");
    Serial.print(status);
}

//pwm function
void hydrogeolog::switch_power(int power_sw_idx, int status)
{
    if (status == 1)
    {
        digitalWrite(power_sw_idx, HIGH);
        Serial.print("now is high");
    }
    else
    {
        digitalWrite(power_sw_idx, LOW);
        Serial.print("now is low");
    }

} // switch_power

void hydrogeolog::dht22_excite_read(int power_sw_idx, int digi_idx, int number_of_dummies, int number_of_measurements, int measure_time_interval)
{
    dht DHT;
#define DHT22_PIN digi_idx

    digitalWrite(power_sw_idx, HIGH);
    delay(1000);

    dht22_read(digi_idx, number_of_dummies, number_of_measurements, measure_time_interval);

    digitalWrite(power_sw_idx, LOW);
} // dht_excite_read

void hydrogeolog::dht22_read(int digi_idx, int number_of_dummies, int number_of_measurements, int measure_time_interval)
{
    dht DHT;
#define DHT22_PIN digi_idx
    if (measure_time_interval < 1000)
    {
        measure_time_interval = 1000;
    }

    float results = 0.0;
    for (int j = 0; j < number_of_dummies; j++)
    {
        int chk1 = DHT.read22(digi_idx);
        delay(1000);
    }
    float t_results = 0.0;
    float rh_results = 0.0;
    for (int j = 0; j < number_of_measurements; j++)
    {
        int chk1 = DHT.read22(DHT22_PIN);
        t_results += (float)DHT.temperature;
        rh_results += (float)DHT.humidity;
        delay(measure_time_interval);
    }

    t_results /= float(number_of_measurements);
    rh_results /= float(number_of_measurements);
    Serial.print(t_results);
    Serial.print(delimiter);
    Serial.print(rh_results);
    Serial.print(delimiter);
} // dht_read


void hydrogeolog::search_ds18b20(int digi_pin, int power_switch)
{
    OneWire ds(digi_pin); // on pin 2 (a 4.7K resistor is necessary)
    // digitalWrite(power_switch, HIGH);
    // delay(1000);

    byte i;
    byte present = 0;
    byte type_s;
    byte data[12];
    byte addr[8];
    float celsius, fahrenheit;
    int loop_time = 3;
    int searchIndex = 0;
    char hexAddr[4];
    // for (int kk = 0; kk < loop_time; kk++) {
    //     Serial.print(kk);
        boolean while_indicator = true;
        while (while_indicator == true) {
            if (!ds.search(addr)) {
                Serial.println("No more addresses.");
                ds.reset_search();
                delay(250);
                //j+=1;
                while_indicator = false;
                break;
            }
            Serial.print(String(searchIndex) + "_ROM =");
            for (i = 0; i < 8; i++) {
                sprintf(hexAddr, " %02X",addr[i]);
                Serial.print(hexAddr);
                // Serial.write(' ');
                // Serial.print(addr[i], HEX);
            }

            //  if (OneWire::crc8(addr, 7) != addr[7]) {
            //      Serial.println("CRC is not valid!");
            //      return;
            //  }
            //Serial.println();

            // the first ROM byte indicates which chip
            switch (addr[0]) {
            case 0x10:
                //Serial.println("  Chip = DS18S20");  // or old DS1820
                type_s = 1;
                break;
            case 0x28:
                //Serial.println("  Chip = DS18B20");
                type_s = 0;
                break;
            case 0x22:
                //Serial.println("  Chip = DS1822");
                type_s = 0;
                break;
            default:
                //Serial.println("Device is not a DS18x20 family device.");
                Serial.println("");
                return;
            }

            ds.reset();
            ds.select(addr);
            ds.write(0x44); // start conversion, use ds.write(0x44,1) with parasite power on at the end

            delay(1000); // maybe 750ms is enough, maybe not
            // we might do a ds.depower() here, but the reset will take care of it.

            present = ds.reset();
            ds.select(addr);
            ds.write(0xBE); // Read Scratchpad

            //Serial.print("  Data = ");
            //Serial.print(present, HEX);
            //Serial.print(" ");
            for (i = 0; i < 9; i++) { // we need 9 bytes
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
                if (data[7] == 0x10)
                {
                    // "count remain" gives full 12 bit resolution
                    raw = (raw & 0xFFF0) + 12 - data[6];
                }
            } else {
                byte cfg = (data[4] & 0x60);
                // at lower res, the low bits are undefined, so let's zero them
                if (cfg == 0x00)
                    raw = raw & ~7; // 9 bit resolution, 93.75 ms
                else if (cfg == 0x20)
                    raw = raw & ~3; // 10 bit res, 187.5 ms
                else if (cfg == 0x40)
                    raw = raw & ~1; // 11 bit res, 375 ms
                                    //// default is 12 bit resolution, 750 ms conversion time
            }
            celsius = (float)raw / 16.0;
            fahrenheit = celsius * 1.8 + 32.0;
            Serial.print(",  Temperature = ");
            Serial.print(celsius);
            Serial.print(" Celsius, ");
            Serial.print(fahrenheit);
            Serial.println(" Fahrenheit");
            searchIndex++;
        } //while true
    // }     // looptime
} //search_ds18b20

void hydrogeolog::read_DS18B20_by_addr(byte addr[8], int digi_pin)
{
    //byte addr[8];
    byte i;
    byte present = 0;
    byte type_s;
    byte data[12];
    //  byte addr[8];
    float celsius;
    OneWire ds(digi_pin); // on pin 2 (a 4.7K resistor is necessary)

    if (OneWire::crc8(addr, 7) != addr[7])
    {
        Serial.println("CRC is not valid!");
        return;
    }

    ds.reset();
    ds.select(addr);
    ds.write(0x44, 1); // start conversion, with parasite power on at the end

    delay(1000); // maybe 750ms is enough, maybe not
    // we might do a ds.depower() here, but the reset will take care of it.

    present = ds.reset();
    ds.select(addr);
    ds.write(0xBE); // Read Scratchpad

    //Serial.print("  Data = ");
    //Serial.print(present, HEX);
    //Serial.print(" ");
    for (i = 0; i < 9; i++)
    { // we need 9 bytes
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
    if (type_s)
    {
        raw = raw << 3; // 9 bit resolution default
        if (data[7] == 0x10)
        {
            // "count remain" gives full 12 bit resolution
            raw = (raw & 0xFFF0) + 12 - data[6];
        }
    }
    else
    {
        byte cfg = (data[4] & 0x60);
        // at lower res, the low bits are undefined, so let's zero them
        if (cfg == 0x00)
            raw = raw & ~7; // 9 bit resolution, 93.75 ms
        else if (cfg == 0x20)
            raw = raw & ~3; // 10 bit res, 187.5 ms
        else if (cfg == 0x40)
            raw = raw & ~1; // 11 bit res, 375 ms
                            //// default is 12 bit resolution, 750 ms conversion time
    }
    celsius = (float)raw / 16.0;
    //Serial.print(delimiter);
    Serial.print(celsius);
    Serial.print(delimiter);

    return;
}

void hydrogeolog::tcaselect(int i)
{
#define TCAADDR 0x70
    if (i > 7)
        return;
    Wire.beginTransmission(TCAADDR);
    Wire.write(1 << i);
    Wire.endTransmission();
}

// pressure transducers
void hydrogeolog::ms5803(int number_of_dummies, int number_of_measurements, int measure_time_interval_ms, int debug_sw, int tca9548_channel)
{
    //  ADDRESS_HIGH = 0x76
    //  ADDRESS_LOW  = 0x77
    MS5803 sensor(ADDRESS_HIGH);
    float temperature_c;
    double pressure_abs = 0.;
    delay(500);
    sensor.reset();
    delay(500);
    sensor.begin();
    delay(500);
    tcaselect(tca9548_channel);

    delay(500);
    temperature_c = sensor.getTemperature(CELSIUS, ADC_512);
    delay(500);

    for (int j = 0; j < number_of_dummies; j++)
    {
        sensor.getPressure(ADC_4096);
        delay(500);
    }
    float t_results = 0.;
    double pressure = 0.;
    for (int j = 0; j < number_of_measurements; j++)
    {
        pressure = double(sensor.getPressure(ADC_4096));
        pressure_abs += pressure;
        delay(measure_time_interval_ms);
        if (debug_sw == 1)
        {
            Serial.print(pressure);
            Serial.print(delimiter);
        } //debug_sw
    }

    pressure_abs /= double(number_of_measurements);

    Serial.print(temperature_c);
    Serial.print(delimiter);
    Serial.print(pressure_abs);
    Serial.print(delimiter);
} //5803

// pressure transducers
void hydrogeolog::ms5803l(int number_of_dummies, int number_of_measurements, int measure_time_interval_ms, int debug_sw, int tca9548_channel)
{
    //  ADDRESS_HIGH = 0x76
    //  ADDRESS_LOW  = 0x77
    MS5803 sensor(ADDRESS_LOW);
    float temperature_c;
    double pressure_abs = 0.;
    delay(500);
    sensor.reset();
    delay(500);
    sensor.begin();
    delay(500);
    tcaselect(tca9548_channel);

    delay(500);
    temperature_c = sensor.getTemperature(CELSIUS, ADC_512);
    delay(500);

    for (int j = 0; j < number_of_dummies; j++)
    {
        sensor.getPressure(ADC_4096);
        delay(500);
    }
    float t_results = 0.;
    double pressure = 0.;
    for (int j = 0; j < number_of_measurements; j++)
    {
        pressure = double(sensor.getPressure(ADC_4096));
        pressure_abs += pressure;
        delay(measure_time_interval_ms);
        if (debug_sw == 1)
        {
            Serial.print(pressure);
            Serial.print(delimiter);
        } //debug_sw
    }

    pressure_abs /= double(number_of_measurements);

    Serial.print(temperature_c);
    Serial.print(delimiter);
    Serial.print(pressure_abs);
    Serial.print(delimiter);
} //5803l

//sht31 RH&T sensor (I2C interface)
void hydrogeolog::sht31(int number_of_dummies, int number_of_measurements, int measure_time_interval_ms, int debug_sw, int tca9548_channel)
{
    //default_addr = 0x44
    //Set to 0x45 for alternate i2c addr
    Adafruit_SHT31 sht31 = Adafruit_SHT31();
    sht31.begin(0x44);
    float t;
    float h;

    float temp_avg = 0.;
    float humi_avg = 0.;

    tcaselect(tca9548_channel);

    for (int j = 0; j < number_of_dummies; j++)
    {
        t = sht31.readTemperature();
        h = sht31.readHumidity();
        delay(measure_time_interval_ms);
    }

    for (int j = 0; j < number_of_measurements; j++)
    {
        t = sht31.readTemperature();
        h = sht31.readHumidity();
        delay(measure_time_interval_ms);
        temp_avg += t;
        humi_avg += h;
        if (debug_sw == 1)
        {
            Serial.print(t);
            Serial.print(delimiter);
            Serial.print(h);
            Serial.print(delimiter);
        } //debug_sw
    }
    temp_avg /= float(number_of_measurements);
    humi_avg /= float(number_of_measurements);

    Serial.print(temp_avg);
    Serial.print(delimiter);
    Serial.print(humi_avg);
    Serial.print(delimiter);
}

//rcswitch
void hydrogeolog::rcswitch(int rc_switch, int pulselength, const char *sw_code)
//void hydrogeolog::rcswitchAon(int rc_switch, int pulselength)
{

    RCSwitch mySwitch = RCSwitch();
    mySwitch.setProtocol(1);
    mySwitch.setRepeatTransmit(15);
    mySwitch.enableTransmit(rc_switch);
    //mySwitch.enableTransmit(10);
    mySwitch.setPulseLength(pulselength);
    //Serial.print("pulselength ");
    //Serial.println(pulselength);
    //mySwitch.setPulseLength(306);
    //mySwitch.send(binary_code);
    //Serial.println(pulselength);
    //Serial.println(binary_code);
    //Serial.println("011101101101100000001111100111100");
    // below not sucessful
    //char abc="011101101101100000001111100111100";
    //Serial.println(abc);

    // below is now successful
    //char* abc="011101101101100000001111100111100";
    //Serial.println(abc);
    //Serial.print("sw_code ");
    //Serial.println(sw_code);
    mySwitch.send(sw_code);
    //for (sw_code=="Aon"){
    //mySwitch.send("011101101101100000001111100111100");
    //}
}
/*
void hydrogeolog::rcswitchAoff(int rc_switch, int pulselength)
    {

    RCSwitch mySwitch = RCSwitch();
    mySwitch.setProtocol(1);
    mySwitch.setRepeatTransmit(7);
    mySwitch.enableTransmit(rc_switch);
    mySwitch.setPulseLength(pulselength);
    mySwitch.send("011101101101100000001110100111110");
    
    }

void hydrogeolog::rcswitchBon(int rc_switch, int pulselength)
    {

    RCSwitch mySwitch = RCSwitch();
    mySwitch.setProtocol(1);
    mySwitch.setRepeatTransmit(7);
    mySwitch.enableTransmit(rc_switch);
    mySwitch.setPulseLength(pulselength);
    mySwitch.send("011101101101100000001101100111000");
    
    }

void hydrogeolog::rcswitchBoff(int rc_switch, int pulselength)
    {

    RCSwitch mySwitch = RCSwitch();
    mySwitch.setProtocol(1);
    mySwitch.setRepeatTransmit(7);
    mySwitch.enableTransmit(rc_switch);
    mySwitch.setPulseLength(pulselength);
    mySwitch.send("011101101101100000001100100111010");

    }

void hydrogeolog::rcswitchCon(int rc_switch, int pulselength)
    {

    RCSwitch mySwitch = RCSwitch();
    mySwitch.setProtocol(1);
    mySwitch.setRepeatTransmit(7);
    mySwitch.enableTransmit(rc_switch);
    mySwitch.setPulseLength(pulselength);
    mySwitch.send("011101101101100000001011100110100");

    }

void hydrogeolog::rcswitchCoff(int rc_switch, int pulselength)
    {

    RCSwitch mySwitch = RCSwitch();
    mySwitch.setProtocol(1);
    mySwitch.setRepeatTransmit(7);
    mySwitch.enableTransmit(rc_switch);
    mySwitch.setPulseLength(pulselength);
    mySwitch.send("011101101101100000001010100110110");
    
    }
*/
// temperature and humidity by sensirion
void hydrogeolog::sht75(int dataPin, int clockPin, int number_of_dummies, int number_of_measurements, int measure_time_interval_ms, int debug_sw)
{
    float temp;
    float humi;
    float dewp;

    float temp_avg = 0.;
    float humi_avg = 0.;

    Sensirion tempSensor = Sensirion(dataPin, clockPin);
    delay(1000);
    for (int j = 0; j < number_of_dummies; j++)
    {
        tempSensor.measure(&temp, &humi, &dewp); //the reason of doing this is one function returns three values
        delay(measure_time_interval_ms);
    }

    for (int j = 0; j < number_of_measurements; j++)
    {
        tempSensor.measure(&temp, &humi, &dewp);
        delay(measure_time_interval_ms);
        temp_avg += temp;
        humi_avg += humi;
        if (debug_sw == 1)
        {
            Serial.print(temp);
            Serial.print(delimiter);
            Serial.print(humi);
            Serial.print(delimiter);
        } //debug_sw
    }
    temp_avg /= float(number_of_measurements);
    humi_avg /= float(number_of_measurements);

    Serial.print(temp_avg);
    Serial.print(delimiter);
    Serial.print(humi_avg);
    Serial.print(delimiter);
} //sht75

// loop routine to obtain si1145 result
void hydrogeolog::si1145(int number_of_dummies, int number_of_measurements, int measurement_time_interval, int debug_sw, int tca9548_channel)
{
    //Adafruit_SI1145 uv = Adafruit_SI1145();
    float vis = 0.0;
    float ir = 0.0;
    float uvindex = 0.0;
    Adafruit_SI1145 uv = Adafruit_SI1145();
    delay(1000);
    uv.begin();
    tcaselect(tca9548_channel);
    
    for (int j = 0; j < number_of_dummies; j++)
    {
        uv.readVisible();
        delay(1000);
        uv.readIR();
        delay(1000);
        uv.readUV();
        delay(measurement_time_interval);
    }
    for (int j = 0; j < number_of_measurements; j++)
    {
        vis += uv.readVisible();
        delay(100);
        ir += uv.readIR();
        delay(100);
        uvindex += uv.readUV();
        delay(measurement_time_interval);
    }
    vis /= float(number_of_measurements);
    ir /= float(number_of_measurements);
    uvindex /= float(number_of_measurements);
    Serial.print("Vis");
    Serial.print(delimiter);
    Serial.print(vis);
    Serial.print(delimiter);
    Serial.print("IR");
    Serial.print(delimiter);
    Serial.print(ir);
    Serial.print(delimiter);

    // Uncomment if you have an IR LED attached to LED pin!
    //Serial.print("Prox: "); Serial.println(uv.readProx());

    //float UVindex = uv.readUV();
    // the index is multiplied by 100 so to get the
    // integer index, divide by 100!
    //UVindex /= 100.0;
    Serial.print("UV");
    Serial.print(delimiter);
    Serial.print(uvindex);
    Serial.print(delimiter);
}

//  search 9548 sensors
void hydrogeolog::search_9548_channels()
{

    while (!Serial)
        ;
    delay(1000);

    Wire.begin();

    Serial.println("TCAScanner ready!");

    for (uint8_t t = 0; t < 8; t++)
    {
        tcaselect(t);
        Serial.print("TCA Port #");
        Serial.println(t);

        for (uint8_t addr = 0; addr <= 127; addr++)
        {
            if (addr == TCAADDR)
                continue;

            uint8_t data;
            if (!twi_writeTo(addr, &data, 0, 1, 1))
            {
                Serial.print("Found I2C 0x");
                Serial.println(addr, HEX);
            }
        }
    }
    Serial.print("Done");
}
