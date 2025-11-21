from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.db import ScanResult
from ..deps import get_db

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/history")
def list_history(limit: int = 50, db: Session = Depends(get_db)):
    items = db.query(ScanResult).order_by(ScanResult.created_at.desc()).limit(limit).all()
    return [{"id": i.id, "filename": i.filename, "score": i.authenticity_score, "is_fake": i.is_fake, "created_at": str(i.created_at)} for i in items]
