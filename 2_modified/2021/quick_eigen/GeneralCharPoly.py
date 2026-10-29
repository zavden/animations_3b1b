# ==============================================================================
# Scene:      GeneralCharPoly
# Source:     videos/_2021/quick_eigen.py (lines 2776-2815)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl GeneralCharPoly.py GeneralCharPoly -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Matrix no longer has element_to_mobject_config; it is now element_config
# ==============================================================================

from manim_imports_ext import *

COL_COLORS = [MAROON_B, MAROON_C]


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


class GeneralCharPoly(Scene):
    def construct(self):
        t2c = {
            "a": COL_COLORS[0],
            "b": COL_COLORS[1],
            "c": COL_COLORS[0],
            "d": COL_COLORS[1],
            "\\lambda": EIGEN_COLORS[1],
            "-": WHITE,
            "+": WHITE,
            "=": WHITE,
        }
        det = get_det_mod_mat(get_mod_mat([["a", "b"], ["c", "d"]], t2c=t2c))
        rhs1 = OldTex("= (a - \\lambda)(d - \\lambda) - bc", tex_to_color_map=t2c)
        rhs2 = OldTex("= \\lambda^2 - (a + d)\\lambda + (ad - bc)", tex_to_color_map=t2c)

        rhs1.next_to(det, RIGHT)
        rhs2.next_to(rhs1, DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        VGroup(det, rhs1, rhs2).center()

        self.add(det)
        self.wait()
        self.play(TransformMatchingShapes(
            det[-1].get_entries()[0::3].copy(),
            rhs1[:10],
        ))
        self.play(TransformMatchingShapes(
            det[-1].get_entries()[1:3].copy(),
            rhs1[10:],
            path_arc=45 * DEGREES,
        ))
        self.wait()
        self.play(TransformMatchingShapes(rhs1.copy(), rhs2, run_time=1.5))
        self.wait()

        self.play(ShowCreation(SurroundingRectangle(rhs2[3:9], buff=0.05, color=MEAN_COLOR)))
        self.play(ShowCreation(SurroundingRectangle(rhs2[11:], buff=0.05, color=PROD_COLOR)))
        self.wait()

        self.embed()
