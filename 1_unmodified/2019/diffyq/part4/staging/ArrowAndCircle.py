# ==============================================================================
# Scene:      ArrowAndCircle
# Source:     videos/_2019/diffyq/part4/staging.py (lines 1123-1135)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ArrowAndCircle.py ArrowAndCircle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ArrowAndCircle(Scene):
    def construct(self):
        circle = Circle(color=RED)
        circle.set_stroke(width=4)
        circle.set_height(0.25)

        arrow = Vector(DL)
        arrow.set_color(RED)
        arrow.next_to(circle, UR)
        self.play(ShowCreation(arrow))
        self.play(ShowCreation(circle))
        self.play(FadeOut(circle))
        self.wait()
