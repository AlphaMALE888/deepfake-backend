import cv2
import numpy as np
import requests
from ..utils.config import settings

# ------------------------------
# FACE PRESENCE DETECTION
# ------------------------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def detect_face_presence(frame_path: str) -> bool:
    """Check if any face is present in the given frame."""
    try:
        img = cv2.imread(frame_path)
        if img is None:
            return False
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 4)
        return len(faces) > 0
    except Exception as e:
        print("[FACE DETECTION ERROR]:", e)
        return False


# ------------------------------
# HUGGINGFACE API PREDICT
# ------------------------------
def hf_predict_frame(frame_path: str):
    """
    Sends a frame image to HuggingFace API.
    Returns:
        (fake_score [0..1], "hf_api") if success,
        (None, None) if failed.
    """
    model_id = settings.HF_DEEPFAKE_MODEL or "umarbutler/deepfake-detection"
    headers = {}
    if settings.HF_TOKEN:
        headers["Authorization"] = f"Bearer {settings.HF_TOKEN}"

    try:
        with open(frame_path, "rb") as f:
            img_bytes = f.read()

        response = requests.post(
            f"https://api-inference.huggingface.co/models/{model_id}",
            headers=headers,
            data=img_bytes,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                # Try to find label with "fake"
                fake_prob = None
                for item in data:
                    if "fake" in str(item.get("label", "")).lower():
                        fake_prob = float(item.get("score", 0.0))
                        break
                if fake_prob is None:
                    fake_prob = float(max(x.get("score", 0.0) for x in data))
                return fake_prob, "hf_api"

        print("[HF API] Unexpected response:", response.status_code, response.text)
        return None, None

    except Exception as e:
        print("[HF API ERROR]:", e)
        return None, None


# ------------------------------
# SIMPLE HEURISTIC FALLBACK
# ------------------------------
def heuristic_predict(frame_path: str):
    """
    Simple fallback when HuggingFace API fails.
    Uses image sharpness as heuristic score.
    """
    try:
        img = cv2.imread(frame_path)
        if img is None:
            return 0.5, "heuristic"

        lap = cv2.Laplacian(img, cv2.CV_64F).var()
        score = max(0.0, min(1.0, 1 - np.tanh(lap / 1000)))
        return float(score), "heuristic"
    except Exception as e:
        print("[HEURISTIC ERROR]:", e)
        return 0.5, "heuristic"


# ------------------------------
# MAIN PREDICTION FUNCTION
# ------------------------------
def predict_frame(frame_path: str):
    """Main unified prediction entry."""
    hf_score, method = hf_predict_frame(frame_path)
    if hf_score is not None:
        return hf_score, method
    return heuristic_predict(frame_path)




