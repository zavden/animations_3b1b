# ==============================================================================
# Scene:      Rearrange2DEquation
# Source:     videos/_2018/WindingNumber_G.py (lines 1411-1452)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/WindingNumber.py, _2018/uncertainty.py
#
# Run from this folder:
#     manimgl Rearrange2DEquation.py Rearrange2DEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings
import mpmath


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/WindingNumber.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


mpmath.mp.dps = 7



# ----- From _2018/WindingNumber_G.py -----

class AltTeacherStudentsScene(TeacherStudentsScene):
    def setup(self):
        TeacherStudentsScene.setup(self)
        self.teacher.set_color(YELLOW_E)


class Rearrange2DEquation(AltTeacherStudentsScene):
    def construct(self):
        f_tex, g_tex, h_tex = [
            "%s(\\text{2d point})"%char
            for char in ("f", "g", "h") 
        ]
        zero_tex = "\\vec{\\textbf{0}}"
        equations = VGroup(
            OldTex(g_tex, "", "=", h_tex, ""),
            OldTex(g_tex, "-", h_tex, "=", zero_tex),
        )
        equations.move_to(self.hold_up_spot, DOWN)
        equations.shift_onto_screen()

        brace = Brace(equations[1], UP)
        zero_eq = brace.get_tex("%s = %s"%(f_tex, zero_tex))

        for equation in equations:
            equation.set_color_by_tex(g_tex, BLUE)
            equation.set_color_by_tex(h_tex, YELLOW)
            equation.sort_alphabetically()


        self.teacher_holds_up(equations[0])
        self.play_all_student_changes("pondering")
        self.play(Transform(
            *equations,
            run_time = 1.5,
            path_arc = TAU/2
        ))
        self.play(
            Succession(
                GrowFromCenter(brace),
                Write(zero_eq, run_time = 1)
            ),
            self.change_students(*["happy"]*3)
        )
        self.play(*[
            ApplyMethod(pi.change, "thinking", self.screen)
            for pi in self.pi_creatures
        ])
        self.wait(3)
