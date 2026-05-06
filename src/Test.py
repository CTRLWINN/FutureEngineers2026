#KOD ZA PREPOZNAVANJE BOJA
import cv2
import numpy as np

def detect_multiple_colors():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Greška: Ne mogu otvoriti kameru.")
        return

    # --- DEFINICIJA RASPONA BOJA (HSV) ---
    # Crvena boja (dva raspona jer se nalazi na krajevima HSV spektra)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Zelena boja
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([90, 255, 255])

    print("Program pokrenut. Tražim crvene i zelene objekte...")
    print("Pritisnite 'q' za izlaz.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 1. KREIRANJE MASKI
        # Maska za crvenu
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.addWeighted(mask_red1, 1.0, mask_red2, 1.0, 0.0)

        # Maska za zelenu
        mask_green = cv2.inRange(hsv, lower_green, upper_green)

        # Funkcija za obradu kontura kako ne bismo ponavljali kod
        def process_color(mask, color_bgr, label):
            # Čišćenje šuma (morfologija)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                if cv2.contourArea(contour) > 1000: # Filtriraj male objekte
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Crtanje okvira
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color_bgr, 2)
                    
                    # Ispis labele i širine u pikselima (w)
                    info_text = f"{label} w={w}px"
                    cv2.putText(frame, info_text, (x, y - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_bgr, 2)

        # 2. PROCESIRANJE OBJE BOJE
        process_color(mask_red, (0, 0, 255), "CRVENA")   # Crvena boja okvira
        process_color(mask_green, (0, 255, 0), "ZELENA") # Zelena boja okvira

        # Prikaz slike
        cv2.imshow('Detekcija Boja (Crvena i Zelena)', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_multiple_colors()
