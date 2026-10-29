# ==============================================================================
# Scene:      LeadToPhysicsAndQM
# Source:     videos/_2021/matrix_exp.py (lines 229-274)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LeadToPhysicsAndQM.py LeadToPhysicsAndQM -w -m --fps 15
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


class LeadToPhysicsAndQM(Scene):
    def construct(self):
        de_words = OldTexText("Differential\\\\equations", font_size=60)
        de_words.set_x(-3).to_edge(UP)
        mat_exp = get_matrix_exponential([[3, 1, 4], [1, 5, 9], [2, 6, 5]])
        mat_exp[1].set_color(TEAL)
        mat_exp.next_to(de_words, DOWN, buff=3)

        qm_words = OldTexText("Quantum\\\\mechanics", font_size=60)
        qm_words.set_x(3).to_edge(UP)
        physics_words = OldTexText("Physics", font_size=60)
        physics_words.move_to(qm_words)

        qm_exp = OldTex("e^{-i \\hat{H} t / \\hbar}")
        qm_exp.scale(2)
        qm_exp.refresh_bounding_box()
        qm_exp[0][0].set_height(mat_exp[0].get_height(), about_edge=UR)
        qm_exp[0][0].shift(SMALL_BUFF * DOWN)
        qm_exp.match_x(qm_words)
        qm_exp.align_to(mat_exp, DOWN)
        qm_exp[0][3:5].set_color(TEAL)

        de_arrow = Arrow(de_words, mat_exp)
        qm_arrow = Arrow(qm_words, qm_exp)
        top_arrow = Arrow(de_words, qm_words)

        self.add(de_words)
        self.play(
            GrowArrow(de_arrow),
            FadeIn(mat_exp, shift=DOWN),
        )
        self.wait()
        self.play(
            GrowArrow(top_arrow),
            FadeIn(physics_words, RIGHT)
        )
        self.wait()
        self.play(
            FadeOut(physics_words, UP),
            FadeIn(qm_words, UP),
        )
        self.play(
            TransformFromCopy(de_arrow, qm_arrow),
            FadeTransform(mat_exp.copy(), qm_exp),
        )
        self.wait()
