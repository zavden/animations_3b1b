# ==============================================================================
# Scene:      ExpandOutFullProduct
# Source:     videos/_2018/quat3d.py (lines 1340-1384)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExpandOutFullProduct.py ExpandOutFullProduct -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

W_COLOR = YELLOW


I_COLOR = GREEN


J_COLOR = RED


K_COLOR = BLUE


class ExpandOutFullProduct(TeacherStudentsScene):
    def construct(self):
        product = OldTex(
            """
            (w_0 + x_0 i + y_0 j + z_0 k)
            (x_1 i + y_1 j + z_1 k)
            (w_0 - x_0 i - y_0 j - z_0 k)
            """,
            tex_to_color_map={
                "w_0": W_COLOR, "(": WHITE, ")": WHITE,
                "x_0": I_COLOR, "y_0": J_COLOR, "z_0": K_COLOR,
                "x_1": I_COLOR, "y_1": J_COLOR, "z_1": K_COLOR,
            }
        )
        product.set_width(FRAME_WIDTH - 1)
        product.to_edge(UP)

        n = 10
        q_brace = Brace(product[:n], DOWN)
        p_brace = Brace(product[n:-n], DOWN)
        q_inv_brace = Brace(product[-n:], DOWN)
        braces = VGroup(q_brace, p_brace, q_inv_brace)
        for brace, tex in zip(braces, ["q", "p", "q^{-1}"]):
            brace.add(brace.get_tex(tex))

        words = OldTexText("= Rotation of $p$")
        words.next_to(braces, DOWN)

        self.play(
            self.teacher.change, "raise_right_hand",
            FadeInFromDown(product)
        )
        self.play(
            LaggedStartMap(GrowFromCenter, braces),
            self.change_students(
                "confused", "horrified", "confused"
            )
        )
        self.wait(2)
        self.play(Write(words))
        self.play_student_changes(
            "pondering", "confused", "erm",
            look_at=words
        )
        self.wait(5)
