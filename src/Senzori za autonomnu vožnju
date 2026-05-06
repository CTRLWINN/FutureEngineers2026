#include <Wire.h>
#include "Adafruit_VL53L0X.h"

#define MUX_ADDR 0x70 // Adresa tvog multipleksora

Adafruit_VL53L0X lox = Adafruit_VL53L0X();

// Funkcija za odabir kanala (0-7)
void tcaselect(uint8_t i) {
  if (i > 7) return;
  Wire.beginTransmission(MUX_ADDR);
  Wire.write(1 << i);
  Wire.endTransmission();  
}

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22); // Dasduino Connect I2C pinovi
  
  Serial.println("Inicijalizacija oba senzora...");

  // Inicijalizacija PRVOG senzora (Kanal 0)
  tcaselect(0);
  if (!lox.begin()) {
    Serial.println(F("Greska: Senzor 1 (Kanal 0) nije pronadjen!"));
  } else {
    Serial.println(F("Senzor 1 spreman."));
  }

  // Inicijalizacija DRUGOG senzora (Kanal 1)
  tcaselect(1);
  if (!lox.begin()) {
    Serial.println(F("Greska: Senzor 2 (Kanal 1) nije pronadjen!"));
  } else {
    Serial.println(F("Senzor 2 spreman."));
  }
}

void loop() {
  int offset = 40; // Tvoja kalibracija od 4cm

  // --- OCITAVANJE SENZORA 1 ---
  tcaselect(0);
  VL53L0X_RangingMeasurementData_t measure1;
  lox.rangingTest(&measure1, false);
  
  int dist1 = (measure1.RangeStatus != 4) ? (measure1.RangeMilliMeter - offset) : -1;
  if (dist1 < 0 && measure1.RangeStatus != 4) dist1 = 0;

  // --- OCITAVANJE SENZORA 2 ---
  tcaselect(1);
  VL53L0X_RangingMeasurementData_t measure2;
  lox.rangingTest(&measure2, false);
  
  int dist2 = (measure2.RangeStatus != 4) ? (measure2.RangeMilliMeter - offset) : -1;
  if (dist2 < 0 && measure2.RangeStatus != 4) dist2 = 0;

  // --- ISPIS REZULTATA ---
  Serial.print("Senzor 1: ");
  if (dist1 == -1) Serial.print("OUT "); else { Serial.print(dist1); Serial.print("mm "); }
  
  Serial.print(" | Senzor 2: ");
  if (dist2 == -1) Serial.println("OUT"); else { Serial.print(dist2); Serial.println("mm"); }

  delay(100); // Brzina osvjezavanja
}
