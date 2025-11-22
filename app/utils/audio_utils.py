import librosa
import numpy as np

def analyze_audio_features(wav_path: str) -> dict:
    """
    Analyze an audio file (.wav) and extract useful features.
    
    Returns a dictionary with:
      - energy: average signal energy
      - zcr: zero crossing rate
      - mfcc_mean: mean MFCC coefficients
      - fake_score: heuristic 'fake probability' (0–100)
    """
    try:
        # Load audio safely
        y, sr = librosa.load(wav_path, sr=16000, mono=True)
    except Exception as e:
        return {
            "error": "Audio load failed",
            "detail": str(e),
            "path": wav_path
        }

    if y is None or len(y) == 0:
        return {"error": "Empty audio file", "path": wav_path}

    # 🎵 Feature Extraction
    energy = float(np.mean(y ** 2))                        # signal power
    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))  # noise/variation
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = mfcc.mean(axis=1).tolist()

    # ⚙️ Heuristic fake score (placeholder logic)
    # In real model, you'd pass these features into an ML classifier
    fake_score = round(min(100.0, (energy * 10000 + zcr * 100)), 2)

    return {
        "energy": round(energy, 6),
        "zcr": round(zcr, 6),
        "mfcc_mean": [round(x, 4) for x in mfcc_mean],
        "fake_score": fake_score,
        "status": "analyzed"
    }

