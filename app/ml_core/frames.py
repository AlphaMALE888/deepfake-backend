import cv2
import os

def extract_frames(video_path: str, output_folder: str, fps: int = 1):
    """
    Extract frames from a video file at the specified FPS.
    Returns a list of saved frame paths.
    """
    try:
        os.makedirs(output_folder, exist_ok=True)

        vidcap = cv2.VideoCapture(video_path)
        if not vidcap.isOpened():
            print(f"[FRAME EXTRACTION ERROR] Could not open video: {video_path}")
            return []

        original_fps = vidcap.get(cv2.CAP_PROP_FPS)
        if not original_fps or original_fps <= 0:
            original_fps = fps  # fallback to user FPS

        frame_interval = max(1, int(round(original_fps / fps)))

        frames = []
        count = 0
        saved = 0

        while True:
            success, frame = vidcap.read()
            if not success:
                break

            if count % frame_interval == 0:
                frame_path = os.path.join(output_folder, f"frame_{saved:05d}.jpg")
                success_write = cv2.imwrite(frame_path, frame)
                if success_write:
                    frames.append(frame_path)
                    saved += 1
            count += 1

        vidcap.release()

        print(f"[FRAME EXTRACTION] {saved} frames extracted from {video_path}")
        return frames

    except Exception as e:
        print("[FRAME EXTRACTION FAILED]:", str(e))
        return []
