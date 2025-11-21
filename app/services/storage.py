import os
from ..config import settings
from uuid import uuid4
from pathlib import Path
import aiofiles

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

async def save_upload_file(field, filename=None):
    ext = Path(field.filename).suffix if hasattr(field, "filename") else ".bin"
    filename = filename or f"{uuid4().hex}{ext}"
    out_path = os.path.join(settings.UPLOAD_DIR, filename)
    async with aiofiles.open(out_path, "wb") as f:
        content = await field.read()
        await f.write(content)
    return out_path
