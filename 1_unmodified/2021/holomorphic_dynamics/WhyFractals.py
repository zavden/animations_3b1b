# ==============================================================================
# Scene:      WhyFractals
# Source:     videos/_2021/holomorphic_dynamics.py (lines 2607-2612)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyFractals.py WhyFractals -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyFractals(Scene):
    def construct(self):
        words = Text("Why fractals?")
        words.set_stroke(BLACK, 5, background=True)
        self.play(Write(words))
        self.wait()
