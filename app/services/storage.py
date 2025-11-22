import os
from app.utils.config import settings
from uuid import uuid4
from pathlib import Path
import aiofiles

# Ensure upload directory exists
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


async def save_upload_file(field, filename: str = None) -> str:
    """
    Asynchronously saves an uploaded file.

    Args:
        field: FastAPI UploadFile object.
        filename (str, optional): Custom name to save the file with.

    Returns:
        str: Full saved file path.
    """
    try:
        # Ensure file starts reading from beginning
        await field.seek(0)

        # Extract safe extension
        ext = Path(field.filename).suffix if hasattr(field, "filename") else ".bin"
        filename = filename or f"{uuid4().hex}{ext}"

        out_path = os.path.join(settings.UPLOAD_DIR, filename)

        # Asynchronous file write
        async with aiofiles.open(out_path, "wb") as f:
            while chunk := await field.read(1024 * 1024):  # write in 1MB chunks
                await f.write(chunk)

        print(f"[STORAGE] File saved at: {out_path}")
        return out_path

    except Exception as e:
        print("[STORAGE ERROR]:", e)
        raise RuntimeError(f"Failed to save upload file: {str(e)}")
