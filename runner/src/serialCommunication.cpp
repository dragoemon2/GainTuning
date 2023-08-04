#include <mbed.h>
#include "serialCommunication.hpp"

using namespace std;

void splitString(string* results, string str, char letter){
    int i = 0;
    string result = "";
    for(char c: str){
        if(c == letter){
            results[i] = result;
            i++;
            result = "";
        }else{
            result += c;
        }
    }
    results[i] = result;
}

SerialCommunication::SerialCommunication(): serialPort(USBTX, USBRX) {
    str = "";
    function = [](string comment) {return;};
    serialPort.baud(9600);
    serialPort.format(
        /* bits */ 8,
        /* parity */ SerialBase::None,
        /* stop bit */ 1
    );
    serialPort.attach([this]() {readChar();});
}

void SerialCommunication::writeline(string comment) {
    serialPort.write((comment+'\n').c_str(), comment.size() + 1);
}

void SerialCommunication::readChar() {
    char c;
    while(serialPort.readable()){
        serialPort.read(&c, 1);
        if(c == '\n'){
            function(str);
            str = "";
        }else{
            str = str + c;
        }
    }
}

void SerialCommunication::attach(std::function<void(string)> func, char split) {
    function = func;
}

void SerialCommunication::detach(){
    function = [](string comment) {return;};
}


