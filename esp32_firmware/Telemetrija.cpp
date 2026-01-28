
#include "Telemetrija.h"

Telemetrija::Telemetrija() {
    aktivno = false;
}

void Telemetrija::inicijalizacija(String imeuredaja) {
    aktivno = SerialBT.begin(imeuredaja); // Bluetooth device name
    if (aktivno) {
        Serial.println("Bluetooth pokrenut! Čekam spajanje...");
    } else {
        Serial.println("Greška pri pokretanju Bluetootha.");
    }
}

void Telemetrija::posaljiPodatke(float ax, float ay, float az, float d_lij, float d_sred, float d_des) {
    if (SerialBT.hasClient()) {
        // CSV format: timestamp, ax, ay, az, d_l, d_c, d_r
        String paket = String(millis()) + "," + 
                       String(ax, 2) + "," + String(ay, 2) + "," + String(az, 2) + "," +
                       String(d_lij, 1) + "," + String(d_sred, 1) + "," + String(d_des, 1);
        SerialBT.println(paket);
    }
}

void Telemetrija::posaljiPoruku(String poruka) {
    if (SerialBT.hasClient()) {
        SerialBT.println("LOG:" + poruka);
    }
}
