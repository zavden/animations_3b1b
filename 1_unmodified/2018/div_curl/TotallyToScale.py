# ==============================================================================
# Scene:      TotallyToScale
# Source:     videos/_2018/div_curl.py (lines 1374-1382)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TotallyToScale.py TotallyToScale -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TotallyToScale(Scene):
    def construct(self):
        words = OldTexText(
            "Totally drawn to scale. \\\\ Don't even worry about it."
        )
        words.set_width(FRAME_WIDTH - 1)
        words.add_background_rectangle()
        self.add(words)
        self.wait()
