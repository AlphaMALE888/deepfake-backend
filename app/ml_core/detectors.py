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

def detect_face_presence(frame_path):
    img = cv2.imread(frame_path)
    if img is None:
        return False
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 4)
    return len(faces) > 0


# ------------------------------
# HUGGINGFACE API PREDICT
# ------------------------------
def hf_predict_frame(frame_path):
    """
    Sends a single frame (image file path) to HuggingFace API.
    Returns:
        score (0.0 to 1.0), method_name
        OR (None, None) if failed
    """

    if not settings.HF_TOKEN or not settings.HF_DEEPFAKE_MODEL:
        return None, None  # HF not configured

    with open(frame_path, "rb") as f:
        img_bytes = f.read()

    headers = {
        "Authorization": f"Bearer {settings.HF_TOKEN}"
    }

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{settings.HF_DEEPFAKE_MODEL}",
            headers=headers,
            data=img_bytes,
            timeout=20
        )

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                score = float(data[0].get("score", 0.5))
                return score, "hf_api"

    except Exception as e:
        print("HF API ERROR:", e)

    return None, None


# ------------------------------
# SIMPLE HEURISTIC FALLBACK
# ------------------------------
def heuristic_predict(frame_path):
    img = cv2.imread(frame_path)
    if img is None:
        return 0.5, "heuristic"

    lap = cv2.Laplacian(img, cv2.CV_64F).var()
    score = max(0.0, min(1.0, 1 - np.tanh(lap/1000)))
    return float(score), "heuristic"


# ------------------------------
# MAIN FINAL PREDICT FUNCTION
# ------------------------------
def predict_frame(frame_path):
    """
    Returns:
        (fake_probability, method_used)
    """

    # 1️⃣ Try HuggingFace API first
    score, method = hf_predict_frame(frame_path)
    if score is not None:
        return score, method

    # 2️⃣ Fallback to heuristic if HF fails
    return heuristic_predict(frame_path)



