# ==============================================================================
# Scene:      LetsSolveThis
# Source:     videos/_2017/eoc/chapter9.py (lines 971-989)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LetsSolveThis.py LetsSolveThis -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LetsSolveThis(TeacherStudentsScene):
    def construct(self):
        expression = OldTex(
            "{\\int_0^\\pi ", " \\sin(x)", "\\,dx \\over \\pi}"
        )
        expression.to_corner(UP+LEFT)
        question = OldTexText(
            "What's the antiderivative \\\\ of",
            "$\\sin(x)$",
            "?"
        )
        for tex_mob in expression, question:
            tex_mob.set_color_by_tex("sin", BLUE)
        self.add(expression)

        self.teacher_says("Let's compute it.")
        self.wait()
        self.student_thinks(question)
        self.wait(2)
