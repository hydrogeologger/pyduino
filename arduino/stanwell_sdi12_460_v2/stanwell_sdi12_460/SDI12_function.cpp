#include "common.h"
#include "SDI12_function.h"
#include "timing.h"

boolean sdi12_check_pin(int sdi12_data)
{
    for (int i = 0; i < SDI12_PIN_COUNT; i++)
    {
        if (sdi12_data == sdi12_pins[i])
        {
            return true;
        }
    }
    return false;
}

/*
initiate sdi12 on a pin
*/
boolean sdi12_init(int sdi12_data)
{
    if (sdi12_check_pin(sdi12_data) == false)
        return false;
    mySDI12 = SDI12(sdi12_data);
    mySDI12.begin();
    if (isInit)
    {
        return true;
    }
    delay(500); // allow things to settle
    boolean foundSensor = false;
    int count = 0;
    //scan the pin for all avaliable sensors
    for (uint8_t i = 0; i < MAX_NUM_ADDR; i++)
    {
        char c = convert_bit_number_to_char(i);
        if (checkActive(c))
        {
            setTaken(c);
            foundSensor = true;
            count++;
        }
    }
    isInit = true;
    return foundSensor;
}

/*
looping to read SDI-12 sensor
*/
void sdi12_loop()
{
    // scan address space 0-9
    for (uint8_t i = 0; i < MAX_NUM_ADDR; i++)
    {
        {
            char c = convert_bit_number_to_char(i);
            if (isTaken(c))
            {
                for (int j = 0; j < 10; j++)
                {
                    if (checkActive(c))
                    {
                        printInfo(c);
                        takeMeasurement_sdi12(c);
                        break;
                    }
                    delay(100);
                }
            }
        }
    }
    mySDI12.end();
}

void takeMeasurement_sdi12(char i)
{
    String command = "";
    command += i;
    command += "M!"; // SDI-12 measurement command format  [address]['M'][!]
    mySDI12.sendCommand(command);
    // wait for acknowlegement with format [address][ttt (3 char, seconds)][number of measurments available, 0-9]

    String sdiResponse = "";
    delay(30);
    while (mySDI12.available()) // build response string
    {
        char c = mySDI12.read();
        if ((c != '\n') && (c != '\r'))
        {
            sdiResponse += c;
            delay(5);
        }
    }
    mySDI12.clearBuffer();

    // find out how long we have to wait (in seconds).
    unsigned int wait = 0;
    wait = sdiResponse.substring(1, 4).toInt();

    // Set up the number of results to expect

    int numMeasurements = sdiResponse.substring(4, 5).toInt();
    Serial.print("wait,");
    Serial.print(wait);
    Serial.print(",");
    Serial.print("points,");
    Serial.print(numMeasurements);
    Serial.print(",");

    unsigned long timerStart = millis();
    while ((millis() - timerStart) < (1000 * wait))
    {
        if (mySDI12.available()) // sensor can interrupt us to let us know it is done early
        {
            mySDI12.clearBuffer();
            break;
        }
    }
    // Wait for anything else and clear it out
    delay(30);
    mySDI12.clearBuffer();

    // in this example we will only take the 'DO' measurement
    command = "";
    command += i;
    command += "D0!"; // SDI-12 command to get data [address][D][dataOption][!]
    mySDI12.sendCommand(command);
    while ((!mySDI12.available()) > 1)
        ;       // wait for acknowlegement
    delay(300); // let the data transfer
    printBufferToScreen();
    mySDI12.flush();
    mySDI12.clearBuffer();
}

void printBufferToScreen()
{
    String buffer = "";
    mySDI12.read(); // consume address
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
    Serial.print(buffer);
}

// this checks for activity at a particular address
// expects a char, '0'-'9', 'a'-'z', or 'A'-'Z'
boolean checkActive(char i)
{
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
        mySDI12.clearBuffer();
        return true;
    }
    else
    { // otherwise it is vacant.
        mySDI12.clearBuffer();
    }
    return false;
}

uint8_t convert_char_to_bit_number(char c)
{
    //bit 0 to bit 9
    if (c >= '0' && c <= '9')
    {
        return c - '0';
    }
    //bit 10 to bit 35
    if (c >= 'a' && c <= 'z')
    {
        return c - 'a' + 10;
    }
    //bit 36 to 61
    return c - 'A' + 36;
}

char convert_bit_number_to_char(uint8_t bit)
{
    if (bit >= 0 && bit <= 9)
    {
        return bit + '0';
    }
    if (bit >= 10 && bit <= 35)
    {
        return bit - 10 + 'a';
    }
    return bit - 36 + 'A';
}

// this sets the bit in the proper location within the addressRegister
// to record that the sensor is active and the address is taken.
boolean setTaken(char c)
{
    //first convert the char c to bit number
    uint8_t bit = convert_char_to_bit_number(c);
    //check if this bit is set in the addressSpace
    uint8_t bitInSpace = (uint8_t)((addressSpace & (uint64_t)(1 << bit)) >> bit);
    if (bitInSpace == 1)
    {
        return false; //already set
    }
    else
    {
        //set the bit in the addressSpace
        addressSpace |= (uint64_t)(1 << bit);
        return true;
    }
}

boolean isTaken(char c)
{
    uint8_t bit = convert_char_to_bit_number(c);
    //check if this bit is set in the addressSpace
    uint8_t bitInSpace = (uint8_t)((addressSpace & (uint64_t)(1 << bit)) >> bit);
    return (bitInSpace == 1);
}

// gets identification information from a sensor, and prints it to the serial port
// expects a character between '0'-'9', 'a'-'z', or 'A'-'Z'.
void printInfo(char i)
{
    //int j;
    String command = "";
    command += (char)i;
    command += "I!";
    mySDI12.sendCommand(command);
    delay(30);
    if (mySDI12.available() > 1)
    {
        Serial.print("Addr,");
        Serial.print(i);
        Serial.print(DELIMITER);
    }
    if (mySDI12.available())
        mySDI12.read();
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

//SDI-12,50,power,49,debug,1