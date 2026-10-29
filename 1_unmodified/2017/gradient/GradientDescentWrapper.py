# ==============================================================================
# Scene:      GradientDescentWrapper
# Source:     videos/_2017/gradient.py (lines 9-18)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GradientDescentWrapper.py GradientDescentWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GradientDescentWrapper(Scene):
    def construct(self):
        title = OldTexText("Gradient descent")
        title.to_edge(UP)
        rect = ScreenRectangle(height=6)
        rect.next_to(title, DOWN)

        self.add(title)
        self.play(ShowCreation(rect))
        self.wait()
