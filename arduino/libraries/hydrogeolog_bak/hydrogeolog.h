#ifndef hydrogeolog_h
#define hydrogeolog_h

#include "Arduino.h"
//#include "hydrogeolog"

class hydrogeolog
{
    public:
      hydrogeolog(const char delimiter);
      //int split_strings(String inp);    
      //void print_str_ay(int number_opts);
      int split_strings(String inp2,String str_ay2[20]);    
      void print_str_ay(int number_opts,String str_ay2[20]);
    private:
      int _pin;
      String inp2; 
      String str_ay2[20];
      int number_opts;
      const char delimiter=',';

}; // class

#endif

