# ==============================================================================
# Scene:      SplitScreen
# Source:     videos/_2023/clt_proof/main.py (lines 5-11)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SplitScreen.py SplitScreen -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SplitScreen(InteractiveScene):
    def construct(self):
        h_lines = Line(DOWN, UP).set_height(FRAME_HEIGHT).replicate(2)
        h_lines.arrange(RIGHT, buff=FRAME_WIDTH / 3)
        h_lines.center()
        h_lines.set_stroke(GREY_B, 2)
        self.add(h_lines)
