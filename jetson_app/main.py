
import time
import signal
import sys
from config.settings import Postavke
from drivers.serial_interface import SerijskoSucelje
from drivers.camera import Kamera
from perception.ai_inference import AIInferencija
from perception.obstacle_avoidance import IzbjegavanjePrepreka
from control.pid import PIDKontroler
from utils.utils import Utils

def signal_handler(sig, frame):
    print("\nPrekidam program... Zaustavljanje robota.")
    global running
    running = False

signal.signal(signal.SIGINT, signal_handler)

running = True

def main():
    print("Inicijalizacija Jetson Nano Robota...")
    Utils.kreiraj_direktorije()

    # Inicijalizacija modula
    serija = SerijskoSucelje()
    if not serija.spoji():
        print("Ne mogu otvoriti serijski port. Nastavljam u debug modu bez motora.")
    
    kamera = Kamera(korisi_csi=True) # Postavi na False za USB kameru lokalno
    if not kamera.pokreni():
        print("Ne mogu pokrenuti kameru. Izlazim.")
        return

    ai = AIInferencija()
    izbjegavanje = IzbjegavanjePrepreka()
    pid = PIDKontroler()

    print("Sustav spreman. Počinjem glavnu petlju.")

    while running:
        start_time = time.time()

        # 1. Percepcija
        slika = kamera.dohvati_sliku()
        if slika is None:
            continue

        # AI predikcija
        x_pred, y_pred = ai.predvidi(slika)
        
        # Čitanje senzora s ESP32
        senzori = serija.dohvati_podatke()
        sonari = senzori.get("dist", []) # Očekujemo [L, C, R]
        
        # 2. Sigurnosna provjera (Obstacle Avoidance)
        faktor_brzine, korekcija_smjera = izbjegavanje.provjeri_put(sonari)

        # 3. Kontrola
        # PID izračun skretanja
        # Cilj je x=0 (sredina slike je x=0, lijevo -1, desno 1, ili ovisno o treningu)
        # Ovdje pretpostavljamo da model vraća x u rangeu [-1, 1] gdje je 0 ravno.
        # Ako model vraća pixele, treba normalizirati.
        # Uzmimo da model vraća normalizirane vrijednosti.
        
        # Kombiniraj AI odluku i Obstacle avoidance
        if korekcija_smjera != 0.0:
            # Prepreka ima prioritet
            konacni_kut = korekcija_smjera
            konacna_brzina = Postavke.OSNOVNA_BRZINA * faktor_brzine
        else:
            # AI vozi
            steering_output = pid.izracunaj(x_pred) # PID na grešku
            # Ili direktno koristi x_pred ako je model dobro treniran
            konacni_kut = x_pred 
            konacna_brzina = Postavke.OSNOVNA_BRZINA

        # 4. Aktuacija (Slanje na ESP32)
        serija.posalji_komandu(konacna_brzina, konacni_kut)

        # Trpaj u log/debug
        # print(f"AI: {x_pred:.2f}, Sonar: {p_speed:.2f}, Out: {final_throttle:.2f}/{final_steering:.2f}")

        # Održavanje FPS-a
        sleep_time = 0.05 - (time.time() - start_time)
        if sleep_time > 0:
            time.sleep(sleep_time)

    # Cleanup
    serija.posalji_komandu(0, 0) # Zaustavi motore
    time.sleep(0.5)
    serija.zaustavi()
    kamera.zaustavi()
    print("Program završen.")

if __name__ == "__main__":
    main()
