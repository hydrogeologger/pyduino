#ifndef hydrogeolog_h
#define hydrogeolog_h

#include "Arduino.h"
#include <dht.h>
//#include <DHT.h>
#include <OneWire.h>
//#include "hydrogeolog"

class hydrogeolog
{
    public:
      hydrogeolog(const char delimiter);
      //int split_strings(String inp);    
      //void print_str_ay(int number_opts);
      int split_strings(String inp2,String str_ay2[20]);    
      int strcmpi(String str_source, int number_opts,String str_ay2[20]);
      int parse_argument(String str_source, int default_values, int number_opts, String str_ay2[20]);
      String parse_argument_string(String str_source, String default_values, int number_opts, String str_ay2[20]);
      char parse_argument_char(String str_source, char default_values, int number_opts, String str_ay2[20]);
      void print_str_ay(int number_opts,String str_ay2[20]);
      void analog_excite_read(int power_sw_idx,int analog_idx,int number_of_dummies,int number_of_measurement,int measure_time_interval);
      void analog_read(int analog_idx,int number_of_dummies,int number_of_measurement,int measure_time_interval);
      void switch_power(int power_sw_idx,int status);
      void dht22_excite_read(int power_sw_idx,int digi_idx,int number_of_dummies,int number_of_measurements,int measure_time_interval); 
      void dht22_read(int digi_idx,int number_of_dummies,int number_of_measurements,int measure_time_interval);
      void print_string_delimiter_value(String string_input,String value);
      void search_ds18b20(int digi_pin,int power_switch);
      void read_DS18B20_by_addr(byte addr[8],int digi_pin);
      private:
      int _pin;
      String inp2; 
      String str_ay2[20];
      int number_opts;
      const char delimiter=',';

}; // class

#endif

