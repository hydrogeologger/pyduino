/*Include libraries ===========================================================*/
/*
in /home/pi/Arduino/libraries
place new libraries in this location and include as
#include <library.h>
*note the <> not ""
*/

#include <SDI12.h>
#include <hydrogeolog.h>
#include <Wire.h>
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
    //Serial1.begin(9600);
    //Serial2.begin(9600);
    //Serial3.begin(9600);
    for (int i = 0; i < DIGITAL_PIN_COUNT; i++)
    {
        pinMode(digi_out_pins[i], OUTPUT);
    }
    isComm = FALSE;
    pinMode(MULTIPLEXER_SW, OUTPUT);
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
    if (analog_in_pin != INVALID)
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
            hydrogeolog1.analog_read(ana_o2_ay[i], number_of_dummies, number_of_measurements, measure_time_interval_ms);
        }
        digitalWrite(power_sw_pin, LOW);
        Serial.println();
    }
}

boolean is_pwm_pin(int pow_sw)
{
    for (int i = 0; i < PWM_PIN_COUNT; i++)
    {
        if (pow_sw == pwm_pins[i])
        {
            return true;
        }
    }
    return false;
}

boolean is_digi_out_pin(int pinName)
{
    for (int i = 0; i < DIGITAL_PIN_COUNT; i++)
    {
        if (pinName == digi_out_pins[i])
        {
            return true;
        }
    }
    return false;
}


/* 
 * Function power_switch
 * Desc     Sets power pin or initiate PWM for compatible pins.
 * 
 * Note     Power_status of 255 will be treated as power_status = 1 for
 *          backwards compatibilityfor backwards compatibility
 * 
 * Input    pow_sw: power switch pin number
 *          pow_sw_status: digital state of power switch pin
 *          pwmValue: PWM value between 0 - 255
 * Output   none
 * 
 * Logic    PWM refers to any pwm value between 0 and 255 non inclusive
 *          power_status | PWM  | pin state
 *          1 or 255     |  0   | HIGH
 *          1 or 255     | 255  | HIGH
 *          0            | 255  | HIGH
 *          0            |  0   | LOW
 *          1 or 255     | PWM  | PWM for PWM pins
 *          0            | PWM  | PWM for PWM pins
 * 
 * Usage    power_switch,46,power_switch_status,1
 *          power_switch,10,pwm_status,50
 * 
 * Prints   Prints "Invalid" to serial if incorrect power pin selected
 *          Will print invalid status if incorrect configuration
 */
void power_switch(int pow_sw, int pow_sw_status, int pwmValue)
{
    if (pow_sw != INVALID)
    {
        if (is_pwm_pin(pow_sw) || is_digi_out_pin(pow_sw)) {      
            // pwm value protection as max is 255 for arduino
            if (pwmValue >= 255) {
                pwmValue = 255;
            }
            
            // For backward compatibility
            if (pow_sw_status == 255 || (pow_sw_status == LOW && pwmValue == 255)) {
                pow_sw_status = HIGH;
            }

            hydrogeolog1.print_string_delimiter_value("power_switch", String(pow_sw));

            if (is_pwm_pin(pow_sw) && pwmValue > 0 && pwmValue < 255) {
                hydrogeolog1.pwm_switch_power(pow_sw, pwmValue);
            } else if ((pwmValue == 0 || pwmValue == 255) && (pow_sw_status == LOW || pow_sw_status == HIGH)) {
                // Treat pin as normal digital pin if pwm is 0 or 255
                hydrogeolog1.print_string_delimiter_value("power_switch_status", String(pow_sw_status));
                hydrogeolog1.switch_power(pow_sw, pow_sw_status);
            } else {
                Serial.print("Invalid status");
            }
            Serial.println();

        } else {
            // if not valid power pin or pwm pin
            Serial.println("Invalid");
        }
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
    //luminox sensor
    //lumino2,M 2,power,42,serial,2
    
    /*if ((lumino2 != "") && (power_sw_pin != INVALID) && (serial_pin >= 1) && (serial_pin <= 3))
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
    } */
}

void ds18b20_search(int ds18b20_search_pin, int power_sw_pin)
{
    /*ds18b20 search
    ds18b20_search,13,power,42
    */
    if ((ds18b20_search_pin != INVALID) && (power_sw_pin != INVALID))
    {
        hydrogeolog1.print_string_delimiter_value("ds18b20_search", String(ds18b20_search_pin));
        digitalWrite(power_sw_pin, HIGH);
        delay(1000);
        hydrogeolog1.search_ds18b20(ds18b20_search_pin, power_sw_pin);
        digitalWrite(power_sw_pin, LOW);
    }
}

void ds18b20_measurement(int str_ay_size, String thermal_suction_ds18b20, int thermal_suction_digi_pin,
                         int power_sw_pin, String str_ay[])
{
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
    if ((thermal_suction_ds18b20 != "") && (power_sw_pin != INVALID))
    {
        hydrogeolog1.print_string_delimiter_value("thermal_suction_ds18b20", String(thermal_suction_ds18b20));
        hydrogeolog1.print_string_delimiter_value("power", String(power_sw_pin));
        byte CardNumberByte[4];
        const char *CardNumber = thermal_suction_ds18b20.c_str();
        unsigned long number = strtoul(CardNumber, nullptr, 16);

        for (int i = 3; i >= 0; i--)
        {
            CardNumberByte[i] = byte(number);
            number = number >> 8;
        }
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
        heat_suction_sensor_addr[4] = 0x0A;
        heat_suction_sensor_addr[5] = 0x00;
        heat_suction_sensor_addr[6] = 0x00;
        heat_suction_sensor_addr[7] = CardNumberByte[3];
        digitalWrite(power_sw_pin, HIGH);
        delay(1000);
        hydrogeolog1.read_DS18B20_by_addr(heat_suction_sensor_addr, thermal_suction_digi_pin);
        Serial.println();
        digitalWrite(power_sw_pin, LOW);
    }
}

void fredlund_measurement(int str_ay_size, int debug_sw, int digital_input,
                          int power_heating_pin, int output_temp_interval_ms, int output_number_temp,
                          int power_sw_pin, String str_ay[])
{
    /*
    fred,464CBABE,digi_inp,13,senpow,42,heatpow,35,itval,2000,opt_no,5
    fred,DE9F96DC,digi_inp,13,senpow,42,heatpow,35,itval,2000,opt_no,5
    */

    String fredlund_suction_ds18b20 = hydrogeolog1.parse_argument_string("fred", "", str_ay_size, str_ay);
    fredlund_suction_ds18b20 = fredlund_suction_ds18b20 == "" ? hydrogeolog1.parse_argument_string("fred9", "", str_ay_size, str_ay) : fredlund_suction_ds18b20;
    if ((fredlund_suction_ds18b20 != "") && (power_sw_pin != INVALID))
    {
        hydrogeolog1.print_string_delimiter_value("fred_ds18", String(fredlund_suction_ds18b20));
        if (debug_sw == 1)
        {
            hydrogeolog1.print_string_delimiter_value("sensor_power", String(power_sw_pin));              // "snpw"
            hydrogeolog1.print_string_delimiter_value("digital_input", String(digital_input));            // "dgin"
            hydrogeolog1.print_string_delimiter_value("power_heating_pin", String(power_heating_pin));    // "htpw"
            hydrogeolog1.print_string_delimiter_value("interval_ms", String(output_temp_interval_ms));    // "itv"
            hydrogeolog1.print_string_delimiter_value("output_number", String(output_number_temp));       // "otno"
        }
       if (fredlund_suction_ds18b20.length() != 16) 
           {
           Serial.println("Input length of sensor address is not 16");
           }
       else
           {
           byte heat_suction_sensor_addr[8];
           for(int i=0; i<8; i++)
               {
               String fredlund_suction_ds18b20_section1=fredlund_suction_ds18b20.substring(i*2,(i+1)*2);
               const char * CardNumber = fredlund_suction_ds18b20_section1.c_str();
               unsigned long number = strtoul( CardNumber, nullptr, 16);
               byte CardNumberByte = byte( number);
               heat_suction_sensor_addr[i]=CardNumberByte;
               Serial.print(CardNumberByte,HEX);
               }
            Serial.print(DELIMITER);

            digitalWrite(power_sw_pin,HIGH);
            delay(1000);
            hydrogeolog1.read_DS18B20_by_addr(heat_suction_sensor_addr,digital_input) ;
            digitalWrite(power_heating_pin,HIGH);
            for(int i=0;i<output_number_temp;i++)
            {
                delay(output_temp_interval_ms);
                hydrogeolog1.read_DS18B20_by_addr(heat_suction_sensor_addr,digital_input) ;
            }
            digitalWrite(power_heating_pin,LOW);
            for(int i=0;i<output_number_temp;i++)
            {
                delay(output_temp_interval_ms);
                hydrogeolog1.read_DS18B20_by_addr(heat_suction_sensor_addr,digital_input) ;
            }
            Serial.println();
            digitalWrite(power_sw_pin,LOW); 
               
            }  //fredlund_suction_ds18b20.length else 
    }  //((fredlund_suction_ds18b20 != "") && (power_sw_pin != INVALID))
} // fredlund_measurement

String get_cmd()
{
    String content = "";
    char character;
    while (Serial.available())
    {
        character = Serial.read();
        content.concat(character);
        delay(10);
    }
    return content;
}

void read_i2c_sensor(String type, int number_of_dummies, int number_of_measurements, int measure_time_interval_ms,
                          int debug_sw, int tca9548_channel)
{
    if (type == "5803")
    {
        hydrogeolog1.ms5803(number_of_dummies, number_of_measurements, measure_time_interval_ms, debug_sw, tca9548_channel);
    }
    else if (type == "5803l")
    {
        hydrogeolog1.ms5803l(number_of_dummies, number_of_measurements, measure_time_interval_ms, debug_sw, tca9548_channel);
    }
    else if (type == "sht31")
    {
        hydrogeolog1.sht31(number_of_dummies, number_of_measurements, measure_time_interval_ms, debug_sw, tca9548_channel);
    }
    else if (type == "si1145")
    {
        hydrogeolog1.si1145(number_of_dummies, number_of_measurements, measure_time_interval_ms, debug_sw, tca9548_channel);
    } else {
        Serial.print("INVALID_TYPE");
    }
}



/* 
 * Function MultiplexerReset
 * Desc     Resets 9548 i2c multiplexer by disable twi and toggle multiplexer power
 * 
 * Input    Time interval for power off in milliseconds
 * Output   none
 * 
 * Usage    9548_reset
 *          9548_reset,400
 * 
 * Prints   Time duration for power off in milliseconds
 */
void multiplexer_i2c_reset(int delayMillisValue) {
    if (delayMillisValue > INVALID) {
        // Require a minimum of 400ms delay to hold MULTIPLEXER_SW
        if (delayMillisValue < 400) {
            delayMillisValue = 400;
        }

        // provide serial feedback of power toggle duration
        hydrogeolog1.print_string_delimiter_value("9548_reset", String(delayMillisValue));
        Serial.println();

        // Disable Atmel 2-wire interface, to enable direct control of SDA & SCL pins
        // TWCR &= ~(_BV(TWEN));
        // disable twi module, acks, and twi interrupt
        TWCR &= ~(_BV(TWEN) | _BV(TWIE) | _BV(TWEA));

        // deactivate internal pullups for twi.
        digitalWrite(SDA, 0);
        digitalWrite(SCL, 0);

        // Force SDA & SCL line to low
        pinMode(SDA, OUTPUT);
        pinMode(SCL, OUTPUT);
        digitalWrite(SDA, 0);
        digitalWrite(SCL, 0);

        digitalWrite(MULTIPLEXER_SW, HIGH); // Power down
        delay(delayMillisValue);    // Power down time

        // Return pins to INPUT
        pinMode(SDA, INPUT);
        pinMode(SCL, INPUT);
        digitalWrite(MULTIPLEXER_SW, LOW); // Power up

        // Reinitialize Atmel 2-Wire interface
        Wire.begin();
    }
}

void multiplexer_search(int search_9548)
{
    /*
    search channels for 9548 i2c multiplexer
    9548_search
    */
    if (search_9548 != INVALID)
    {
        hydrogeolog1.print_string_delimiter_value("9548_search", String(search_9548));
        hydrogeolog1.search_9548_channels();
        Serial.println();
    }
}

void multiplexer_read(int str_ay_size, int debug_sw, String i2c_type, int tca9548_channel,
                      int power_sw_pin, String str_ay[])
{
    /*
    use tca9548 i2c multiplexer to obtain results from ms5803 pressure transducer 
    9548,2,type,5803,debug,1
    9548,2,type,sht31,power,34,debug,1
    */
    if ((tca9548_channel != INVALID) && (i2c_type != ""))
    {
        // Initialize TWI if has been disabled
        if ((TWCR & _BV(TWEN)) == 0) {
            Wire.begin();
        }

        int number_of_measurements = hydrogeolog1.parse_argument("points", 3, str_ay_size, str_ay);
        int number_of_dummies = hydrogeolog1.parse_argument("dummies", 3, str_ay_size, str_ay);
        int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", 1000, str_ay_size, str_ay);
        int power_sw_pin = hydrogeolog1.parse_argument("power", INVALID, str_ay_size, str_ay);

        if (debug_sw == 1)
        {
            hydrogeolog1.print_string_delimiter_value("9548", String(tca9548_channel));
            print_debug(debug_sw, power_sw_pin, number_of_measurements, number_of_dummies, measure_time_interval_ms);
            hydrogeolog1.print_string_delimiter_value("type", i2c_type);
        }

        // Turn on power switch
        if (power_sw_pin != INVALID) {
            digitalWrite(power_sw_pin, HIGH);
        }

        // Select multiplexer channel and read from sensor
        hydrogeolog1.tcaselect(tca9548_channel);
        delay(500);
        read_i2c_sensor(i2c_type, number_of_dummies, number_of_measurements, measure_time_interval_ms, debug_sw, tca9548_channel);
        delay(500);

        // Turn power switch off
        if (power_sw_pin != INVALID) {
            digitalWrite(power_sw_pin, LOW);
        }

        Serial.println();   // Terminate serial message with new line
    }
}


void rc_swtich(int str_ay_size, int debug_sw, String sw_code, int rc_sw, String str_ay[])
{
    /*rcswitch for arlec RC213 sockets 
    rc_sw,5,code,011101101101100000001111100111100,pulse_len,306
    */
    if ((rc_sw != INVALID) && (sw_code != ""))
    {
        int pulselength = hydrogeolog1.parse_argument("pulse_len", INVALID, str_ay_size, str_ay);
        hydrogeolog1.print_string_delimiter_value("code", sw_code);
        hydrogeolog1.print_string_delimiter_value("pulse_len", String(pulselength));
        hydrogeolog1.print_string_delimiter_value("rc_sw", String(rc_sw));
        char binary[1024];
        binary[0] = 0;
        sw_code.toCharArray(binary, sw_code.length());
        hydrogeolog1.rcswitch(rc_sw, pulselength, (const char *)binary);
        Serial.println();
    }
}

void sht75_measurement(int str_ay_size, int debug_sw, int sht75_data, int sht75_clk, int power_sw_pin,
                       String str_ay[])
{
    /*
    use sht75 to measure temperature and humidity
    75,11,clk,12,power,42,debug,1
    */
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
    }
}


void SDI12_sensor(int str_ay_size, int debug_sw, int power_sw_pin, String str_ay[])
{
    int sdi12_data = hydrogeolog1.parse_argument("SDI-12", -1, str_ay_size, str_ay);
    if (sdi12_data != -1)
    {
        String default_cmd = hydrogeolog1.parse_argument_string("default_cmd", "", str_ay_size, str_ay);
        int start_index_custom_cmd = hydrogeolog1.strcmpi("custom_cmd", str_ay_size, str_ay);
        // String custom_cmd = hydrogeolog1.parse_argument_string("custom_cmd", "", str_ay_size, str_ay);
        String new_addr = "";
        String custom_cmd = "";
        int power_off = hydrogeolog1.parse_argument("power_off", 1, str_ay_size, str_ay);

        if (default_cmd == "change") {
            new_addr = hydrogeolog1.parse_argument_string("change", "", str_ay_size, str_ay);
        } else if (start_index_custom_cmd > -1) {
            for (int i = start_index_custom_cmd + 1; i < str_ay_size; i++) {
                custom_cmd.concat(str_ay[i]);
                if (str_ay[i].lastIndexOf("!") > -1) {
                    break;
                }
                custom_cmd.concat(DELIMITER);
            }
        }

        if (debug_sw == 1) {
            hydrogeolog1.print_string_delimiter_value("SDI-12", String(sdi12_data));
            if (default_cmd != "") {
                hydrogeolog1.print_string_delimiter_value("default_cmd", default_cmd);
                if (default_cmd == "change") {
                    Serial.print(new_addr);
                    Serial.print(DELIMITER);
                }
            } else if (custom_cmd != "") {
                hydrogeolog1.print_string_delimiter_value("custom_cmd", "\"" + custom_cmd + "\"");
            }
            hydrogeolog1.print_string_delimiter_value("power", String(power_sw_pin));
            hydrogeolog1.print_string_delimiter_value("power_off", String(power_off));
        }

        if (power_sw_pin != -1) {
            digitalWrite(power_sw_pin, HIGH);
        }

        int num_sensors = 0;
        if (sdi12_init(sdi12_data, &num_sensors) == false) {
            Serial.println("No SDI12 found!");
            digitalWrite(power_sw_pin, LOW);
            return;
        }

        if (default_cmd != "" && custom_cmd == "") {
            //Serial.println("HERE");
            process_command(default_cmd, num_sensors, new_addr, false);
        } else if (default_cmd == "" && custom_cmd != "") {
            int str_idx = hydrogeolog1.strcmpi("custom_cmd", str_ay_size, str_ay);

            process_command(custom_cmd, num_sensors, new_addr, true);
        }
        
        if (power_off) {
            digitalWrite(power_sw_pin, LOW);
        }

        Serial.println();
    }//sdi12
}

void check_serial(String content)
    /*
     if input abc in serial, arduino will return abc
    */
  
{
    if (content == "abc")
    {
        Serial.println(content);
    }
    //Serial.print("CMD: "); Serial.println(content);
}

// the loop routine runs over and over again forever:
void loop()
{
    timeout_reset_pi();
    String content = get_cmd();
    if (content == "")
        timing_no_comm();
    else // there is input from serial
    {
        command_reset_pi(content);
        command_check_millis(content);
        check_serial(content);
        reset_timer();
        String str_ay[20];
        int str_ay_size = hydrogeolog1.split_strings(content, str_ay);
        int debug_sw = hydrogeolog1.parse_argument("debug", 0, str_ay_size, str_ay);
        int power_sw_pin = hydrogeolog1.parse_argument("power", INVALID, str_ay_size, str_ay);

        analog_reading(str_ay_size, debug_sw,
                       hydrogeolog1.parse_argument("analog", INVALID, str_ay_size, str_ay),
                       power_sw_pin, str_ay);

        array_analog_reading(str_ay_size, debug_sw,
                             hydrogeolog1.parse_argument("anaay", INVALID, str_ay_size, str_ay),
                             power_sw_pin, str_ay);

        o2_array_analog_reading(str_ay_size, debug_sw,
                                hydrogeolog1.parse_argument("o2_ana_ay", INVALID, str_ay_size, str_ay),
                                power_sw_pin, str_ay);

        power_switch(hydrogeolog1.parse_argument("power_switch", INVALID, str_ay_size, str_ay),
                     hydrogeolog1.parse_argument("power_switch_status", 0, str_ay_size, str_ay),
                     hydrogeolog1.parse_argument("pwm_status", 0, str_ay_size, str_ay));

        dht22_measurement(str_ay_size, debug_sw,
                          hydrogeolog1.parse_argument("dht22", INVALID, str_ay_size, str_ay),
                          power_sw_pin, str_ay);

        dhto2_measurement(str_ay_size, debug_sw,
                          hydrogeolog1.parse_argument("dhto2", INVALID, str_ay_size, str_ay),
                          hydrogeolog1.parse_argument("anain", INVALID, str_ay_size, str_ay),
                          power_sw_pin, str_ay);

        luminox_reading(str_ay_size,
                        hydrogeolog1.parse_argument_string("lumino2", "", str_ay_size, str_ay),
                        hydrogeolog1.parse_argument("serial", INVALID, str_ay_size, str_ay),
                        power_sw_pin, str_ay);

        ds18b20_search(hydrogeolog1.parse_argument("ds18b20_search", INVALID, str_ay_size, str_ay),
                       power_sw_pin);

        ds18b20_measurement(str_ay_size,
                            hydrogeolog1.parse_argument_string("thermal_suction_ds18b20", "", str_ay_size, str_ay),
                            hydrogeolog1.parse_argument("digital_input", INVALID, str_ay_size, str_ay),
                            power_sw_pin, str_ay);

        fredlund_measurement(str_ay_size, debug_sw,
                             hydrogeolog1.parse_argument("dgin", INVALID, str_ay_size, str_ay),
                             hydrogeolog1.parse_argument("htpw", INVALID, str_ay_size, str_ay),
                             hydrogeolog1.parse_argument("itv" , INVALID, str_ay_size, str_ay),
                             hydrogeolog1.parse_argument("otno", INVALID, str_ay_size, str_ay),
                             hydrogeolog1.parse_argument("snpw", INVALID, str_ay_size, str_ay),
                             str_ay);

        multiplexer_i2c_reset(hydrogeolog1.parse_argument("9548_reset", INVALID, str_ay_size, str_ay));

        multiplexer_search(hydrogeolog1.parse_argument("9548_search", INVALID, str_ay_size, str_ay));

        multiplexer_read(str_ay_size, debug_sw,
                         hydrogeolog1.parse_argument_string("type", "", str_ay_size, str_ay),
                         hydrogeolog1.parse_argument("9548", INVALID, str_ay_size, str_ay),
                         power_sw_pin, str_ay);

        rc_swtich(str_ay_size, debug_sw,
                  hydrogeolog1.parse_argument_string("code", "", str_ay_size, str_ay),
                  hydrogeolog1.parse_argument("rc_sw", INVALID, str_ay_size, str_ay),
                  str_ay);

        sht75_measurement(str_ay_size, debug_sw,
                          hydrogeolog1.parse_argument("75", INVALID, str_ay_size, str_ay),
                          hydrogeolog1.parse_argument("clk", INVALID, str_ay_size, str_ay),
                          power_sw_pin, str_ay);
        SDI12_sensor(str_ay_size, debug_sw, power_sw_pin, str_ay);
    }//communication
} //loop
/*===========================================================================*/

/*================================END OF FILE================================*/
