# ==============================================================================
# Scene:      OutpaintTransition
# Source:     videos/_2022/galois/art_supplements.py (lines 49-64)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl OutpaintTransition.py OutpaintTransition -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - transition-to-hospital-2.png (placeholder, raster_images/; make_galois_assets.py)
# ==============================================================================

from manim_imports_ext import *

class OutpaintTransition(InteractiveScene):
    image_path = "/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/2022/galois/artwork/chapter 1/wounded-by-pond/transition-to-hospital-2.png"

    def construct(self):
        image = ImageMobject(self.image_path)
        image.set_height(FRAME_HEIGHT)
        image.to_edge(LEFT, buff=0)
        self.add(image)

        # Pan
        self.play(
            image.animate.to_edge(RIGHT, buff=-1),
            run_time=8,
            rate_func=bezier([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])
        )
        image.to_edge(RIGHT, buff=-1)
