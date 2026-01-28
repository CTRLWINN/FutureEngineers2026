
#ifndef SONAR_SENZOR_H
#define SONAR_SENZOR_H

#include <Arduino.h>

class SonarSenzor {
private:
    int pinTrig;
    int pinEcho;
    unsigned long timeout;

public:
    SonarSenzor(int trig, int echo);
    void inicijalizacija();
    float izmjeriUdaljenost(); // u cm
};

#endif
