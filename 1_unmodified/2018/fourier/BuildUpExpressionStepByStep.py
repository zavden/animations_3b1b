# ==============================================================================
# Scene:      BuildUpExpressionStepByStep
# Source:     videos/_2018/fourier.py (lines 3166-3208)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BuildUpExpressionStepByStep.py BuildUpExpressionStepByStep -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BuildUpExpressionStepByStep(TeacherStudentsScene):
    def construct(self):
        expression = OldTex(
            "\\frac{1}{t_2 - t_1}", "\\int_{t_1}^{t_2}",
            "g(t)", "e", "^{-2\\pi i", "f", "t}", "dt"
        )
        frac, integral, g, e, two_pi_i, f, t, dt = expression
        expression.next_to(self.teacher, UP+LEFT)
        t.set_color(YELLOW)
        g[2].set_color(YELLOW)
        dt[1].set_color(YELLOW)
        f.set_color(GREEN)
        t.save_state()
        t.move_to(f, LEFT)

        self.play(
            self.teacher.change, "raise_right_hand",
            FadeIn(e),
            FadeIn(two_pi_i),
        )
        self.play(
            self.change_students(*["pondering"]*3),
            FadeIn(t),
        )
        self.play(
            FadeIn(f),
            t.restore,
        )
        self.wait()
        self.play(FadeIn(g), Blink(self.students[1]))
        self.wait()
        self.play(
            FadeIn(integral),
            FadeIn(frac),
            FadeIn(dt),
        )
        self.wait(3)
        self.teacher_says(
            "Just one final \\\\ distinction.",
            bubble_config = {"height" : 2.5, "width" : 3.5},
            added_anims = [expression.to_corner, UP+RIGHT]
        )
        self.wait(3)
