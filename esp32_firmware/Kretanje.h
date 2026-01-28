
#ifndef KRETANJE_H
#define KRETANJE_H

#include <Arduino.h>
#include <ESP32Servo.h>
#include "HardwareMap.h"

class Kretanje {
private:
    Servo servoSkretanje;
    Servo escMotor;
    
    // PID varijable (ako je PID na ESP-u, ali plan kaže Jetson šalje komande)
    // Ako Jetson šalje steering (-1 do 1), ovdje samo mapiramo.
    
    // Limiti
    const int SERVO_MIN = 0;   // Stupnjevi ili mikrosekunde
    const int SERVO_MAX = 180;
    const int SERVO_CENTER = 90;

    const int ESC_MIN = 1000;  // PWM mikrosekunde
    const int ESC_MAX = 2000;
    const int ESC_STOP = 1500; // Neutralno

    float trenutniKut;
    float trenutnaBrzina;

public:
    Kretanje();
    void inicijalizacija();
    void postaviKomande(float brzina, float kut, float dt); // brzina [-1, 1], kut [-1, 1]
    void sigurnosnoZaustavljanje();
};

#endif
