# ==============================================================================
# Scene:      RewriteEquationWithTeacher
# Source:     videos/_2018/WindingNumber_G.py (lines 637-710)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/WindingNumber.py, _2018/uncertainty.py
#
# Run from this folder:
#     manimgl RewriteEquationWithTeacher.py RewriteEquationWithTeacher -w -m --fps 15
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


class RewriteEquationWithTeacher(AltTeacherStudentsScene):
    def construct(self):
        root_two_equations = VGroup(
            OldTex("x^2", "", "=", "2", ""),
            OldTex("x^2", "-", "2", "=", "0"),
        )
        for equation in root_two_equations:
            equation.sort_alphabetically()
            for part in equation.get_parts_by_tex("text"):
                part[2:-1].set_color(YELLOW)
                part[2:-1].scale(0.9)
            equation.move_to(self.hold_up_spot, DOWN)

        brace = Brace(root_two_equations[1], UP)
        f_equals_0 = brace.get_tex("f(x) = 0")

        self.teacher_holds_up(root_two_equations[0])
        self.wait()
        self.play(Transform(
            *root_two_equations, 
            run_time = 1.5,
            path_arc = TAU/2
        ))
        self.play(self.change_students(*["pondering"]*3))
        self.play(
            GrowFromCenter(brace),
            self.teacher.change, "happy"
        )
        self.play(Write(f_equals_0))
        self.play_student_changes(*["happy"]*3)
        self.wait()

        #
        to_remove = VGroup(root_two_equations[0], brace, f_equals_0)
        two_d_equation = OldTex("""
            \\left[\\begin{array}{c}
                ye^x \\\\
                \\sin(xy)
            \\end{array}\\right] = 
            \\left[\\begin{array}{c}
                y^2 + x^3 \\\\
                3y - x
            \\end{array}\\right]
        """)
        complex_equation = OldTex("z", "^5 + ", "z", " + 1 = 0")
        z_def = OldTexText(
            "(", "$z$", " is complex, ", "$a + bi$", ")",
            arg_separator = ""
        )
        complex_group = VGroup(complex_equation, z_def)
        complex_group.arrange(DOWN)
        for tex in complex_group:
            tex.set_color_by_tex("z", GREEN)
        complex_group.move_to(self.hold_up_spot, DOWN)

        self.play(
            ApplyMethod(
                to_remove.next_to, FRAME_X_RADIUS*RIGHT, RIGHT,
                remover = True,
                rate_func = running_start,
                path_arc = -TAU/4,
            ),
            self.teacher.change, "hesitant",
            self.change_students(*["erm"]*3)
        )
        self.teacher_holds_up(two_d_equation)
        self.play_all_student_changes("horrified")
        self.wait()
        self.play(
            FadeOut(two_d_equation),
            FadeInFromDown(complex_group),
        )
        self.play_all_student_changes("confused")
        self.wait(3)
