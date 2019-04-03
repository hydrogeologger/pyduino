/*Include libraries ===========================================================*/
/*
in /home/pi/Arduino/libraries
place new libraries in this location and include as
#include <library.h>
*note the <> not ""
*/

#include <SDI12.h>
#include <hydrogeolog.h>
#include "timing.h"
#include "common.h"
#include "SDI12_function.h"

/*===========================================================================*/

/*Global variables and defines ==============================================*/
hydrogeolog hydrogeolog1(DELIMITER);
/*===========================================================================*/

/*Function prototypes========================================================*/

/*===========================================================================*/

/*Function definition========================================================*/

void setup()
{
    // initialize serial communication at 9600 bits per second:
    Serial.begin(9600);
    Serial1.begin(9600);
    Serial2.begin(9600);
    Serial3.begin(9600);
    for (int i = 0; i < DIGITAL_PIN_COUNT; i++)
    {
        pinMode(digi_out_pins[i], OUTPUT);
    }
    isComm = FALSE;
}

void print_debug(int debug_sw, int pw_pin, int no_measures, int no_dum, int interval)
{
    if (debug_sw)
    {
        hydrogeolog1.print_string_delimiter_value("power", String(pw_pin));
        hydrogeolog1.print_string_delimiter_value("points", String(no_measures));
        hydrogeolog1.print_string_delimiter_value("dummies", String(no_dum));
        hydrogeolog1.print_string_delimiter_value("interval_mm", String(interval));
    }
}

void analog_reading(int str_ay_size, int debug_sw, int analog_in_pin, int power_sw_pin, String str_ay[])
{
    //E.g: power,43,analog,15,point,3,interval_mm,200,debug,1  -> checking voltage
    if ((analog_in_pin != INVALID) && (power_sw_pin != INVALID))
    {
        int number_of_measurements = hydrogeolog1.parse_argument("points", DEFAULT_POINTS, str_ay_size, str_ay);
        int number_of_dummies = hydrogeolog1.parse_argument("dummies", DEFAULT_DUMMIES, str_ay_size, str_ay);
        int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", DEFAULT_INTERVAL, str_ay_size, str_ay);
        hydrogeolog1.print_string_delimiter_value("analog", String(analog_in_pin));
        print_debug(debug_sw, power_sw_pin, number_of_measurements, number_of_dummies, measure_time_interval_ms);
        hydrogeolog1.analog_excite_read(power_sw_pin, analog_in_pin, number_of_dummies, number_of_measurements, measure_time_interval_ms);
        Serial.println();
    }
}

void array_analog_reading(int str_ay_size, int debug_sw, int analog_array, int power_sw_pin, String str_ay[])
{
    /**analog reading in an array
         anaay,1,power,48,point,3,interval_mm,200,debug,1
    **/
    if ((analog_array != INVALID) && (power_sw_pin != INVALID)) //
    {
        int number_of_measurements = hydrogeolog1.parse_argument("points", DEFAULT_POINTS, str_ay_size, str_ay);
        int number_of_dummies = hydrogeolog1.parse_argument("dummies", DEFAULT_DUMMIES, str_ay_size, str_ay);
        int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", DEFAULT_INTERVAL, str_ay_size, str_ay);
        hydrogeolog1.print_string_delimiter_value("analog_array", String(analog_array));
        print_debug(debug_sw, power_sw_pin, number_of_measurements, number_of_dummies, measure_time_interval_ms);
        digitalWrite(power_sw_pin, HIGH);
        delay(1000);
        for (int i = 0; i < ANALOG_MOIS_COUNT; i++)
        {
            hydrogeolog1.analog_read(ana_moisture_ay[i], number_of_dummies, number_of_measurements, measure_time_interval_ms);
        }
        digitalWrite(power_sw_pin, LOW);
        Serial.println();
    }
}

void o2_array_analog_reading(int str_ay_size, int debug_sw, int o2_ana_array, int power_sw_pin, String str_ay[])
{
    /**analog reading in an array
    E.g:
    o2_ana_ay,1,power,43,point,3,interval_mm,200,debug,1
    o2_ana_ay,1,power,48,point,3,interval_mm,200,debug,1
    **/
    if ((o2_ana_array != INVALID) && (power_sw_pin != INVALID)) //
    {
        int number_of_measurements = hydrogeolog1.parse_argument("points", DEFAULT_POINTS, str_ay_size, str_ay);
        int number_of_dummies = hydrogeolog1.parse_argument("dummies", DEFAULT_DUMMIES, str_ay_size, str_ay);
        int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", DEFAULT_INTERVAL, str_ay_size, str_ay);
        hydrogeolog1.print_string_delimiter_value("o2_ana_ay", String(o2_ana_array));
        print_debug(debug_sw, power_sw_pin, number_of_measurements, number_of_dummies, measure_time_interval_ms);
        digitalWrite(power_sw_pin, HIGH);
        delay(1000);
        for (int i = 0; i < ANALOG_MOIS_COUNT; i++)
        {
            hydrogeolog1.dht22_read(digi_dht_ay[i], number_of_dummies, number_of_measurements, measure_time_interval_ms);
            hydrogeolog1.analog_read(ana_o2_ay[i], number_of_dummies, number_of_measurements, measure_time_interval_ms);
        }
        digitalWrite(power_sw_pin, LOW);
        Serial.println();
    }
}

void power_switch(int pow_sw, int pow_sw_status)
{
    /*
    E.g:
    power_switch,46,power_switch_status,1
    */
    if ((pow_sw != INVALID))
    {
        hydrogeolog1.print_string_delimiter_value("power_switch", String(pow_sw));
        hydrogeolog1.print_string_delimiter_value("power_switch_status", String(pow_sw_status));
        hydrogeolog1.switch_power(pow_sw, pow_sw_status);
        Serial.println();
    }
}

void dht22_measurement(int str_ay_size, int debug_sw, int dht22_in_pin, int power_sw_pin, String str_ay[])
{
    /*dht22 measurement
    dht22,10,power,48,points,2,dummies,1,interval_mm,200,debug,1
    a 10 k resistor is required to put between digi 10 and ground
    */
    if ((dht22_in_pin != INVALID) && (power_sw_pin != INVALID))
    {
        int number_of_measurements = hydrogeolog1.parse_argument("points", DEFAULT_POINTS, str_ay_size, str_ay);
        int number_of_dummies = hydrogeolog1.parse_argument("dummies", DEFAULT_DUMMIES, str_ay_size, str_ay);
        int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", DEFAULT_INTERVAL, str_ay_size, str_ay);
        if (measure_time_interval_ms < 1000)
        {
            measure_time_interval_ms = 1000;
        }
        // needs to be at leaset 1000 ms
        hydrogeolog1.print_string_delimiter_value("dht22", String(dht22_in_pin));
        print_debug(debug_sw, power_sw_pin, number_of_measurements, number_of_dummies, measure_time_interval_ms);
        hydrogeolog1.dht22_excite_read(power_sw_pin, dht22_in_pin, number_of_dummies, number_of_measurements, measure_time_interval_ms);
        Serial.println();
    }
}

void dhto2_measurement(int str_ay_size, int debug_sw, int dhto2_in_pin, int anain_pin, int power_sw_pin, String str_ay[])
{
    /*v measurement, measuring analog and dht22 at same time
       dhto2,12,power,41,points,2,anain,0,dummies,1,interval_mm,1000,debug,1
       dhto2,10,power,48,points,2,anain,0,dummies,1,interval_mm,1000,debug,1
    */
    if ((dhto2_in_pin != INVALID) && (power_sw_pin != INVALID) && (anain_pin != INVALID))
    {
        int number_of_measurements = hydrogeolog1.parse_argument("points", 1, str_ay_size, str_ay);
        int number_of_dummies = hydrogeolog1.parse_argument("dummies", 0, str_ay_size, str_ay);
        int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", 1000, str_ay_size, str_ay);
        // needs to be at leaset 1000 ms
        measure_time_interval_ms = measure_time_interval_ms < 1000 ? 1000 : measure_time_interval_ms;
        hydrogeolog1.print_string_delimiter_value("dhto2", String(dhto2_in_pin));
        print_debug(debug_sw, power_sw_pin, number_of_measurements, number_of_dummies, measure_time_interval_ms);
        digitalWrite(power_sw_pin, HIGH);
        delay(1000);
        hydrogeolog1.dht22_read(dhto2_in_pin, number_of_dummies, number_of_measurements, measure_time_interval_ms);
        hydrogeolog1.analog_read(anain_pin, number_of_dummies, number_of_measurements, measure_time_interval_ms);
        digitalWrite(power_sw_pin, LOW);
        Serial.println();
    }
}

void luminox_reading(int str_ay_size, String lumino2, int serial_pin, int power_sw_pin, String str_ay[])
{
    /*luminox sensor
    lumino2,M 2,power,42,serial,2
    */
    if ((lumino2 != "") && (power_sw_pin != INVALID) && (serial_pin >= 1) && (serial_pin <= 3))
    {
        int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", 1000, str_ay_size, str_ay);
        String input_linebreak = hydrogeolog1.parse_argument_string("inp_linebreak", "\r\n", str_ay_size, str_ay);
        hydrogeolog1.print_string_delimiter_value("lumino2_cmd", lumino2);
        hydrogeolog1.print_string_delimiter_value("pow", String(power_sw_pin));
        hydrogeolog1.print_string_delimiter_value("serial", String(serial_pin));
        hydrogeolog1.print_string_delimiter_value("delay", String(measure_time_interval_ms));
        // needs to be at leaset 1000 ms
        measure_time_interval_ms = measure_time_interval_ms < 1000 ? 1000 : measure_time_interval_ms;
        digitalWrite(power_sw_pin, HIGH);
        delay(1000);
        HardwareSerial mySerial = Serial;
        switch (serial_pin)
        {
        case 1:
            mySerial = Serial1;
            break;
        case 2:
            mySerial = Serial2;
            break;
        case 3:
            mySerial = Serial3;
            break;
        default:
            return;
        }
        mySerial.print("M 1\r\n");
        delay(measure_time_interval_ms);
        String aa1 = mySerial.readStringUntil('\n');
        Serial.print(aa1);
        mySerial.print("M 1\r\n");
        delay(measure_time_interval_ms);
        aa1 = mySerial.readStringUntil('\n');
        Serial.print(aa1);
        Serial.print("result,");
        mySerial.print(lumino2);
        mySerial.print("\r\n");
        delay(measure_time_interval_ms);
        String aa = mySerial.readStringUntil('\n');
        Serial.print(aa);
        delay(measure_time_interval_ms);
        aa = mySerial.readStringUntil('\n');
        Serial.println(aa);
        digitalWrite(power_sw_pin, LOW);
    }
}

// the loop routine runs over and over again forever:
void loop()
{
    timeout_reset_pi();
    String content = "";
    char character;
    while (Serial.available())
    {
        character = Serial.read();
        content.concat(character);
        delay(10);
    }
    command_reset_pi(content);
    if (content == "")
    {
        timing_no_comm();
    }
    else
    {
        reset_timer();
        String str_ay[20];
        int str_ay_size = hydrogeolog1.split_strings(content, str_ay);
        int debug_sw = hydrogeolog1.parse_argument("debug", 0, str_ay_size, str_ay);
        int power_sw_pin = hydrogeolog1.parse_argument("power", -1, str_ay_size, str_ay);

        analog_reading(str_ay_size, debug_sw,
                       hydrogeolog1.parse_argument("analog", -1, str_ay_size, str_ay),
                       power_sw_pin, str_ay);

        array_analog_reading(str_ay_size, debug_sw,
                             hydrogeolog1.parse_argument("anaay", -1, str_ay_size, str_ay),
                             power_sw_pin, str_ay);

        o2_array_analog_reading(str_ay_size, debug_sw,
                                hydrogeolog1.parse_argument("o2_ana_ay", -1, str_ay_size, str_ay),
                                power_sw_pin, str_ay);

        power_switch(hydrogeolog1.parse_argument("power_switch", -1, str_ay_size, str_ay),
                     hydrogeolog1.parse_argument("power_switch_status", 0, str_ay_size, str_ay));

        dht22_measurement(str_ay_size, debug_sw,
                          hydrogeolog1.parse_argument("dht22", -1, str_ay_size, str_ay),
                          power_sw_pin, str_ay);

        dhto2_measurement(str_ay_size, debug_sw,
                          hydrogeolog1.parse_argument("dhto2", -1, str_ay_size, str_ay),
                          hydrogeolog1.parse_argument("anain", -1, str_ay_size, str_ay),
                          power_sw_pin, str_ay);

        luminox_reading(str_ay_size,
                        hydrogeolog1.parse_argument_string("lumino2", "", str_ay_size, str_ay),
                        hydrogeolog1.parse_argument("serial", -1, str_ay_size, str_ay),
                        power_sw_pin, str_ay);

        /*ds18b20 search
        ds18b20_search,13,power,42
       */
        int ds18b20_search_pin = hydrogeolog1.parse_argument("ds18b20_search", -1, str_ay_size, str_ay);
        power_sw_pin = hydrogeolog1.parse_argument("power", -1, str_ay_size, str_ay);
        if ((ds18b20_search_pin != INVALID) && (power_sw_pin != INVALID))
        {
            hydrogeolog1.print_string_delimiter_value("ds18b20_search", String(ds18b20_search_pin));
            digitalWrite(power_sw_pin, HIGH);
            delay(1000);
            hydrogeolog1.search_ds18b20(ds18b20_search_pin, power_sw_pin);
            digitalWrite(power_sw_pin, LOW);
        }

        /*
         thermal_suction_ds18b20,28E5A34A0800007F,power,4,numbersd,1
         thermal_suction_ds18b20,A3CF969B,digital_input,13,power,42
         thermal_suction_ds18b20,464CBABE,digital_input,13,power,42
         RESULT FROM 8
         thermal_suction_ds18b20,28E5A34A0800007F,power,4,50,56,69,53,65,51,52,0,40,229,163,74,8,0,0,127
         RESULT FROM 2
         thermal_suction_ds18b20,28E5A34A0800007F,power,4,50,0,5,74,5,0,0,3,40,229,163,74,8,0,0,127
         thermal_suction_ds18b20,28E5A34A,power,4,numbersd,1
         28 A3 CF 96 8 0 0 9B
         */
        String thermal_suction_ds18b20 = hydrogeolog1.parse_argument_string("thermal_suction_ds18b20", "", str_ay_size, str_ay);
        power_sw_pin = hydrogeolog1.parse_argument("power", -1, str_ay_size, str_ay);
        int thermal_suction_digi_pin = hydrogeolog1.parse_argument("digital_input", -1, str_ay_size, str_ay);
        //int numbersd= hydrogeolog1.parse_argument("numbersd",-1,str_ay_size,str_ay);

        if ((thermal_suction_ds18b20 != "") && (power_sw_pin != INVALID))
        {
            hydrogeolog1.print_string_delimiter_value("thermal_suction_ds18b20", String(thermal_suction_ds18b20));
            hydrogeolog1.print_string_delimiter_value("power", String(power_sw_pin));
            //hydrogeolog1.print_string_delimiter_value("numbersd"  ,String(numbersd)  );
            //the reason i did not wrap this in hydrogeolog is because function in c normally can not return an array
            byte CardNumberByte[4]; // https://stackoverflow.com/questions/347949/how-to-convert-a-stdstring-to-const-char-or-char
            const char *CardNumber = thermal_suction_ds18b20.c_str();
            unsigned long number = strtoul(CardNumber, nullptr, 16);
            for (int i = 3; i >= 0; i--) // start with lowest byte of number
            {
                //Serial.println(number,HEX);
                //Serial.println(byte(number));
                //Serial.println(byte(number),HEX);
                CardNumberByte[i] = byte(number);
                number >>= 8; // get next byte into position
            }
            //
            for (int i = 0; i < 4; i++)
            {
                Serial.print("0x");
                Serial.print(CardNumberByte[i], HEX);
                Serial.print(DELIMITER);
            }
            byte heat_suction_sensor_addr[8];
            heat_suction_sensor_addr[0] = 0x28;
            heat_suction_sensor_addr[1] = CardNumberByte[0];
            heat_suction_sensor_addr[2] = CardNumberByte[1];
            heat_suction_sensor_addr[3] = CardNumberByte[2];
            heat_suction_sensor_addr[4] = 0x08;
            heat_suction_sensor_addr[5] = 0x00;
            heat_suction_sensor_addr[6] = 0x00;
            heat_suction_sensor_addr[7] = CardNumberByte[3];

            digitalWrite(power_sw_pin, HIGH);
            delay(1000);

            hydrogeolog1.read_DS18B20_by_addr(heat_suction_sensor_addr, thermal_suction_digi_pin);
            //hydrogeolog1.search_ds18b20(ds18b20_search_pin,power_sw_pin);
            Serial.println();
            digitalWrite(power_sw_pin, LOW);
            //          thermal_suction_sensor[0]=char(thermal_suction_ds18b20);
            //          thermal_suction_ds18b20.getBytes(thermal_suction_sensor, numbersd) ;

        } // ds18b20 temperature by search.

        /*
         thermal_suction_ds18b20,28E5A34A0800007F,power,4,numbersd,1
         thermal_suction_ds18b20,A3CF969B,digital_input,13,power,42
         thermal_suction_ds18b20,464CBABE,digital_input,13,sensor_power,42,power_heating_pin,35,output_temp_interval,2000,output_number_temp,5
         fredlund_ds18b20,464CBABE,digital_input,13,sensor_power,42,heating_pin,35,interval,2000,output_number,5
         fred,464CBABE,digi_inp,13,senpow,42,heatpow,35,itval,2000,opt_no,5
         fred,DE9F96DC,digi_inp,13,senpow,42,heatpow,35,itval,2000,opt_no,5
28 DE 9F 96 8 0 0 DC
         RESULT FROM 8
         thermal_suction_ds18b20,28E5A34A0800007F,power,4,50,56,69,53,65,51,52,0,40,229,163,74,8,0,0,127
         RESULT FROM 2
         thermal_suction_ds18b20,28E5A34A0800007F,power,4,50,0,5,74,5,0,0,3,40,229,163,74,8,0,0,127
         thermal_suction_ds18b20,28E5A34A,power,4,numbersd,1
         28 A3 CF 96 8 0 0 9B
         
         */
        String fredlund_suction_ds18b20 = hydrogeolog1.parse_argument_string("fred", "", str_ay_size, str_ay);
        power_sw_pin = hydrogeolog1.parse_argument("snpw", -1, str_ay_size, str_ay);
        int digital_input = hydrogeolog1.parse_argument("dgin", -1, str_ay_size, str_ay);
        int power_heating_pin = hydrogeolog1.parse_argument("htpw", -1, str_ay_size, str_ay);
        int output_temp_interval_ms = hydrogeolog1.parse_argument("itv", -1, str_ay_size, str_ay);
        int output_number_temp = hydrogeolog1.parse_argument("otno", -1, str_ay_size, str_ay);

        if ((fredlund_suction_ds18b20 != "") && (power_sw_pin != INVALID))
        {
            //hydrogeolog1.print_string_delimiter_value("input",content);
            hydrogeolog1.print_string_delimiter_value("fred_ds18", String(fredlund_suction_ds18b20));
            if (debug_sw == 1)
            {

                hydrogeolog1.print_string_delimiter_value("sensor_power", String(power_sw_pin));
                hydrogeolog1.print_string_delimiter_value("digital_input", String(digital_input));
                hydrogeolog1.print_string_delimiter_value("power_heating_pin", String(power_heating_pin));
                hydrogeolog1.print_string_delimiter_value("interval_ms", String(output_temp_interval_ms));
                hydrogeolog1.print_string_delimiter_value("output_number", String(output_number_temp));
            }

            //the reason i did not wrap this in hydrogeolog is because function in c normally can not return an array
            byte CardNumberByte[4]; // https://stackoverflow.com/questions/347949/how-to-convert-a-stdstring-to-const-char-or-char
            const char *CardNumber = fredlund_suction_ds18b20.c_str();
            unsigned long number = strtoul(CardNumber, nullptr, 16);
            for (int i = 3; i >= 0; i--) // start with lowest byte of number
            {
                //Serial.println(number,HEX);
                //Serial.println(byte(number));
                //Serial.println(byte(number),HEX);
                CardNumberByte[i] = byte(number);
                number >>= 8; // get next byte into position
            }
            //
            //            for(int i=0; i<4; i++)
            //            {
            //              Serial.print("0x");
            //              Serial.print(CardNumberByte[i], HEX);
            //              Serial.print(delimiter);
            //            }
            byte heat_suction_sensor_addr[8];
            heat_suction_sensor_addr[0] = 0x28;
            heat_suction_sensor_addr[1] = CardNumberByte[0];
            heat_suction_sensor_addr[2] = CardNumberByte[1];
            heat_suction_sensor_addr[3] = CardNumberByte[2];
            heat_suction_sensor_addr[4] = 0x08;
            heat_suction_sensor_addr[5] = 0x00;
            heat_suction_sensor_addr[6] = 0x00;
            heat_suction_sensor_addr[7] = CardNumberByte[3];

            digitalWrite(power_sw_pin, HIGH);
            delay(1000);

            hydrogeolog1.read_DS18B20_by_addr(heat_suction_sensor_addr, digital_input);
            digitalWrite(power_heating_pin, HIGH);
            for (int i = 0; i < output_number_temp; i++)
            {
                delay(output_temp_interval_ms);
                hydrogeolog1.read_DS18B20_by_addr(heat_suction_sensor_addr, digital_input);
            }
            digitalWrite(power_heating_pin, LOW);
            for (int i = 0; i < output_number_temp; i++)
            {
                delay(output_temp_interval_ms);
                hydrogeolog1.read_DS18B20_by_addr(heat_suction_sensor_addr, digital_input);
            }

            //hydrogeolog1.search_ds18b20(ds18b20_search_pin,power_sw_pin);

            Serial.println();
            digitalWrite(power_sw_pin, LOW);
            //          thermal_suction_sensor[0]=char(thermal_suction_ds18b20);
            //          thermal_suction_ds18b20.getBytes(thermal_suction_sensor, numbersd) ;

        } // fred temperature by search.
        String fredlund_suction_ds18b209 = hydrogeolog1.parse_argument_string("fred9", "", str_ay_size, str_ay);
        if ((fredlund_suction_ds18b209 != "") && (power_sw_pin != INVALID))
        {
            hydrogeolog1.print_string_delimiter_value("fred_ds18", String(fredlund_suction_ds18b209));
            if (debug_sw == 1)
            {

                hydrogeolog1.print_string_delimiter_value("sensor_power", String(power_sw_pin));
                hydrogeolog1.print_string_delimiter_value("digital_input", String(digital_input));
                hydrogeolog1.print_string_delimiter_value("power_heating_pin", String(power_heating_pin));
                hydrogeolog1.print_string_delimiter_value("interval_ms", String(output_temp_interval_ms));
                hydrogeolog1.print_string_delimiter_value("output_number", String(output_number_temp));
            }

            //the reason i did not wrap this in hydrogeolog is because function in c normally can not return an array
            byte CardNumberByte[4]; // https://stackoverflow.com/questions/347949/how-to-convert-a-stdstring-to-const-char-or-char
            const char *CardNumber = fredlund_suction_ds18b209.c_str();
            unsigned long number = strtoul(CardNumber, nullptr, 16);
            for (int i = 3; i >= 0; i--) // start with lowest byte of number
            {
                //Serial.println(number,HEX);
                //Serial.println(byte(number));
                //Serial.println(byte(number),HEX);
                CardNumberByte[i] = byte(number);
                number >>= 8; // get next byte into position
            }
            //
            //            for(int i=0; i<4; i++)
            //            {
            //              Serial.print("0x");
            //              Serial.print(CardNumberByte[i], HEX);
            //              Serial.print(delimiter);
            //            }
            byte heat_suction_sensor_addr[8];
            heat_suction_sensor_addr[0] = 0x28;
            heat_suction_sensor_addr[1] = CardNumberByte[0];
            heat_suction_sensor_addr[2] = CardNumberByte[1];
            heat_suction_sensor_addr[3] = CardNumberByte[2];
            heat_suction_sensor_addr[4] = 0x09;
            heat_suction_sensor_addr[5] = 0x00;
            heat_suction_sensor_addr[6] = 0x00;
            heat_suction_sensor_addr[7] = CardNumberByte[3];
            digitalWrite(power_sw_pin, HIGH);
            delay(1000);
            hydrogeolog1.read_DS18B20_by_addr(heat_suction_sensor_addr, digital_input);
            digitalWrite(power_heating_pin, HIGH);
            for (int i = 0; i < output_number_temp; i++)
            {
                delay(output_temp_interval_ms);
                hydrogeolog1.read_DS18B20_by_addr(heat_suction_sensor_addr, digital_input);
            }
            digitalWrite(power_heating_pin, LOW);
            for (int i = 0; i < output_number_temp; i++)
            {
                delay(output_temp_interval_ms);
                hydrogeolog1.read_DS18B20_by_addr(heat_suction_sensor_addr, digital_input);
            }
            Serial.println();
            digitalWrite(power_sw_pin, LOW);
        } // ds18b209
        /*
         use tca9548 i2c multiplexer to obtain results from ms5803 pressure transducer 
         9548,2,type,5803,debug,1
         9548,2,type,sht31,power,34,debug,1
         */
        int tca9548_channel = hydrogeolog1.parse_argument("9548", -1, str_ay_size, str_ay);
        String i2c_type = hydrogeolog1.parse_argument_string("type", "", str_ay_size, str_ay);
        //if ( (ms5803!=-1) && (power_sw_pin!=-1))
        if ((tca9548_channel != INVALID) && (i2c_type != ""))
        {
            int number_of_measurements = hydrogeolog1.parse_argument("points", 3, str_ay_size, str_ay);
            int number_of_dummies = hydrogeolog1.parse_argument("dummies", 3, str_ay_size, str_ay);
            int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", 1000, str_ay_size, str_ay);
            int power_sw_pin = hydrogeolog1.parse_argument("power", -1, str_ay_size, str_ay);
            //int digital_input = hydrogeolog1.parse_argument("dgin", -1, str_ay_size, str_ay);
            if (debug_sw == 1)
            {
                hydrogeolog1.print_string_delimiter_value("9548", String(tca9548_channel));
                hydrogeolog1.print_string_delimiter_value("power", String(power_sw_pin));
                hydrogeolog1.print_string_delimiter_value("points", String(number_of_measurements));
                hydrogeolog1.print_string_delimiter_value("dummies", String(number_of_dummies));
                hydrogeolog1.print_string_delimiter_value("itv", String(measure_time_interval_ms));
                hydrogeolog1.print_string_delimiter_value("type", i2c_type);
            }
            if (power_sw_pin != INVALID)
                digitalWrite(power_sw_pin, HIGH);
            delay(500);
            Wire.begin();
            delay(500);
            hydrogeolog1.tcaselect(tca9548_channel);
            delay(500);
            hydrogeolog1.tcaselect(tca9548_channel);
            delay(500);
            if (i2c_type == "5803")
            {
                hydrogeolog1.ms5803(number_of_dummies, number_of_measurements, measure_time_interval_ms, debug_sw, tca9548_channel);
            } // 5803
            delay(500);
            hydrogeolog1.tcaselect(tca9548_channel);
            delay(500);
            if (i2c_type == "5803")
            {
                hydrogeolog1.ms5803(number_of_dummies, number_of_measurements, measure_time_interval_ms, debug_sw, tca9548_channel);
            } // 5803
            delay(500);
            if (i2c_type == "5803l")
            {
                hydrogeolog1.ms5803l(number_of_dummies, number_of_measurements, measure_time_interval_ms, debug_sw, tca9548_channel);
                delay(500);
                hydrogeolog1.tcaselect(tca9548_channel);
                delay(500);
                hydrogeolog1.ms5803l(number_of_dummies, number_of_measurements, measure_time_interval_ms, debug_sw, tca9548_channel);
            } // 5803
            delay(500);

            delay(500);
            if (i2c_type == "5803l")
            {
            } // 5803
            delay(500);

            //sht31 RH/T sensor
            if (i2c_type == "sht31")
            {
                hydrogeolog1.sht31(number_of_dummies, number_of_measurements, measure_time_interval_ms, debug_sw, tca9548_channel);
            } // sht31
            delay(500);

            if (power_sw_pin != INVALID)
                digitalWrite(power_sw_pin, LOW);
            Serial.println();
        } //tca9548_channel

        /*rcswitch for arlec RC213 sockets 
        rc_sw,5,code,011101101101100000001111100111100,pulse_len,306
        */
        int rc_sw = hydrogeolog1.parse_argument("rc_sw", -1, str_ay_size, str_ay);
        String sw_code = hydrogeolog1.parse_argument_string("code", "", str_ay_size, str_ay);

        if ((rc_sw != INVALID) && (sw_code != ""))
        {
            int pulselength = hydrogeolog1.parse_argument("pulse_len", -1, str_ay_size, str_ay);
            hydrogeolog1.print_string_delimiter_value("code", sw_code);
            hydrogeolog1.print_string_delimiter_value("pulse_len", String(pulselength));
            hydrogeolog1.print_string_delimiter_value("rc_sw", String(rc_sw));
            char binary[1024];
            binary[0] = 0;
            sw_code.toCharArray(binary, sw_code.length());
            hydrogeolog1.rcswitch(rc_sw, pulselength, (const char *)binary);
            Serial.println();
        }

        /*
         use sht75 to measure temperature and humidity
         75,11,clk,12,power,42,debug,1
         */
        int sht75_data = hydrogeolog1.parse_argument("75", -1, str_ay_size, str_ay);
        int sht75_clk = hydrogeolog1.parse_argument("clk", -1, str_ay_size, str_ay);
        power_sw_pin = hydrogeolog1.parse_argument("power", -1, str_ay_size, str_ay);
        if ((sht75_data != INVALID) && (sht75_clk != INVALID))
        {
            int number_of_measurements = hydrogeolog1.parse_argument("points", 3, str_ay_size, str_ay);
            int number_of_dummies = hydrogeolog1.parse_argument("dummies", 3, str_ay_size, str_ay);
            int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", 2000, str_ay_size, str_ay);
            if (debug_sw == 1)
            {
                hydrogeolog1.print_string_delimiter_value("75", String(sht75_data));
                hydrogeolog1.print_string_delimiter_value("clock", String(sht75_clk));
                hydrogeolog1.print_string_delimiter_value("points", String(number_of_measurements));
                hydrogeolog1.print_string_delimiter_value("dummies", String(number_of_dummies));
                hydrogeolog1.print_string_delimiter_value("power", String(power_sw_pin));
                hydrogeolog1.print_string_delimiter_value("itv", String(measure_time_interval_ms));
            }
            if (power_sw_pin != INVALID)
                digitalWrite(power_sw_pin, HIGH);
            delay(1000);
            hydrogeolog1.sht75(sht75_data, sht75_clk, number_of_dummies, number_of_measurements, measure_time_interval_ms, debug_sw);
            if (power_sw_pin != INVALID)
                digitalWrite(power_sw_pin, LOW);
            Serial.println();
        } //sht75

        //TO-DO SDI 12 implementation need to be changed for v2 board
        //also try to remove the dead lock of while (true) if no sensor is found
        //X.lei J.tran
        /*
         int sdi12_data = hydrogeolog1.parse_argument("12",-1,str_ay_size,str_ay);
         if  (sdi12_data!=-1) {
            int measure_time_interval_ms=hydrogeolog1.parse_argument("interval_mm",2000,str_ay_size,str_ay);
            if (debug_sw==1)
            {            
                hydrogeolog1.print_string_delimiter_value("12"  ,String(sdi12_data)  );
                hydrogeolog1.print_string_delimiter_value("power",String(power_sw_pin)  );              
            }
            if (power_sw_pin!=-1) digitalWrite(power_sw_pin,HIGH);
            delay(1000);
            Serial.println("HERE");   
            sdi12_init(sdi12_data);
            delay(2000);
            sdi12_loop(sdi12_data);
            if (power_sw_pin!=-1) digitalWrite(power_sw_pin,LOW);
            Serial.println();
         }  //sht75
        */

        /*
        search channels for 9548 i2c multiplexer
        9548_search
        */
        int search_9548 = hydrogeolog1.parse_argument("9548_search", -1, str_ay_size, str_ay);
        power_sw_pin = hydrogeolog1.parse_argument("power", -1, str_ay_size, str_ay);
        if (search_9548 != INVALID)
        {
            //int number_of_measurements=hydrogeolog1.parse_argument("9548_search",3,stsearch_9548,1,power,2r_ay_size,str_ay);
            hydrogeolog1.print_string_delimiter_value("9548_search", String(search_9548));
            hydrogeolog1.search_9548_channels();
            Serial.println();
        } //9548_search
        if (content == "abc")
        {
            Serial.println(content);
        }
    } //if string is not empty
}
/*===========================================================================*/

/*================================END OF FILE================================*/
