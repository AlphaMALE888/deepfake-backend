import librosa
import numpy as np

def analyze_audio_features(wav_path):
    try:
        y, sr = librosa.load(wav_path, sr=16000, mono=True)
    except Exception as e:
        return {"error":"librosa load failed", "detail": str(e)}
    energy = float(np.mean(y**2))
    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = mfcc.mean(axis=1).tolist()
    return {"energy": energy, "zcr": zcr, "mfcc_mean": mfcc_mean}
