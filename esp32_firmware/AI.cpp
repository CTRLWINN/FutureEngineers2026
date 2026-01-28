
#include "AI.h"

AI::AI(Kretanje* k) {
    this->kretanje = k;
    this->zadnjiPaketVrijeme = 0;
}

void AI::inicijalizacija() {
    Serial.begin(115200);
    // Čekaj serijsku? Ne nužno, jer robot mora raditi i ako se Jetson tek boota.
}

void AI::azuriraj() {
    if (Serial.available() > 0) {
        String linija = Serial.readStringUntil('\n'); // Čitaj do kraja reda
        linija.trim(); // Ukloni whitespace

        if (linija.length() > 0) {
            // Parsiranje JSON-a
            // Primjer: {"T": 0.5, "S": -0.2}
            StaticJsonDocument<200> doc;
            DeserializationError error = deserializeJson(doc, linija);

            if (!error) {
                float throttle = doc["T"];
                float steering = doc["S"];
                
                // Ažuriraj kretanje
                kretanje->postaviKomande(throttle, steering, 0.0);
                zadnjiPaketVrijeme = millis();
            }
        }
    }
}

bool AI::provjeriVezu() {
    if (millis() - zadnjiPaketVrijeme > TIMEOUT_MS) {
        return false; // Veza izgubljena
    }
    return true;
}
