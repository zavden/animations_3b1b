# ==============================================================================
# Scene:      Link
# Source:     videos/_2018/quat3d.py (lines 1387-1408)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Link.py Link -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Link(Scene):
    def construct(self):
        word = OldTexText("eater.net/quaternions")
        word.add_background_rectangle()
        rect = SurroundingRectangle(word)
        rect.set_color(BLUE)
        arrow = Vector(UR, color=GREEN)
        arrow.next_to(rect, UP)
        arrow.align_to(rect, RIGHT)
        short_arrow = arrow.copy().scale(0.8, about_edge=DL)

        self.add(word)
        self.play(
            ShowCreation(rect),
            GrowArrow(arrow),
        )
        for x in range(10):
            self.play(Transform(
                arrow, short_arrow,
                rate_func=there_and_back,
                run_time=2
            ))
