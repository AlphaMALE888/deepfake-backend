import numpy as np
import matplotlib.pyplot as plt

def create_heatmap_from_scores(frames, scores, output_path):
    """
    Generates a horizontal heatmap representing fake probabilities of video frames.

    Args:
        frames (list): list of frame paths (optional, for reference)
        scores (list): list of float scores (0–1)
        output_path (str): path to save the heatmap image
    """
    try:
        if not scores or len(scores) == 0:
            print("[HEATMAP] No scores found — skipping heatmap generation.")
            return None

        arr = np.array(scores)

        plt.figure(figsize=(12, 2))
        plt.imshow(arr[np.newaxis, :], cmap='inferno', aspect="auto")
        plt.colorbar(label="Fake Probability (0–1)")
        plt.title("Deepfake Detection Heatmap — Frame-wise Fake Probability")
        plt.xlabel("Frames")
        plt.yticks([])
        plt.tight_layout()
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()

        print(f"[HEATMAP] Saved successfully at: {output_path}")
        return output_path

    except Exception as e:
        print("[HEATMAP ERROR]:", e)
        return None
