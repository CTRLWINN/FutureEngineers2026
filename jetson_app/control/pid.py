
import time
from config.settings import Postavke

class PIDKontroler:
    """
    PID kontroler za upravljanje skretanjem.
    """
    def __init__(self, kp=Postavke.PID_KP, ki=Postavke.PID_KI, kd=Postavke.PID_KD):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        self.p_error = 0.0
        self.i_error = 0.0
        self.d_error = 0.0
        
        self.last_error = 0.0
        self.last_time = time.time()

    def izracunaj(self, greska):
        """
        Računa izlaz PID kontrolera na temelju greške (npr. x koordinata - centar).
        """
        current_time = time.time()
        delta_time = current_time - self.last_time
        
        if delta_time <= 0:
            return 0.0

        self.p_error = greska
        self.i_error += greska * delta_time
        
        # Anti-windup (ograničenje integrala)
        self.i_error = max(min(self.i_error, 1.0), -1.0)

        self.d_error = (greska - self.last_error) / delta_time

        output = (self.kp * self.p_error) + (self.ki * self.i_error) + (self.kd * self.d_error)
        
        self.last_error = greska
        self.last_time = current_time
        
        # Ograničenje izlaza na [-1, 1]
        return max(min(output, 1.0), -1.0)
    
    def reset(self):
        self.p_error = 0.0
        self.i_error = 0.0
        self.d_error = 0.0
        self.last_error = 0.0
        self.last_time = time.time()
