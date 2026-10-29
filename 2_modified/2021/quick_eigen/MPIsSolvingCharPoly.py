# ==============================================================================
# Scene:      MPIsSolvingCharPoly
# Source:     videos/_2021/quick_eigen.py (lines 2430-2461)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MPIsSolvingCharPoly.py MPIsSolvingCharPoly -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Matrix no longer has element_to_mobject_config; it is now element_config
# ==============================================================================

from manim_imports_ext import *

EIGEN_COLORS = [TEAL_A, TEAL_D]


MEAN_COLOR = BLUE_B


PROD_COLOR = BLUE_D


def get_mod_mat(matrix, h_buff=1.3, v_buff=0.8, t2c={}):
    t2c["\\lambda"] = EIGEN_COLORS[1]
    mod_mat = Matrix(
        [
            [matrix[0][0] + " - \\lambda", matrix[0][1]],
            [matrix[1][0], matrix[1][1] + " - \\lambda"],
        ],
        # CHANGE: Matrix no longer has element_to_mobject_config; it is now element_config
        element_config={"tex_to_color_map": t2c},
        h_buff=h_buff,
        v_buff=v_buff,
    )
    return mod_mat


def get_det_mod_mat(mod_mat):
    parens = OldTex("(", ")")
    parens.stretch(2, 1)
    parens.match_height(mod_mat)
    parens[0].next_to(mod_mat, LEFT, SMALL_BUFF)
    parens[1].next_to(mod_mat, RIGHT, SMALL_BUFF)
    det = Text("det")
    det.next_to(parens, LEFT, SMALL_BUFF)
    return VGroup(det, parens, mod_mat)


class MPIsSolvingCharPoly(TeacherStudentsScene):
    def construct(self):
        formula = OldTex(
            "{m} \\pm \\sqrt{\\,{m}^2 - {p}}",
            tex_to_color_map={"{m}": MEAN_COLOR, "{p}": PROD_COLOR},
            font_size=72
        )
        char_poly = get_det_mod_mat(get_mod_mat([["a", "b"], ["c", "d"]]))
        eq0 = OldTex("=0")
        eq0.next_to(char_poly, RIGHT, SMALL_BUFF)
        char_poly.add(eq0)
        char_poly.move_to(self.hold_up_spot, DOWN)
        arrow = Arrow(RIGHT, LEFT)
        arrow.next_to(char_poly, LEFT)

        self.teacher_holds_up(formula)
        self.play_student_changes(
            "happy", "thinking", "tease",
            look_at=formula
        )
        self.wait()
        self.play(
            self.teacher.change("hooray", char_poly),
            formula.animate.next_to(arrow, LEFT),
            FadeIn(char_poly, 0.5 * UP),
        )
        self.play_student_changes(
            "erm", "pondering", "pondering",
            look_at=char_poly,
            added_anims=[GrowArrow(arrow)]
        )
        self.wait(3)
