import numpy as np
import matplotlib.pyplot as plt

def create_heatmap_from_scores(frames, scores, output_path):
    if not scores:
        return

    arr = np.array(scores)
    plt.figure(figsize=(10, 2))
    plt.imshow(arr[np.newaxis, :], cmap='jet', aspect="auto")
    plt.colorbar()
    plt.title("Frame Fake Probability Heatmap")
    plt.savefig(output_path)
    plt.close()
