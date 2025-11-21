from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.db import ScanResult, get_db

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/history")
def list_history(limit: int = 50, db: Session = Depends(get_db)):
    # Fetch latest scan results
    items = (
        db.query(ScanResult)
        .order_by(ScanResult.created_at.desc())
        .limit(limit)
        .all()
    )

    # Format JSON response
    results = [
        {
            "id": item.id,
            "filename": item.filename,
            "score": item.authenticity_score,
            "is_fake": item.is_fake,
            "created_at": item.created_at.isoformat(),
        }
        for item in items
    ]
    
    return {"history": results, "total": len(results)}

