
import os
import cv2
import time
import uuid
import json

class Utils:
    
    @staticmethod
    def spremi_sliku_i_podatke(slika, x, y, direktorij="data/dataset"):
        """Sprema sliku i JSON labelu za trening."""
        if not os.path.exists(direktorij):
            os.makedirs(direktorij)
            
        timestamp = int(time.time() * 1000)
        u_id = str(uuid.uuid4())[:8]
        ime_slike = f"{timestamp}_{u_id}.jpg"
        full_path = os.path.join(direktorij, ime_slike)
        
        cv2.imwrite(full_path, slika)
        
        # Spremi i labelu kao ime slike ili u json (ovdje koristimo ime slike konvenciju xy_...)
        # Alternativno, bolji pristup je xy_timestamp.jpg 
        # Ali za ovaj projekt, napravimo jednostavan log file
        return ime_slike

    @staticmethod
    def kreiraj_direktorije():
        dirs = ["data/dataset", "models", "logs"]
        for d in dirs:
            if not os.path.exists(d):
                os.makedirs(d)
                print(f"Kreiran direktorij: {d}")
