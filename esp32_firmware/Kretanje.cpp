
#include "Kretanje.h"

Kretanje::Kretanje() {
    trenutniKut = 0.0;
    trenutnaBrzina = 0.0;
}

void Kretanje::inicijalizacija() {
    // Alokacija timer-a za ESP32 Servo
    ESP32PWM::allocateTimer(0);
    ESP32PWM::allocateTimer(1);
    
    servoSkretanje.setPeriodHertz(50); 
    servoSkretanje.attach(PIN_SERVO_SKRETANJE, 500, 2400); // Prilagoditi min/max pulse width za servo

    escMotor.setPeriodHertz(50);
    escMotor.attach(PIN_ESC_MOTOR, 1000, 2000); 

    // Inicijalno zaustavljanje
    sigurnosnoZaustavljanje();
    
    // ESC often requires a specific startup sequence (calibration) or just starting at neutral
    escMotor.writeMicroseconds(ESC_STOP);
    delay(100);
}

void Kretanje::postaviKomande(float brzina, float kut, float dt) {
    // kut je u rasponu [-1.0 (lijevo), 1.0 (desno)] -> mapirati na [SERVO_MIN, SERVO_MAX]
    // brzina je u rasponu [-1.0 (nazad), 1.0 (naprijed)] -> mapirati na [ESC_MIN, ESC_MAX]

    // Ograničavanje ulaza
    if (kut < -1.0) kut = -1.0;
    if (kut > 1.0) kut = 1.0;
    if (brzina < -1.0) brzina = -1.0;
    if (brzina > 1.0) brzina = 1.0;

    // Mapiranje kuta
    // 0 -> 90 stupnjeva
    // -1 -> 0 stupnjeva (ili min)
    // 1 -> 180 stupnjeva (ili max)
    int servoKut = map((long)(kut * 1000), -1000, 1000, 45, 135); // Ograničio sam na 45-135 radi sigurnosti mehaničkih dijelova
    servoSkretanje.write(servoKut);

    // Mapiranje brzine
    int pwmValue = ESC_STOP;
    if (brzina > 0) {
        pwmValue = map((long)(brzina * 1000), 0, 1000, ESC_STOP, ESC_MAX);
    } else {
        pwmValue = map((long)(brzina * 1000), -1000, 0, ESC_MIN, ESC_STOP);
    }
    escMotor.writeMicroseconds(pwmValue);
    
    this->trenutniKut = kut;
    this->trenutnaBrzina = brzina;
}

void Kretanje::sigurnosnoZaustavljanje() {
    escMotor.writeMicroseconds(ESC_STOP);
    // Servo možda ostaviti gdje je ili centrirati? Centrirajmo ga.
    servoSkretanje.write(SERVO_CENTER);
    this->trenutnaBrzina = 0;
    this->trenutniKut = 0;
}
