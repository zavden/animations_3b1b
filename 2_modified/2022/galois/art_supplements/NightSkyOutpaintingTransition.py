# ==============================================================================
# Scene:      NightSkyOutpaintingTransition
# Source:     videos/_2022/galois/art_supplements.py (lines 67-88)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NightSkyOutpaintingTransition.py NightSkyOutpaintingTransition -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - mural.png (placeholder, raster_images/; make_galois_assets.py)
# ==============================================================================

from manim_imports_ext import *

class NightSkyOutpaintingTransition(InteractiveScene):
    image_path = "/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/2022/galois/artwork/chapter 1/transition-to-night-sky/mural.png"

    def construct(self):
        # Add image
        image = ImageMobject(self.image_path)
        image.set_width(FRAME_WIDTH + 6)
        image.to_edge(DL, buff=0)
        image.shift(2 * DOWN + LEFT)
        self.add(image)

        # Pan
        image.generate_target()
        image.target.set_width(FRAME_WIDTH)
        image.target.center().to_edge(UP, buff=0)

        self.play(
            MoveToTarget(image),
            run_time=12,
            rate_func=bezier([0, 0, 0, 1, 1, 1])
        )
        self.wait()
