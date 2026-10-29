# ==============================================================================
# Scene:      PiRSquared
# Source:     videos/_2021/shadows.py (lines 5800-5805)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiRSquared.py PiRSquared -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PiRSquared(Scene):
    def construct(self):
        form = OldTex("\\pi R^2")[0]
        form[1].set_color(BLUE)
        self.play(Write(form))
        self.wait()
