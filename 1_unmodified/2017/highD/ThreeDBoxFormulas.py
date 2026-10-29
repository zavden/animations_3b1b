# ==============================================================================
# Scene:      ThreeDBoxFormulas
# Source:     videos/_2017/highD.py (lines 1844-1868)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeDBoxFormulas.py ThreeDBoxFormulas -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThreeDBoxFormulas(Scene):
    def construct(self):
        question = OldTex(
            "||(1, 1, 1)||", "=", "???"
        )
        answer = OldTex(
            "||(1, 1, 1)||", "&=", "\\sqrt{1^2 + 1^2 + 1^2}\\\\",
            "&= \\sqrt{3}\\\\", "&\\approx", "1.73",
        )
        for mob in question, answer:
            mob.to_corner(UP+LEFT)
        inner_r = OldTex(
            "\\text{Inner radius}", "&=", "\\sqrt{3} - 1\\\\",
            "&\\approx", "0.73"
        )
        inner_r.next_to(answer, DOWN, LARGE_BUFF, LEFT)
        inner_r.set_color(GREEN_C)
        VGroup(question, answer).shift(0.55*RIGHT)

        self.play(Write(question))
        self.wait(2)
        self.play(ReplacementTransform(question, answer))
        self.wait(2)
        self.play(Write(inner_r))
        self.wait(2)
