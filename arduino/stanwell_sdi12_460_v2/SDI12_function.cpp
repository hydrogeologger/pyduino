#include "common.h"
#include "SDI12_function.h"
#include "timing.h"


boolean is_valid_addr(char c) {
    if ((c >= '0' && c <= '9') || (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') )
        return true;
    return false;
}

void process_command(String cmd, char new_addr) {
    uint8_t num_sensors = 0;

    if (!is_valid_addr(new_addr) || cmd == "change") {
        num_sensors = sdi12_scan();
        if (num_sensors <= 0) {
            Serial.print("No Sensors found!");
            return;
        }
        Serial.print("no_sensors,");
        Serial.print(num_sensors);
        Serial.print(DELIMITER);
    }

    if (cmd == "read") {
        if (is_valid_addr(new_addr)) {
            if (checkActive(new_addr)) {
                printInfo(new_addr);
                Serial.print(DELIMITER);
                takeMeasurement_sdi12(new_addr);
            } else {
                Serial.print("No response!");
            }
        } else {
            sdi12_loop_get_measurements();
        }
    } else if (cmd == "change") {
        if (num_sensors != 1) {
            Serial.print("Expect only ONE sensor connected! => ABORT!");
        } else {
            if (is_valid_addr(new_addr) == false) {
                Serial.print("Invalid new addr => ABORT!");
            } else {
                sdi12_change(new_addr);
            }
        }
    } else {
        Serial.print("INVALID CMD!");
    }
}

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

/**
 * @brief Counts the number of connected active SDI-12 devices.
 *
 * @return uint8_t Number of unique SDI-12 sensor address
 */
uint8_t sdi12_scan(void) {
    uint8_t count = 0;
    //scan the pin for all avaliable sensors
    for (uint8_t i = 0; i < MAX_NUM_ADDR; i++) {
        char c = convert_bit_number_to_char(i);
        if (checkActive(c)) {
            setTaken(c);
            count++;
        }
    }
    return count;
}

/*
initiate sdi12 on a pin
*/
boolean sdi12_init(int sdi12_pin) {
    if (sdi12_check_pin(sdi12_pin) == false)
        return false;
    mySDI12 = SDI12(sdi12_pin);
    mySDI12.begin();
    delay(500); // allow things to settle
    return true;
}

void sdi12_end(void) {
    addressSpace[LOW] = (uint32_t)0x00;
    addressSpace[HIGH] = (uint32_t)0x00;
    mySDI12.flush();
    mySDI12.clearBuffer();
    mySDI12.end();
}

boolean sdi12_change(char new_addr)
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
                        String cmd = "" + String(c) + "A" + String(new_addr) + "!";
                        printInfo(c);
                        Serial.print(DELIMITER);
                        sdi12_send_command(cmd, false);
                        addressSpace[LOW] = (uint32_t)0x00;
                        addressSpace[HIGH] = (uint32_t)0x00;
                        printInfo(new_addr);
                        Serial.print(DELIMITER);
                        return true;
                    }
                    delay(100);
                }
            }
        }
    }
    return false;
}

void sdi12_send_command(String cmd, boolean read) {
    mySDI12.sendCommand(cmd);
    delay(30);
    if (mySDI12.available()) {
        if (read)
            Serial.print("response,");
        while (mySDI12.available())
        {
            char c = mySDI12.read();
            if ((c != '\n') && (c != '\r') && read)
            {
                Serial.write(c); //print sensor info and type
            }
            delay(10);
        }
        Serial.print(DELIMITER);
    } else {
        Serial.print("no_response,");
    }
    //Serial.println();
}

/*
looping to read SDI-12 sensor
*/
void sdi12_loop_get_measurements()
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
                        Serial.print(DELIMITER);
                        takeMeasurement_sdi12(c);
                        break;
                    }
                    delay(100);
                }
            }
        }
    }
}

void takeMeasurement_sdi12(char address) {
    char command[4+1];
    uint8_t received_count = 0;

    mySDI12.clearBuffer();

    // SDI-12 measurement command format  [address]['M'][!]
    sprintf(command, "%cM!", address);
    mySDI12.sendCommand(command);

    // wait for acknowlegement with format [address][ttt (3 char, seconds)][number of measurments available, 0-9]
    String sdiResponse = "";
    delay(60);  // wait for atttn\r\n
    // build response string
    while (mySDI12.available()) {
        char c = mySDI12.read();
        if ((c != '\n') && (c != '\r')) {
            sdiResponse += c;
        } else if (c == '\n') {
            break;
        }
        if (!mySDI12.available()) delay(10);
    }

    // find out how long we have to wait (in seconds).
    unsigned int wait = 1;
    wait = sdiResponse.substring(1, 4).toInt();
    if (wait <= 0) { wait = 1; }

    // Set up the number of results to expect
    int expected_count = sdiResponse.substring(4, 5).toInt();
    Serial.print("points");
    Serial.print(DELIMITER);
    Serial.print(expected_count);
    Serial.print(DELIMITER);

    // Wait for maximum duration for reply or service request
    for (uint16_t i = 0; i < (1000u * wait); i++) {
        if (mySDI12.available() >= 3) break;  // Service request received
        delay(1);
    }

    // Start requesting data
    mySDI12.clearBuffer();
    for (uint8_t i = 0; received_count < expected_count && i <= 9; i++) {
        // SDI-12 command to get data [address][D][dataOption][!]
        sprintf(command, "%cD%d!", address, i);
        mySDI12.sendCommand(command);
        // wait for acknowlegement
        while (mySDI12.available() < 1) {
            delay(20);
        }
        received_count += printBufferToScreen();
    }
}

uint8_t printBufferToScreen(void) {
    bool first_run = true;
    uint8_t received_count = 0;
    String buffer = "";

    mySDI12.read();  // consume address
    while (mySDI12.available() > 0) {
        char c = mySDI12.read();
        // Add to buffer for printable characters only
        if (c >= 32 && c <= 126) {
            if (c == '+' || c == '-') {
                // Only add delimiter for 2nd sign onwards
                if (first_run) {
                    first_run = false;
                } else {
                    buffer += DELIMITER;
                }
                if (c == '-') buffer += '-';
                received_count++;
            } else {
                buffer += c;
            }
        } else if (c == '\n') {
            buffer += DELIMITER; // Replace newline with delimiter
        }
        delay(10);
    }
    Serial.print(buffer);
    return received_count;
}

// this checks for activity at a particular address
// expects a char, '0'-'9', 'a'-'z', or 'A'-'Z'
boolean checkActive(char addr) {
    char myCommand[2+1];

    // sends basic 'acknowledge' command [address][!]
    sprintf(myCommand, "%c!", addr); // sends basic 'acknowledge' command [address][!]
    mySDI12.clearBuffer();

    for (int i = 0; i < 3; i++) {  // goes through three rapid contact attempts
        mySDI12.sendCommand(myCommand);
        delay(25);
        if (mySDI12.available() >= 3) break;
    }
    if (mySDI12.read() == addr) {  // if it hears anything it assumes the address is occupied
        mySDI12.clearBuffer();
        return true;
    }
    // otherwise it is vacant.
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
    //set the bit in the addressSpace
    addressSpace[bit < 32 ? LOW : HIGH] |= ((uint32_t)1 << (uint32_t)(bit < 32 ? bit : bit - 32));
    return true;
}

boolean isTaken(char c)
{
    uint8_t bit = convert_char_to_bit_number(c);
    //check if this bit is set in the addressSpace
    uint8_t bitInSpace = addressSpace[bit < 32 ? LOW : HIGH] >> (bit < 32 ? bit : bit - 32) & 0x01;
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
        Serial.print("_");
    }
    else
    {
        printInfo(i);
    }
    if (mySDI12.available())
        mySDI12.read();
    int count = 0;
    while (mySDI12.available())
    {
        char c = mySDI12.read();
        if ((c != '\n') && (c != '\r') && (c != ' ') && count < 3 && (c < '0' || c > '9'))
        {
            Serial.write(c); //print sensor info and type
            count++;
        }
        delay(10);
    }
}

void sdi12_loop(void) {
    String myCommand = "";
    String sdiResponse = "";
    char c;

    while (true) {
        // SDI12 buffer overflow, clear buffer
        if (mySDI12.available() < 0) { mySDI12.clearBuffer(); }
        while (Serial.available() > 0) {
            // Read all characters
            c = Serial.read();
            myCommand += String(c);
            delay(2);  // 1 character ~ 1.04 ms @ 9600 baud
        }

        // Pass through mode escape
        if (myCommand == "SDIPASSEXIT" || millis() > 300000ul) {
            Serial.println("SDIPASS,END!");
            return;
        }

        if (myCommand.length() > 0 || c == '\n' || c == '\r') {
            reset_timer();  // Reset timer for pass through time limit
            mySDI12.clearBuffer();
            mySDI12.sendCommand(myCommand);
            myCommand = "";
            c = '\0';

            // Wait for maximum duration for reply
            for (uint16_t i = 0; i < 5000u; i++) {
                delay(1);
                if (mySDI12.available()) {
                    break;
                }
            }
        }

        while (mySDI12.available() > 0) {
            c = mySDI12.read();
            if (c == '\r' || c == '\n') {
                Serial.println(sdiResponse);  // write the response to the screen
                Serial.flush();
                sdiResponse = "";
                c = '\0';
                mySDI12.clearBuffer();
                mySDI12.forceListen();
                break;
            } else if (c >= 32 && c <= 126) {
                sdiResponse += String(c);
            }
            delay(10);  // 1 character ~ 8.33 ms @ 1200 baud
        }
    }
}

//SDI-12,50,power,49,debug,1
