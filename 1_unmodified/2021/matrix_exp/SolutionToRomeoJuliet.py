# ==============================================================================
# Scene:      SolutionToRomeoJuliet
# Source:     videos/_2021/matrix_exp.py (lines 3748-3787)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SolutionToRomeoJuliet.py SolutionToRomeoJuliet -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_matrix_exponential(matrix, height=1.5, scalar_tex="t", **matrix_config):
    elem = matrix[0][0]
    if isinstance(elem, str):
        mat_class = Matrix
    elif isinstance(elem, int) or isinstance(elem, np.int64):
        mat_class = IntegerMatrix
    else:
        mat_class = DecimalMatrix

    matrix = mat_class(matrix, **matrix_config)
    base = OldTex("e")
    base.set_height(0.4 * height)
    matrix.set_height(0.6 * height)
    matrix.move_to(base.get_corner(UR), DL)
    result = VGroup(base, matrix)
    if scalar_tex:
        scalar = OldTex(scalar_tex)
        scalar.set_height(0.7 * base.get_height())
        scalar.next_to(matrix, RIGHT, buff=SMALL_BUFF, aligned_edge=DOWN)
        result.add(scalar)
    return result


class SolutionToRomeoJuliet(Scene):
    def construct(self):
        mat_exp = get_matrix_exponential(
            [["0", "-1"], ["1", "0"]],
            h_buff=1.0,
        )
        solution = VGroup(
            Matrix(
                [["x(t)"], ["y(t)"]],
                bracket_h_buff=SMALL_BUFF,
                bracket_v_buff=SMALL_BUFF,
            ),
            OldTex("="),
            mat_exp,
            Matrix(
                [["x(0)"], ["y(0)"]],
                bracket_h_buff=SMALL_BUFF,
                bracket_v_buff=SMALL_BUFF,
            )
        )
        solution[2].match_height(solution[0])
        solution[3].match_height(solution[0])
        solution.arrange(RIGHT)

        self.add(solution)
        self.wait()
        rect = SurroundingRectangle(mat_exp, buff=0.1)
        rect_copy = rect.copy()
        self.play(ShowCreation(rect))
        self.wait()
        self.play(rect.animate.become(SurroundingRectangle(solution[-1], color=BLUE)))
        self.wait()
        rot_question = Text("Rotation?")
        rot_question.next_to(rect_copy, DOWN)
        rot_question.set_color(YELLOW)
        self.play(
            rect.animate.become(rect_copy),
            Write(rot_question)
        )
        self.wait()
