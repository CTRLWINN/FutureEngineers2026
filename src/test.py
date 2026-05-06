#TEST BEZ KRIŽA
import cv2
import numpy as np

def detect_and_label_objects():
    # Pokretanje kamere
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Greška: Ne mogu otvoriti kameru.")
        return

    # --- KONSTANTE ---
    W_STVARNA = 6.0        # Stvarna širina predmeta u cm
    FOKALNA = 650          # Tvoja kalibrirana fokalna duljina
    
    # Raspon zelene boje u HSV-u
    LOWER_GREEN = np.array([40, 40, 40])
    UPPER_GREEN = np.array([90, 255, 255])

    while True:
        ret, frame = cap.read()
        if not ret: 
            break

        # Pretvorba u HSV i kreiranje maske
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
        
        # Pronalaženje kontura
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Filtriranje malih šumova (samo objekti veći od 1000 piksela)
            if cv2.contourArea(contour) > 1000:
                x, y, w, h = cv2.boundingRect(contour)
                
                # --- IZRAČUN UDALJENOSTI (DUBINA) ---
                # Formula: (Stvarna širina * Fokalna duljina) / Širina u pikselima
                udaljenost_cm = (W_STVARNA * FOKALNA) / w

                # --- CRTANJE ---
                # Zeleni okvir oko detektiranog predmeta
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Prikaz izračunate udaljenosti iznad okvira
                cv2.putText(frame, f"UDALJENOST: {udaljenost_cm:.1f} cm", (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Prikaz prozora
        cv2.imshow('Detekcija udaljenosti', frame)
        
        # Izlaz na tipku 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_and_label_objects()
