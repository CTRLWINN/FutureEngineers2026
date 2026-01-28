
import torch
import torchvision.transforms as transforms
import cv2
import numpy as np
from config.settings import Postavke
import os

class AIInferencija:
    """
    Klasa za učitavanje PyTorch modela i predikciju koordinata (x, y) za vožnju.
    """
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.mean = torch.Tensor([0.485, 0.456, 0.406]).to(self.device)
        self.std = torch.Tensor([0.229, 0.224, 0.225]).to(self.device)
        
        self._ucitaj_model()

    def _ucitaj_model(self):
        try:
            putanja = Postavke.PUTANJA_MODELA
            if os.path.exists(putanja):
                # Pretpostavka: Koristimo ResNet18 model prilagođen za regresiju (izlaz x, y)
                from torchvision.models import resnet18
                self.model = resnet18(pretrained=False)
                self.model.fc = torch.nn.Linear(512, 2) # x, y izlaz
                self.model.load_state_dict(torch.load(putanja))
                self.model = self.model.to(self.device)
                self.model = self.model.eval().half() # Optimizacija za Jetson (FP16)
                print(f"Model uspješno učitan s {putanja}")
            else:
                print(f"Upozorenje: Model nije pronađen na {putanja}. Koristim dummy mod.")
        except Exception as e:
            print(f"Greška pri učitavanju modela: {e}")

    def obradi_sliku(self, slika):
        """Preprocesiranje slike za model."""
        slika = cv2.cvtColor(slika, cv2.COLOR_BGR2RGB)
        slika = slika.transpose((2, 0, 1)) # HWC -> CHW
        slika = torch.from_numpy(slika).float().to(self.device)
        slika = slika.half() # FP16
        slika = slika / 255.0
        slika = slika.sub(self.mean[:, None, None]).div(self.std[:, None, None])
        return slika[None, ...] # Dodaj batch dimenziju

    def predvidi(self, slika):
        """Vraća predviđene koordinate (x, y)."""
        if self.model is None:
            return 0.0, 0.0 # Dummy vrijednosti ako modela nema

        try:
            tensor_slike = self.obradi_sliku(slika)
            with torch.no_grad():
                izlaz = self.model(tensor_slike)
            xy = izlaz.cpu().numpy().flatten()
            return xy[0], xy[1] # x (skretanje), y (throttle/brzina - opcionalno)
        except Exception as e:
            print(f"Greška pri inferenciji: {e}")
            return 0.0, 0.0
