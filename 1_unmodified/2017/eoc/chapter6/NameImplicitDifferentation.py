# ==============================================================================
# Scene:      NameImplicitDifferentation
# Source:     videos/_2017/eoc/chapter6.py (lines 521-555)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NameImplicitDifferentation.py NameImplicitDifferentation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NameImplicitDifferentation(TeacherStudentsScene):
    def construct(self):
        title = OldTexText("``Implicit differentiation''")

        equation = OldTex("x^2", "+", "y^2", "=", "5^2")
        derivative = OldTex(
            "2x\\,dx", "+", "2y\\,dy", "=", "0"
        )
        VGroup(*derivative[0][2:]).set_color(GREEN)
        VGroup(*derivative[2][2:]).set_color(RED)
        arrow = Arrow(ORIGIN, DOWN, buff = SMALL_BUFF)
        group = VGroup(title, equation, arrow, derivative)
        group.arrange(DOWN)
        group.to_edge(UP)

        self.add(title, equation)
        self.play(
            self.get_teacher().change_mode, "raise_right_hand",
            ShowCreation(arrow)
        )
        self.play_student_changes(
            *["confused"]*3,
            look_at = derivative,
            added_anims = [ReplacementTransform(equation.copy(), derivative)]
        )
        self.wait(2)
        self.teacher_says(
            "Don't worry...",
            added_anims = [
                group.scale, 0.7,
                group.to_corner, UP+LEFT,
            ]
        )
        self.play_student_changes(*["happy"]*3)
        self.wait(3)
