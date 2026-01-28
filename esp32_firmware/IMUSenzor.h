
#ifndef IMU_SENZOR_H
#define IMU_SENZOR_H

#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include "HardwareMap.h"

class IMUSenzor {
private:
    Adafruit_MPU6050 mpu;
    bool inicijalizirano;

public:
    IMUSenzor();
    bool inicijalizacija();
    void dohvatiPodatke(float &ax, float &ay, float &az);
};

#endif
