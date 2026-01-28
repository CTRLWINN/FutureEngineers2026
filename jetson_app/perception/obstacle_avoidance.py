
from config.settings import Postavke

class IzbjegavanjePrepreka:
    """
    Jednostavna logika za izbjegavanje prepreka na temelju podataka s ultrazvučnih senzora.
    """
    def __init__(self):
        self.sigurnosna_udaljenost = Postavke.SIGURNOSNA_UDALJENOST

    def provjeri_put(self, sonari):
        """
        Provjerava je li put slobodan.
        sonari: lista [lijevo, sredina, desno] u cm
        Vraća: faktor_korekcije (float) -> 1.0 (sve ok) do 0.0 (stani), i smjer izbjegavanja.
        """
        if not sonari or len(sonari) < 3:
            return 1.0, 0.0 # Nema podataka, pretpostavi da je sigurno

        lijevo, sredina, desno = sonari

        # Filtriranje šuma (0 često znači greška ili > range)
        max_dist = 200 # cm
        lijevo = lijevo if 0 < lijevo < max_dist else max_dist
        sredina = sredina if 0 < sredina < max_dist else max_dist
        desno = desno if 0 < desno < max_dist else max_dist

        min_dist = min(lijevo, sredina, desno)

        if min_dist < self.sigurnosna_udaljenost:
            print(f"PREPREKA DETEKTIRANA! Udaljenost: {min_dist} cm")
            # Ako je preblizu, stani
            if min_dist < 10:
                return 0.0, 0.0 
            
            # Odluči kamo skrenuti
            if lijevo > desno:
                return 0.5, 0.5 # Uspori i skreni desno (pozitivno) - čekaj, ako je lijevo > desno, tamo je više mjesta
                                # Zapravo, ako je lijevo (dist) > desno (dist), lijevo je slobodnije.
                                # Skretanje: -1 (lijevo), 1 (desno) ? Ovisi o konvenciji.
                                # Pretpostavimo: -1 lijevo, 1 desno.
                return 0.5, -0.8 # Skreni lijevo jako
            else:
                return 0.5, 0.8 # Skreni desno jako
        
        return 1.0, 0.0 # Sve čisto
