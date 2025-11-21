import ffmpeg
import os
import cv2

def extract_audio_from_video(video_path, out_audio):
    try:
        (
            ffmpeg
            .input(video_path)
            .output(out_audio, acodec='pcm_s16le', ac=1, ar='16000')
            .overwrite_output()
            .run(quiet=True)
        )
    except Exception as e:
        raise e
    return out_audio

def extract_frames(video_path, out_dir, fps=1):
    os.makedirs(out_dir, exist_ok=True)
    vidcap = cv2.VideoCapture(video_path)
    if not vidcap.isOpened():
        return []
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_fps = vidcap.get(cv2.CAP_PROP_FPS) or fps
    step = max(1, int(round(video_fps / fps))) if video_fps>0 else 1
    extracted = []
    count = 0
    saved = 0
    while True:
        success, image = vidcap.read()
        if not success:
            break
        if count % step == 0:
            p = os.path.join(out_dir, f"frame_{saved:06d}.jpg")
            cv2.imwrite(p, image)
            extracted.append(p)
            saved += 1
        count += 1
    vidcap.release()
    return extracted
