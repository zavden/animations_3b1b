# ==============================================================================
# Scene:      SimpleDerivativeOfExp
# Source:     videos/_2021/matrix_exp.py (lines 2761-2815)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleDerivativeOfExp.py SimpleDerivativeOfExp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleDerivativeOfExp(TeacherStudentsScene):
    def construct(self):
        eq = OldTex(
            "{d \\over dt}", "e^{rt}", "=", "r", "e^{rt}",
        )
        eq.set_color_by_tex("r", TEAL, substring=False)
        for part in eq.get_parts_by_tex("e^{rt}"):
            part[1].set_color(TEAL)

        s0, s1, s2 = self.students
        morty = self.teacher
        bubble = s2.get_bubble(eq)

        self.play(
            s2.change("pondering", eq),
            FadeIn(bubble, lag_ratio=0.2),
        )
        self.play(
            LaggedStart(
                s0.change("hesitant", eq),
                s1.change("erm", eq),
                morty.change("tease"),
            ),
            Write(eq[:2])
        )
        self.wait()
        self.play(
            TransformFromCopy(*eq.get_parts_by_tex("e^{rt}"), path_arc=45 * DEGREES),
            Write(eq.get_part_by_tex("=")),
            *(
                pi.animate.look_at(eq[4])
                for pi in self.pi_creatures
            )
        )
        self.play(
            FadeTransform(eq[4][1].copy(), eq[3][0], path_arc=90 * DEGREES)
        )
        self.play(
            LaggedStart(
                s0.change("thinking"),
                s1.change("tease"),
            )
        )
        self.wait(2)

        rect = ScreenRectangle(height=3.5)
        rect.set_fill(BLACK, 1)
        rect.set_stroke(BLUE_B, 2)
        rect.to_corner(UR)
        self.play(
            morty.change("raise_right_hand", rect),
            self.change_students("pondering", "pondering", "pondering", look_at=rect),
            FadeIn(rect, UP)
        )
        self.wait(10)
