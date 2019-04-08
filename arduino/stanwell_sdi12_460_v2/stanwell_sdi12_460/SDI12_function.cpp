#include "common.h"
#include <SDI12.h>
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
    SDI12 mySDI12(sdi12_data);

    mySDI12.begin();
    delay(500); // allow things to settle

    for (byte i = '0'; i <= '9'; i++)
        if (checkActive(i, sdi12_data))
            setTaken(i); // scan address space 0-9
    for (byte i = 0; i < 62; i++)
    {
        if (isTaken(i))
        {
            return true;
        }
    }
    return false;
}

/*
looping to read SDI-12 sensor
*/
void sdi12_loop(int sdi12_data)
{
    // scan address space 0-9
    for (char i = '0'; i <= '9'; i++)
    {
        if (isTaken(i))
        {
            printInfo(i, sdi12_data);
            takeMeasurement_sdi12(i, sdi12_data);
        }
    }
}

void takeMeasurement_sdi12(char i, int sdi12_data)
{
    SDI12 mySDI12(sdi12_data);
    String command = "";
    command += i;
    command += "M!"; // SDI-12 measurement command format  [address]['M'][!]
    mySDI12.sendCommand(command);
    while (mySDI12.available() < 5)
        ;
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
    while (mySDI12.available() < 1)
        ;       // wait for acknowlegement
    delay(300); // let the data transfer
    printBufferToScreen(sdi12_data);
    mySDI12.flush();
}

void printBufferToScreen(int sdi12_data)
{
    SDI12 mySDI12(sdi12_data);
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
    Serial.print(buffer);
}

// this checks for activity at a particular address
// expects a char, '0'-'9', 'a'-'z', or 'A'-'Z'
boolean checkActive(char i, int sdi12_data)
{
    SDI12 mySDI12(sdi12_data);

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
    SDI12 mySDI12(sdi12_data);
    int j;
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
