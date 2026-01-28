
#include "SonarSenzor.h"

SonarSenzor::SonarSenzor(int trig, int echo) {
    this->pinTrig = trig;
    this->pinEcho = echo;
    // Timeout od 15000us je cca 2.5m (zvuk ~343m/s -> 29us/cm -> 58us/cm roundtrip)
    // 15000 / 58 = 258cm
    this->timeout = 15000; 
}

void SonarSenzor::inicijalizacija() {
    pinMode(pinTrig, OUTPUT);
    pinMode(pinEcho, INPUT);
    digitalWrite(pinTrig, LOW);
}

float SonarSenzor::izmjeriUdaljenost() {
    // Generiranje impulsa
    digitalWrite(pinTrig, LOW);
    delayMicroseconds(2);
    digitalWrite(pinTrig, HIGH);
    delayMicroseconds(10);
    digitalWrite(pinTrig, LOW);

    // Mjerenje trajanja. Ovo blokira do timeouta (max 15ms).
    long trajanje = pulseIn(pinEcho, HIGH, timeout);

    if (trajanje == 0) return 300.0; // Nema povrata -> daleko ili greška

    float udaljenost = trajanje * 0.034 / 2;
    return udaljenost;
}
