
#include <mbed.h>
#include "driveMotor.hpp"
#include "parameters.hpp"
#include "serialCommunication.hpp"
#include <string>
#include <stdio.h>

using namespace std;

SerialCommunication serial;
Timer rtimer;
Ticker ticker;
DriveMotor motor0(D9, D8, D12, D11, 1.3f, 0.06f, 0, 0.00004f, 0.000001f, 0);

float kp1, ki1, kd1, kp2, ki2, kd2;
bool moving = true;
bool quit = false;


void interrupt(string comment){
    if(comment == "quit"){
        quit = true;
    }else{
        sscanf(comment.c_str(), "%f,%f,%f,%f,%f,%f", &kp1, &ki1, &kd1, &kp2, &ki2, &kd2);
        motor0.stop();
        motor0.pidController.setGain(kp1, ki1, kd1);
        motor0.pidSpeedController.setGain(kp2, ki2, kd2);
        motor0.rotateTo(10000, false);
    }
}


int main(){
    serial.attach(interrupt);
    motor0.rotateTo(10000, false);


    while(!(quit)){ 
        ThisThread::sleep_for(20);
        char line[256];
        sprintf(line, "%d, %d, %d, %d", int(motor0._s2), int(motor0._s1), 10000, int(motor0.encoder.getAmount()));
        serial.writeline(line);

    }
    motor0.stop();
}

