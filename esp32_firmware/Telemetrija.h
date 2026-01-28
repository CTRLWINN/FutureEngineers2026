
#ifndef TELEMETRIJA_H
#define TELEMETRIJA_H

#include <Arduino.h>
#include "BluetoothSerial.h"

class Telemetrija {
private:
    BluetoothSerial SerialBT;
    bool aktivno;

public:
    Telemetrija();
    void inicijalizacija(String imeuredaja);
    void posaljiPodatke(float ax, float ay, float az, float d_lij, float d_sred, float d_des);
    void posaljiPoruku(String poruka);
};

#endif
