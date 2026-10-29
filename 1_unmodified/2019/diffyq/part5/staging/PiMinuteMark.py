# ==============================================================================
# Scene:      PiMinuteMark
# Source:     videos/_2019/diffyq/part5/staging.py (lines 1372-1385)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiMinuteMark.py PiMinuteMark -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PiMinuteMark(Scene):
    def construct(self):
        text = OldTex(
            "\\pi \\text{ minutes} \\approx \\text{3:08}"
        )
        rect = SurroundingRectangle(text)
        rect.set_fill(BLACK, 1)
        rect.set_stroke(WHITE, 2)

        self.play(
            FadeInFromDown(rect),
            FadeInFromDown(text),
        )
        self.wait()
