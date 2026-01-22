# WRO 2026: Future Engineers | Tim Ctrl+Win

Dobrodošli u službeni repozitorij robotičkog tima Ctrl+Win iz Pazina. Ovaj prostor služi za razvoj, testiranje i dokumentiranje autonomnih sustava namijenjenih natjecanju World Robot Olympiad (WRO) 2026 u kategoriji Future Engineers.

## O timu

Mi smo Ctrl+Win, tim ambicioznih srednjoškolaca iz Gimnazije i strukovne škole Jurja Dobrile Pazin, okupljeni pod okriljem udruge Centar Pozitron.

Naša vizija nadilazi pobjede na natjecanjima; mi gradimo centar izvrsnosti gdje se teorijsko znanje iz matematike, fizike i informatike pretvara u opipljive mehatroničke inovacije. Naš rad karakterizira moto: "Beyond Limits".

## Kategorija: Future Engineers

WRO Future Engineers zahtijeva razvoj naprednog autonomnog vozila sposobnog za navigaciju kompleksnim poligonima bez ljudske intervencije. Izazovi uključuju:

* Autonomno kretanje: Precizno praćenje staze i izbjegavanje prepreka.
* Računalni vid: Detekcija boja (semafora) i prepoznavanje prometnih znakova u realnom vremenu.
* Inženjerska optimizacija: Balans između brzine, težine i energetske učinkovitosti hardvera.

## Tehničke specifikacije (Stack)

Naš robot koristi napredne tehnologije slične onima u našem glavnom projektu Nexus (Mars Rover):

* **Mikrokontroleri/Računala:** NVIDIA Jetson Nano / Raspberry Pi (za AI obradu) i ESP32/Arduino (za kontrolu motora).
* **Senzori:** LiDAR za 2D mapiranje okoline, ultrazvučni senzori za detekciju prepreka, te visokorezolucijske kamere.
* **Programski jezici:**
* C++ za low-level kontrolu i firmware.
* Python za algoritme računalnog vida (OpenCV) i AI modele.


* **Operativni sustav:** ROS (Robot Operating System) ili prilagođeni Linux kernel.
* **Dizajn:** 3D modeliranje šasije (Fusion 360) i 3D printanje od laganih, ali čvrstih materijala (PLA/PETG/Carbon Fiber).

## Struktura repozitorija

* `/firmware`: Kod za mikrokontrolere i upravljanje pokretačima.
* `/vision`: Algoritmi za obradu slike i prepoznavanje objekata.
* `/docs`: Tehnička dokumentacija, sheme spajanja i inženjerski dnevnik.
* `/sim`: Simulacijska okruženja za testiranje algoritama prije fizičke implementacije.

## Plan razvoja: Od Istre do Marsa

Naš put je jasno definiran:

1. **Faza 1:** Razvoj prototipa i testiranje osnovne navigacije.
2. **Faza 2:** Implementacija AI vizije i optimizacija skretanja.
3. **Faza 3:** Sudjelovanje na nacionalnim kvalifikacijama (WRO Croatia).
4. **Faza 4:** Svjetsko finale WRO 2026.

Naša stečena znanja s WRO-a direktno primjenjujemo na projekt Nexus, prvi hrvatski srednjoškolski Mars Rover namijenjen natjecanju European Rover Challenge.

## Sponzorstvo i podrška

Naš rad zahtijeva značajna sredstva za opremu (senzore, motore, AI računala) i putovanja. Ukoliko želite podržati budućnost hrvatske robotike, nudimo sponzorske pakete:

* **Perseverance:** Generalni sponzori.
* **Curiosity / Opportunity / Ingenuity:** Logotipi na robotu, odjeći i medijskim objavama.

Saznajte više na: [https://ctrlwin.centar-pozitron.hr/](https://ctrlwin.centar-pozitron.hr/)

### Kontakt:

* **Email:** ctrlwin@centar-pozitron.hr
* **Lokacija:** Pazin / Poreč, Hrvatska

*Razvijeno od strane Ctrl+Win tima.*
