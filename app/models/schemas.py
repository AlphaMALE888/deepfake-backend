from pydantic import BaseModel
from typing import Optional, Any
import datetime

# -------------------------------------------
# CREATE SCHEMA (not heavily used but good to keep)
# -------------------------------------------
class ScanCreate(BaseModel):
    filename: str
    user: Optional[str] = "anonymous"


# -------------------------------------------
# READ SCHEMA FOR API RESPONSES
# -------------------------------------------
class ScanRead(BaseModel):
    id: int
    filename: str
    user: str
    created_at: datetime.datetime
    authenticity_score: float
    is_fake: int
    report: Optional[Any]

    class Config:
        from_attributes = True   # <-- SUPER IMPORTANT FIX
