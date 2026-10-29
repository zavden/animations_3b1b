# ==============================================================================
# Scene:      Grey
# Source:     videos/_2021/some1.py (lines 294-296)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Grey.py Grey -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Grey(Scene):
    def construct(self):
        self.add(FullScreenRectangle().set_fill(GREY_D, 1))
