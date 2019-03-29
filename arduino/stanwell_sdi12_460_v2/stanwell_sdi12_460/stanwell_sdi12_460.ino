/*Include libraries ===========================================================*/
/*
in /home/pi/Arduino/libraries
place new libraries in this location and include as
#include <library.h>
*note the <> not ""
*/
#include <SDI12.h>
#include <hydrogeolog.h>
/*===========================================================================*/

/*Global variables and defines ==============================================*/
extern volatile unsigned long timer0_millis;
#define TRUE 1
#define FALSE 0
#define TIMEOUT (unsigned long)(5ul * 60ul * 60ul * 1000ul)
#define DOWN_TIME 3 * 1000 //seconds
/*
keeps track of active addresses
each bit represents an address:
1 is active (taken), 0 is inactive (available)
setTaken('A') will set the proper bit for sensor 'A'
set
*/
byte addressRegister[8] = {
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000};

/*
v 2.0 PCB global pins variables
*/
static const int digi_dht_ay[] = {50, 51, 52, 53, 14, 15};
static const uint8_t ana_o2_ay[] = {A0, A1, A2, A3, A5, A6};
#define DIGITAL_DHT_COUNT = 6;
static const uint8_t ana_moisture_ay[] = {A7, A8, A9, A10, A11, A12};
#define ANALOG_MOIS_COUNT 6
static const uint8_t analog_pins[] = {A0, A1, A2, A3, A4,
                                      A5, A6, A7, A8, A9,
                                      A10, A11, A12, A13, A14,
                                      A15};
#define ANALOG_PIN_COUNT 16;
#define MULTIPLEXER_SW 7
#define PI_SW 6
#define HUMIDITY_SEN_SW 2
#define REVERSE_SW_1 10
#define REVERSE_SW_2 11
#define REVERSE_SW_3 12
#define REVERSE_SW_4 13
#define _12V5V_SW_1 8
#define _12V5V_SW_2 9
static int digi_out_pins[] = {
    22, 23, 24, 25, 26, 27, 28,
    29, 30, 31, 32, 33, 34, 35,
    36, 37, 38, 39, 40, 41, 42,
    43, 44, 45, 46, 47, 48, 49,
    MULTIPLEXER_SW, PI_SW, HUMIDITY_SEN_SW,
    REVERSE_SW_1, REVERSE_SW_2, REVERSE_SW_3, REVERSE_SW_4,
    _12V5V_SW_1, _12V5V_SW_2};
#define DIGITAL_PIN_COUNT 37

#define DELIMITER ','
hydrogeolog hydrogeolog1(DELIMITER);
String str_ay[20];
/*===========================================================================*/

/*Function prototypes========================================================*/

void sdi12_loop(int sdi12_data);
void takeMeasurement_sdi12(char i, int sdi12_data);
void printBufferToScreen(int sdi12_data);
boolean checkActive(char i, int sdi12_data);
boolean setTaken(byte i);
boolean setVacant(byte i);
boolean isTaken(byte i);
void printInfo(char i, int sdi12_data);
byte charToDec(char i);
char decToChar(byte i);
/*===========================================================================*/

/*Function definition========================================================*/
/*
set the new value for millis()
*/
void setMillis(unsigned long new_millis)
{
    uint8_t oldSREG = SREG;
    cli();
    timer0_millis = new_millis;
    SREG = oldSREG;
    sei();
}


/*
looping to read SDI-12 sensor
*/
void sdi12_loop(int sdi12_data)
{
    // scan address space 0-9
    for (char i = '0'; i <= '9'; i++)
        if (isTaken(i))
        {
            printInfo(i, sdi12_data);
            takeMeasurement_sdi12(i, sdi12_data);
        }
    delay(10000); // wait ten seconds between measurement attempts.
}

void takeMeasurement_sdi12(char i, int sdi12_data)
{
#define DATAPIN sdi12_data // change to the proper pin,pwm pins are needed, see tutorial, only limited pins are able to get this
    SDI12 mySDI12(DATAPIN);
    String command = "";
    command += i;
    command += "M!"; // SDI-12 measurement command format  [address]['M'][!]
    mySDI12.sendCommand(command);
    while (!mySDI12.available() > 5); 
    // wait for acknowlegement with format [address][ttt (3 char, seconds)][number of measurments available, 0-9]
    delay(100);

    mySDI12.read(); //consume address

    // find out how long we have to wait (in seconds).
    unsigned long wait = 0;
    wait += 100 * mySDI12.read() - '0';
    wait += 10 * mySDI12.read() - '0';
    wait += 1 * mySDI12.read() - '0';

    mySDI12.read(); // ignore # measurements, for this simple examlpe
    mySDI12.read(); // ignore carriage return
    mySDI12.read(); // ignore line feed
    setMillis(0);
    unsigned long timerStart = millis();
    while ((millis() - timerStart) > (1000 * wait))
    {
        if (mySDI12.available())
            break; //sensor can interrupt us to let us know it is done early
    }

    // in this example we will only take the 'DO' measurement
    mySDI12.flush();
    command = "";
    command += i;
    command += "D0!"; // SDI-12 command to get data [address][D][dataOption][!]
    mySDI12.sendCommand(command);
    while (!mySDI12.available() > 1)
        ;       // wait for acknowlegement
    delay(300); // let the data transfer
    printBufferToScreen(sdi12_data);
    mySDI12.flush();
}

void printBufferToScreen(int sdi12_data)
{
#define DATAPIN sdi12_data // change to the proper pin,pwm pins are needed, see tutorial, only limited pins are able to get this
    SDI12 mySDI12(DATAPIN);
    String buffer = "";
    mySDI12.read(); // consume address
    while (mySDI12.available())
    {
        char c = mySDI12.read();
        if (c == '+' || c == '-')
        {
            buffer += DELIMITER; // the comma in between the results
            if (c == '-')
                buffer += '-';
        }
        else
        {
            buffer += c;
        }
        delay(100);
    }
    buffer.replace("\n", ""); // to remove the cartriage from the buffer
    buffer.replace("\r", ""); // added to make sure all cartriage is removed
    //Serial.print(delimiter);
    Serial.print(buffer);
    //Serial.print(delimiter);
}

// this checks for activity at a particular address
// expects a char, '0'-'9', 'a'-'z', or 'A'-'Z'
boolean checkActive(char i, int sdi12_data)
{
#define DATAPIN sdi12_data // change to the proper pin,pwm pins are needed, see tutorial, only limited pins are able to get this
    SDI12 mySDI12(DATAPIN);

    String myCommand = "";
    myCommand = "";
    myCommand += (char)i; // sends basic 'acknowledge' command [address][!]
    myCommand += "!";

    for (int j = 0; j < 3; j++)
    { // goes through three rapid contact attempts
        mySDI12.sendCommand(myCommand);
        if (mySDI12.available() > 1)
            break;
        delay(30);
    }
    if (mySDI12.available() > 2)
    { // if it hears anything it assumes the address is occupied
        mySDI12.flush();
        return true;
    }
    else
    { // otherwise it is vacant.
        mySDI12.flush();
    }
    return false;
}

// this sets the bit in the proper location within the addressRegister
// to record that the sensor is active and the address is taken.
boolean setTaken(byte i)
{
    boolean initStatus = isTaken(i);
    i = charToDec(i); // e.g. convert '0' to 0, 'a' to 10, 'Z' to 61.
    byte j = i / 8;   // byte #
    byte k = i % 8;   // bit #
    addressRegister[j] |= (1 << k);
    return !initStatus; // return false if already taken
}

// THIS METHOD IS UNUSED IN THIS EXAMPLE, BUT IT MAY BE HELPFUL.
// this unsets the bit in the proper location within the addressRegister
// to record that the sensor is active and the address is taken.
boolean setVacant(byte i)
{
    boolean initStatus = isTaken(i);
    i = charToDec(i); // e.g. convert '0' to 0, 'a' to 10, 'Z' to 61.
    byte j = i / 8;   // byte #
    byte k = i % 8;   // bit #
    addressRegister[j] &= ~(1 << k);
    return initStatus; // return false if already vacant
}

// this quickly checks if the address has already been taken by an active sensor
boolean isTaken(byte i)
{
    i = charToDec(i);                     // e.g. convert '0' to 0, 'a' to 10, 'Z' to 61.
    byte j = i / 8;                       // byte #
    byte k = i % 8;                       // bit #
    return addressRegister[j] & (1 << k); // return bit status
}

// gets identification information from a sensor, and prints it to the serial port
// expects a character between '0'-'9', 'a'-'z', or 'A'-'Z'.
void printInfo(char i, int sdi12_data)
{
// change to the proper pin,pwm pins are needed, see tutorial, only limited pins are able to get this
#define DATAPIN sdi12_data
    SDI12 mySDI12(DATAPIN);
    int j;
    int ii;
    String command = "";
    command += (char)i;
    command += "I!";
    for (j = 0; j < 1; j++)
    {
        mySDI12.sendCommand(command);
        delay(30);
        if (mySDI12.available() > 1)
        {
            Serial.write("SuTp");
            Serial.print(DELIMITER);
            break;
        }
        if (mySDI12.available())
            mySDI12.read();
    }
    while (mySDI12.available())
    {
        char c = mySDI12.read();
        if ((c != '\n') && (c != '\r'))
        {
            Serial.write(c); //print sensor info and type
        }
        delay(5);
    }
    Serial.print(DELIMITER);
}

// converts allowable address characters '0'-'9', 'a'-'z', 'A'-'Z',
// to a decimal number between 0 and 61 (inclusive) to cover the 62 possible addresses
byte charToDec(char i)
{
    if ((i >= '0') && (i <= '9'))
        return i - '0';
    if ((i >= 'a') && (i <= 'z'))
        return i - 'a' + 10;
    if ((i >= 'A') && (i <= 'Z'))
        return i - 'A' + 37;
    return 0;
}

// THIS METHOD IS UNUSED IN THIS EXAMPLE, BUT IT MAY BE HELPFUL.
// maps a decimal number between 0 and 61 (inclusive) to
// allowable address characters '0'-'9', 'a'-'z', 'A'-'Z',
char decToChar(byte i)
{
    if ((i >= 0) && (i <= 9))
        return i + '0';
    if ((i >= 10) && (i <= 36))
        return i + 'a' - 10;
    if ((i >= 37) && (i <= 62))
        return i + 'A' - 37;
    return 0;
}

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
}

unsigned char noComm = FALSE;
// the loop routine runs over and over again forever:
void loop()
{
    if (millis() > TIMEOUT)
    {
        /*reset*/
        setMillis(0);
        noComm = FALSE;
        //digitalWrite(13, HIGH);
        digitalWrite(PI_SW, HIGH);
        delay(DOWN_TIME);
        //digitalWrite(13, LOW);
        digitalWrite(PI_SW, LOW);
    }
    String content = "";
    char character;
    while (Serial.available())
    {
        character = Serial.read();
        content.concat(character);
        delay(10);
    }
    if (content == "RESET\n")
    {
        Serial.println("Reboot in 30 s....");
        delay(20000);
        setMillis(0);
        noComm = FALSE;
        digitalWrite(13, HIGH);
        digitalWrite(PI_SW, HIGH);
        delay(DOWN_TIME);
        digitalWrite(13, LOW);
        digitalWrite(PI_SW, LOW);
    }
    if (content == "")
    {
        /*No communication reset millis*/
        if (noComm == FALSE)
        {
            setMillis(0);
            noComm = TRUE;
        }
    }
    else
    {
        setMillis(0);
        noComm = FALSE;
        //Serial.println(content);
        int str_ay_size = hydrogeolog1.split_strings(content, str_ay);
        //Serial.println(str_ay_size);
        //Serial.print(delimiter);
        //hydrogeolog1.print_str_ay(str_ay_size,str_ay);
        // assign power pins
        //power,43,analog,15,point,3,interval_mm,200,debug,1 checking voltage
        //
        int debug_sw = hydrogeolog1.parse_argument("debug", 0, str_ay_size, str_ay);
        int analog_in_pin = hydrogeolog1.parse_argument("analog", -1, str_ay_size, str_ay);
        int power_sw_pin = hydrogeolog1.parse_argument("power", -1, str_ay_size, str_ay);

        //analog reading
        if ((analog_in_pin != -1) && (power_sw_pin != -1)) //&&(number_of_measurements!=-1) && (number_of_dummies!=-1)
        {
            int number_of_measurements = hydrogeolog1.parse_argument("points", 5, str_ay_size, str_ay);
            int number_of_dummies = hydrogeolog1.parse_argument("dummies", 3, str_ay_size, str_ay);
            int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", 10, str_ay_size, str_ay);
            hydrogeolog1.print_string_delimiter_value("analog", String(analog_in_pin));
            if (debug_sw == 1)
            {
                hydrogeolog1.print_string_delimiter_value("power", String(power_sw_pin));
                hydrogeolog1.print_string_delimiter_value("points", String(number_of_measurements));
                hydrogeolog1.print_string_delimiter_value("dummies", String(number_of_dummies));
                hydrogeolog1.print_string_delimiter_value("interval_mm", String(measure_time_interval_ms));
            }
            hydrogeolog1.analog_excite_read(power_sw_pin, analog_in_pin, number_of_dummies, number_of_measurements, measure_time_interval_ms);
            Serial.println();
        } // analog read

        int analog_array = hydrogeolog1.parse_argument("anaay", -1, str_ay_size, str_ay);
        /**analog reading in an array
         anaay,1,power,48,point,3,interval_mm,200,debug,1
        **/
        if ((analog_array != -1) && (power_sw_pin != -1)) //
        {
            int number_of_measurements = hydrogeolog1.parse_argument("points", 5, str_ay_size, str_ay);
            int number_of_dummies = hydrogeolog1.parse_argument("dummies", 3, str_ay_size, str_ay);
            int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", 10, str_ay_size, str_ay);
            hydrogeolog1.print_string_delimiter_value("analog_array", String(analog_array));

            if (debug_sw == 1)
            {
                hydrogeolog1.print_string_delimiter_value("power", String(power_sw_pin));
                hydrogeolog1.print_string_delimiter_value("points", String(number_of_measurements));
                hydrogeolog1.print_string_delimiter_value("dummies", String(number_of_dummies));
                hydrogeolog1.print_string_delimiter_value("interval_mm", String(measure_time_interval_ms));
            }
            //Serial.print(no_ana_moisture_ay);
            //Serial.println();
            digitalWrite(power_sw_pin, HIGH);
            delay(1000);
            for (int i = 0; i < ANALOG_MOIS_COUNT; i++)
            {
                hydrogeolog1.analog_read(ana_moisture_ay[i], number_of_dummies, number_of_measurements, measure_time_interval_ms);
            }
            digitalWrite(power_sw_pin, LOW);
            Serial.println();
        } // analog read

        int o2_ana_array = hydrogeolog1.parse_argument("o2_ana_ay", -1, str_ay_size, str_ay);
        /**analog reading in an array
         o2_ana_ay,1,power,43,point,3,interval_mm,200,debug,1
         o2_ana_ay,1,power,48,point,3,interval_mm,200,debug,1
        **/
        if ((o2_ana_array != -1) && (power_sw_pin != -1)) //
        {
            int number_of_measurements = hydrogeolog1.parse_argument("points", 5, str_ay_size, str_ay);
            int number_of_dummies = hydrogeolog1.parse_argument("dummies", 3, str_ay_size, str_ay);
            int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", 10, str_ay_size, str_ay);
            hydrogeolog1.print_string_delimiter_value("o2_ana_ay", String(o2_ana_array));

            if (debug_sw == 1)
            {
                hydrogeolog1.print_string_delimiter_value("power", String(power_sw_pin));
                hydrogeolog1.print_string_delimiter_value("points", String(number_of_measurements));
                hydrogeolog1.print_string_delimiter_value("dummies", String(number_of_dummies));
                hydrogeolog1.print_string_delimiter_value("interval_mm", String(measure_time_interval_ms));
            }
            //Serial.print(no_digi_dht);
            //Serial.println();

            digitalWrite(power_sw_pin, HIGH);
            delay(1000);
            for (int i = 0; i < ANALOG_MOIS_COUNT; i++)
            {
                hydrogeolog1.dht22_read(digi_dht_ay[i], number_of_dummies, number_of_measurements, measure_time_interval_ms);
                hydrogeolog1.analog_read(ana_o2_ay[i], number_of_dummies, number_of_measurements, measure_time_interval_ms);
            }
            digitalWrite(power_sw_pin, LOW);
            Serial.println();
        } // analog read

        // assign powerswitch
        // power_switch,46,power_switch_status,1   //switch for raspberry pi

        int pow_sw = hydrogeolog1.parse_argument("power_switch", -1, str_ay_size, str_ay);
        int pow_sw_status = hydrogeolog1.parse_argument("power_switch_status", 0, str_ay_size, str_ay);
        if ((pow_sw != -1))
        {
            hydrogeolog1.print_string_delimiter_value("power_switch", String(pow_sw));
            hydrogeolog1.print_string_delimiter_value("power_switch_status", String(pow_sw_status));
            hydrogeolog1.switch_power(pow_sw, pow_sw_status);
            Serial.println();
        } //power switch

        int dht22_in_pin = hydrogeolog1.parse_argument("dht22", -1, str_ay_size, str_ay);
        power_sw_pin = hydrogeolog1.parse_argument("power", -1, str_ay_size, str_ay);

        /*dht22 measurement
       dht22,10,power,48,points,2,dummies,1,interval_mm,200,debug,1
       a 10 k resistor is required to put between digi 10 and ground
       */
        if ((dht22_in_pin != -1) && (power_sw_pin != -1)) //&&(number_of_measurements!=-1) && (number_of_dummies!=-1)
        {
            int number_of_measurements = hydrogeolog1.parse_argument("points", 1, str_ay_size, str_ay);
            int number_of_dummies = hydrogeolog1.parse_argument("dummies", 0, str_ay_size, str_ay);
            int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", 1000, str_ay_size, str_ay);
            if (measure_time_interval_ms < 1000)
            {
                measure_time_interval_ms = 1000;
            }
            // needs to be at leaset 1000 ms
            hydrogeolog1.print_string_delimiter_value("dht22", String(dht22_in_pin));
            if (debug_sw == 1)
            {
                hydrogeolog1.print_string_delimiter_value("power", String(power_sw_pin));
                hydrogeolog1.print_string_delimiter_value("points", String(number_of_measurements));
                hydrogeolog1.print_string_delimiter_value("dummies", String(number_of_dummies));
                hydrogeolog1.print_string_delimiter_value("interval_mm", String(measure_time_interval_ms));
            }
            hydrogeolog1.dht22_excite_read(power_sw_pin, dht22_in_pin, number_of_dummies, number_of_measurements, measure_time_interval_ms);
            Serial.println();
        } // dht22 read

        int dhto2_in_pin = hydrogeolog1.parse_argument("dhto2", -1, str_ay_size, str_ay);
        int anain_pin = hydrogeolog1.parse_argument("anain", -1, str_ay_size, str_ay);
        /*dhto2 measurement, measuring analog and dht22 at same time
       dhto2,12,power,41,points,2,anain,0,dummies,1,interval_mm,1000,debug,1
       dhto2,10,power,48,points,2,anain,0,dummies,1,interval_mm,1000,debug,1
       */
        if ((dhto2_in_pin != -1) && (power_sw_pin != -1) && (anain_pin != -1))
        {
            int number_of_measurements = hydrogeolog1.parse_argument("points", 1, str_ay_size, str_ay);
            int number_of_dummies = hydrogeolog1.parse_argument("dummies", 0, str_ay_size, str_ay);
            int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", 1000, str_ay_size, str_ay);

            if (measure_time_interval_ms < 1000)
            {
                measure_time_interval_ms = 1000;
            }
            // needs to be at leaset 1000 ms
            hydrogeolog1.print_string_delimiter_value("dhto2", String(dhto2_in_pin));
            if (debug_sw == 1)
            {
                hydrogeolog1.print_string_delimiter_value("power", String(power_sw_pin));
                hydrogeolog1.print_string_delimiter_value("points", String(number_of_measurements));
                hydrogeolog1.print_string_delimiter_value("dummies", String(number_of_dummies));
                hydrogeolog1.print_string_delimiter_value("interval_mm", String(measure_time_interval_ms));
            }
            digitalWrite(power_sw_pin, HIGH);
            delay(1000);
            hydrogeolog1.dht22_read(dhto2_in_pin, number_of_dummies, number_of_measurements, measure_time_interval_ms);
            hydrogeolog1.analog_read(anain_pin, number_of_dummies, number_of_measurements, measure_time_interval_ms);
            digitalWrite(power_sw_pin, LOW);
            Serial.println();
        } // analog read

        String lumino2 = hydrogeolog1.parse_argument_string("lumino2", "", str_ay_size, str_ay);
        power_sw_pin = hydrogeolog1.parse_argument("power", -1, str_ay_size, str_ay);
        int serial_pin = hydrogeolog1.parse_argument("serial", -1, str_ay_size, str_ay);
        int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", 1000, str_ay_size, str_ay);

        /*luminox sensor
       lumino2,M 2,power,42,serial,2
       lumino2,M 1,power,42,serial,2
       lumino2,M 0,power,42,serial,2
       lumino2,A,power,42,serial,2
       */
        if ((lumino2 != "") && (power_sw_pin != -1) && (serial_pin != -1)) //&&(number_of_measurements!=-1) && (number_of_dummies!=-1)
        {
            String input_linebreak = hydrogeolog1.parse_argument_string("inp_linebreak", "\r\n", str_ay_size, str_ay);
            char ouput_linebreak = hydrogeolog1.parse_argument_char("otp_linebreak", '\n', str_ay_size, str_ay);
            hydrogeolog1.print_string_delimiter_value("lumino2_cmd", lumino2);
            hydrogeolog1.print_string_delimiter_value("pow", String(power_sw_pin));
            hydrogeolog1.print_string_delimiter_value("serial", String(serial_pin));
            hydrogeolog1.print_string_delimiter_value("delay", String(measure_time_interval_ms));
            if (measure_time_interval_ms < 1000)
            {
                measure_time_interval_ms = 1000;
            }

            digitalWrite(power_sw_pin, HIGH);
            delay(1000);
            if (serial_pin == 1)
            {
                Serial1.print("M 1");
                Serial1.print("\r\n");
                delay(measure_time_interval_ms);
                String aa1 = Serial1.readStringUntil('\n');
                Serial.print(aa1);
                Serial1.print("M 1");
                Serial1.print("\r\n");
                delay(measure_time_interval_ms);
                aa1 = Serial1.readStringUntil('\n');
                Serial.print(aa1);
                Serial.print("result,");
                Serial1.print(lumino2);
                Serial1.print("\r\n");
                delay(measure_time_interval_ms);
                String aa = Serial1.readStringUntil('\n');
                Serial.print(aa);
                delay(measure_time_interval_ms);
                aa = Serial1.readStringUntil('\n');
                Serial.println(aa);
            }
            if (serial_pin == 2)
            {
                Serial2.print("M 1");
                Serial2.print("\r\n");
                delay(measure_time_interval_ms);
                String aa2 = Serial2.readStringUntil('\n');
                Serial2.print("M 1");
                Serial2.print("\r\n");
                Serial.print(aa2);
                delay(measure_time_interval_ms);
                aa2 = Serial2.readStringUntil('\n');
                Serial.print(aa2);
                Serial.print("result,");
                Serial2.print(lumino2);
                Serial2.print("\r\n");
                delay(measure_time_interval_ms);
                String aa = Serial2.readStringUntil('\n');
                Serial.print(aa);
                delay(measure_time_interval_ms);
                aa = Serial1.readStringUntil('\n');
                Serial.println(aa);
            }
            if (serial_pin == 3)
            {
                Serial3.print("M 1");
                Serial3.print("\r\n");
                delay(measure_time_interval_ms);
                String aa3 = Serial3.readStringUntil('\n');
                Serial.print(aa3);
                delay(1000);
                Serial3.print("M 1");
                Serial3.print("\r\n");
                delay(measure_time_interval_ms);
                aa3 = Serial3.readStringUntil('\n');
                Serial.print(aa3);
                Serial.print("result,");
                Serial3.print(lumino2);
                Serial3.print("\r\n");
                delay(measure_time_interval_ms);
                String aa = Serial3.readStringUntil('\n');
                Serial.print(aa);
                delay(measure_time_interval_ms);
                aa = Serial3.readStringUntil('\n');
                Serial.println(aa);
            }
            digitalWrite(power_sw_pin, LOW);
        } // lumino2

        /*ds18b20 search
        ds18b20_search,13,power,42
       */
        int ds18b20_search_pin = hydrogeolog1.parse_argument("ds18b20_search", -1, str_ay_size, str_ay);
        power_sw_pin = hydrogeolog1.parse_argument("power", -1, str_ay_size, str_ay);
        if ((ds18b20_search_pin != -1) && (power_sw_pin != -1))
        {
            hydrogeolog1.print_string_delimiter_value("ds18b20_search", String(ds18b20_search_pin));
            digitalWrite(power_sw_pin, HIGH);
            delay(1000);
            //for (int i=0; i<10;i++){

            hydrogeolog1.search_ds18b20(ds18b20_search_pin, power_sw_pin);

            //}
            digitalWrite(power_sw_pin, LOW);
        } //if ds18b20_search

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

        if ((thermal_suction_ds18b20 != "") && (power_sw_pin != -1))
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

        if ((fredlund_suction_ds18b20 != "") && (power_sw_pin != -1))
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
        if ((fredlund_suction_ds18b209 != "") && (power_sw_pin != -1))
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
        if ((tca9548_channel != -1) && (i2c_type != ""))
        {
            int number_of_measurements = hydrogeolog1.parse_argument("points", 3, str_ay_size, str_ay);
            int number_of_dummies = hydrogeolog1.parse_argument("dummies", 3, str_ay_size, str_ay);
            int measure_time_interval_ms = hydrogeolog1.parse_argument("interval_mm", 1000, str_ay_size, str_ay);
            int power_sw_pin = hydrogeolog1.parse_argument("power", -1, str_ay_size, str_ay);
            int digital_input = hydrogeolog1.parse_argument("dgin", -1, str_ay_size, str_ay);
            if (debug_sw == 1)
            {
                hydrogeolog1.print_string_delimiter_value("9548", String(tca9548_channel));
                hydrogeolog1.print_string_delimiter_value("power", String(power_sw_pin));
                hydrogeolog1.print_string_delimiter_value("points", String(number_of_measurements));
                hydrogeolog1.print_string_delimiter_value("dummies", String(number_of_dummies));
                hydrogeolog1.print_string_delimiter_value("itv", String(measure_time_interval_ms));
                hydrogeolog1.print_string_delimiter_value("type", i2c_type);
            }
            if (power_sw_pin != -1)
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

            if (power_sw_pin != -1)
                digitalWrite(power_sw_pin, LOW);
            Serial.println();
        } //tca9548_channel

        /*rcswitch for arlec RC213 sockets 
        rc_sw,5,code,011101101101100000001111100111100,pulse_len,306
        */
        int rc_sw = hydrogeolog1.parse_argument("rc_sw", -1, str_ay_size, str_ay);
        String sw_code = hydrogeolog1.parse_argument_string("code", "", str_ay_size, str_ay);

        if ((rc_sw != -1) && (sw_code != ""))
        {
            //String sw_code=hydrogeolog1.parse_argument_string("code","",str_ay_size,str_ay);
            //int binary_len=binary_code.length()+1;
            //char binary_length[binary_len];
            //binary_code.toCharArray(binary_length,binary_len);
            //char binary_code=hydrogeolog1.parse_argument_char("bin_code","",str_ay_size,str_ay);
            //char binary_code_char=binary_code.toCharArray();
            //char binary_code_char[50];
            //binary_code.toCharArray(binary_code_char,50);
            //char* binary_code_char;
            //binary_code.toCharArray(binary_code_char,50);
            int pulselength = hydrogeolog1.parse_argument("pulse_len", -1, str_ay_size, str_ay);
            hydrogeolog1.print_string_delimiter_value("code", sw_code);
            hydrogeolog1.print_string_delimiter_value("pulse_len", String(pulselength));
            hydrogeolog1.print_string_delimiter_value("rc_sw", String(rc_sw));
            //if (sw_code=="Aon")
            //{
            //    hydrogeolog1.rcswitchAon(rc_sw,pulselength);
            //}
            //if (sw_code=="Aoff")
            //{
            //    hydrogeolog1.rcswitchAoff(rc_sw,pulselength);
            //}
            //if (sw_code=="Bon")
            //{
            //    hydrogeolog1.rcswitchBon(rc_sw,pulselength);
            //}
            //if (sw_code=="Boff")
            //{
            //    hydrogeolog1.rcswitchBoff(rc_sw,pulselength);
            //}
            //if (sw_code=="Con")
            //{
            //    hydrogeolog1.rcswitchCon(rc_sw,pulselength);
            //}
            //if (sw_code=="Coff")
            //{
            //    hydrogeolog1.rcswitchCoff(rc_sw,pulselength);
            //}
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
        if ((sht75_data != -1) && (sht75_clk != -1))
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
            if (power_sw_pin != -1)
                digitalWrite(power_sw_pin, HIGH);
            delay(1000);
            hydrogeolog1.sht75(sht75_data, sht75_clk, number_of_dummies, number_of_measurements, measure_time_interval_ms, debug_sw);
            if (power_sw_pin != -1)
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
        if (search_9548 != -1)
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
