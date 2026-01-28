
import cv2
import time
from config.settings import Postavke

class Kamera:
    """
    Omotač za dohvat slike s kamere (CSI ili USB).
    Koristi GStreamer pipeline za CSI kameru na Jetsonu ili običan indeks za USB.
    """
    def __init__(self, korisi_csi=False):
        self.width = Postavke.REZOLUCIJA_KAMERE[0]
        self.height = Postavke.REZOLUCIJA_KAMERE[1]
        self.fps = Postavke.FPS_KAMERE
        self.running = False
        self.cap = None

        if korisi_csi:
            self.pipeline = self._gstreamer_pipeline()
            self.source = self.pipeline
            print(f"Koristim GStreamer pipeline: {self.pipeline}")
        else:
            self.source = 0 # Default USB kamera

    def _gstreamer_pipeline(self, capture_width=1280, capture_height=720, display_width=224, display_height=224, framerate=21, flip_method=0):
        return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
        )

    def pokreni(self):
        self.cap = cv2.VideoCapture(self.source, cv2.CAP_GSTREAMER if isinstance(self.source, str) else cv2.CAP_ANY)
        if self.cap.isOpened():
            self.running = True
            print("Kamera pokrenuta.")
            return True
        else:
            print("Nije moguće otvoriti kameru.")
            return False

    def dohvati_sliku(self):
        """Vraća trenutni frame (Numpy array)."""
        if self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Ovdje možemo dodati resize ako nije odrađen u pipelineu
                if frame.shape[:2] != (self.height, self.width):
                    frame = cv2.resize(frame, (self.width, self.height))
                return frame
        return None

    def zaustavi(self):
        self.running = False
        if self.cap:
            self.cap.release()
            print("Kamera zaustavljena.")
