from pydantic import BaseModel
from typing import Optional, Any
import datetime

class ScanCreate(BaseModel):
    filename: str
    user: Optional[str] = "anonymous"

class ScanRead(BaseModel):
    id: int
    filename: str
    user: str
    created_at: datetime.datetime
    authenticity_score: float
    is_fake: int
    report: Optional[Any]
