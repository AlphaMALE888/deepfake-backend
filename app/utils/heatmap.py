import cv2
import numpy as np
import os

def create_heatmap_from_scores(frames, scores, out_path, alpha=0.6):
    # generate grid of top frames with overlays
    if not frames:
        return None
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:6]
    thumbs = []
    for i in top_idx:
        img = cv2.imread(frames[i])
        if img is None:
            continue
        h,w = img.shape[:2]
        overlay = np.zeros_like(img, dtype=np.uint8)
        val = int(min(255, max(0, scores[i]*255)))
        overlay[:] = (val, 0, 255-val)  # visual gradient
        blended = cv2.addWeighted(img, 1-alpha, overlay, alpha, 0)
        cv2.putText(blended, f"{scores[i]*100:.1f}%", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        thumbs.append(cv2.resize(blended, (320,180)))
    if not thumbs:
        return None
    # create grid rows of 3
    rows = []
    for i in range(0, len(thumbs), 3):
        block = thumbs[i:i+3]
        while len(block) < 3:
            block.append(np.zeros_like(block[0]))
        rows.append(np.hstack(block))
    grid = np.vstack(rows)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    cv2.imwrite(out_path, grid)
    return out_path
