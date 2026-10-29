# ==============================================================================
# Scene:      BeforeGettingToTheFullMath
# Source:     videos/_2018/fourier.py (lines 2233-2256)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BeforeGettingToTheFullMath.py BeforeGettingToTheFullMath -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BeforeGettingToTheFullMath(TeacherStudentsScene):
    def construct(self):
        formula = OldTex(
            "\\hat{g}(f) = \\int_{-\\infty}^{\\infty}" + \
            "g(t)e^{-2\\pi i f t}dt"
        )
        formula.next_to(self.teacher, UP+LEFT)

        self.play(
            Write(formula),
            self.teacher.change, "raise_right_hand",
            self.change_students(*["confused"]*3)
        )
        self.wait()
        self.play(
            ApplyMethod(
                formula.next_to, FRAME_X_RADIUS*RIGHT, RIGHT,
                path_arc = TAU/16,
                rate_func = running_start,
            ),
            self.change_students(*["pondering"]*3)
        )
        self.teacher_says("Consider sound editing\\dots")
        self.wait(3)
