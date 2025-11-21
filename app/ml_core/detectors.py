import numpy as np
import cv2
import os
from PIL import Image
import torch
import torchvision.transforms as transforms
from ..config import settings

def heuristic_frame_artifact_score(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return 0.0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_64F).var()
    # scale to 0..100 (rough)
    score = max(0, min(100, 100 - lap/10))
    return float(score)

def detect_face_presence(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return False
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray, 1.1, 4)
    return len(faces) > 0

class XceptionDetector:
    def __init__(self, model_path=None, device='cpu'):
        self.device = device
        self.model = None
        if model_path and os.path.exists(model_path):
            try:
                self.model = torch.load(model_path, map_location=device)
                self.model.eval()
            except Exception as e:
                print("Failed loading Xception model:", e)
        self.transform = transforms.Compose([
            transforms.Resize((299,299)),
            transforms.ToTensor(),
            transforms.Normalize([0.5,0.5,0.5],[0.5,0.5,0.5])
        ])

    def predict_frame(self, img_path):
        if not self.model:
            return {"fake_prob": heuristic_frame_artifact_score(img_path)/100.0}
        try:
            img = Image.open(img_path).convert("RGB")
            x = self.transform(img).unsqueeze(0).to(self.device)
            with torch.no_grad():
                out = self.model(x)
                # model output expected logits for 2 classes; adjust as needed
                probs = torch.softmax(out, dim=1).cpu().numpy()[0]
                fake_prob = float(probs[1])
                return {"fake_prob": fake_prob}
        except Exception as e:
            return {"fake_prob": 0.0, "error": str(e)}

# instantiate
x_detector = XceptionDetector(model_path=settings.ML_MODEL_PATH, device='cpu')
