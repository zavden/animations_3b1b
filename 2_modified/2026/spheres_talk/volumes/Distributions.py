# ==============================================================================
# Scene:      Distributions
# Source:     videos/_2026/spheres_talk/volumes.py (lines 1367-1384)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Distributions.py Distributions -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The scene created a 100000 x 10000 float64 matrix (~8 GB, another ~8 GB when computing the norms) and the kernel killed it for lack of memory: now the vectors are generated in blocks of 1000 and only their normalized last coordinate is kept (same parameters and same histogram).
#   - Matplotlib Agg backend and fig.savefig() + ImageMobject instead of plt.show(), which opens a window and blocks the render; the histogram is shown as a still image in the scene.
#
# Notes:
#   It is a test scene (histogram of the last coordinate of random unit vectors in dimension 10000: it concentrates around 0). It uses no manim mobjects. The original 'import torch' was left in, although it is not used.
# ==============================================================================

from manim_imports_ext import *

class Distributions(InteractiveScene):
    def construct(self):
        # Test
        # CHANGE: windowless backend (Agg); the original used plt.show(), which opens a window and blocks the render
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import torch

        # List of vectors in some dimension, with many
        # more vectors than there are dimensions
        num_vectors = 100000
        vector_len = 10000

        # CHANGE: the original created the full matrix (num_vectors x vector_len, ~8 GB of float64 and another ~8 GB when
        # CHANGE: computing the norms), which exhausted the RAM. Only the last coordinate of each vector is used, so
        # CHANGE: the vectors are generated in blocks and only that already-normalized coordinate is saved (same parameters, same histogram).
        chunk = 1000
        last_coords = np.zeros(num_vectors)
        for start in range(0, num_vectors, chunk):
            block = np.random.normal(size=(chunk, vector_len))
            norms = np.linalg.norm(block, axis=1)
            last_coords[start:start + chunk] = block[:, -1] / norms

        plt.style.use('dark_background')
        fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
        plt.hist(last_coords, bins=1000, range=(-1, 1))
        # CHANGE: instead of plt.show() the histogram is saved and shown as an image in the scene
        import tempfile, os
        hist_path = os.path.join(tempfile.gettempdir(), "distributions_hist.png")
        fig.savefig(hist_path)
        plt.close(fig)
        hist_image = ImageMobject(hist_path)
        hist_image.set_height(FRAME_HEIGHT)
        self.add(hist_image)
        self.wait()
