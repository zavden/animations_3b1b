# ==============================================================================
# Scene:      MatrixProduct
# Source:     videos/_2020/hamming.py (lines 5943-6010)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MatrixProduct.py MatrixProduct -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MatrixProduct(Scene):
    def construct(self):
        title = OldTexText("(7, 4) Hamming code")
        title.set_height(0.7)
        title.to_edge(UP)
        title.set_color(GREY_A)

        encoder_matrix = np.array([
           [1, 1, 0, 1],
           [1, 0, 1, 1],
           [1, 0, 0, 0],
           [0, 1, 1, 1],
           [0, 1, 0, 0],
           [0, 0, 1, 0],
           [0, 0, 0, 1],
        ])
        message_matrix = np.array([1, 0, 1, 1]).reshape((4, 1))
        result_matrix = np.dot(encoder_matrix, message_matrix) % 2

        kw = {"v_buff": 0.6, "h_buff": 0.75}
        encoder, message, result = [
            IntegerMatrix(matrix, **kw)
            for matrix in [encoder_matrix, message_matrix, result_matrix]
        ]
        equation = VGroup(
            encoder, message, OldTex("="), result
        )
        equation.arrange(RIGHT, buff=MED_LARGE_BUFF)
        equation.to_edge(LEFT, buff=2)

        # Labels
        message_label = OldTexText("Content")
        message_label.move_to(message)
        message_label.to_edge(DOWN)
        message_arrow = Arrow(
            message_label.get_top(),
            message.get_bottom(),
        )
        message_label.set_color(YELLOW)
        message_arrow.set_color(YELLOW)

        brace = Brace(result, RIGHT)
        brace_text = brace.get_text("Error-resistant\\\\block")
        brace.set_color(BLUE)
        brace_text.set_color(BLUE)

        # Animate
        self.add(title)
        self.add(equation)

        self.play(FadeIn(message_label, UP), GrowArrow(message_arrow))
        self.play(GrowFromCenter(brace), FadeIn(brace_text, LEFT))

        equation.set_fill(opacity=0.8)
        for n in range(encoder.mob_matrix.shape[0]):
            row = VGroup(*encoder.mob_matrix[n, :]).copy()
            col = VGroup(*message.elements).copy()
            rhs = result.mob_matrix[n, 0].copy()

            mult_group = VGroup(row, col, rhs)
            mult_group.set_fill(YELLOW, 1)
            self.play(
                ShowIncreasingSubsets(row),
                ShowIncreasingSubsets(col),
                FadeIn(rhs),
            )
            self.wait()
            self.remove(mult_group)
