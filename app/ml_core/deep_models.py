import subprocess
import os
from ..config import settings

def run_deepfacelive_check(video_path, out_json):
    if not settings.ENABLE_DEEPFACELIVE:
        return {"status":"disabled"}
    cmd = [
        "python", "external_tools/deepfacelive_check.py",
        "--video", video_path,
        "--out", out_json
    ]
    try:
        subprocess.run(cmd, check=True, timeout=900)
        import json
        with open(out_json, "r") as f:
            return json.load(f)
    except Exception as e:
        return {"status":"error","detail": str(e)}
