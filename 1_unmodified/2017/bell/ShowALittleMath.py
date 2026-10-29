# ==============================================================================
# Scene:      ShowALittleMath
# Source:     videos/_2017/bell.py (lines 369-407)
# Category:   1 · Renders unmodified
# Includes code copied from: _2017/waves.py
#
# Run from this folder:
#     manimgl ShowALittleMath.py ShowALittleMath -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2017/waves.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2017/bell.py -----

class ShowALittleMath(TeacherStudentsScene):
    def construct(self):
        exp1 = OldTex(
            "|", "\\psi", "\\rangle = ",
            "\\alpha", "|\\uparrow\\rangle", 
            "+", "\\beta", "|\\rightarrow\\rangle"
        )
        exp2 = OldTex(
            "|| \\langle", "\\psi", "|", "\\psi", "\\rangle ||^2",
            "= ", "\\alpha", "^2", "+", "\\beta", "^2"
        )
        color_map = {
            "alpha" : GREEN,
            "beta" : RED,
            "psi" : BLUE
        }
        for exp in exp1, exp2:
            exp.set_color_by_tex_to_color_map(color_map)
        exp1.next_to(self.teacher.get_corner(UP+LEFT), UP, LARGE_BUFF)

        exp2.move_to(exp1)

        self.play(
            Write(exp1, run_time = 2),
            self.teacher.change, "raise_right_hand"
        )
        self.play(exp1.shift, UP)
        self.play(*[
                ReplacementTransform(
                    exp1.get_parts_by_tex(tex).copy(),
                    exp2.get_parts_by_tex(tex).copy(),
                )
                for tex in list(color_map.keys())
        ] + [Write(exp2, run_time = 2)])
        self.play_student_changes(
            *["pondering"]*3,
            look_at = exp2
        )
        self.wait(2)
