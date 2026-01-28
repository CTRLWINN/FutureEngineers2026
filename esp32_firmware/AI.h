
#ifndef AI_H
#define AI_H

#include <Arduino.h>
#include <ArduinoJson.h>
#include "Kretanje.h"

class AI {
private:
    Kretanje* kretanje;
    unsigned long zadnjiPaketVrijeme;
    const unsigned long TIMEOUT_MS = 500;

public:
    AI(Kretanje* k);
    void inicijalizacija();
    void azuriraj();
    bool provjeriVezu();
};

#endif
