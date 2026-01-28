
#include <Arduino.h>
#include "HardwareMap.h"
#include "Kretanje.h"
#include "AI.h"
#include "Telemetrija.h"
#include "IMUSenzor.h"
#include "SonarSenzor.h"

// --- Globalni Objekti ---
Kretanje kretanje;
AI ai(&kretanje); // AI kontrolira kretanje
Telemetrija telemetrija;
IMUSenzor imu;

// Sonari
SonarSenzor sonarL(PIN_SONAR_L_TRIG, PIN_SONAR_L_ECHO);
SonarSenzor sonarC(PIN_SONAR_C_TRIG, PIN_SONAR_C_ECHO);
SonarSenzor sonarR(PIN_SONAR_R_TRIG, PIN_SONAR_R_ECHO);

// --- Tajming ---
unsigned long zadnjeMjereneje = 0;
const unsigned long PERIOD_MJERENJA = 100; // ms (10 Hz telemetrija)

void setup() {
    Serial.begin(115200);
    
    // Inicijalizacija modula
    kretanje.inicijalizacija();
    ai.inicijalizacija();
    telemetrija.inicijalizacija("JetBot_ESP32"); // Ime za Bluetooth
    
    // Inicijalizacija senzora
    imu.inicijalizacija();
    sonarL.inicijalizacija();
    sonarC.inicijalizacija();
    sonarR.inicijalizacija();

    // Signalizacija spremnosti (LED blink)
    pinMode(LED_INDIKATOR, OUTPUT);
    digitalWrite(LED_INDIKATOR, HIGH);
    delay(500);
    digitalWrite(LED_INDIKATOR, LOW);
}

void loop() {
    // 1. Provjeri i obradi dolazne komande s Jetsona
    ai.azuriraj();

    // 2. Sigurnosna provjera veze (Safety Stop)
    if (!ai.provjeriVezu()) {
        kretanje.sigurnosnoZaustavljanje();
        digitalWrite(LED_INDIKATOR, LOW); // Indikator greške/čekanja
    } else {
        digitalWrite(LED_INDIKATOR, HIGH); // Veza aktivna
    }

    // 3. Očitavanje senzora i telemetrija (periodički)
    if (millis() - zadnjeMjereneje > PERIOD_MJERENJA) {
        float ax, ay, az;
        imu.dohvatiPodatke(ax, ay, az);

        float distL = sonarL.izmjeriUdaljenost();
        float distC = sonarC.izmjeriUdaljenost();
        float distR = sonarR.izmjeriUdaljenost();
        
        // Slanje na Bluetooth
        telemetrija.posaljiPodatke(ax, ay, az, distL, distC, distR);
        
        // Slanje i na Serial za Jetson (u JSON formatu)
        // {"accel": [ax, ay, az], "dist": [distL, distC, distR]}
        Serial.printf("{\"accel\":[%.2f,%.2f,%.2f],\"dist\":[%.1f,%.1f,%.1f]}\n", 
                      ax, ay, az, distL, distC, distR);

        zadnjeMjereneje = millis();
    }
}
