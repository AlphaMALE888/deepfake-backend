import cv2
import os

def extract_frames(video_path, output_folder, fps=1):
    os.makedirs(output_folder, exist_ok=True)

    vidcap = cv2.VideoCapture(video_path)
    original_fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(original_fps / fps) if original_fps > 0 else 1

    frames = []
    count = 0
    saved = 0

    while True:
        success, frame = vidcap.read()
        if not success:
            break

        if count % frame_interval == 0:
            frame_path = os.path.join(output_folder, f"frame_{saved}.jpg")
            cv2.imwrite(frame_path, frame)
            frames.append(frame_path)
            saved += 1

        count += 1

    vidcap.release()
    return frames
