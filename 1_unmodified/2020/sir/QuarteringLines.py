# ==============================================================================
# Scene:      QuarteringLines
# Source:     videos/_2020/sir.py (lines 2444-2454)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuarteringLines.py QuarteringLines -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuarteringLines(Scene):
    def construct(self):
        lines = VGroup(
            Line(UP, DOWN),
            Line(LEFT, RIGHT),
        )
        lines.set_width(FRAME_WIDTH)
        lines.set_height(FRAME_HEIGHT, stretch=True)
        lines.set_stroke(WHITE, 3)
        self.play(ShowCreation(lines))
        self.wait()
