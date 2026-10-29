# ==============================================================================
# Scene:      DrawUnderline
# Source:     videos/_2020/beta/beta2.py (lines 444-451)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DrawUnderline.py DrawUnderline -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DrawUnderline(Scene):
    def construct(self):
        line = Line(2 * LEFT, 2 * RIGHT)
        line.set_stroke(PINK, 5)
        self.play(ShowCreation(line))
        self.wait()
        line.reverse_points()
        self.play(Uncreate(line))
