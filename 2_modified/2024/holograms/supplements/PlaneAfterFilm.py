# ==============================================================================
# Scene:      PlaneAfterFilm
# Source:     videos/_2024/holograms/supplements.py (lines 1778-1805)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PlaneAfterFilm.py PlaneAfterFilm -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Private images from Grant's Dropbox (FilmFromBehind.png) replaced with regenerable placeholders
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/FilmFromBehind.png  (placeholder; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
# ==============================================================================

from manim_imports_ext import *

class PlaneAfterFilm(InteractiveScene):
    def construct(self):
        # Test
        image = ImageMobject("FilmFromBehind")
        image.set_height(FRAME_HEIGHT)
        image.set_height(FRAME_HEIGHT)
        image.fix_in_frame()
        # self.add(image)

        rect = Polygon(
            (2.56, -0.12, 0.0),
            (5.69, -2.51, 0.0),
            (6.25, 1.31, 0.0),
            (2.72, 2.62, 0.0),
        )
        rect.set_fill(BLACK, 0.75)
        rect.set_stroke(BLUE, 10)
        rect.fix_in_frame()
        words = Text("True on this\n2D Plane")

        self.set_floor_plane("xz")
        self.frame.reorient(73, -24, 0, (-1.53, -0.68, 4.14), 9.19)

        self.play(
            DrawBorderThenFill(rect),
            FadeIn(words),
        )
        self.wait()
