# ==============================================================================
# Scene:      GaussTitle
# Source:     videos/_2018/cramer.py (lines 321-332)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GaussTitle.py GaussTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GaussTitle(Scene):
    def construct(self):
        title = OldTexText("Gaussian Elimination")
        title.scale(1.5)
        title.to_edge(UP)
        line = Line(LEFT, RIGHT).scale(7)
        line.next_to(title, DOWN)
        self.play(
            FadeIn(title, lag_ratio=0.2),
            ShowCreation(line),
        )
        self.wait()
