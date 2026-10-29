# ==============================================================================
# Scene:      LastVideoWrapper
# Source:     videos/_2017/eoc/chapter9.py (lines 1931-1941)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LastVideoWrapper.py LastVideoWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LastVideoWrapper(Scene):
    def construct(self):
        title = OldTexText("Chapter 8: Integrals")
        title.to_edge(UP)
        rect = Rectangle(height = 9, width = 16)
        rect.set_stroke(WHITE)
        rect.set_height(1.5*FRAME_Y_RADIUS)
        rect.next_to(title, DOWN)

        self.play(Write(title), ShowCreation(rect))
        self.wait(5)
