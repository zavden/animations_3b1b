# ==============================================================================
# Scene:      AskAboutNaturalLog
# Source:     videos/_2017/eoc/chapter6.py (lines 2197-2228)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutNaturalLog.py AskAboutNaturalLog -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutNaturalLog(TeacherStudentsScene):
    def construct(self):
        exp_deriv = OldTex("\\frac{d(e^x)}{dx} = e^x")
        for i in 2, 3, 9, 10:
            exp_deriv[i].set_color(BLUE)
        log_deriv = OldTex("\\frac{d(\\ln(x))}{dx} = ???")
        VGroup(*log_deriv[2:2+5]).set_color(GREEN)

        for deriv in exp_deriv, log_deriv:
            deriv.next_to(self.get_teacher().get_corner(UP+LEFT), UP)

        self.teacher_says(
            """We can find
            new derivatives""",
            target_mode = "hooray"
        )
        self.play_student_changes(*["happy"]*3)
        self.play(RemovePiCreatureBubble(
            self.get_teacher(),
            target_mode = "raise_right_hand"
        ))
        self.play(Write(exp_deriv))
        self.wait()
        self.play(
            Write(log_deriv),
            exp_deriv.next_to, log_deriv, UP, LARGE_BUFF,
            *[
                ApplyMethod(pi.change_mode, "confused")
                for pi in self.get_pi_creatures()
            ]
        )
        self.wait(3)
