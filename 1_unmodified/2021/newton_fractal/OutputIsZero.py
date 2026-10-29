# ==============================================================================
# Scene:      OutputIsZero
# Source:     videos/_2021/newton_fractal.py (lines 2799-2811)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OutputIsZero.py OutputIsZero -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OutputIsZero(Scene):
    def construct(self):
        words = OldTexText("Output $\\approx 0$")
        words.set_stroke(BLACK, 5, background=True)
        arrow = Vector(0.5 * UL)
        words.next_to(arrow, DR)
        words.shift(0.5 * LEFT)

        self.play(
            Write(words),
            ShowCreation(arrow)
        )
        self.wait()
