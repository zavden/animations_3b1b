# ==============================================================================
# Scene:      Leftrightarrow
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 148-152)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Leftrightarrow.py Leftrightarrow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Leftrightarrow(InteractiveScene):
    def construct(self):
        arrow = Tex(R"\longleftrightarrow", font_size=90)
        self.play(GrowFromCenter(arrow, run_time=2))
        self.wait(2)
