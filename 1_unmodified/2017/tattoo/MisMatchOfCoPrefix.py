# ==============================================================================
# Scene:      MisMatchOfCoPrefix
# Source:     videos/_2017/tattoo.py (lines 779-809)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MisMatchOfCoPrefix.py MisMatchOfCoPrefix -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MisMatchOfCoPrefix(TeacherStudentsScene):
    def construct(self):
        eq1 = OldTex(
            "\\text{secant}(\\theta) = \\frac{1}{\\text{cosine}(\\theta)}"
        )
        eq2 = OldTex(
            "\\text{cosecant}(\\theta) = \\frac{1}{\\text{sine}(\\theta)}"
        )
        eq1.to_corner(UP+LEFT)
        eq1.to_edge(LEFT)
        eq2.next_to(eq1, DOWN, buff = LARGE_BUFF)
        eqs = VGroup(eq1, eq2)

        self.play(
            self.get_teacher().change_mode, "speaking",
            Write(eqs),
            *[
                ApplyMethod(pi.look_at, eqs)
                for pi in self.get_students()
            ]
        )
        self.random_blink()
        self.play(
            VGroup(*eq1[-9:-7]).set_color, YELLOW,
            VGroup(*eq2[:2]).set_color, YELLOW,
            *[
                ApplyMethod(pi.change_mode, "confused")
                for pi in self.get_students()
            ]
        )
        self.random_blink(2)
