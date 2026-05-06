# -- coding: utf-8 --
import cv2 # Uvozimo biblioteku OpenCV za rad sa slikom i kamerom
import time # Uvozimo biblioteku time za pauziranje i praćenje vremena
import threading # Uvozimo threading za paralelno izvođenje koda (prikaz slike i slušanje tipkovnice)
from jetracer.nvidia_racecar import NvidiaRacecar # Uvozimo klasu za upravljanje motorima i skretanjem
from pynput import keyboard # Uvozimo keyboard za prepoznavanje pritisaka tipki na tipkovnici

class WRO_Robot: # Definiramo klasu robota kako bismo organizirali kod na profesionalan način
    def __init__(self): # Inicijalizacijska funkcija koja se pokreće prilikom stvaranja objekta robota
        self.car = NvidiaRacecar() # Stvaramo objekt car koji direktno upravlja hardverom
        
        self.car.steering_offset = 0.0 # Postavljamo početno odstupanje skretanja na nulu
        self.car.steering_gain = 0.8 # Postavljamo raspon okretanja kotača (gain) na 80% maksimalnog
        self.car.throttle_gain = 0.5 # Postavljamo snagu motora na 50% radi sigurnosti
        
        self.current_throttle = 0.0 # Početna snaga kojom robot stoji na mjestu je nula
        self.throttle_step = 0.05 # Definiramo korak za povećanje ili smanjenje brzine na 5%
        self.max_throttle = 0.7 # Suštinsko ograničenje maksimalne brzine na 40% kako robot ne bi odletio
        
        self.calibration_mode = False # Robot na početku nije u modu za kalibraciju
        self.running = True # Varijabla koja drži cijeli program budnim (aktivnim)

        # Inicijalizacija kamere pomoću GStreamer funkcije koja ubrzava obradu
        self.cap = cv2.VideoCapture(self._gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER) 
        
        self.camera_thread = threading.Thread(target=self._view_camera) # Pripremamo proces za kameru
        self.camera_thread.daemon = True # Postavljamo proces u pozadinu (gasi se kad i glavni program)
        self.camera_thread.start() # Pokrećemo proces prikaza videa s kamere

        print("Robot inicijaliziran. Koristite WSAD za vožnju, SPACE za kalibraciju.") # Ispisujemo poruku korisniku

    def _gstreamer_pipeline(self, capture_width=1280, capture_height=720, display_width=640, display_height=360, framerate=30, flip_method=0): # Definiramo funkciju za postavke kamere
        return ( # Vraćamo dugački tekst (string) s postavkama koje Jetson Nano hardver razumije
            "nvarguscamerasrc ! " # Pozivamo Nvidijin driver za kameru
            "video/x-raw(memory:NVMM), " # Koristimo brzu memoriju grafičke kartice
            "width=(int)%d, height=(int)%d, " % (capture_width, capture_height) + # Postavljamo ulaznu rezoluciju
            "format=(string)NV12, framerate=(fraction)%d/1 ! " % framerate + # Određujemo broj sličica u sekundi
            "nvvidconv flip-method=%d ! " % flip_method + # Omogućujemo rotaciju slike ako je kamera naopako
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! " % (display_width, display_height) + # Smanjujemo sliku za brži prikaz
            "videoconvert ! " # Pretvaramo format boja u onaj koji OpenCV razumije
            "video/x-raw, format=(string)BGR ! appsink" # Šaljemo konačnu sliku našem programu
        ) # Završavamo GStreamer tekst

    def _view_camera(self): # Funkcija koja u beskonačnoj petlji čita sliku
        while self.running: # Vrti se sve dok je varijabla running jednaka True
            ret, frame = self.cap.read() # Čitamo jedan okvir (sliku) s kamere
            if ret: # Ako je slika uspješno pročitana
                cv2.imshow("Robot Live View", frame) # Prikazujemo sliku u novom prozoru
                if cv2.waitKey(1) & 0xFF == ord('q'): # Provjeravamo je li netko pritisnuo tipku Q u prozoru slike
                    break # Ako jest, prekidamo petlju prikaza
        self.cap.release() # Oslobađamo kameru kako bi ju drugi programi mogli koristiti
        cv2.destroyAllWindows() # Zatvaramo sve prozorčiće s videom

    def on_press(self, key): # Funkcija koja se poziva svaki put kad pritisnemo neku tipku
        try: # Pokušavamo pročitati znak tipke (npr. 'w' ili 'a')
            k = key.char # Spremamo znak tipke u varijablu k
        except AttributeError: # Ako tipka nema znak (npr. Space ili Enter)
            k = key.name # Čitamo njeno ime

        if k == 'space': # Ako je pritisnuta razmaknica
            self.calibration_mode = not self.calibration_mode # Mijenjamo stanje kalibracije (pali/gasi)
            status = "UKLJUČEN" if self.calibration_mode else "ISKLJUČEN" # Spremamo riječ ovisno o stanju
            print(f"\n--- Mod kalibracije: {status} ---") # Ispisujemo korisniku je li mod aktivan
            if not self.calibration_mode: # Ako izlazimo iz kalibracije
                print(f"Spremljen offset: {self.car.steering_offset}") # Ispisujemo trenutni offset
            return # Prekidamo izvršavanje ove funkcije za ovu tipku

        if self.calibration_mode: # Provjeravamo je li robot u modu za kalibraciju
            if k == 'o': # Ako je pritisnuto slovo O
                self.car.steering_offset -= 0.01 # Pomičemo kotače malo ulijevo
                print(f"Offset: {self.car.steering_offset:.2f}") # Ispisujemo novu vrijednost na ekran
            elif k == 'p': # Ako je pritisnuto slovo P
                self.car.steering_offset += 0.01 # Pomičemo kotače malo udesno
                print(f"Offset: {self.car.steering_offset:.2f}") # Ispisujemo novu vrijednost na ekran
            elif k == 'enter': # Ako je pritisnuta tipka Enter
                self.calibration_mode = False # Izlazimo iz moda kalibracije
                print(f"Kalibracija završena. Finalni offset: {self.car.steering_offset:.2f}") # Potvrđujemo završetak
        else: # Ako nismo u kalibraciji, znači da vozimo
            if k == 'w': # Ako pritisnemo W
                self.car.throttle = self.current_throttle if self.current_throttle != 0 else 0.5 # Pokrećemo robota naprijed brzinom current_throttle
            elif k == 's': # Ako pritisnemo S
                self.car.throttle = -0.5 # Šaljemo jači signal kako bismo probili ESC mrtvu zonu
            elif k == 'a': # Ako pritisnemo A
                self.car.steering = 1.0 # Skrećemo kotače maksimalno ulijevo
            elif k == 'd': # Ako pritisnemo D
                self.car.steering = -1.0 # Skrećemo kotače maksimalno udesno
            elif k in ['plus', '+', '=']: # Ako želimo povećati brzinu
                self.current_throttle = min(self.max_throttle, self.current_throttle + self.throttle_step) # Povećavamo gas, ali pazimo da ne pređe maksimum
                print(f"Snaga motora: {self.current_throttle:.2f}") # Ispisujemo novu brzinu
            elif k in ['minus', '-']: # Ako želimo smanjiti brzinu
                self.current_throttle = max(0.0, self.current_throttle - self.throttle_step) # Smanjujemo gas, ali pazimo da ne padne ispod nule
                print(f"Snaga motora: {self.current_throttle:.2f}") # Ispisujemo novu brzinu

    def on_release(self, key): # Funkcija koja se poziva kad pustimo pritisnutu tipku
        # 1. Prvo moramo prepoznati koju smo tipku točno pustili (kao u on_press)
        try: 
            k = key.char
        except AttributeError:
            k = key.name

        # 2. Reagiramo samo na specifične tipke
        if not self.calibration_mode:
            if k in ['w', 's']: # Ako smo pustili naprijed ili nazad
                self.car.throttle = 0.0 # Zaustavi motor
                
            if k in ['a', 'd']: # Ako smo pustili lijevo ili desno
                self.car.steering = 0.0 # Vrati kotače ravno
        
        # 3. Gašenje programa na ESC
        if key == keyboard.Key.esc: 
            self.running = False 
            return False

    def run(self): # Glavna funkcija koja pokreće upravljanje
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener: # Pokrećemo proces koji osluškuje tipkovnicu
            listener.join() # Čekamo da proces završi (dok ne stisnemo Escape)

if __name__ == "__main__": # Provjeravamo jesmo li skriptu pokrenuli direktno
    robot = WRO_Robot() # Stvaramo našeg robota iz klase
    try: # Pokušavamo izvršiti blok koda ispod
        robot.run() # Pokrećemo glavnu petlju programa
    except KeyboardInterrupt: # Ako korisnik u terminalu pritisne Ctrl+C
        print("Program prekinut.") # Ispisujemo poruku o prekidu
    finally: # Bez obzira na to kako program završi (normalno ili greškom)
        robot.car.throttle = 0.0 # Relevantno je ugasiti motore kako robot ne bi nastavio voziti
        robot.running = False # Gasimo sve procese

