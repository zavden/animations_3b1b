# ==============================================================================
# Scene:      Thumbnail2
# Source:     videos/_2019/windmill.py (lines 4116-4134)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Thumbnail2.py Thumbnail2 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class Thumbnail2(Scene):
    def construct(self):
        words = OldTexText("Olympics\\\\", "for\\\\", "math", alignment="")
        # words.arrange(DOWN, aligned_edge=LEFT)

        words.set_height(FRAME_HEIGHT - 1.5)
        words.to_edge(LEFT)

        logo = ImageMobject("imo_logo")
        logo.set_height(4.5)
        logo.to_corner(DR, buff=LARGE_BUFF)

        rect = FullScreenFadeRectangle()
        rect.set_fill([GREY, BLACK], 1)

        self.clear()
        self.add(rect)
        self.add(words)
        self.add(logo)
