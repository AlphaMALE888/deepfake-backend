# app/ml_core/hf_model.py
from transformers import AutoModelForImageClassification, AutoImageProcessor
import torch
from PIL import Image

# ------------------------------
# HUGGING FACE MODEL SETTINGS
# ------------------------------
HF_MODEL = "umarbutler/deepfake-detection"  # ✅ public + working model

# ------------------------------
# LOAD MODEL SAFELY
# ------------------------------
try:
    print(f"[HF MODEL] Loading model: {HF_MODEL} ...")
    processor = AutoImageProcessor.from_pretrained(HF_MODEL)
    model = AutoModelForImageClassification.from_pretrained(HF_MODEL)
    model.eval()
    print(f"[HF MODEL] Loaded successfully: {HF_MODEL}")
except Exception as e:
    print(f"[HF MODEL ERROR] Could not load {HF_MODEL}")
    print("Error:", str(e))
    processor = None
    model = None


# ------------------------------
# IMAGE PREDICTION FUNCTION
# ------------------------------
def hf_predict_image(image_path: str) -> float:
    """
    Predict fake probability (0–1) for a single image.
    Returns 0.0 if model is not loaded or fails.
    """
    if processor is None or model is None:
        print("[HF_MODEL] Model not loaded properly, returning 0.0")
        return 0.0

    try:
        img = Image.open(image_path).convert("RGB")
        inputs = processor(images=img, return_tensors="pt")

        with torch.no_grad():
            outputs = model(**inputs)

        probs = torch.softmax(outputs.logits, dim=1)[0]
        labels = model.config.id2label

        # Try to find “fake” label automatically
        fake_index = next(
            (i for i, lbl in labels.items() if "fake" in lbl.lower()), 1
        )

        fake_prob = float(probs[fake_index])
        print(f"[HF_MODEL] Fake probability: {fake_prob:.4f}")
        return fake_prob

    except Exception as e:
        print("[HF_MODEL] Prediction failed:", str(e))
        return 0.0
