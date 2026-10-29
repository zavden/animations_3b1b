# ==============================================================================
# Scene:      ShowDerivativeAtExamplePoint
# Source:     videos/_2017/gradient.py (lines 321-399)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowDerivativeAtExamplePoint.py ShowDerivativeAtExamplePoint -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowDerivativeAtExamplePoint(Scene):
    def construct(self):
        tex_to_color_map = {
            "x": BLUE,
            "y": RED,
        }
        func_tex = OldTex(
            "f", "(", "x", ",", "y", ")", "=",
            "e^{", "-x^2", "+ \\cos(2y)}",
            tex_to_color_map=tex_to_color_map
        )
        gradient_tex = OldTex(
            "\\nabla", "f", "(", "x", ",", "y", ")", "=",
            tex_to_color_map=tex_to_color_map
        )

        partial_vect = Matrix([
            ["{\\partial f / \\partial x}"],
            ["{\\partial f / \\partial y}"],
        ])
        partial_vect.get_mob_matrix()[0, 0][-1].set_color(BLUE)
        partial_vect.get_mob_matrix()[1, 0][-1].set_color(RED)
        result_vector = self.get_result_vector("x", "y")

        gradient = VGroup(
            gradient_tex,
            partial_vect,
            OldTex("="),
            result_vector
        )
        gradient.arrange(RIGHT, buff=SMALL_BUFF)

        func_tex.to_edge(UP)
        gradient.next_to(func_tex, DOWN, buff=LARGE_BUFF)

        example_lhs = OldTex(
            "\\nabla", "f", "(", "1", ",", "3", ")", "=",
            tex_to_color_map={"1": BLUE, "3": RED},
        )
        example_result_vector = self.get_result_vector("1", "3")
        example_rhs = DecimalMatrix([[-1.92], [0.54]])
        example = VGroup(
            example_lhs,
            example_result_vector,
            OldTex("="),
            example_rhs,
        )
        example.arrange(RIGHT, buff=SMALL_BUFF)
        example.next_to(gradient, DOWN, LARGE_BUFF)

        self.add(func_tex, gradient)
        self.wait()
        self.play(
            ReplacementTransform(gradient_tex.copy(), example_lhs),
            ReplacementTransform(result_vector.copy(), example_result_vector),
        )
        self.wait()
        self.play(Write(example[2:]))
        self.wait()

    def get_result_vector(self, x, y):
        result_vector = Matrix([
            ["e^{-%s^2 + \\cos(2\\cdot %s)} (-2\\cdot %s)" % (x, y, x)],
            ["e^{-%s^2 + \\cos(2\\cdot %s)} \\big(-\\sin(2\\cdot %s) \\cdot 2\\big)" % (x, y, y)],
        ], v_buff=1.2, element_alignment_corner=ORIGIN)

        x_terms = VGroup(
            result_vector.get_mob_matrix()[0, 0][2],
            result_vector.get_mob_matrix()[1, 0][2],
            result_vector.get_mob_matrix()[0, 0][-2],
        )
        y_terms = VGroup(
            result_vector.get_mob_matrix()[0, 0][11],
            result_vector.get_mob_matrix()[1, 0][11],
            result_vector.get_mob_matrix()[1, 0][-5],
        )
        x_terms.set_color(BLUE)
        y_terms.set_color(RED)
        return result_vector
