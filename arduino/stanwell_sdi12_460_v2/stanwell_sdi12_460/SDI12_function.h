#include <SDI12.h>

boolean sdi12_init(int sdi12_data);
void sdi12_loop(int sdi12_data);
void takeMeasurement_sdi12(char i, int sdi12_data);
void printBufferToScreen(int sdi12_data);
boolean checkActive(char i, int sdi12_data);
boolean setTaken(byte i);
boolean setVacant(byte i);
boolean isTaken(byte i);

