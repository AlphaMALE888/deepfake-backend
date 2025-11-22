import os
import shutil
from fastapi import APIRouter, UploadFile, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.models.db import SessionLocal, ScanResult
from app.ml_core.frames import extract_frames
from app.ml_core.audio import extract_audio_from_video
from app.ml_core.heatmap import create_heatmap_from_scores
from app.ml_core.detectors import predict_frame, detect_face_presence
from app.utils.config import settings
from app.ml_core.hf_model import hf_predict_image
from app.utils.audio_utils import analyze_audio_features

router = APIRouter()

UPLOAD_DIR = settings.UPLOAD_DIR
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------------------------------------------
# BACKGROUND VIDEO ANALYSIS PIPELINE
# -------------------------------------------------------
def run_full_pipeline(video_path: str, db: Session, filename: str):
    try:
        print(f"[PIPELINE] Starting analysis for {filename}")

        # 1️⃣ Extract audio
        audio_path = video_path + "_audio.wav"
        extracted_audio = extract_audio_from_video(video_path, audio_path)

        # 2️⃣ Extract frames
        frames_dir = video_path + "_frames"
        frames = extract_frames(video_path, frames_dir, fps=1)

        if not frames:
            print("⚠️ No frames extracted — skipping analysis.")
            return

        frame_scores = []
        frame_results = []

        # 3️⃣ Analyze each frame
        for frame_path in frames:
            score, method = predict_frame(frame_path)
            has_face = detect_face_presence(frame_path)
            frame_scores.append(score)
            frame_results.append({
                "frame": os.path.basename(frame_path),
                "fake_prob": score,
                "method": method,
                "has_face": has_face
            })

        # 4️⃣ Compute authenticity score
        overall_score = float(100 * (sum(frame_scores) / len(frame_scores))) if frame_scores else 0.0
        is_fake = 1 if overall_score > 50 else 0

        # 5️⃣ Generate HEATMAP
        heatmap_path = os.path.join(UPLOAD_DIR, f"{os.path.basename(video_path)}_heatmap.jpg")
        create_heatmap_from_scores(frames, frame_scores, heatmap_path)

        # 6️⃣ Analyze audio features (optional)
        audio_features = None
        if extracted_audio and os.path.exists(extracted_audio):
            audio_features = analyze_audio_features(extracted_audio)

        # 7️⃣ Build report
        report = {
            "audio": extracted_audio,
            "audio_features": audio_features,
            "frames_sample": frame_results[:20],
            "heatmap": heatmap_path,
            "frame_scores": frame_scores
        }

        # 8️⃣ Save to DB
        record = ScanResult(
            filename=filename,
            user="anonymous",
            authenticity_score=overall_score,
            is_fake=is_fake,
            report=report
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        print(f"✅ SCAN COMPLETED — ID: {record.id}")

    except Exception as e:
        print("❌ PIPELINE FAILED:", e)
        raise e

    finally:
        db.close()


# -------------------------------------------------------
# VIDEO ANALYSIS ENDPOINT
# -------------------------------------------------------
@router.post("/analyze/video")
async def analyze_video(file: UploadFile, background_tasks: BackgroundTasks):
    try:
        out_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(out_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        db = SessionLocal()
        background_tasks.add_task(run_full_pipeline, out_path, db, file.filename)

        return {"message": "Video uploaded successfully — processing started.", "file_saved_as": out_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video analysis failed: {e}")


# -------------------------------------------------------
# IMAGE ANALYSIS ENDPOINT
# -------------------------------------------------------
@router.post("/analyze/image")
async def analyze_image(file: UploadFile):
    try:
        path = os.path.join(UPLOAD_DIR, file.filename)
        with open(path, "wb") as f:
            f.write(await file.read())

        fake_prob = hf_predict_image(path)
        return {"filename": file.filename, "fake_prob_percent": round(fake_prob * 100, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image analysis failed: {e}")


# -------------------------------------------------------
# AUDIO ANALYSIS ENDPOINT
# -------------------------------------------------------
@router.post("/analyze/audio")
async def analyze_audio(file: UploadFile):
    try:
        path = os.path.join(UPLOAD_DIR, file.filename)
        with open(path, "wb") as f:
            f.write(await file.read())

        features = analyze_audio_features(path)
        return {"filename": file.filename, "audio_features": features}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio analysis failed: {e}")
