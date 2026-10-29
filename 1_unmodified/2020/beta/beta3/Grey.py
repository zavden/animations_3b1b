# ==============================================================================
# Scene:      Grey
# Source:     videos/_2020/beta/beta3.py (lines 748-750)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Grey.py Grey -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Grey(Scene):
    def construct(self):
        self.add(FullScreenFadeRectangle(fill_color=GREY_D, fill_opacity=1))
