
# config/settings.py
# Postavke za robota - konstante i konfiguracija

class Postavke:
    # Serijska komunikacija
    SERIJSKI_PORT = "/dev/ttyUSB0"  # Prilagoditi po potrebi (npr. COM3 na Windowsima za test)
    BAUD_RATE = 115200
    TIMEOUT = 1  # sekunde

    # Kamera
    REZOLUCIJA_KAMERE = (224, 224)  # Standardno za ResNet
    FPS_KAMERE = 21

    # PID Kontroler (Početne vrijednosti, potrebno tuniranje)
    PID_KP = 0.1
    PID_KI = 0.0
    PID_KD = 0.05

    # Vožnja
    OSNOVNA_BRZINA = 0.2  # 0.0 do 1.0
    MAX_BRZINA = 0.5
    SIGURNOSNA_UDALJENOST = 20.0  # cm

    # Putanje modela
    PUTANJA_MODELA = "models/best_steering_model_xy.pth"
