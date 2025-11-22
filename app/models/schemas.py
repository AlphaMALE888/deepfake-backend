from pydantic import BaseModel
from typing import Optional, Any, List
import datetime

# -------------------------------------------------------
# CREATE SCHEMA (used when inserting new analysis results)
# -------------------------------------------------------
class ScanCreate(BaseModel):
    filename: str
    user: Optional[str] = "anonymous"

    class Config:
        schema_extra = {
            "example": {
                "filename": "test_video.mp4",
                "user": "anonymous"
            }
        }


# -------------------------------------------------------
# READ SCHEMA (used for API responses)
# -------------------------------------------------------
class ScanRead(BaseModel):
    id: int
    filename: str
    user: str
    created_at: datetime.datetime
    authenticity_score: float
    is_fake: int
    report: Optional[Any] = None

    class Config:
        from_attributes = True  # Pydantic v2 compatibility
        json_schema_extra = {
            "example": {
                "id": 1,
                "filename": "sample_video.mp4",
                "user": "anonymous",
                "created_at": "2025-11-22T12:30:00",
                "authenticity_score": 78.52,
                "is_fake": 1,
                "report": {
                    "audio": "./uploads/sample_audio.wav",
                    "frames_sample": [
                        {"frame": "frame_00001.jpg", "fake_prob": 0.72, "method": "hf_api", "has_face": True}
                    ],
                    "heatmap": "./uploads/sample_heatmap.jpg",
                    "frame_scores": [0.72, 0.68, 0.80]
                }
            }
        }


# -------------------------------------------------------
# MULTIPLE RECORDS RESPONSE (for admin/history endpoint)
# -------------------------------------------------------
class ScanHistoryResponse(BaseModel):
    history: List[ScanRead]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "history": [
                    {
                        "id": 1,
                        "filename": "test.mp4",
                        "authenticity_score": 54.2,
                        "is_fake": 1,
                        "created_at": "2025-11-22T09:40:00"
                    }
                ],
                "total": 1
            }
        }

