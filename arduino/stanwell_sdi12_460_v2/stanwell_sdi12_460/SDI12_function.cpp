#include "SDI12.h"

/*
initiate sdi12 on a pin
*/
boolean sdi12_init(int sdi12_data)
{
#define DATAPIN sdi12_data
    SDI12 mySDI12(DATAPIN);

    mySDI12.begin();
    delay(500); // allow things to settle

    for (byte i = '0'; i <= '9'; i++)
        if (checkActive(i, sdi12_data))
            setTaken(i); // scan address space 0-9
    boolean found = false;
    for (byte i = 0; i < 62; i++)
    {
        if (isTaken(i))
        {
            found = true;
            return true;
        }
    }
    return false;
}
