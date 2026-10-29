# ==============================================================================
# Scene:      TwoThirdsDivision
# Source:     videos/_2025/grover/qc_supplements.py (lines 337-357)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoThirdsDivision.py TwoThirdsDivision -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoThirdsDivision(InteractiveScene):
    def construct(self):
        # Test
        self.add(FullScreenRectangle().set_fill(GREY_E, 0.5))

        rects = Rectangle(3, 0.5).replicate(2)
        rects.arrange(RIGHT, buff=0)
        rects.set_fill(BLUE_E, 1)
        rects.set_submobject_colors_by_gradient(BLUE_E, BLUE_D)
        rects.set_stroke(WHITE, 1)
        rects.stretch_to_fit_width(12)
        rects.move_to(2 * DOWN)

        self.add(rects)
        self.wait()
        self.play(
            rects[0].animate.stretch_to_fit_width(8, about_edge=LEFT),
            rects[1].animate.stretch_to_fit_width(4, about_edge=RIGHT),
            run_time=2
        )
        self.wait()
