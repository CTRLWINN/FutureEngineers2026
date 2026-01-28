
#include "IMUSenzor.h"

IMUSenzor::IMUSenzor() {
    inicijalizirano = false;
}

bool IMUSenzor::inicijalizacija() {
    Wire.begin(I2C_SDA, I2C_SCL);
    
    if (!mpu.begin()) {
        Serial.println("Greška: MPU6050 nije pronađen!");
        return false;
    }
    
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
    
    inicijalizirano = true;
    return true;
}

void IMUSenzor::dohvatiPodatke(float &ax, float &ay, float &az) {
    if (!inicijalizirano) {
        ax = ay = az = 0.0;
        return;
    }

    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    ax = a.acceleration.x;
    ay = a.acceleration.y;
    az = a.acceleration.z;
}
