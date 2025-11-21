import subprocess
import os

def extract_audio_from_video(video_path, audio_path):
    try:
        # Convert backslashes to forward-slashes (Windows fix)
        safe_video = video_path.replace("\\", "/")
        safe_audio = audio_path.replace("\\", "/")

        cmd = [
            "ffmpeg",
            "-y",
            "-i", safe_video,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            safe_audio
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            print("FFMPEG ERROR:", result.stderr.decode())
            return None

        print("Audio extracted successfully:", safe_audio)
        return safe_audio

    except Exception as e:
        print("Audio extractor failed:", e)
        return None
