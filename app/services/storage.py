import os
from app.utils.config import settings
from uuid import uuid4
from pathlib import Path
import aiofiles

# Ensure upload directory exists
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


async def save_upload_file(field, filename=None):
    """
    Saves an uploaded file asynchronously.

    - field: UploadFile object
    - filename: override name (optional)

    RETURNS:
        full saved file path
    """

    # Ensure we start from beginning of file
    await field.seek(0)

    # Extract extension safely
    ext = Path(field.filename).suffix if hasattr(field, "filename") else ".bin"
    filename = filename or f"{uuid4().hex}{ext}"

    out_path = os.path.join(settings.UPLOAD_DIR, filename)

    # Async write
    async with aiofiles.open(out_path, "wb") as f:
        content = await field.read()
        await f.write(content)

    return out_path
