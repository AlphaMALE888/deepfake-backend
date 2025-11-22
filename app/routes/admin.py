from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.db import ScanResult, get_db
from ..models.schemas import ScanHistoryResponse

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/history", response_model=ScanHistoryResponse)
def list_history(limit: int = 50, db: Session = Depends(get_db)):
    """
    Returns the latest deepfake analysis history (video/image/audio scans).
    - limit: number of records to return (default = 50)
    """
    try:
        # Fetch recent scan results
        items = (
            db.query(ScanResult)
            .order_by(ScanResult.created_at.desc())
            .limit(limit)
            .all()
        )

        if not items:
            raise HTTPException(status_code=404, detail="No analysis records found")

        results = [
            {
                "id": i.id,
                "filename": i.filename,
                "authenticity_score": i.authenticity_score,
                "is_fake": i.is_fake,
                "created_at": i.created_at.isoformat(),
                "user": i.user,
            }
            for i in items
        ]

        return {"history": results, "total": len(results)}

    except Exception as e:
        print("[ADMIN HISTORY ERROR]:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
