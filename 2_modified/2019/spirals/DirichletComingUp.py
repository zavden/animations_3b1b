# ==============================================================================
# Scene:      DirichletComingUp
# Source:     videos/_2019/spirals.py (lines 1216-1234)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DirichletComingUp.py DirichletComingUp -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class DirichletComingUp(Scene):
    def construct(self):
        image = ImageMobject("Dirichlet")
        image.set_height(3)
        words = OldTexText(
            "Coming up: \\\\", "Dirichlet's theorem",
            alignment="",
        )
        words.set_color_by_tex("Dirichlet's", YELLOW)
        words.scale(1.5)
        words.next_to(image, RIGHT)
        words.set_stroke(BLACK, 8, background=True)
        Group(words, image).center()

        self.play(
            FadeIn(image, RIGHT),
            FadeIn(words, LEFT),
        )
        self.wait()
