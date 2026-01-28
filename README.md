# Pregled Projekta: Modularni AI Robot

Ovaj dokument opisuje softver za autonomnog robota (Jetson Nano + ESP32).

## Struktura Projekta

### 1. Jetson Nano Aplikacija (`jetson_app/`)
Napisana u Pythonu, modularna i spremna za proširenje.

- **`main.py`**: Glavna petlja koja orkestrira percepciju, odluke i vožnju.
- **`config/settings.py`**: Sve postavke na jednom mjestu (pinovi, PID, brzine).
- **`drivers/`**:
  - `serial_interface.py`: Komunikacija s ESP32 u zasebnoj dretvi (NON-BLOCKING).
  - `camera.py`: Podrška za CSI (GStreamer) i USB kamere.
- **`perception/`**:
  - `ai_inference.py`: Učitavanje PyTorch modela i inferencija.
  - `obstacle_avoidance.py`: Logika za izbjegavanje prepreka pomoću sonara.
- **`control/pid.py`**: PID regulator za glatko praćenje linije/staze.
- **`utils/utils.py`**: Spremanje podataka za treniranje.

### 2. ESP32 Firmware (`esp32_firmware/`)
Napisan u C++ (Arduino ekosustav), podijeljen na biblioteke.

- **`esp32_firmware.ino`**: Glavna skica.
- **`HardwareMap.h`**: Popis svih pinova. Promijenite ovo ako mijenjate ožičenje.
- **`Kretanje`**: Upravljanje motorima (ESC + Servo).
- **`AI`**: Parsiranje JSON komandi s Jetsona (`{"T":..., "S":...}`).
- **`Telemetrija`**: Slanje podataka preko Bluetootha u CSV formatu.
- **`Senzori`**:
  - `IMUSenzor`: MPU6050 akcelerometar/žiroskop.
  - `SonarSenzor`: HC-SR04 drajver.

## Upute za Pokretanje

### Na Jetson Nano
1. Instalirajte zavisnosti:
   ```bash
   pip3 install -r jetson_app/requirements.txt
   ```
2. Pokrenite aplikaciju:
   ```bash
   python3 jetson_app/main.py
   ```

### Na ESP32
1. Otvorite `esp32_firmware/esp32_firmware.ino` u Arduino IDE.
2. Instalirajte potrebne biblioteke putem Library Managera:
   - `ArduinoJson`
   - `Adafruit MPU6050`
   - `ESP32Servo`
3. Odaberite "DOIT ESP32 DEVKIT V1" (ili odgovarajuću pločicu).
4. Uploadajte kod.

## Napomene
- **Sigurnost**: Robot će stati ako izgubi vezu s Jetsonom na duže od 500ms.
- **Kalibracija**: Prije prve vožnje provjerite smjer vrtnje motora i PWM granice u `Kretanje.cpp`.
- **Sonar**: Sonari koriste `pulseIn` funkciju koja kratko blokira (max 15ms po senzoru). Ako to uzrokuje probleme s brzim serijskim podacima, razmotrite prelazak na interrupts.
