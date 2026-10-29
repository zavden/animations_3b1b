# ==============================================================================
# Scene:      TexturedSphereExample
# Source:     videos/_2026/2025_P6/p6.py (lines 1074-1084)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TexturedSphereExample.py TexturedSphereExample -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - RandomGrid.png is not in the repo: it was generated from a frame of RandomGridThumbnailTest (see notes)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/RandomGrid.png  (generated, not a generic placeholder: 1280x720 frame of RandomGridThumbnailTest)
#
# Notes:
#   RandomGrid.png is not in the repo (Grant's Dropbox). It was very likely a screenshot of the RandomGridThumbnailTest scene (the same random 70x70 grid with blue tiles and holes with a yellow glow), so it was generated faithfully by rendering that scene (a copy with an added wait, via _tools/render.py in the queue) and extracting a 1280x720 frame. The grid is random, so it is not identical to Grant's. The script used is kept at _lib/assets/generated/2026/2025_P6/make_RandomGrid_png_scene.py. To regenerate it: render that script and save a frame as _lib/assets/raster_images/RandomGrid.png.
# ==============================================================================

import tempfile
import os
from manim_imports_ext import *

class TexturedSphereExample(InteractiveScene):
    def construct(self):
        # Put the grid on a sphere
        self.camera.frame.reorient(55, 71, 0, (-0.02, -0.00, 0.87), 0.32)
        sphere = Sphere(
            radius=1,
            resolution=(70, 70),
            v_range=(PI * 0.9, PI)
        )
        textured_sphere = TexturedSurface(sphere, "RandomGrid.png")
        self.add(textured_sphere)


_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)
