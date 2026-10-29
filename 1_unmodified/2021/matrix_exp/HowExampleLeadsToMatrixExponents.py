# ==============================================================================
# Scene:      HowExampleLeadsToMatrixExponents
# Source:     videos/_2021/matrix_exp.py (lines 1954-2005)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowExampleLeadsToMatrixExponents.py HowExampleLeadsToMatrixExponents -w -m --fps 15
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


class HowExampleLeadsToMatrixExponents(Scene):
    def construct(self):
        # Screen
        self.add(FullScreenRectangle())
        screen = ScreenRectangle()
        screen.set_height(3)
        screen.set_fill(BLACK, 1)
        screen.set_stroke(BLUE_B, 2)
        screen.to_edge(LEFT)
        self.add(screen)

        # Mat exp
        mat_exp = get_matrix_exponential(
            [["a", "b"], ["c", "d"]],
            height=2,
            h_buff=0.95, v_buff=0.75
        )
        mat_exp.set_x(FRAME_WIDTH / 4)

        def get_arrow():
            return Arrow(screen, mat_exp[0])

        arrow = get_arrow()

        self.play(
            GrowArrow(arrow),
            FadeIn(mat_exp, RIGHT)
        )
        self.wait()

        # New screen
        screen2 = screen.copy()
        screen2.set_stroke(GREY_BROWN, 2)
        screen2.to_corner(DR)

        mat_exp.generate_target()
        mat_exp.target.to_edge(UP)
        mat_exp.target.match_x(screen2)
        double_arrow = VGroup(
            Arrow(mat_exp.target, screen2),
            Arrow(screen2, mat_exp.target),
        )
        for mob in double_arrow:
            mob.scale(0.9, about_point=mob.get_end())

        self.play(
            MoveToTarget(mat_exp),
            GrowFromCenter(double_arrow),
            arrow.animate.become(Arrow(screen, screen2)),
            FadeIn(screen2, DOWN),
        )
        self.wait()
