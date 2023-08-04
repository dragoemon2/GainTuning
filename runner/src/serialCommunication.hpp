#pragma once

#include <mbed.h>
#include <string>

using namespace std;

void splitString(string* results, string str, char letter);

class SerialCommunication{
    public:
        UnbufferedSerial serialPort;
        SerialCommunication();
        void attach(std::function<void(string)> func, char split='\n');
        void detach();
        void writeline(string comment);
        void readChar();
    private:
        string str;
        
        std::function<void(string)> function;
};