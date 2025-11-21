from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException
from ..services.storage import save_upload_file
from ..utils.video_utils import extract_audio_from_video, extract_frames
from ..ml_core.detectors import x_detector, heuristic_frame_artifact_score, detect_face_presence
from ..utils.heatmap import create_heatmap_from_scores
from ..models.db import ScanResult
from ..deps import get_db
from ..config import settings
from sqlalchemy.orm import Session
import os

router = APIRouter(prefix="/analyze", tags=["analyze"])

def run_full_pipeline(video_path, db_session: Session, filename: str):
    # audio extraction
    audio_path = video_path + ".wav"
    try:
        extract_audio_from_video(video_path, audio_path)
    except Exception as e:
        audio_path = None

    # frames
    frames_dir = video_path + "_frames"
    frames = extract_frames(video_path, frames_dir, fps=1)

    frame_scores = []
    frame_results = []
    for f in frames:
        heur = heuristic_frame_artifact_score(f)
        xres = x_detector.predict_frame(f)
        has_face = detect_face_presence(f)
        fake_prob = float(xres.get("fake_prob", 0.0))
        combined = (fake_prob * 0.6) + ((heur/100.0) * 0.3) + (0.1 if not has_face else 0)
        frame_scores.append(combined)
        frame_results.append({"frame": f, "fake_prob": fake_prob, "heur": heur, "has_face": has_face})

    overall_score = float(max(0.0, min(100.0, 100*(sum(frame_scores)/len(frame_scores))))) if frame_scores else 0.0
    is_fake = 1 if overall_score > 50 else 0

    heatmap_path = os.path.join(settings.UPLOAD_DIR, f"{os.path.basename(video_path)}_heatmap.jpg")
    create_heatmap_from_scores(frames, frame_scores, heatmap_path)

    report = {
        "audio": audio_path,
        "frames_sample": frame_results[:10],
        "heatmap": heatmap_path,
        "frame_scores": frame_scores
    }

    sr = ScanResult(filename=filename, user="anonymous", authenticity_score=overall_score, is_fake=is_fake, report=report)
    db_session.add(sr)
    db_session.commit()
    db_session.refresh(sr)
    return {"id": sr.id, "authenticity_score": overall_score, "is_fake": is_fake, "heatmap": heatmap_path}

@router.post("/video")
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(get_db)):
    path = await save_upload_file(file)
    background_tasks.add_task(run_full_pipeline, path, db, os.path.basename(path))
    return {"message":"Uploaded and processing in background", "path": path}
