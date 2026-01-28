
#ifndef HARDWARE_MAP_H
#define HARDWARE_MAP_H

#include <Arduino.h>

// Definiranje pinova i hardverskih konstanti
// Promjena ožičenja zahtijeva izmjenu SAMO ove datoteke.

// --- I2C (IMU - MPU6050/BNO055) ---
#define I2C_SDA 21
#define I2C_SCL 22

// --- Aktuatori ---
#define PIN_SERVO_SKRETANJE 13
#define PIN_ESC_MOTOR 12

// --- Ultrazvučni Senzori (HC-SR04) ---
// Lijevi
#define PIN_SONAR_L_TRIG 5
#define PIN_SONAR_L_ECHO 18

// Srednji
#define PIN_SONAR_C_TRIG 19
#define PIN_SONAR_C_ECHO 23

// Desni
#define PIN_SONAR_R_TRIG 4
#define PIN_SONAR_R_ECHO 14 // Paziti na pull-up/down kod bootanja ako se koriste određeni pinovi

// --- Serijska Komunikacija (s Jetsonom) ---
// Koristimo standardni Serial (USB)
#define SERIAL_BAUD_RATE 115200

// --- Ostalo ---
#define LED_INDIKATOR 2

#endif
