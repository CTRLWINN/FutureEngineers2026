
import serial
import json
import threading
import time
from config.settings import Postavke

class SerijskoSucelje:
    """
    Klasa za rukovanje serijskom komunikacijom s ESP32.
    Koristi zasebnu dretvu za čitanje podataka kako ne bi blokirala glavni program.
    """
    def __init__(self):
        self.port = Postavke.SERIJSKI_PORT
        self.baud = Postavke.BAUD_RATE
        self.serial_conn = None
        self.running = False
        self.zadnji_podaci = {"imu": {}, "sonar": []}
        self.lock = threading.Lock()

    def spoji(self):
        """Otvara serijsku vezu."""
        try:
            self.serial_conn = serial.Serial(self.port, self.baud, timeout=Postavke.TIMEOUT)
            self.running = True
            # Pokreni dretvu za čitanje
            self.thread = threading.Thread(target=self._citaj_petlja)
            self.thread.daemon = True
            self.thread.start()
            print(f"Serijska veza uspostavljena na {self.port}")
            return True
        except serial.SerialException as e:
            print(f"Greška pri spajanju na serijski port: {e}")
            return False

    def _citaj_petlja(self):
        """Unutarnja petlja koja se vrti u pozadini i čita podatke."""
        while self.running and self.serial_conn.is_open:
            try:
                if self.serial_conn.in_waiting > 0:
                    linija = self.serial_conn.readline().decode('utf-8').strip()
                    if linija:
                        try:
                            podaci = json.loads(linija)
                            with self.lock:
                                self.zadnji_podaci = podaci
                        except json.JSONDecodeError:
                            # Ponekad podaci mogu biti korumpirani
                            pass
            except Exception as e:
                print(f"Greška u čitanju serijskih podataka: {e}")
                time.sleep(0.1)

    def posalji_komandu(self, brzina, kut_skretanja):
        """
        Šalje komandu na ESP32 u JSON formatu.
        brzina: float (-1.0 do 1.0)
        kut_skretanja: float (-1.0 do 1.0, gdje je 0 ravno)
        """
        if self.serial_conn and self.serial_conn.is_open:
            komanda = {
                "T": round(brzina, 3),  # Throttle
                "S": round(kut_skretanja, 3)  # Steering
            }
            json_str = json.dumps(komanda) + '\n'
            try:
                self.serial_conn.write(json_str.encode('utf-8'))
            except Exception as e:
                print(f"Greška pri slanju: {e}")

    def dohvati_podatke(self):
        """Vraća zadnje pročitane podatke (IMU, Sonar)."""
        with self.lock:
            return self.zadnji_podaci.copy()

    def zaustavi(self):
        """Zatvara vezu i zaustavlja dretvu."""
        self.running = False
        if self.serial_conn:
            self.serial_conn.close()
            print("Serijska veza zatvorena.")
